from django.urls import path

from .views import (
    AssortmentAutocompleteView,
    AssortmentDetailView,
    AssortmentIndexView,
    CategoryAutocompleteView,
    CategoryDetailView,
    CategoryIndexView,
    ConsumableDetailView,
    ConsumableIndexView,
    DashboardView,
    DummyView,
    GlobalSearchView,
    ProductAutocompleteView,
    ProductDetailView,
    ProductIndexView,
    RecursiveTreeView,
)


app_name = "atoum"


urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),

    # Full recursive tree of everything
    path("tree/", RecursiveTreeView.as_view(), name="tree"),

    path(
        "consumables/",
        ConsumableIndexView.as_view(),
        name="consumable-index"
    ),
    path(
        "assortments/",
        AssortmentIndexView.as_view(),
        name="assortment-index"
    ),
    path(
        "categories/",
        CategoryIndexView.as_view(),
        name="category-index"
    ),
    path(
        "products/",
        ProductIndexView.as_view(),
        name="product-index"
    ),
    path(
        "consumables/<slug:slug>/",
        ConsumableDetailView.as_view(),
        name="consumable-detail"
    ),
    path(
        "consumables/<slug:consumable_slug>/<slug:assortment_slug>/",
        AssortmentDetailView.as_view(),
        name="assortment-detail"
    ),
    path(
        (
            "consumables/<slug:consumable_slug>/<slug:assortment_slug>/"
            "<slug:category_slug>/"
        ),
        CategoryDetailView.as_view(),
        name="category-detail"
    ),
    path(
        (
            "consumables/<slug:consumable_slug>/<slug:assortment_slug>/"
            "<slug:category_slug>/<slug:product_slug>/"
        ),
        ProductDetailView.as_view(),
        name="product-detail"
    ),

    # TODO: These are temporarily dummy views enabled to allow reversing until
    # implemented
    path(
        "brands/<slug:slug>/",
        DummyView.as_view(),
        name="brand-detail"
    ),

    # Autocomplete views for various models, only for staff users
    path(
        "autocomplete/assortments/",
        AssortmentAutocompleteView.as_view(),
        name="autocomplete-assortments",
    ),
    path(
        "autocomplete/categories/",
        CategoryAutocompleteView.as_view(),
        name="autocomplete-categories",
    ),
    path(
        "autocomplete/products/",
        ProductAutocompleteView.as_view(),
        name="autocomplete-products",
    ),

    path("search/", GlobalSearchView.as_view(), name="search-results"),
]
