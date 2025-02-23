from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html

from smart_media.mixins import SmartFormatMixin
from smart_media.modelfields import SmartMediaField
from smart_media.signals import auto_purge_files_on_change, auto_purge_files_on_delete


class Product(SmartFormatMixin, models.Model):
    """
    Product of a Category.

    TODO: We should add a new field 'unit' that would be a choice of free(?), volume,
    weight. So shopping item can choose a proper quantity like 50L for a volume or
    2Kg for a weight and finally a free quantity amount for a free input.

    Attributes:
        category (models.ForeignKey): Required Assortment object.
        brand (models.ForeignKey): Optional Brand object.
        created (models.DateTimeField): Required creation datetime, automatically
            filled.
        modified (models.DateTimeField): Required creation datetime, automatically
            filled.
        title (models.CharField): Required unique title string.
        slug (models.CharField): Required unique slug string.
        description (models.TextField): Optional description long string.
        cover (SmartMediaField): Optional cover image file.
    """
    category = models.ForeignKey(
        "atoum.category",
        verbose_name=_("Category"),
        on_delete=models.CASCADE
    )
    brand = models.ForeignKey(
        "atoum.brand",
        verbose_name=_("brand"),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        default=None,
    )
    created = models.DateTimeField(
        _("creation date"),
        db_index=True,
        default=timezone.now,
    )
    modified = models.DateTimeField(
        _("modification date"),
        db_index=True,
        default=timezone.now,
    )
    title = models.CharField(
        _("title"),
        blank=False,
        max_length=100,
        default="",
        unique=True,
    )
    slug = models.CharField(
        _("slug"),
        blank=False,
        max_length=130,
        default="",
        unique=True,
    )
    description = models.TextField(
        _("description"),
        blank=True,
        default="",
    )
    cover = SmartMediaField(
        verbose_name=_("cover image"),
        upload_to="atoum/product/cover/%y/%m",
        max_length=255,
        blank=True,
        default="",
    )

    COMMON_ORDER_BY = ["title"]
    """
    List of field names for ordering queryset related to the same assortment.
    """

    HIERARCHY_SELECT_RELATED = [
        "category",
        "category__assortment",
        "category__assortment__consumable",
    ]
    """
    List of foreign-key relationships field names to "follow" in queryset to avoid
    multiple queries. Commonly used in ``Queryset.select_related()``.
    """

    HIERARCHY_ORDER = [
        "category__assortment__consumable__title",
        "category__assortment__title",
        "category__title",
        "title"
    ]
    """
    List of field names for ordering queryset respecting relationships. This is to be
    used when listing assortments related to mixed consumables.
    """

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        ordering = [
            "title",
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """
        Return absolute URL to the detail view.

        Returns:
            string: An URL.
        """
        return reverse("atoum:product-detail", kwargs={
            "consumable_slug": self.category.assortment.consumable.slug,
            "assortment_slug": self.category.assortment.slug,
            "category_slug": self.category.slug,
            "product_slug": self.slug,
        })

    def parenting_crumbs(self):
        """
        Return parenting crumbs from Consumable to Assortment to Category to Product.

        Returns:
            list: List of crumb titles in order.
        """
        return [
            self.category.assortment.consumable.title,
            self.category.assortment.title,
            self.category.title,
            self.title
        ]

    def parenting_crumbs_html(self):
        """
        Display HTML of Product label with its parent consumable then assortment.

        Returns:
            string: A label such as ``Consumable > Assortment > Category > Product``.
        """
        return format_html("{0} &gt; {1} &gt; {2} &gt; {3}", *self.parenting_crumbs())

    def save(self, *args, **kwargs):
        # Auto update 'modified' value on each save
        self.modified = timezone.now()

        super().save(*args, **kwargs)


# Connect some signals
post_delete.connect(
    auto_purge_files_on_delete(["cover"]),
    dispatch_uid="product_cover_on_delete",
    sender=Product,
    weak=False,
)
pre_save.connect(
    auto_purge_files_on_change(["cover"]),
    dispatch_uid="product_cover_on_change",
    sender=Product,
    weak=False,
)
