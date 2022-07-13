from django.views.generic import TemplateView


class OfficeIndexView(TemplateView):
    template_name = "office/main/index.html"

    def get_context_data(self, **kwargs):
        return {}
