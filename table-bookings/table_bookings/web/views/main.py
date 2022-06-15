import datetime

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

        weekday = self.request.GET.get("weekday")
        start_time = self.request.GET.get("start")
        end_time = self.request.GET.get("end")

        category = None

        queryset = Restaurant.objects.filter(visible=True).order_by("-created_at")
        if keyword:
            queryset = queryset.filter(Q(name__istartswith=keyword) | Q(address__istartswith=keyword))
        if category_id:
            category = get_object_or_404(Category, id=int(category_id))
            queryset = queryset.filter(category=category)

        relation_conditions = None

        if weekday:
            # SELECT * FROM Restaurant r INNER JOIN RestaurantTable rt ON rt.restaurant_id = r.id
            # WHERE rt.weekday = :weekday
            relation_conditions = Q(restauranttable__weekday=weekday)

        if start_time:
            start_time = datetime.time.fromisoformat(start_time)

            if relation_conditions:
                relation_conditions = relation_conditions & Q(restauranttable__time__gte=start_time)
            else:
                relation_conditions = Q(restauranttable__time__gte=start_time)

        if end_time:
            end_time = datetime.time.fromisoformat(end_time)

            if relation_conditions:
                relation_conditions = relation_conditions & Q(restauranttable__time__lte=end_time)
            else:
                relation_conditions = Q(restauranttable__time__lte=end_time)

        if relation_conditions:
            queryset = queryset.filter(relation_conditions)

        restaurants = queryset.distinct().all()
        paginator = Paginator(restaurants, 12)

        paging = paginator.get_page(page_number)

        return {
            "paging": paging,
            "selected_keyword": keyword,
            "selected_category": category,
            "selected_weekday": weekday,
            "selected_start": datetime.time.isoformat(start_time) if start_time else "",
            "selected_end": datetime.time.isoformat(end_time) if end_time else "",
        }
