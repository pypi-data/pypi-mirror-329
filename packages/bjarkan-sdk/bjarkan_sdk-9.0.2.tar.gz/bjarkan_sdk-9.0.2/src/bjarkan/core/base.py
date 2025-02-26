import asyncio
import time
from typing import Dict, List, Set, Optional, Callable
import ccxt.pro as ccxt
from bjarkan.utils.logger import logger, catch_exception
from bjarkan.exceptions import BjarkanError


class BaseExchangeManager:
    """Base class for exchange data managers (orderbook and trades)."""
    @catch_exception
    def __init__(self, config):
        self.config = config
        self.exchanges = self._initialize_exchanges()
        self.exchange_symbols = {}  # Map of exchange -> supported symbols
        self.running = True
        self.lock = asyncio.Lock()
        self.update_event = asyncio.Event()
        self._callbacks = []
        self._collection_tasks = []

    @catch_exception
    def _initialize_exchanges(self) -> Dict[str, ccxt.Exchange]:
        """Initialize exchange instances with appropriate settings."""
        exchanges = {}
        for exchange_id in self.config.exchanges:
            exchange_class = getattr(ccxt, exchange_id)
            instance = exchange_class({
                'enableRateLimit': True,
            })
            is_sandbox = self.config.sandbox_mode.get(exchange_id, False)
            instance.set_sandbox_mode(is_sandbox)
            exchanges[exchange_id] = instance
        return exchanges

    @catch_exception
    async def _verify_exchange_symbols(self):
        """Verify which symbols are available on each exchange."""
        for exchange_id, exchange in self.exchanges.items():
            markets = await exchange.load_markets()
            available_symbols = set()
            for symbol in self.config.symbols:
                if symbol in markets:
                    available_symbols.add(symbol)
            self.exchange_symbols[exchange_id] = available_symbols
            logger.info(f"Exchange {exchange_id} supports symbols: {available_symbols}")

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
    async def _execute_callbacks(self, data):
        """Execute registered callbacks with data."""
        for callback in self._callbacks:
            await callback(data)

    @catch_exception
    async def start(self, timeout=None):
        """
        Start collecting data for all valid exchange-symbol combinations.
        Args:
            timeout: Optional timeout in seconds. If None, runs indefinitely.
        """
        # First verify which exchanges support which symbols
        await self._verify_exchange_symbols()

        # Subclasses should override and implement this method to create collection tasks
        # using self._create_collection_tasks() and then call super().start(timeout)

        # If timeout is set, create a task to handle it
        if timeout is not None:
            asyncio.create_task(self._handle_timeout(timeout))

    @catch_exception
    async def _handle_timeout(self, timeout):
        """Handle timeout for the manager."""
        await asyncio.sleep(timeout)
        logger.info(f"Manager reached timeout of {timeout} seconds")
        self.running = False

    @catch_exception
    async def close(self):
        """Clean up resources and close exchange connections."""
        self.running = False

        # Cancel any running collection tasks
        for task in self._collection_tasks:
            task.cancel()
        if self._collection_tasks:
            await asyncio.gather(*self._collection_tasks, return_exceptions=True)
        self._collection_tasks.clear()

        # Close exchange connections
        await asyncio.gather(*[exchange.close() for exchange in self.exchanges.values()], return_exceptions=True)
        self._callbacks.clear()

        logger.info(f"{self.__class__.__name__} closed")
