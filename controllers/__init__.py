# controllers/__init__.py

from .dashboard_controller import dashboard
# from .user_controller import user
from .product_controller import product
from .category_controller import category
from .brand_controller import brand
from .tag_controller import tag
from .unit_controller import unit

# You can also create an easy way to access all controllers if needed
__all__ = [
    'dashboard',
    # 'user',
    'product',
    'category',
    'brand',
    'tag',
    'unit',
]
