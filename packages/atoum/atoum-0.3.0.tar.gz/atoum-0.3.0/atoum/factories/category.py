import factory

from ..models import Category
from .assortment import AssortmentFactory


class CategoryFactory(factory.django.DjangoModelFactory):
    """
    Factory to create instance of a Category.
    """
    assortment = factory.SubFactory(AssortmentFactory)
    title = factory.Sequence(lambda n: "Category {0}".format(n))
    slug = factory.Sequence(lambda n: "category-{0}".format(n))

    class Meta:
        model = Category
