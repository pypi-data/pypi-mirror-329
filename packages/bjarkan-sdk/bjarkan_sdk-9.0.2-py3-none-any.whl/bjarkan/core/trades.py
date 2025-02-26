import asyncio
import time
from typing import Dict, List, Set
import ccxt.pro as ccxt
from bjarkan.models import TradesConfig
from bjarkan.utils.logger import logger, catch_exception
from bjarkan.core.base import BaseExchangeManager
from bjarkan.exceptions import BjarkanError


class TradesManager(BaseExchangeManager):
    @catch_exception
    def __init__(self, trades_config: TradesConfig):
        """Initialize TradesManager with given configuration."""
        super().__init__(trades_config)
        self.config = trades_config
        self.symbols = trades_config.symbols
        self.fees = self._initialize_fees()
        self.size_filters = trades_config.size or {}
        self.trades = {}  # Will be initialized after symbol verification

    @catch_exception
    async def _verify_exchange_symbols(self):
        """Verify which symbols are available on each exchange."""
        await super()._verify_exchange_symbols()

        # Initialize trades dictionary only for supported symbols
        self.trades = {
            ex: {sym: [] for sym in symbols}
            for ex, symbols in self.exchange_symbols.items()
        }

    @catch_exception
    def _initialize_fees(self) -> Dict[str, Dict[str, float]]:
        """Initialize fee structure for all exchanges and symbols."""
        if not self.config.fees_bps:
            return {exchange: {symbol: 0 for symbol in self.symbols} for exchange in self.exchanges}

        fees = {}
        for exchange, fee_info in self.config.fees_bps.items():
            if isinstance(fee_info, dict):
                fees[exchange] = {symbol: fee / 10000 for symbol, fee in fee_info.items()}
            else:
                fees[exchange] = {symbol: fee_info / 10000 for symbol in self.symbols}
        return fees

    @catch_exception
    def apply_fees(self, exchange: str, symbol: str, price: float, amount: float) -> tuple:
        """Apply exchange fees to trade price."""
        fee = self.fees.get(exchange, {}).get(symbol, 0)
        if fee != 0:
            price = round(price * (1 + fee), 8)
        return price, amount

    @catch_exception
    def filter_by_size(self, symbol: str, price: float, amount: float) -> bool:
        """Check if trade meets minimum size requirements."""
        if symbol not in self.size_filters:
            return True

        filter_info = self.size_filters[symbol]
        base, quote = symbol.split('/')

        if base in filter_info:
            return amount >= filter_info[base]
        elif quote in filter_info:
            return price * amount >= filter_info[quote]

        return True

    @catch_exception
    async def collect_trades(self, exchange_name: str, symbol: str):
        """Collect and process trade data from specified exchange."""
        # Skip if exchange doesn't support this symbol
        if symbol not in self.exchange_symbols.get(exchange_name, set()):
            logger.warning(f"Skipping collection for {exchange_name}.{symbol} - symbol not supported")
            return

        exchange = self.exchanges[exchange_name]

        while self.running:
            trades = await exchange.watch_trades(symbol)

            async with self.lock:
                for trade in trades:
                    price, amount = self.apply_fees(exchange_name, symbol, trade['price'], trade['amount'])

                    if self.filter_by_size(symbol, price, amount):
                        processed_trade = {
                            'id': trade['id'],
                            'symbol': symbol,
                            'exchange': exchange_name,
                            'timestamp': int(time.time() * 1000),
                            'exchange_timestamp': trade['timestamp'],
                            'price': price,
                            'amount': amount,
                            'side': trade['side']
                        }

                        self.trades[exchange_name][symbol].append(processed_trade)

                        # Execute callbacks outside of the lock
                        asyncio.create_task(self._execute_callbacks(processed_trade))

            self.update_event.set()

            # Small sleep to prevent tight loop
            await asyncio.sleep(0.01)

    @catch_exception
    async def get_latest_trades(self) -> Dict[str, Dict[str, List]]:
        """Get latest trades for all exchange-symbol pairs."""
        async with self.lock:
            latest_trades = {
                ex: {symbol: trades.copy() for symbol, trades in symbol_trades.items()}
                for ex, symbol_trades in self.trades.items()
            }

            # Clear the stored trades after returning them
            for ex in self.trades:
                for symbol in self.trades[ex]:
                    self.trades[ex][symbol].clear()

            return latest_trades

    @catch_exception
    async def _create_collection_tasks(self):
        """Create collection tasks for trade data."""
        # Clear any existing tasks
        self._collection_tasks.clear()

        # Create tasks for each valid combination
        for exchange_id, supported_symbols in self.exchange_symbols.items():
            for symbol in supported_symbols:
                task = asyncio.create_task(self.collect_trades(exchange_id, symbol))
                self._collection_tasks.append(task)

    @catch_exception
    async def start(self, timeout=None):
        """
        Start collecting trade data for all valid exchange-symbol combinations.
        Args:
            timeout: Optional timeout in seconds. If None, runs indefinitely.
        """
        # First verify which symbols are supported
        await self._verify_exchange_symbols()

        # Create collection tasks
        await self._create_collection_tasks()

        # Call parent implementation for timeout handling
        await super().start(timeout)

        logger.info("Trades manager started")
