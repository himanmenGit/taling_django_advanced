from datetime import timedelta, date

from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.utils import timezone

from ..models import Restaurant, RestaurantTable, RestaurantImage
from ..utils import convert_weekday


class RestaurantView(TemplateView):
    template_name = "restaurant/detail.html"

    def get_context_data(self, restaurant_id: int):
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)
        images = RestaurantImage.objects.filter(restaurant=restaurant)
        tables = list(RestaurantTable.objects.filter(restaurant=restaurant))

        slots = []
        span_deys = 10
        available_start_day = date.today() + timedelta(days=1)

        for i in range(span_deys):
            slot_day = available_start_day + timedelta(days=i)
            week_value = convert_weekday(slot_day.weekday())
            times = [table for table in tables if table.weekday == week_value]

            slots.append(
                {
                    "day": slot_day,
                    "times": times
                }
            )

        return {
            "restaurant": restaurant,
            "images": images,
            "slots": slots
        }
