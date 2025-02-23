from django.views.generic import TemplateView
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ..models import Assortment, Category, Consumable, Product
from .mixins import AtoumBreadcrumMixin


class DashboardView(AtoumBreadcrumMixin, TemplateView):
    """
    Catalog dashboard view

    .. todo::
        This should list:

        * Catalog models
        * open shopping lists
        * stock resume

    """
    template_name = "atoum/dashboard.html"
    crumb_title = _("Catalog dashboard")
    crumb_urlname = "atoum:dashboard"

    @property
    def crumbs(self):
        return [
            (self.crumb_title, reverse(self.crumb_urlname)),
        ]

    def get_consumable_queryset(self):
        """
        Build consumable queryset.
        """
        qs = Consumable.objects.all().order_by(*Consumable.COMMON_ORDER_BY)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            "consumable_count": Consumable.objects.all().count(),
            "assortment_count": Assortment.objects.all().count(),
            "category_count": Category.objects.all().count(),
            "product_count": Product.objects.all().count(),
        })

        return context
