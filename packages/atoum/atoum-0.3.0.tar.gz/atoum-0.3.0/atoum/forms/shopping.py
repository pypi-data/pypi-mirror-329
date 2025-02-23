from django import forms

from dal import autocomplete

from ..models import Product, ShoppingItem


class ProductBreadcrumbChoiceField(forms.ModelChoiceField):
    """
    Customize product model choice field.
    """
    def label_from_instance(self, obj):
        """
        Display product parenting crumbs of a choice option.

        This label should be the same returned from
        ``ProductAutocompleteView.get_selected_result_label()``.
        """
        return obj.parenting_crumbs_html()


class ShoppingItemInlineForm(autocomplete.FutureModelForm):
    class Meta:
        fields = "__all__"
        model = ShoppingItem

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Override Product model form field to customize option label and enable
        # DAL autocompletion
        self.fields["product"] = ProductBreadcrumbChoiceField(
            queryset=Product.objects.all().select_related(
                "category",
                "category__assortment",
                "category__assortment__consumable"
            ),
            required=True,
            blank=False,
            widget=autocomplete.ModelSelect2(
                url="atoum:autocomplete-products",
                attrs={"data-html": True},
            ),
        )
