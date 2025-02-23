from zoneinfo import ZoneInfo

import factory
from faker import Faker

from ..models import Shopping, ShoppingItem
from .product import ProductFactory


class ShoppingFactory(factory.django.DjangoModelFactory):
    """
    Factory to create instance of a Shopping.
    """
    title = factory.Sequence(lambda n: "Shopping {0}".format(n))
    done = False

    class Meta:
        model = Shopping
        skip_postgeneration_save = True

    @factory.lazy_attribute
    def planning(self):
        """
        Fill planning with a datetime this year after now.

        Returns:
            datetime.datetime: A datetime.
        """
        value = Faker().date_time_this_year(
            after_now=True,
            tzinfo=ZoneInfo("UTC"),
        )

        return value.replace()

    @factory.post_generation
    def fill_products(self, create, extracted, **kwargs):
        """
        Add products.

        Arguments:
            create (bool): True for create strategy, False for build strategy.
            extracted (object): If ``True``, will create a new random product
                object. If a list assume it's a list of tuple ``(Product, Dict)``
                for item to add. The ``Dict`` is a dictionnary for ``through_defaults``
                to use that should at least contains required ``quantity`` value.
        """
        # Do nothing for build strategy
        if not create or not extracted:
            return

        # Create a new random item adopting directly with the item factory
        if extracted is True:
            ShoppingItemFactory(shopping=self)
        # Take given item objects
        else:
            # Add items
            for product, through_defaults in extracted:
                self.products.add(product, through_defaults=through_defaults)


class ShoppingItemFactory(factory.django.DjangoModelFactory):
    """
    Factory to create instance of a ShoppingItem.
    """
    shopping = factory.SubFactory(ShoppingFactory)
    product = factory.SubFactory(ProductFactory)
    quantity = 1
    done = False

    class Meta:
        model = ShoppingItem
