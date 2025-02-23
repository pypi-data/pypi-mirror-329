import factory

from ..models import Assortment
from .consumable import ConsumableFactory


class AssortmentFactory(factory.django.DjangoModelFactory):
    """
    Factory to create instance of a Assortment.
    """
    consumable = factory.SubFactory(ConsumableFactory)
    title = factory.Sequence(lambda n: "Assortment {0}".format(n))
    slug = factory.Sequence(lambda n: "assortment-{0}".format(n))

    class Meta:
        model = Assortment
