from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import Http404, HttpResponseBadRequest
from django.views.generic import ListView, TemplateView
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from dal import autocomplete

from ..models import Product
from .category import CategoryDetailView
from .consumable import ConsumableDetailView
from .assortment import AssortmentDetailView
from .mixins import AtoumBreadcrumMixin


class ProductIndexView(AtoumBreadcrumMixin, ListView):
    """
    List of products
    """
    model = Product
    template_name = "atoum/product/index.html"
    paginate_by = settings.PRODUCT_PAGINATION
    crumb_title = _("Products")
    crumb_urlname = "atoum:product-index"

    def get_queryset(self):
        return self.model.objects.order_by("title").select_related(
            *Product.HIERARCHY_SELECT_RELATED
        )

    @property
    def crumbs(self):
        return [
            (
                ProductIndexView.crumb_title,
                reverse(ProductIndexView.crumb_urlname)
            ),
        ]


class ProductDetailView(AtoumBreadcrumMixin, SingleObjectMixin, TemplateView):
    """
    Product detail and its related product list
    """
    template_name = "atoum/product/detail.html"
    context_object_name = "product_object"
    crumb_title = None  # No usage since title depends from object
    crumb_urlname = "atoum:product-detail"

    @property
    def crumbs(self):
        return [
            (
                self.object.category.assortment.consumable.title,
                reverse(ConsumableDetailView.crumb_urlname, kwargs={
                    "slug": self.object.category.assortment.consumable.slug,
                })
            ),
            (
                self.object.category.assortment.title,
                reverse(AssortmentDetailView.crumb_urlname, kwargs={
                    "consumable_slug": self.object.category.assortment.consumable.slug,
                    "assortment_slug": self.object.category.assortment.slug,
                })
            ),
            (
                self.object.category.title,
                reverse(CategoryDetailView.crumb_urlname, kwargs={
                    "consumable_slug": self.object.category.assortment.consumable.slug,
                    "assortment_slug": self.object.category.assortment.slug,
                    "category_slug": self.object.category.slug,
                })
            ),
            (
                self.object.title,
                reverse(self.crumb_urlname, kwargs={
                    "consumable_slug": self.object.category.assortment.consumable.slug,
                    "assortment_slug": self.object.category.assortment.slug,
                    "category_slug": self.object.category.slug,
                    "product_slug": self.object.slug,
                })
            ),
        ]

    def get_object(self):
        """
        Get the Product object for details
        """
        consumable_slug = self.kwargs.get("consumable_slug")
        assortment_slug = self.kwargs.get("assortment_slug")
        category_slug = self.kwargs.get("category_slug")
        product_slug = self.kwargs.get("product_slug")

        try:
            obj = Product.objects.filter(**{
                "category__assortment__consumable__slug": consumable_slug,
                "category__assortment__slug": assortment_slug,
                "category__slug": category_slug,
                "slug": product_slug,
            }).select_related(
                *Product.HIERARCHY_SELECT_RELATED
            ).get()
        except Product.DoesNotExist:
            raise Http404(
                _("No {} found matching the query").format(
                    Product._meta.verbose_name
                )
            )

        return obj

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        return super().get(request, *args, **kwargs)


class ProductAutocompleteView(UserPassesTestMixin, autocomplete.Select2QuerySetView):
    """
    View for Product autocompletion list with DAL.
    """
    def test_func(self):
        """
        Limit to admin only
        """
        return self.request.user.is_staff

    def get_queryset(self):
        """
        Build list queryset.

        Enable ``select_related`` on deep relations.
        """
        if not self.request.user.is_authenticated:
            return Product.objects.none()

        qs = Product.objects.all()

        if self.q:
            qs = qs.filter(title__istartswith=self.q).select_related(
                *Product.HIERARCHY_SELECT_RELATED
            )

        return qs.order_by(*Product.HIERARCHY_ORDER)

    def get_result_label(self, result):
        """
        Format a better list result display.
        """
        template = (
            "<small>{consumable} &gt; {assortment} &gt; {category}</small><br>{product}"
        )
        return format_html(
            template,
            consumable=result.category.assortment.consumable.title,
            assortment=result.category.assortment.title,
            category=result.category.title,
            product=result.title,
        )

    def get_selected_result_label(self, result):
        """
        Format a better selected result display.
        """
        return result.parenting_crumbs_html()

    def post(self, request, *args, **kwargs):
        """
        POST request is forbidden since DAL would allow creation of new object for a
        missing value and we don't want it.
        """
        return HttpResponseBadRequest()
