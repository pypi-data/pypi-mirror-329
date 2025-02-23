from django import forms

from dal import autocomplete

from ..models import Category, Product


class CategoryBreadcrumbChoiceField(forms.ModelChoiceField):
    """
    Customize category model choice field.
    """
    def label_from_instance(self, obj):
        """
        Display category parenting crumbs of a choice option.

        This label should be the same returned from
        ``CategoryAutocompleteView.get_selected_result_label()``.
        """
        return obj.parenting_crumbs_html()


class ProductAdminForm(autocomplete.FutureModelForm):
    class Meta:
        fields = "__all__"
        model = Product

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Override Category model form field to customize option label and enable
        # DAL autocompletion
        self.fields["category"] = CategoryBreadcrumbChoiceField(
            queryset=Category.objects.all().select_related(
                "assortment",
                "assortment__consumable"
            ),
            required=True,
            blank=False,
            widget=autocomplete.ModelSelect2(
                url="atoum:autocomplete-categories",
                attrs={"data-html": True},
            ),
        )
