from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export import fields
from import_export.widgets import ForeignKeyWidget

from ..models import Assortment, Consumable
from .category import CategoryInline


class AssortmentResource(resources.ModelResource):
    """
    Data resource configuration for 'django-import-export'.
    """
    consumable = fields.Field(
        column_name="consumable",
        attribute="consumable",
        widget=ForeignKeyWidget(Consumable, field="title")
    )

    class Meta:
        model = "atoum.Assortment"
        fields = ("title", "slug", "consumable")
        import_id_fields = ("slug",)


@admin.register(Assortment)
class AssortmentAdmin(ImportExportModelAdmin):
    """
    Model admin controller.
    """
    list_select_related = ["consumable"]
    readonly_fields = ["created", "modified"]
    prepopulated_fields = {
        "slug": ("title",),
    }
    ordering = Assortment.COMMON_ORDER_BY
    search_fields = [
        "title",
    ]
    list_display = (
        "title",
        "consumable",
        "count_categories",
        "modified",
    )
    list_filter = (
        "consumable",
    )
    autocomplete_fields = ["consumable"]
    inlines = [
        CategoryInline,
    ]
    resource_classes = [AssortmentResource]

    def count_categories(self, obj):
        """
        Count related categories.
        """
        return obj.category_set.count()
    count_categories.short_description = _("Categories")


class AssortmentInline(admin.StackedInline):
    """
    Inline model admin controller to be used in other model admin controllers.
    """
    model = Assortment
    exclude = ["created", "modified"]
    prepopulated_fields = {
        "slug": ("title",),
    }
    extra = 0
    can_delete = False
