from django.contrib import admin

from ..forms import ShoppingItemInlineForm
from ..models import Shopping, ShoppingItem


class ShoppingItemInlineAdmin(admin.StackedInline):
    """
    Inline model admin controller for 'ShoppingItem' to be used in other model admin
    controllers.
    """
    form = ShoppingItemInlineForm
    model = ShoppingItem
    exclude = ["created", "modified"]
    extra = 0
    can_delete = True


@admin.register(Shopping)
class ShoppingAdmin(admin.ModelAdmin):
    """
    Model admin controller for 'Shopping'.
    """
    inlines = [
        ShoppingItemInlineAdmin,
    ]
