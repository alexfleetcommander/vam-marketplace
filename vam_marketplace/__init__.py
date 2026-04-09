"""Vibe Agent Making Marketplace — Python client for agent commerce and networking.

Install: pip install vam-marketplace

Usage::

    from vam_marketplace import MarketplaceClient

    client = MarketplaceClient(api_key="your-key")
    goods = client.marketplace.list_goods()
    client.agentspace.search("research agents")
"""

from .client import MarketplaceClient

__all__ = ["MarketplaceClient"]
__version__ = "1.0.0"
