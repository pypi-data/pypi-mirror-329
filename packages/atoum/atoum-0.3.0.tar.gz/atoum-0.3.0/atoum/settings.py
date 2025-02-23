"""
Default application settings
----------------------------

These are the default settings you can override in your own project settings
right after the line which load the default app settings.

"""

ASSORTMENT_PAGINATION = 30
"""
Assortment per page limit for pagination, set it to ``None`` to disable
pagination.
"""

CATEGORY_PAGINATION = 25
"""
Category per page limit for pagination, set it to ``None`` to disable
pagination.
"""

PRODUCT_PAGINATION = 50
"""
Product per page limit for pagination, set it to ``None`` to disable
pagination.
"""

ATOUM_BREADCRUMBS_SHOW_HOME = True
"""
If breadcrumbs should include the site homepage entry or not. This is only working
in Atoum views.
"""
