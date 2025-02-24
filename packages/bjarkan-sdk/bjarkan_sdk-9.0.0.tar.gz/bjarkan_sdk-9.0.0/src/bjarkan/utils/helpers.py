import os
from typing import List, Optional
from bjarkan.models import APIConfig
from bjarkan.utils.logger import catch_exception


@catch_exception
def get_api_configs(exchanges: List[str]) -> Optional[List[APIConfig]]:
    """
    Get API configurations for specified exchanges from environment variables.

    Args:
        exchanges (List[str]): List of exchange names to get configurations for

    Returns:
        Optional[List[APIConfig]]: List of API configurations if successful, None if no valid configs

    Raises:
        ValueError: If any required credentials are missing

    Example:
        >>> api_configs = get_api_configs(['binance', 'bybit'])
    """
    api_configs = []
    missing_credentials = []

    # Exchanges that require additional password
    exchanges_with_password = {'okx'}

    for exchange in exchanges:
        exchange = exchange.lower()
        key = os.getenv(f'{exchange.upper()}_API_KEY')
        secret = os.getenv(f'{exchange.upper()}_API_SECRET')
        password = os.getenv(f'{exchange.upper()}_API_PASSWORD') if exchange in exchanges_with_password else None

        if not key or not secret or (exchange in exchanges_with_password and not password):
            missing_credentials.append(exchange)
            continue

        config = APIConfig(
            exchange=exchange,
            api_key=key,
            secret=secret,
            password=password
        )
        api_configs.append(config)

    if missing_credentials:
        raise ValueError(
            f"Missing API credentials for exchanges: {', '.join(missing_credentials)}\n"
            f"Please set environment variables for each exchange:\n" +
            "\n".join([
                f"- {ex.upper()}: {ex.upper()}_API_KEY, {ex.upper()}_API_SECRET" +
                (f", {ex.upper()}_API_PASSWORD" if ex in exchanges_with_password else "")
                for ex in missing_credentials
            ])
        )

    return api_configs if api_configs else None
