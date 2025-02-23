import factory

from ..models import Brand
from ..utils.imaging import DjangoSampleImageCrafter


class BrandFactory(factory.django.DjangoModelFactory):
    """
    Factory to create instance of a Brand.
    """
    title = factory.Sequence(lambda n: "Brand {0}".format(n))
    slug = factory.Sequence(lambda n: "brand-{0}".format(n))
    description = factory.Faker("text", max_nb_chars=50)

    class Meta:
        model = Brand

    @factory.lazy_attribute
    def cover(self):
        """
        Fill cover field with generated image.

        Returns:
            django.core.files.File: File object.
        """
        crafter = DjangoSampleImageCrafter()
        return crafter.create()
