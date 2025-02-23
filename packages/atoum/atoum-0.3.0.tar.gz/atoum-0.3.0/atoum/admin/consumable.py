from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from ..models import Consumable
from .assortment import AssortmentInline


class ConsumableResource(resources.ModelResource):
    """
    Data resource configuration for 'django-import-export'.
    """
    class Meta:
        model = "atoum.Consumable"
        fields = ("title", "slug")
        import_id_fields = ("slug",)


@admin.register(Consumable)
class ConsumableAdmin(ImportExportModelAdmin):
    """
    Model admin controller.
    """
    readonly_fields = ["created", "modified"]
    prepopulated_fields = {
        "slug": ("title",),
    }
    ordering = Consumable.COMMON_ORDER_BY
    search_fields = [
        "title",
    ]
    list_display = (
        "title",
        "count_assortments",
        "modified",
    )
    inlines = [
        AssortmentInline,
    ]
    resource_classes = [ConsumableResource]

    def count_assortments(self, obj):
        """
        Count related assortments.
        """
        return obj.assortment_set.count()
    count_assortments.short_description = _("Assortments")
