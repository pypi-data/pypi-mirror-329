# netdots/__init__.py

# Global API key that the user must set.
api_key = None

# (Optional) Expose the internal client if needed.
from .api_client import Netdots

__all__ = ["api_key", "Netdots"]
