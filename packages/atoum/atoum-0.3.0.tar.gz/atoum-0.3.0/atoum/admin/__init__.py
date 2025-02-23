from .assortment import AssortmentAdmin, AssortmentResource
from .brand import BrandAdmin
from .category import CategoryAdmin, CategoryResource
from .consumable import ConsumableAdmin, ConsumableResource
from .product import ProductAdmin, ProductAdminInline, ProductResource
from .shopping import ShoppingAdmin


__all__ = [
    "AssortmentAdmin",
    "AssortmentResource",
    "BrandAdmin",
    "CategoryAdmin",
    "CategoryResource",
    "ConsumableResource",
    "ConsumableAdmin",
    "ProductAdmin",
    "ProductResource",
    "ProductAdminInline",
    "ShoppingAdmin",
]
