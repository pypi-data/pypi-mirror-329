from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils import timezone


class Shopping(models.Model):
    """
    Shopping object to gather choices of products.

    Attributes:
        created (models.DateTimeField): Required creation datetime, automatically
            filled.
        planning (models.DateTimeField): Required planning datetime, automatically
            filled.
        title (models.CharField): Optional title string.
        done (models.CharField): Optional boolean.
        products (models.ManyToManyField): Optional product selection
    """
    created = models.DateTimeField(
        _("creation date"),
        db_index=True,
        default=timezone.now,
    )
    planning = models.DateTimeField(
        _("planning date"),
        db_index=True,
        default=timezone.now,
    )
    title = models.CharField(
        _("title"),
        blank=True,
        max_length=100,
        default="",
    )
    done = models.BooleanField(
        verbose_name=_("done"),
        default=False,
        blank=True,
    )
    products = models.ManyToManyField(
        "atoum.Product",
        verbose_name=_("items"),
        related_name="shoppings",
        blank=True,
        through="atoum.ShoppingItem",
        through_fields=("shopping", "product"),
    )

    COMMON_ORDER_BY = ["-planning"]
    """
    List of field order commonly used in frontend view/api
    """

    class Meta:
        verbose_name = _("Shopping")
        verbose_name_plural = _("Shoppings")
        ordering = [
            "title",
        ]

    def __str__(self):
        """
        TODO: We should return a localized and humanized date when falling back to
        planning date because of empty title.
        """
        return self.title or str(self.planning)

    def get_absolute_url(self):
        """
        Return absolute URL to the detail view.

        Returns:
            string: An URL.
        """
        return reverse("atoum:shopping-detail", args=[self.id])

    def save(self, *args, **kwargs):
        # Auto update 'modified' value on each save
        self.modified = timezone.now()

        super().save(*args, **kwargs)


class ShoppingItem(models.Model):
    """
    Shopping list item object.

    .. todo::
        Quantity value may be a choice field if product unit was a volume or weight.

    Attributes:
        created (models.DateTimeField): Required creation datetime, automatically
            filled.
        shopping (atoum.models.Shopping): Required
        product (atoum.models.Product): Required
        quantity (models.PositiveSmallIntegerField): Required positive small integer.
        done (models.CharField): Optional boolean.
    """
    created = models.DateTimeField(
        _("creation date"),
        default=timezone.now,
    )
    shopping = models.ForeignKey(
        "atoum.Shopping",
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        "atoum.Product",
        on_delete=models.CASCADE
    )
    quantity = models.PositiveSmallIntegerField(_("quantity"))
    done = models.BooleanField(
        verbose_name=_("done"),
        default=False,
        blank=True,
    )

    class Meta:
        verbose_name = _("Shopping item")
        verbose_name_plural = _("Shopping items")
        ordering = [
            "shopping", "product",
        ]
        constraints = [
            # Enforce unique couple shopping + product
            models.UniqueConstraint(
                fields=[
                    "shopping", "product"
                ],
                name="atoum_unique_shoppingitem_shopping_product"
            ),
        ]
