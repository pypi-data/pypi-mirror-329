import asyncio
from typing import Dict, List, Optional, Callable
from bjarkan.utils.logger import logger, catch_exception
import ccxt.pro as ccxt

from bjarkan.models import OrderbookConfig, TradesConfig, APIConfig, OrderConfig
from bjarkan.core.orderbook import OrderbookManager
from bjarkan.core.trades import TradesManager
from bjarkan.core.executor import OrderExecutor
from bjarkan.exceptions import BjarkanError


class BjarkanSDK:
    """Main SDK client for interacting with cryptocurrency exchanges."""

    @catch_exception
    def __init__(self):
        self._orderbook_manager = None
        self._trades_manager = None
        self._order_executor = None
        self._running = True
        logger.info("Initialized Bjarkan SDK")

    @catch_exception
    async def __aenter__(self):
        """Async context manager entry point."""
        return self

    @catch_exception
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit point that automatically cleans up resources."""
        await self.close()
        return False  # Allow any exceptions to propagate

    @catch_exception
    async def set_config(self, *, type: str, **config_params) -> Dict:
        """Unified configuration method for both orderbook and trades.

        Args:
            type: The type of configuration ('orderbook' or 'trades')
            **config_params: Configuration parameters specific to the type

        Returns:
            Dict with status and message

        Examples:
            --> await sdk.set_config(
            ...     type="orderbook",
            ...     aggregated=True,
            ...     exchanges=["binance", "okx"],
            ...     symbols=["BTC/USDT"],
            ...     depth=10
            ... )
        """
        if not isinstance(type, str):
            raise BjarkanError(f"Config type must be a string, got {type.__class__.__name__}")

        type = type.lower()
        if type not in ['orderbook', 'trades']:
            raise BjarkanError(
                f"Invalid config type: '{type}'. Must be 'orderbook' or 'trades'."
                "\nExample usage:"
                "\n  await sdk.set_config("
                "\n      type='orderbook',"
                "\n      aggregated=True,"
                "\n      exchanges=['binance', 'okx'],"
                "\n      symbols=['BTC/USDT'],"
                "\n      depth=10"
                "\n  )"
            )

        if type == 'orderbook':
            config = OrderbookConfig(**config_params)
            self._orderbook_manager = OrderbookManager(config)
            return {"status": "success", "message": "Orderbook configuration set"}
        else:  # trades
            config = TradesConfig(**config_params)
            self._trades_manager = TradesManager(config)
            return {"status": "success", "message": "Trades configuration set"}

    @catch_exception
    async def start_stream(self, stream_type: str, callback: Optional[Callable] = None,
                           timeout: Optional[float] = None) -> Dict:
        """
        Unified method to start either orderbook or trades stream.

        Args:
            stream_type: Either 'orderbook' or 'trades'
            callback: Optional callback function to receive updates
            timeout: Optional timeout in seconds. If None, runs indefinitely.

        Returns:
            Dict: Status and message
        """
        if stream_type not in ['orderbook', 'trades']:
            raise BjarkanError(f"Invalid stream type: {stream_type}. Must be 'orderbook' or 'trades'")

        if stream_type == 'orderbook':
            if not self._orderbook_manager:
                raise BjarkanError("Orderbook not configured. Call set_config(type='orderbook', ...) first")
            if callback:
                self._orderbook_manager.add_callback(callback)
            await self._orderbook_manager.start(timeout=timeout)
            return {"status": "success", "message": "Orderbook stream started"}
        else:  # trades
            if not self._trades_manager:
                raise BjarkanError("Trades not configured. Call set_config(type='trades', ...) first")
            if callback:
                self._trades_manager.add_callback(callback)
            await self._trades_manager.start(timeout=timeout)
            return {"status": "success", "message": "Trades stream started"}

    @catch_exception
    async def stop_stream(self, stream_type: str) -> Dict:
        """Unified method to stop either orderbook or trades stream."""
        if stream_type not in ['orderbook', 'trades']:
            raise BjarkanError(f"Invalid stream type: {stream_type}. Must be 'orderbook' or 'trades'")

        if stream_type == 'orderbook':
            if self._orderbook_manager:
                await self._orderbook_manager.close()
                return {"status": "success", "message": "Orderbook stream stopped"}
        else:  # trades
            if self._trades_manager:
                await self._trades_manager.close()
                return {"status": "success", "message": "Trades stream stopped"}
        return {"status": "success", "message": f"{stream_type} stream was not running"}

    @catch_exception
    async def get_latest_data(self, data_type: str) -> Dict:
        """Unified method to get latest data from either orderbook or trades."""
        if data_type not in ['orderbook', 'trades']:
            raise BjarkanError(f"Invalid data type: {data_type}. Must be 'orderbook' or 'trades'")

        if data_type == 'orderbook':
            if not self._orderbook_manager:
                raise BjarkanError("Orderbook not configured. Call set_config(type='orderbook', ...) first")
            return await self._orderbook_manager.get_latest_orderbooks()
        else:  # trades
            if not self._trades_manager:
                raise BjarkanError("Trades not configured. Call set_config(type='trades', ...) first")
            return await self._trades_manager.get_latest_trades()

    @catch_exception
    async def initialize_executor(self, api_configs: List[APIConfig], margin_mode: bool = False) -> None:
        """Initialize the order executor with API configs."""
        if not self._orderbook_manager:
            raise BjarkanError("Orderbook must be configured before initializing executor. Call set_config(type='orderbook', ...) first")

        if not self._orderbook_manager.config.aggregated:
            raise BjarkanError("Orderbook must be configured with aggregation enabled for order execution")

        # Create and initialize executor
        self._order_executor = OrderExecutor(self._orderbook_manager.config, api_configs, margin_mode)
        await self._order_executor.initialize()

    @catch_exception
    async def execute_order(self, order: OrderConfig) -> Dict:
        """Execute an order using the initialized executor."""
        if not self._order_executor:
            raise BjarkanError("Order executor not initialized. Call initialize_executor first")

        # Get latest orderbook data for execution
        orderbook = await self.get_latest_data('orderbook')

        # Execute the order
        await self._order_executor.update_orderbook(orderbook)
        return await self._order_executor.execute_order(order)

    @catch_exception
    async def close(self):
        """Clean up resources and close connections."""
        self._running = False
        tasks = []

        if self._orderbook_manager:
            tasks.append(self._orderbook_manager.close())
        if self._trades_manager:
            tasks.append(self._trades_manager.close())
        if self._order_executor:
            tasks.append(self._order_executor.close())

        await asyncio.gather(*tasks, return_exceptions=True)
        logger.info("SDK closed")
