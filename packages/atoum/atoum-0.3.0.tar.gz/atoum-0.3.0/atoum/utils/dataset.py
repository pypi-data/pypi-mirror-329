import json

from atoum.models import Assortment, Brand, Category, Consumable, Product

from dataclasses import dataclass, field


@dataclass
class InitialCatalog:
    """
    Class for keeping track of created catalog objects.

    .. Note::
        The tree methods purpose is mostly for debugging. Their behavior is to start
        from stored objects then recursively list their children directly from database
        instead of those from this dataclass because retrieving children is more
        difficult from store than from db.
    """
    assortments: dict[Assortment] = field(default_factory=dict)
    brands: dict[Brand] = field(default_factory=dict)
    consumables: dict[Consumable] = field(default_factory=dict)
    categories: dict[Category] = field(default_factory=dict)
    products: dict[Product] = field(default_factory=dict)

    def get_repr(self, value, attr=None):
        """
        Return representation of an object.

        Arguments:
            value (object): Model object.

        Keyword Arguments:
            attr (string): If given it will get representation from given attribute
                from given object. Else on default it uses the ``repr()`` function.
        """
        if attr:
            return getattr(value, attr)
        return repr(value)

    def get_product_tree(self, category, attr=None):
        """
        Get recursive tree of all Product objects.

        Keyword Arguments:
            category (Category): Category object to walk directly from database.
                If not given, default is to walk on all stored Category objects.
            attr (string): If given it will get representation from given attribute
                from given object. Else on default it uses the ``repr()`` function.
                The representation attribute is given to all recursive method so it
                must exists on all models.

        Returns:
            list: List of tuples, each tuple contains the object slug and null value,
            since product has no children but we want to conserve the same dump
            structure for all model.
        """
        products = (
            category.get_products()
            if category
            else self.products.values()
        )
        return [
            (self.get_repr(v, attr=attr), None)
            for v in products
        ]

    def get_category_tree(self, assortment=None, attr=None):
        """
        Get recursive tree of all Category objects.

        Keyword Arguments:
            assortment (Assortment): Assortment object to walk directly from database.
                If not given, default is to walk on all stored Assortment objects.
            attr (string): If given it will get representation from given attribute
                from given object. Else on default it uses the ``repr()`` function.
                The representation attribute is given to all recursive method so it
                must exists on all models.

        Returns:
            list: List of tuples, each tuple contains the object slug and its possible
                children products.
        """
        categories = (
            assortment.get_categories()
            if assortment
            else self.categories.values()
        )
        return [
            (self.get_repr(v, attr=attr), self.get_product_tree(v, attr=attr))
            for v in categories
        ]

    def get_assortment_tree(self, consumable=None, attr=None):
        """
        Get recursive tree of all Assortment objects.

        Keyword Arguments:
            consumable (Consumable): Consumable object to walk directly from database.
                If not given, default is to walk on all stored Consumable objects.
            attr (string): If given it will get representation from given attribute
                from given object. Else on default it uses the ``repr()`` function.
                The representation attribute is given to all recursive method so it
                must exists on all models.

        Returns:
            list: List of tuples, each tuple contains the object slug and its possible
                children categories.
        """
        assortments = (
            consumable.get_assortments()
            if consumable
            else self.assortments.values()
        )
        return [
            (self.get_repr(v, attr=attr), self.get_category_tree(v, attr=attr))
            for v in assortments
        ]

    def get_consumable_tree(self, attr=None):
        """
        Get recursive tree of all stored Consumable objects.

        Keyword Arguments:
            attr (string): If given it will get representation from given attribute
                from given object. Else on default it uses the ``repr()`` function.
                The representation attribute is given to all recursive method so it
                must exists on all models.

        Returns:
            list: List of tuples, each tuple contains the object slug and its possible
                children assortments.
        """
        return [
            (self.get_repr(v, attr=attr), self.get_assortment_tree(v, attr=attr))
            for v in self.consumables.values()
        ]

    def get_brand_tree(self, attr=None):
        """
        Get recursive tree of all stored Brand objects.

        .. Note::
            Opposed to other model objects, Brand is out the consumable tree and live
            along so it is not included in every "full tree" methods.

        .. Todo::
            Each brand should list its related products.

        Keyword Arguments:
            attr (string): If given it will get representation from given attribute
                from given object. Else on default it uses the ``repr()`` function.
                The representation attribute is given to all recursive method so it
                must exists on all models.

        Returns:
            list: List of tuples, each tuple contains the object slug and a null value
            to be consistant with other tree structure.
        """
        return [
            (self.get_repr(v, attr=attr), None)
            for v in self.brands.values()
        ]

    def get_json_tree(self, attr=None):
        """
        Return a JSON payload of the full tree starting from consumables.

        Keyword Arguments:
            attr (string): If given it will get representation from given attribute
                from given object. Else on default it uses the ``repr()`` function.
                The representation attribute is given to all recursive method so it
                must exists on all models.

        Returns:
            string: JSON payload.
        """
        return json.dumps(self.get_consumable_tree(attr=attr), indent=4)

    def _recursive_walk(self, nodes, items, level=1, attr=None):
        if items:
            indent = ("   " * level) + "└─"
            for key, children in items:
                nodes.append(indent + key)
                self._recursive_walk(nodes, children, level=level + 1)

    def get_ascii_tree(self, attr=None):
        """
        Build a basic recursive ascii tree starting from consumables.

        Keyword Arguments:
            attr (string): If given it will get representation from given attribute
                from given object. Else on default it uses the ``repr()`` function.
                The representation attribute is given to all recursive method so it
                must exists on all models.

        Returns:
            string: An ascii tree.
        """
        nodes = []
        for key, children in self.get_consumable_tree(attr=attr):
            nodes.append("───" + key)
            self._recursive_walk(nodes, children)

        return "\n".join(nodes)
