from django.core.paginator import Paginator
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.db.models import Q

from ..models import Recommendation, Restaurant, Category


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


class SearchView(TemplateView):
    template_name = "main/search.html"

    def get_context_data(self, **kwargs):
        page_number = self.request.GET.get("page", 1)
        keyword = self.request.GET.get("keyword")
        category_id = self.request.GET.get("category")

        category = None

        queryset = Restaurant.objects.filter(visible=True).order_by("-created_at")
        if keyword:
            queryset = queryset.filter(Q(name__istartswith=keyword) | Q(address__istartswith=keyword))
        if category_id:
            category = get_object_or_404(Category, id=int(category_id))
            queryset = queryset.filter(category=category)

        restaurants = queryset.all()
        paginator = Paginator(restaurants, 12)

        paging = paginator.get_page(page_number)

        return {
            "paging": paging,
            "selected_keyword": keyword,
            "selected_category": category,
        }
