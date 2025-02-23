from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export import fields
from import_export.widgets import ForeignKeyWidget
from smart_media.admin import SmartAdminMixin

from ..forms import ProductAdminForm
from ..models import Category, Product


class ProductResource(resources.ModelResource):
    """
    Data resource configuration for 'django-import-export'.
    """
    category = fields.Field(
        column_name="category",
        attribute="category",
        widget=ForeignKeyWidget(Category, field="title")
    )

    class Meta:
        model = "atoum.Product"
        fields = ("title", "slug", "category", "description")
        import_id_fields = ("slug",)


@admin.register(Product)
class ProductAdmin(SmartAdminMixin, ImportExportModelAdmin):
    """
    Model admin controller.
    """
    form = ProductAdminForm
    list_select_related = ["category"]
    readonly_fields = ["created", "modified"]
    prepopulated_fields = {
        "slug": ("title",),
    }
    ordering = Product.COMMON_ORDER_BY
    search_fields = [
        "title",
        "description",
    ]
    list_display = (
        "title",
        "category",
        "brand",
        "modified",
    )
    autocomplete_fields = ["brand"]
    list_filter = (
        "category",
        "brand",
    )
    resource_classes = [ProductResource]


class ProductAdminInline(admin.StackedInline):
    """
    Inline model admin controller to be used in other model admin controllers.
    """
    model = Product
    autocomplete_fields = ["category", "brand"]
    exclude = ["created", "modified", "description"]
    prepopulated_fields = {
        "slug": ("title",),
    }
    extra = 0
    can_delete = False
