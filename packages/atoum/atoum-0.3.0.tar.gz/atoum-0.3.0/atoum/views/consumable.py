from django.conf import settings
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ..models import Consumable
from .mixins import AtoumBreadcrumMixin


class ConsumableIndexView(AtoumBreadcrumMixin, ListView):
    """
    List of consumables
    """
    model = Consumable
    template_name = "atoum/consumable/index.html"
    paginate_by = None
    crumb_title = _("Consumables")
    crumb_urlname = "atoum:consumable-index"

    @property
    def crumbs(self):
        return [
            (
                ConsumableIndexView.crumb_title,
                reverse(ConsumableIndexView.crumb_urlname)
            ),
        ]

    def get_queryset(self):
        return self.model.objects.order_by("title")


class ConsumableDetailView(AtoumBreadcrumMixin, SingleObjectMixin, ListView):
    """
    Consumable detail and its related assortment list
    """
    template_name = "atoum/consumable/detail.html"
    paginate_by = settings.ASSORTMENT_PAGINATION
    context_object_name = "consumable_object"
    crumb_title = None  # No usage since title depends from object
    crumb_urlname = "atoum:consumable-detail"

    @property
    def crumbs(self):
        return [
            (
                self.object.title,
                reverse(self.crumb_urlname, kwargs={"slug": self.object.slug})
            ),
        ]

    def get_queryset(self):
        return self.object.assortment_set.order_by("title")

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Consumable.objects.all())

        return super().get(request, *args, **kwargs)
