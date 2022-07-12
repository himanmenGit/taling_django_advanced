from django.views.generic import TemplateView, View
from django.http import JsonResponse
from django.db.models import Avg

from ..models import Recommendation, Restaurant
from .service.search import RestaurantSearch


class IndexView(TemplateView):
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        recommendation = Recommendation.objects.filter(
            visible=True
        ).select_related("restaurant", "restaurant__category", "restaurant__main_image").order_by("sort").all()[:4]

        latest = Restaurant.objects.order_by("-created_at")[:4]
        hottest = Restaurant.objects.annotate(
            average_ratings=Avg("review__ratings")
        ).filter(average_ratings__gte=0).order_by("-average_ratings")[:4]

        context.update({
            "recommendation": recommendation,
            "latest": latest,
            "hottest": hottest
        })
        return context


class SearchView(TemplateView, RestaurantSearch):
    template_name = "main/search.html"

    def get_context_data(self, **kwargs):
        page_number = self.request.GET.get("page", 1)
        keyword = self.request.GET.get("keyword")
        category_id = self.request.GET.get("category")

        weekday = self.request.GET.get("weekday")
        start_time = self.request.GET.get("start")
        end_time = self.request.GET.get("end")

        return self.search(keyword, category_id, weekday, start_time, end_time, page_number)


class SearchJsonView(View, RestaurantSearch):
    def get(self, reqeust):
        page_number = self.request.GET.get("page", 1)
        keyword = self.request.GET.get("keyword")
        category_id = self.request.GET.get("category")

        weekday = self.request.GET.get("weekday")
        start_time = self.request.GET.get("start")
        end_time = self.request.GET.get("end")

        data = self.search(keyword, category_id, weekday, start_time, end_time, page_number)

        result_list = list(
            map(
                lambda restaurant: {
                    "id": restaurant.id,
                    "name": restaurant.name,
                    "address": restaurant.address,
                    "image": str(restaurant.main_image.image),
                    "category_name": restaurant.category.name
                }, data.get("paging")
            )
        )
        results = {
            "has_next_page": data.get("has_next_page", False),
            "object_list": result_list
        }
        return JsonResponse(results, safe=False)
