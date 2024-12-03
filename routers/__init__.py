# routers/__init__.py

from .router import router
from .dashboard_router import dashboard_router
from .user_router import user_router
from .product_router import product_router
from .category_router import category_router
from .brand_router import brand_router
from .tag_router import tag_router
from .unit_router import unit_router
from .main_router import main_router  # Import the new main_router

__all__ = [
    'router',
    'dashboard_router',
    'user_router',
    'product_router',
    'category_router',
    'brand_router',
    'tag_router',
    'unit_router',
    'main_router'  # Add to the list of available routers
]
