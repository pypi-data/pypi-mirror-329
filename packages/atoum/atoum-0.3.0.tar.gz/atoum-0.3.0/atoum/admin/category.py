from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export import fields
from import_export.widgets import ForeignKeyWidget

from ..forms import CategoryAdminForm
from ..models import Assortment, Category
from .product import ProductAdminInline


class CategoryResource(resources.ModelResource):
    """
    Data resource configuration for 'django-import-export'.
    """
    assortment = fields.Field(
        column_name="assortment",
        attribute="assortment",
        widget=ForeignKeyWidget(Assortment, field="title")
    )

    class Meta:
        model = "atoum.Category"
        fields = ("title", "slug", "assortment")
        import_id_fields = ("slug", "assortment")


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    """
    Model admin controller.
    """
    form = CategoryAdminForm
    list_select_related = ["assortment"]
    readonly_fields = ["created", "modified"]
    prepopulated_fields = {
        "slug": ("title",),
    }
    ordering = Category.COMMON_ORDER_BY
    search_fields = [
        "title",
    ]
    list_display = (
        "title",
        "assortment",
        "count_products",
        "modified",
    )
    list_filter = (
        "assortment",
    )
    inlines = [
        ProductAdminInline,
    ]
    resource_classes = [CategoryResource]

    def count_products(self, obj):
        """
        Count related products.
        """
        return obj.product_set.count()
    count_products.short_description = _("Products")


class CategoryInline(admin.StackedInline):
    """
    Inline model admin controller to be used in other model admin controllers.
    """
    model = Category
    exclude = ["created", "modified"]
    prepopulated_fields = {
        "slug": ("title",),
    }
    extra = 0
    can_delete = False
