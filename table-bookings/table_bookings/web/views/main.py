from django.views.generic import TemplateView
from ..models import Recommendation


class IndexView(TemplateView):
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        recommendation = Recommendation.objects.filter(
            visible=True
        ).select_related("restaurant", "restaurant__category", "restaurant__main_image").order_by("sort").all()[:4]

        context.update({
            "recommendation": recommendation
        })
        return context
