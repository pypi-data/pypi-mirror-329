from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html


class Category(models.Model):
    """
    Category of a consumable assortment.

    Attributes:
        assortment (models.ForeignKey): Required Assortment object.
        created (models.DateTimeField): Required creation datetime, automatically
            filled.
        modified (models.DateTimeField): Required creation datetime, automatically
            filled.
        title (models.CharField): Required unique title string.
        slug (models.CharField): Required unique slug string.
    """
    assortment = models.ForeignKey(
        "atoum.assortment",
        verbose_name=_("Assortment"),
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
    )
    slug = models.CharField(
        _("slug"),
        blank=False,
        max_length=130,
        default="",
    )

    COMMON_ORDER_BY = ["title"]
    """
    List of field names for ordering queryset related to the same assortment.
    """

    HIERARCHY_SELECT_RELATED = [
        "assortment",
        "assortment__consumable"
    ]
    """
    List of foreign-key relationships field names to "follow" in queryset to avoid
    multiple queries. Commonly used in ``Queryset.select_related()``.
    """

    HIERARCHY_ORDER = [
        "assortment__consumable__title",
        "assortment__title",
        "title"
    ]
    """
    List of field names for ordering queryset respecting relationships. This is to be
    used when listing objects related to mixed assortments.
    """

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = [
            "title",
        ]
        constraints = [
            # Enforce unique couple assortment + title
            models.UniqueConstraint(
                fields=[
                    "assortment", "title"
                ],
                name="atoum_unique_cat_assortment_title"
            ),
            # Enforce unique couple assortment + slug
            models.UniqueConstraint(
                fields=[
                    "assortment", "slug"
                ],
                name="atoum_unique_cat_assortment_slug"
            ),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """
        Return absolute URL to the detail view.

        Returns:
            string: An URL.
        """
        return reverse("atoum:category-detail", kwargs={
            "consumable_slug": self.assortment.consumable.slug,
            "assortment_slug": self.assortment.slug,
            "category_slug": self.slug,
        })

    def parenting_crumbs(self):
        """
        Return parenting crumbs from Consumable to Assortment to Category.

        Returns:
            list: List of crumb titles in order.
        """
        return [
            self.assortment.consumable.title,
            self.assortment.title,
            self.title
        ]

    def parenting_crumbs_html(self):
        """
        Display HTML of Category label with its parent consumable then assortment.

        Returns:
            string: A label such as ``Consumable > Assortment > Category``.
        """
        return format_html("{0} &gt; {1} &gt; {2}", *self.parenting_crumbs())

    def get_products(self):
        """
        Return a queryset for products related to the category.

        Returns:
            Queryset:
        """
        return self.product_set.all()

    def save(self, *args, **kwargs):
        # Auto update 'modified' value on each save
        self.modified = timezone.now()

        super().save(*args, **kwargs)
