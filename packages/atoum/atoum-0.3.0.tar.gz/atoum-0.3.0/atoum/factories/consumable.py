import factory

from ..models import Consumable


class ConsumableFactory(factory.django.DjangoModelFactory):
    """
    Factory to create instance of a Consumable.
    """
    title = factory.Sequence(lambda n: "Consumable {0}".format(n))
    slug = factory.Sequence(lambda n: "consumable-{0}".format(n))

    class Meta:
        model = Consumable
