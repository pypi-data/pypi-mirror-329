from django.views.generic import ListView


from ..models import Consumable


class RecursiveTreeView(ListView):
    """
    Full recursive tree of Atoum objects (excepted Brand).

    .. WARNING::

        This recursive tree is highly innefficient on database queries.
        Usage of ``prefetch_related`` is not enough to avoid cascade of queryset for
        products.

        If this view is to be keeped, it will need to be optimized with a tree resolving
        that would gather objects of respectively all consumables, assortments,
        categories and then products.

    .. TODO::
        At least if we can make this more efficient and needs to keep it, make it
        restricted to staff users. And possibly cache it ?
    """
    model = Consumable
    template_name = "atoum/recursivetree.html"
    paginate_by = None

    def get_queryset(self):
        q = self.model.objects.all().prefetch_related("assortment_set")
        return q.order_by("title")
