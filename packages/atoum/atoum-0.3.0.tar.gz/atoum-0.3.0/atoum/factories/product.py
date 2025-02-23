import factory

from ..models import Product
from ..utils.imaging import DjangoSampleImageCrafter
from .brand import BrandFactory
from .category import CategoryFactory


class ProductFactory(factory.django.DjangoModelFactory):
    """
    Factory to create instance of a Product.
    """
    category = factory.SubFactory(CategoryFactory)
    brand = factory.SubFactory(BrandFactory)
    title = factory.Sequence(lambda n: "Product {0}".format(n))
    slug = factory.Sequence(lambda n: "product-{0}".format(n))
    description = factory.Faker("text", max_nb_chars=50)

    class Meta:
        model = Product

    @factory.lazy_attribute
    def cover(self):
        """
        Fill cover field with generated image.

        Returns:
            django.core.files.File: File object.
        """
        crafter = DjangoSampleImageCrafter()
        return crafter.create()
