from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import Http404, HttpResponseBadRequest
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from dal import autocomplete

from ..models import Category
from .consumable import ConsumableDetailView
from .assortment import AssortmentDetailView
from .mixins import AtoumBreadcrumMixin


class CategoryIndexView(AtoumBreadcrumMixin, ListView):
    """
    List of categories
    """
    model = Category
    template_name = "atoum/category/index.html"
    paginate_by = settings.CATEGORY_PAGINATION
    crumb_title = _("Categories")
    crumb_urlname = "atoum:category-index"

    def get_queryset(self):
        return self.model.objects.order_by("title").select_related(
                *Category.HIERARCHY_SELECT_RELATED
            )

    @property
    def crumbs(self):
        return [
            (
                CategoryIndexView.crumb_title,
                reverse(CategoryIndexView.crumb_urlname)
            ),
        ]


class CategoryDetailView(AtoumBreadcrumMixin, SingleObjectMixin, ListView):
    """
    Category detail and its related category list
    """
    template_name = "atoum/category/detail.html"
    paginate_by = settings.PRODUCT_PAGINATION
    context_object_name = "category_object"
    crumb_title = None  # No usage since title depends from object
    crumb_urlname = "atoum:category-detail"

    @property
    def crumbs(self):
        return [
            (
                self.object.assortment.consumable.title,
                reverse(ConsumableDetailView.crumb_urlname, kwargs={
                    "slug": self.object.assortment.consumable.slug,
                })
            ),
            (
                self.object.assortment.title,
                reverse(AssortmentDetailView.crumb_urlname, kwargs={
                    "consumable_slug": self.object.assortment.consumable.slug,
                    "assortment_slug": self.object.assortment.slug,
                })
            ),
            (
                self.object.title,
                reverse(self.crumb_urlname, kwargs={
                    "consumable_slug": self.object.assortment.consumable.slug,
                    "assortment_slug": self.object.assortment.slug,
                    "category_slug": self.object.slug,
                })
            ),
        ]

    def get_queryset(self):
        """
        Queryset to list sub relations
        """
        return self.object.product_set.order_by("title")

    def get_object(self):
        """
        Get the Category object for details
        """
        consumable_slug = self.kwargs.get("consumable_slug")
        assortment_slug = self.kwargs.get("assortment_slug")
        category_slug = self.kwargs.get("category_slug")

        try:
            obj = Category.objects.filter(**{
                "assortment__consumable__slug": consumable_slug,
                "assortment__slug": assortment_slug,
                "slug": category_slug,
            }).select_related(
                *Category.HIERARCHY_SELECT_RELATED
            ).get()
        except Category.DoesNotExist:
            raise Http404(
                _("No {} found matching the query").format(
                    Category._meta.verbose_name
                )
            )

        return obj

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        return super().get(request, *args, **kwargs)


class CategoryAutocompleteView(UserPassesTestMixin, autocomplete.Select2QuerySetView):
    """
    View for Category autocompletion list with DAL.
    """
    def test_func(self):
        """
        Limit to admin only
        """
        return self.request.user.is_staff

    def get_queryset(self):
        """
        Build list queryset.

        Enable ``select_related`` on relation ``assortment`` because we intend to use
        it commonly in labels.
        """
        if not self.request.user.is_authenticated:
            return Category.objects.none()

        qs = Category.objects.all()

        if self.q:
            qs = qs.filter(title__istartswith=self.q).select_related(
                *Category.HIERARCHY_SELECT_RELATED
            )

        return qs.order_by(*Category.HIERARCHY_ORDER)

    def get_result_label(self, result):
        """
        Format a better list result display.
        """
        return format_html(
            "<small>{consumable} &gt; {assortment}</small><br>{category}",
            consumable=result.assortment.consumable.title,
            assortment=result.assortment.title,
            category=result.title,
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
