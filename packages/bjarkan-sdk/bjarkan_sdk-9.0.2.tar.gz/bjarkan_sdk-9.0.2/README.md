# Bjarkan SDK

A sophisticated cryptocurrency trading SDK that provides real-time market data aggregation, smart order routing (SOR), and execution capabilities across multiple exchanges.

## Features

- **Real-time Market Data**
  - Aggregated and individual orderbooks across multiple exchanges
  - Trade monitoring with customizable size filters
  - Support for spot, margin, perpetuals, futures and options data/trading
  - Fee-aware price adjustments
  
- **Smart Order Routing**
  - Best execution path calculation
  - VWAP-based price discovery
  - Slippage simulation
  - Cross-exchange liquidity aggregation

- **Advanced Orderbook Processing**
  - Symbol grouping for related markets (e.g., USDT/USDC pairs)
  - Configurable depth levels
  - Custom fee structures
  - Volume-weighted price calculations for slippage simulations

- **Exchange Support**
  - Multiple exchanges (Binance, Bybit, OKX, Coinbase, etc.)
  - Unified API interface
  - Sandbox/testnet mode for testing
  - Comprehensive error handling and logging


---

## For Users

## Installation

```bash
pip install bjarkan-sdk
```

## Quick Start

### Market Data Monitoring

```python
import asyncio
from bjarkan import BjarkanSDK

async def orderbook_callback(orderbook):
    print(f"\nOrderbook Update for {orderbook['symbol']}:")
    print("Top 5 Bids:")
    for price, amount, exchange in orderbook['bids'][:5]:
        print(f"  {exchange}: {price:.2f} @ {amount:.4f}")

async def main():
    # Initialize SDK
    sdk = BjarkanSDK()
    
    # Configure orderbook settings
    await sdk.set_config(
        type="orderbook",
        aggregated=True,
        exchanges=["binance", "bybit", "okx"],
        symbols=["BTC/USDT", "ETH/USDT"],  # Will return 2 different aggregated books
        depth=20
    )
    
    # Start streaming
    await sdk.start_stream("orderbook", callback=orderbook_callback)
    
    # Run for 60 seconds
    await asyncio.sleep(60)
    
    # Cleanup
    await sdk.stop_stream("orderbook")
    await sdk.close()

if __name__ == "__main__":
    asyncio.run(main())
```

### Trade Execution

```python
import asyncio
from bjarkan import BjarkanSDK
from bjarkan.models import OrderConfig

async def main():
    # Initialize SDK
    sdk = BjarkanSDK()
    
    # Configure for trading
    await sdk.set_config(
        type="orderbook",
        aggregated=True,
        exchanges=["binance", "bybit", "okx", "kraken"],
        symbols=["BTC/USDT"],
        depth=20
    )
    
    # Initialize order executor
    api_configs = [
        {
            "exchange": "binance",
            "api_key": "your_api_key",
            "api_secret": "your_secret"
        },
        {
            "exchange": "bybit",
            "api_key": "your_api_key",
            "api_secret": "your_api_secret"
        }
    ]
    
    await sdk.initialize_executor(api_configs)
    
    # Create and execute order
    order = OrderConfig(
        side="buy",
        amount=0.01  # BTC
    )
    
    result = await sdk.execute_order(order)
    print(f"Order execution result: {result}")
    
    await sdk.close()

if __name__ == "__main__":
    asyncio.run(main())
```

## Configuration

API configurations can be passed directly as the `api_configs` dictionary or added to your `.env` file and accessed using the `get_api_config` function.
```python
from bjarkan.utils.helpers import get_api_configs
```

### Environment Variables

Create a `.env` file in your project root:

```env
# Exchange API Keys
BINANCE_API_KEY=your_api_key
BINANCE_API_SECRET=your_secret

BYBIT_API_KEY=your_api_key
BYBIT_API_SECRET=your_secret

OKX_API_KEY=your_api_key
OKX_API_SECRET=your_secret
OKX_API_PASSWORD=your_password

# Optional Logging
BETTERSTACK_TOKEN=your_token
```

### Orderbook Configuration

The SDK supports various orderbook configuration options:

```python
await sdk.set_config(
    type="orderbook",
    aggregated=True,                # Enable cross-exchange aggregation
    exchanges=["binance", "bybit", "coinbase", "okx"],
    symbols=["BTC/USDT", "BTC/USDC"],
    depth=100,                      # Orderbook depth to maintain
    fees_bps={                      # Optional fee configuration
        "binance": 10,              # 0.1% fee
        "bybit": {"BTC/USDT": 10}   # Symbol-specific fees
    },
    group={                        # Optional symbol grouping
        "BTC/USDT": "BTC/USDC"     # Treat BTC/USDT and BTC/USDC pairs as same market
    },
    weighting={"BTC/USDT":         # VWAP to make every level worth $1,000
                   {"USDT": 1000}
               }
)
```

### Trade Monitor Configuration

For monitoring trades across exchanges:

```python
await sdk.set_config(
    type="trades",
    exchanges=["binance", "bybit", "okx"],
    symbols=["BTC/USDT", "ETH/USDT"],
    size={                          # Optional size filters
        "BTC/USDT": {"USDT": 10000} # Only trades > $10,000
    }
)
```

## Advanced Usage

### Sandbox Testing

Enable sandbox/testnet mode for testing. Note that you will need to pass the testnet API keys, and only Binance and Bybit are currently supported for sandbox mode:

```python
await sdk.set_config(
    type="orderbook",
    aggregated=True,
    exchanges=["binance", "bybit"],
    sandbox_mode={
        "binance": True,
        "bybit": True
    },
    symbols=["BTC/USDT"],
    depth=20
)
```

### Margin Trading

Enable spot margin trading mode:

```python
await sdk.initialize_executor(api_configs, margin_mode=True)
```

---

## For developers

### Deployment

1. Update version:
```bash
python bump_version.py patch  # or minor/major
```

2. Deploy to PyPI:
```bash
./deploy.sh
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
