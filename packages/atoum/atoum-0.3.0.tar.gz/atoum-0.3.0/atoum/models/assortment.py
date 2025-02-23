from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html


class Assortment(models.Model):
    """
    Assortment of consumables.

    Attributes:
        consumable (models.ForeignKey): Required Consumable object.
        created (models.DateTimeField): Required creation datetime, automatically
            filled.
        modified (models.DateTimeField): Required creation datetime, automatically
            filled.
        title (models.CharField): Required unique title string.
        slug (models.CharField): Required unique slug string.
    """
    consumable = models.ForeignKey(
        "atoum.consumable",
        verbose_name=_("Consumable"),
        on_delete=models.CASCADE
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

    COMMON_ORDER_BY = ["title"]
    """
    List of field names for ordering queryset related to the same consumable.
    """

    HIERARCHY_SELECT_RELATED = ["consumable"]
    """
    List of foreign-key relationships field names to "follow" in queryset to avoid
    multiple queries. Commonly used in ``Queryset.select_related()``.
    """

    HIERARCHY_ORDER = [
        "consumable__title",
        "title"
    ]
    """
    List of field names for ordering queryset respecting relationships. This is to be
    used when listing objects related to mixed consumables.
    """

    class Meta:
        verbose_name = _("Assortment")
        verbose_name_plural = _("Assortments")
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
        return reverse("atoum:assortment-detail", kwargs={
            "consumable_slug": self.consumable.slug,
            "assortment_slug": self.slug,
        })

    def parenting_crumbs(self):
        """
        Return parenting crumbs from Consumable to Assortment.

        Returns:
            list: List of crumb titles in order.
        """
        return [
            self.consumable.title,
            self.title
        ]

    def parenting_crumbs_html(self):
        """
        Display HTML of Assortment label with its parent consumable.

        Returns:
            string: A label such as ``Consumable > Assortment``.
        """
        return format_html("{0} &gt; {1}", *self.parenting_crumbs())

    def get_categories(self):
        """
        Return a queryset for categories related to the assortment.

        Returns:
            Queryset:
        """
        return self.category_set.all().prefetch_related("product_set")

    def save(self, *args, **kwargs):
        # Auto update 'modified' value on each save
        self.modified = timezone.now()

        super().save(*args, **kwargs)
