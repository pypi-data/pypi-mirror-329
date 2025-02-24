import asyncio
import time
import json
import hashlib
from typing import Dict, List, Tuple, Set
import ccxt.pro as ccxt
from bjarkan.models import OrderbookConfig
from bjarkan.utils.logger import logger, catch_exception
from bjarkan.config import EXCHANGES


class OrderbookManager:
    @catch_exception
    def __init__(self, orderbook_config: OrderbookConfig):
        """Initialize OrderbookManager with given configuration."""
        self.config = orderbook_config
        self.depth = min(orderbook_config.depth, 50)
        self.exchanges = self._initialize_exchanges()
        self.exchange_symbols = {}  # Map of exchange -> supported symbols
        self.fees = self._initialize_fees()
        self.orderbooks = {}
        self.symbol_groups = self._initialize_symbol_groups()
        self.running = True
        self.lock = asyncio.Lock()
        self.update_event = asyncio.Event()
        self._callbacks = []
        self._collection_tasks = []
        self._last_hash = {}
        self._latest_verified_books = {}  # Store latest verified orderbook for each symbol

    def _initialize_symbol_groups(self) -> Dict[str, Set[str]]:
        """Initialize mapping of primary symbols to their group members."""
        groups = {}
        used_symbols = set()

        # First handle explicitly grouped symbols
        if self.config.group:
            for primary, secondary in self.config.group.items():
                if primary not in groups:
                    groups[primary] = {primary}
                groups[primary].add(secondary)
                used_symbols.add(primary)
                used_symbols.add(secondary)

        # Add remaining ungrouped symbols
        for symbol in self.config.symbols:
            if symbol not in used_symbols:
                groups[symbol] = {symbol}

        return groups

    @catch_exception
    async def _verify_exchange_symbols(self):
        """Verify which symbols are available on each exchange."""
        for exchange_id, exchange in self.exchanges.items():
            try:
                markets = await exchange.load_markets()
                available_symbols = set()
                for symbol in self.config.symbols:
                    if symbol in markets:
                        available_symbols.add(symbol)
                self.exchange_symbols[exchange_id] = available_symbols
                logger.info(f"Exchange {exchange_id} supports symbols: {available_symbols}")
            except Exception as e:
                logger.error(f"Error loading markets for {exchange_id}: {str(e)}")
                self.exchange_symbols[exchange_id] = set()

        # Initialize orderbooks only for supported symbols
        self.orderbooks = {
            ex: {sym: None for sym in symbols}
            for ex, symbols in self.exchange_symbols.items()
        }

    @staticmethod
    def _hash_orderbook(bids: List[Tuple], asks: List[Tuple]) -> str:
        """Generate hash of orderbook bids and asks."""
        orderbook_str = json.dumps((bids, asks), separators=(',', ':'))
        return hashlib.md5(orderbook_str.encode()).hexdigest()

    @catch_exception
    @catch_exception
    def _initialize_exchanges(self) -> Dict[str, ccxt.Exchange]:
        """Initialize exchange instances with appropriate settings."""
        exchanges = {}
        for exchange_id in self.config.exchanges:
            exchange_class = getattr(ccxt, exchange_id)
            instance = exchange_class({
                'enableRateLimit': True,
            })
            is_sandbox = self.config.sandbox_mode.get(exchange_id, False)  # Explicitly set sandbox mode
            instance.set_sandbox_mode(is_sandbox)
            exchanges[exchange_id] = instance
        return exchanges

    @catch_exception
    def _initialize_fees(self) -> Dict[str, Dict[str, float]]:
        """Initialize fee structure for all exchanges and symbols."""
        if not self.config.fees_bps:
            fees = {ex: {sym: 1 for sym in self.config.symbols} for ex in self.exchanges}
            return fees

        fees = {}
        for exchange, fee_info in self.config.fees_bps.items():
            fees[exchange] = {}
            for symbol in self.config.symbols:
                fee = fee_info[symbol] if isinstance(fee_info, dict) else fee_info
                fees[exchange][symbol] = 1 + fee / 10000
        return fees

    @catch_exception
    def get_exchange_depth(self, exchange: str) -> int:
        """Get appropriate depth for an exchange within its limits."""
        depths = EXCHANGES[exchange]['available_depth']
        if isinstance(depths, range):
            return min(self.depth, max(depths))
        suitable_depths = [d for d in depths if d >= self.depth]
        return min(suitable_depths) if suitable_depths else max(depths)

    @catch_exception
    def apply_fees(self, exchange: str, symbol: str, bids: List[Tuple], asks: List[Tuple]) -> Tuple[
        List[Tuple], List[Tuple]]:
        """Apply exchange fees to bid and ask prices."""
        fee = self.fees.get(exchange, {}).get(symbol, 1)
        if fee == 1:
            return bids, asks

        processed_bids = []
        processed_asks = []

        for price, amount, exchange in bids:
            adjusted_price = round(float(price) * (1 / fee), 8)
            processed_bids.append((adjusted_price, amount, exchange))

        for price, amount, exchange in asks:
            adjusted_price = round(float(price) * fee, 8)
            processed_asks.append((adjusted_price, amount, exchange))

        return processed_bids, processed_asks

    @catch_exception
    async def collect_orderbook(self, exchange_name: str, symbol: str):
        """Collect and process orderbook data from specified exchange."""
        # Skip if exchange doesn't support this symbol
        if symbol not in self.exchange_symbols.get(exchange_name, set()):
            logger.warning(f"Skipping collection for {exchange_name}.{symbol} - symbol not supported")
            return

        exchange = self.exchanges[exchange_name]
        exchange_depth = self.get_exchange_depth(exchange_name)

        while self.running:
            try:
                raw_orderbook = await exchange.watchOrderBook(symbol, exchange_depth)
                processed_book = self._process_raw_orderbook(
                    raw_orderbook,
                    exchange_name,
                    symbol,
                    raw_orderbook.get('timestamp')
                )

                async with self.lock:
                    self.orderbooks[exchange_name][symbol] = processed_book

                    # Find the primary symbol for this book
                    primary_symbol = self._get_primary_symbol(symbol)
                    if primary_symbol:
                        book_to_send = await self._get_final_orderbook(primary_symbol)
                        if book_to_send:
                            await self._execute_callbacks(book_to_send)

                self.update_event.set()

            except asyncio.CancelledError:
                break
            except Exception as e:
                if self.running:
                    logger.error(f"Error collecting orderbook from {exchange_name}.{symbol}: {str(e)}")
                await asyncio.sleep(5)

    def _get_primary_symbol(self, symbol: str) -> str:
        """Get the primary symbol for a given symbol."""
        for primary, group in self.symbol_groups.items():
            if symbol in group:
                return primary
        return symbol

    @catch_exception
    def _process_raw_orderbook(self, raw_orderbook: Dict, exchange_name: str, symbol: str,
                               exchange_timestamp: int) -> Dict:
        """Process raw orderbook data with fees applied."""
        bids = []
        asks = []

        for order in raw_orderbook['bids'][:self.depth]:
            price, amount = order[:2]
            bids.append((float(price), float(amount), exchange_name))

        for order in raw_orderbook['asks'][:self.depth]:
            price, amount = order[:2]
            asks.append((float(price), float(amount), exchange_name))

        bids, asks = self.apply_fees(exchange_name, symbol, bids, asks)

        current_time = int(time.time() * 1000)
        if exchange_timestamp and exchange_timestamp > current_time:
            exchange_timestamp = current_time

        processed_book = {
            'exchange_timestamp': exchange_timestamp,
            'symbol': symbol,
            'bids': bids,
            'asks': asks
        }
        return processed_book

    @catch_exception
    def calculate_vwap(self, orders: List[Tuple], target_amount: float) -> List[Tuple]:
        """Calculate VWAP for given orders and target amount."""
        if not orders:
            return []

        vwap_orders = []
        remaining = target_amount
        total_value = total_amount = 0
        exchange = orders[0][2]

        for price, amount, _ in orders:
            if total_amount + amount >= remaining:
                partial = remaining - total_amount
                total_value += price * partial
                total_amount += partial
                vwap_price = total_value / total_amount
                vwap_orders.append((vwap_price, target_amount, exchange))
                total_value = total_amount = 0
                remaining = target_amount
            else:
                total_value += price * amount
                total_amount += amount

                if total_amount == target_amount:
                    vwap_price = total_value / total_amount
                    vwap_orders.append((vwap_price, target_amount, exchange))
                    total_value = total_amount = 0

        if total_amount > 0:
            vwap_price = total_value / total_amount
            vwap_orders.append((vwap_price, total_amount, exchange))

        return vwap_orders

    @catch_exception
    def _apply_weighting(self, orderbook: Dict, symbol: str) -> Dict:
        """Apply VWAP calculations based on weighting config."""
        if symbol not in self.config.weighting:
            return orderbook

        weighted_book = orderbook.copy()
        currency, target_amount = next(iter(self.config.weighting[symbol].items()))

        if currency == symbol.split('/')[1]:  # Quote currency
            target_amount = target_amount / orderbook['bids'][0][0]

        weighted_book['bids'] = self.calculate_vwap(orderbook['bids'], target_amount)
        weighted_book['asks'] = self.calculate_vwap(orderbook['asks'], target_amount)

        return weighted_book

    @catch_exception
    def _aggregate_orderbooks(self, orderbooks: List[Dict], primary_symbol: str) -> Dict:
        """Aggregate multiple orderbooks into a single orderbook."""
        if not orderbooks:
            return None

        # Get latest exchange timestamp
        latest_exchange_timestamp = max(
            (ob['exchange_timestamp'] for ob in orderbooks if ob.get('exchange_timestamp')),
            default=None
        )

        all_bids = []
        all_asks = []

        for ob in orderbooks:
            all_bids.extend(ob['bids'])
            all_asks.extend(ob['asks'])

        sorted_bids = sorted(all_bids, key=lambda x: float(x[0]), reverse=True)[:self.depth]
        sorted_asks = sorted(all_asks, key=lambda x: float(x[0]))[:self.depth]

        aggregated_book = {
            'exchange_timestamp': latest_exchange_timestamp,
            'symbol': primary_symbol,
            'bids': sorted_bids,
            'asks': sorted_asks
        }
        return aggregated_book

    @catch_exception
    async def _get_final_orderbook(self, symbol: str) -> Dict:
        """Get final processed orderbook based on configuration."""
        # Get all symbols in this group
        group_symbols = self.symbol_groups.get(symbol, {symbol})

        books = []
        for exchange_id, exchange_obs in self.orderbooks.items():
            # Only try to get orderbooks for symbols this exchange supports
            supported_symbols = self.exchange_symbols[exchange_id]
            for sym in group_symbols:
                if sym in supported_symbols and (ob := exchange_obs.get(sym)):
                    books.append(ob.copy())

        if not books:
            return self._latest_verified_books.get(symbol)  # Return last known good book if no new data

        if self.config.weighting:
            weighted_books = []
            for book in books:
                weighted_book = self._apply_weighting(book, symbol)
                weighted_books.append(weighted_book)
            books = weighted_books

        if self.config.aggregated:
            book = self._aggregate_orderbooks(books, symbol)
        else:
            book = books[0].copy()

        if book is None:
            return self._latest_verified_books.get(symbol)  # Return last known good book if aggregation fails

        # Always create the final book
        final_book = {
            'timestamp': int(time.time() * 1000),
            'exchange_timestamp': book['exchange_timestamp'],
            'symbol': symbol,
            'bids': book['bids'],
            'asks': book['asks']
        }

        # Check hash
        current_hash = OrderbookManager._hash_orderbook(book['bids'], book['asks'])
        if symbol not in self._last_hash or self._last_hash[symbol] != current_hash:
            # New data - update hash and latest verified book
            self._last_hash[symbol] = current_hash
            self._latest_verified_books[symbol] = final_book
            return final_book

        # If same hash but someone explicitly requested data, return the latest verified book
        return self._latest_verified_books.get(symbol)

    @catch_exception
    async def get_latest_orderbooks(self) -> Dict[str, Dict]:
        """Get latest processed orderbooks for all primary symbols."""
        async with self.lock:
            result = {}
            # Only process primary symbols (group keys)
            for symbol in self.symbol_groups.keys():
                book = await self._get_final_orderbook(symbol)
                if book:
                    result[symbol] = book
            return result

    @catch_exception
    async def _execute_callbacks(self, orderbook: Dict):
        """Execute registered callbacks with orderbook data."""
        for callback in self._callbacks:
            try:
                await callback(orderbook)
            except Exception as e:
                logger.error(f"Error in orderbook callback: {str(e)}")

    @catch_exception
    def add_callback(self, callback):
        """Register a new callback function."""
        self._callbacks.append(callback)

    @catch_exception
    def remove_callback(self, callback):
        """Remove a registered callback function."""
        if callback in self._callbacks:
            self._callbacks.remove(callback)

    @catch_exception
    async def start(self):
        """Start collecting orderbook data for all valid exchange-symbol combinations."""
        # First verify which exchanges support which symbols
        await self._verify_exchange_symbols()

        # Then create tasks only for valid combinations
        self._collection_tasks = [
            asyncio.create_task(self.collect_orderbook(exchange_id, symbol))
            for exchange_id, supported_symbols in self.exchange_symbols.items()
            for symbol in supported_symbols
        ]

    @catch_exception
    async def close(self):
        """Clean up resources and close exchange connections."""
        self.running = False
        for task in self._collection_tasks:
            task.cancel()
        if self._collection_tasks:
            await asyncio.gather(*self._collection_tasks, return_exceptions=True)
        self._collection_tasks.clear()
        await asyncio.gather(*[exchange.close() for exchange in self.exchanges.values()], return_exceptions=True)
