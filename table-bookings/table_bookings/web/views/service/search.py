import datetime

from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.core.cache import cache

from ...models import Restaurant, Category


class RestaurantSearch:
    def create_cache_key(self, keyword, category_id, weekday, start_time, end_time, page_number):
        return f"{keyword}:{category_id}:{weekday}:{start_time}:{end_time}:{page_number}"

    def search(self, keyword, category_id, weekday, start_time, end_time, page_number):
        cache_key = self.create_cache_key(keyword, category_id, weekday, start_time, end_time, page_number)
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data

        category = None

        queryset = Restaurant.objects.filter(visible=True).order_by("-created_at")
        if keyword and len(keyword) > 0:
            queryset = queryset.filter(Q(name__istartswith=keyword) | Q(address__istartswith=keyword))
        if category_id and len(category_id) > 0:
            category = get_object_or_404(Category, id=int(category_id))
            queryset = queryset.filter(category=category)

        relation_conditions = None

        if weekday and len(weekday) > 0:
            # SELECT * FROM Restaurant r INNER JOIN RestaurantTable rt ON rt.restaurant_id = r.id
            # WHERE rt.weekday = :weekday
            relation_conditions = Q(restauranttable__weekday=weekday)

        if start_time and len(start_time) > 0:
            start_time = datetime.time.fromisoformat(start_time)

            if relation_conditions:
                relation_conditions = relation_conditions & Q(restauranttable__time__gte=start_time)
            else:
                relation_conditions = Q(restauranttable__time__gte=start_time)

        if end_time and len(end_time) > 0:
            end_time = datetime.time.fromisoformat(end_time)

            if relation_conditions:
                relation_conditions = relation_conditions & Q(restauranttable__time__lte=end_time)
            else:
                relation_conditions = Q(restauranttable__time__lte=end_time)

        if relation_conditions:
            queryset = queryset.filter(relation_conditions)

        restaurants = queryset.distinct().all()
        paginator = Paginator(restaurants, 8)

        paging = paginator.get_page(page_number)

        result = {
            "paging": paging,
            "selected_keyword": keyword,
            "selected_category": category,
            "selected_weekday": weekday,
            "selected_start": datetime.time.isoformat(start_time) if start_time else "",
            "selected_end": datetime.time.isoformat(end_time) if end_time else "",
            "has_next_page": paging.has_next()
        }
        cache.set(cache_key, result, 60)
        return result
