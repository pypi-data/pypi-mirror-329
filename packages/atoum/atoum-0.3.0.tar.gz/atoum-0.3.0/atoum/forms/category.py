from django import forms

from dal import autocomplete

from ..models import Assortment, Category


class AssortmentBreadcrumbChoiceField(forms.ModelChoiceField):
    """
    Customize assortment model choice field.
    """
    def label_from_instance(self, obj):
        """
        Display assortment parenting crumbs of a choice option.

        This label should be the same returned from
        ``AssortmentAutocompleteView.get_selected_result_label()``.
        """
        return obj.parenting_crumbs_html()


class CategoryAdminForm(autocomplete.FutureModelForm):
    class Meta:
        fields = "__all__"
        model = Category

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Override Assortment model form field to customize option label and enable
        # DAL autocompletion
        self.fields["assortment"] = AssortmentBreadcrumbChoiceField(
            queryset=Assortment.objects.all().select_related("consumable"),
            required=True,
            blank=False,
            widget=autocomplete.ModelSelect2(
                url="atoum:autocomplete-assortments",
                attrs={"data-html": True},
            ),
        )
