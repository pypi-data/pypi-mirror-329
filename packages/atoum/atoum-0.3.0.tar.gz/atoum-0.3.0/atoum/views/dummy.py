from django.views.generic import TemplateView


class DummyView(TemplateView):
    """
    Temporary dummy view that show nothing. Used for get_absolute_url from models until
    their detail view has been done.
    """
    template_name = "atoum/dummy.html"
