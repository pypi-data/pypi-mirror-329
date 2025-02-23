from haystack import indexes

from .models import Assortment, Category, Consumable, Product


class ProductIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(
        document=True,
        use_template=True,
        template_name="atoum/search/base_field_indexes_template.txt"
    )
    title_partial = indexes.EdgeNgramField(model_attr="title")

    def get_model(self):
        return Product


class AssortmentIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(
        document=True,
        use_template=True,
        template_name="atoum/search/base_field_indexes_template.txt"
    )
    title_partial = indexes.EdgeNgramField(model_attr="title")

    def get_model(self):
        return Assortment


class ConsumableIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(
        document=True,
        use_template=True,
        template_name="atoum/search/base_field_indexes_template.txt"
    )
    title_partial = indexes.EdgeNgramField(model_attr="title")

    def get_model(self):
        return Consumable


class CategoryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(
        document=True,
        use_template=True,
        template_name="atoum/search/base_field_indexes_template.txt"
    )
    title_partial = indexes.EdgeNgramField(model_attr="title")

    def get_model(self):
        return Category
