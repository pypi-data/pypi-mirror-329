from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils import timezone

from smart_media.mixins import SmartFormatMixin
from smart_media.modelfields import SmartMediaField
from smart_media.signals import auto_purge_files_on_change, auto_purge_files_on_delete


class Brand(SmartFormatMixin, models.Model):
    """
    Brand of products.

    Attributes:
        created (models.DateTimeField): Required creation datetime, automatically
            filled.
        modified (models.DateTimeField): Required creation datetime, automatically
            filled.
        title (models.CharField): Required unique title string.
        slug (models.CharField): Required unique slug string.
        description (models.TextField): Optional description long string.
        cover (SmartMediaField): Optional cover image file.
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
    description = models.TextField(
        _("description"),
        blank=True,
        default="",
    )
    cover = SmartMediaField(
        verbose_name=_("cover image"),
        upload_to="atoum/brand/cover/%y/%m",
        max_length=255,
        blank=True,
        default="",
    )

    COMMON_ORDER_BY = ["title"]
    """
    List of field order commonly used in frontend view/api
    """

    class Meta:
        verbose_name = _("Brand")
        verbose_name_plural = _("Brands")
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
        return reverse("atoum:brand-detail", args=[self.slug])

    def save(self, *args, **kwargs):
        # Auto update 'modified' value on each save
        self.modified = timezone.now()

        super().save(*args, **kwargs)


# Connect some signals
post_delete.connect(
    auto_purge_files_on_delete(["cover"]),
    dispatch_uid="brand_cover_on_delete",
    sender=Brand,
    weak=False,
)
pre_save.connect(
    auto_purge_files_on_change(["cover"]),
    dispatch_uid="brand_cover_on_change",
    sender=Brand,
    weak=False,
)
