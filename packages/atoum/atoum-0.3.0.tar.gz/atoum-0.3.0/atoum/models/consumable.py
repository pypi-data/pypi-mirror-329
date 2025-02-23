from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils import timezone


class Consumable(models.Model):
    """
    The very top level of consumable classification.

    Attributes:
        created (models.DateTimeField): Required creation datetime, automatically
            filled.
        modified (models.DateTimeField): Required creation datetime, automatically
            filled.
        title (models.CharField): Required unique title string.
        slug (models.CharField): Required unique slug string.
    """
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
    List of field order commonly used in frontend view/api
    """

    class Meta:
        verbose_name = _("Consumable")
        verbose_name_plural = _("Consumables")
        ordering = [
            "title",
        ]

    def __str__(self):
        return self.title

    def get_assortments(self):
        """
        Return a queryset for assortment related to the consumable.

        Returns:
            Queryset:
        """
        return self.assortment_set.all()

    def get_absolute_url(self):
        """
        Return absolute URL to the detail view.

        Returns:
            string: An URL.
        """
        return reverse("atoum:consumable-detail", kwargs={
            "slug": self.slug,
        })

    def save(self, *args, **kwargs):
        # Auto update 'modified' value on each save
        self.modified = timezone.now()

        super().save(*args, **kwargs)
