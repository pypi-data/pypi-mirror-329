from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from smart_media.admin import SmartModelAdmin

from ..models import Brand


@admin.register(Brand)
class BrandAdmin(SmartModelAdmin):
    readonly_fields = ["created", "modified"]
    prepopulated_fields = {
        "slug": ("title",),
    }
    ordering = Brand.COMMON_ORDER_BY
    search_fields = [
        "title",
        "description",
    ]
    list_display = (
        "title",
        "count_products",
        "modified",
    )

    def count_products(self, obj):
        """
        Count related products.
        """
        return obj.product_set.count()
    count_products.short_description = _("Products")
