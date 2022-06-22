import datetime
from datetime import timedelta, date
import random

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.http import JsonResponse
from django.urls import reverse_lazy

from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView
from django.utils import timezone

from ..models import (
    Restaurant, RestaurantTable, RestaurantImage, AvailableSeat, Booking, PayHistory
)
from ..utils import convert_weekday


@transaction.atomic
def fetch_remain_and_return_expired_booking(slot_day: date, time: RestaurantTable):
    seat_datetime = timezone.datetime.combine(slot_day, time.time)
    seat, created = AvailableSeat.objects.get_or_create(
        restaurant=time.restaurant,
        table=time,
        datetime=seat_datetime,
        defaults={
            "remain": time.available
        }
    )

    if not created:
        created_time = timezone.datetime.now() - datetime.timedelta(minutes=10)
        expired_count = Booking.objects.filter(seat=seat) \
            .filter(status=Booking.PayStatus.READY) \
            .filter(created_at__lt=created_time) \
            .update(status=Booking.PayStatus.FAILED)
        seat.remain = seat.remain - expired_count
        seat.save()

    return {
        "restaurant_id": time.restaurant.id,
        "seat_id": seat.id,
        "time": time.time,
        "price": time.price,
        "total": time.available,
        "remain": seat.remain
    }


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

            seats = []
            for time in times:
                seat = fetch_remain_and_return_expired_booking(slot_day, time)
                seats.append(seat)

            slots.append(
                {
                    "day": slot_day,
                    "times": seats
                }
            )

        return {
            "restaurant": restaurant,
            "images": images,
            "slots": slots
        }


class BookingView(LoginRequiredMixin, TemplateView):
    template_name = "restaurant/book.html"
    login_url = reverse_lazy("login")

    def create_order_number(self, seat_id):
        now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        return now + str(seat_id) + str(random.randrange(1000, 10000))

    def get_context_data(self, restaurant_id: int, seat_id: int):
        # get: 좌석을 사전에 확보 + 폼 그리기
        # post: 주문 정보 업데이트 + 결제시작

        with transaction.atomic():
            new_order_number = self.create_order_number(seat_id)
            seat = get_object_or_404(AvailableSeat, id=seat_id)
            if seat.remain < 0:
                messages.warning(self.request, "잔여 좌석이 없습니다.")
                return redirect("restaurant-view", restaurant_id)

            booking, created = Booking.objects.get_or_create(
                user=self.request.user,
                restaurant=seat.restaurant,
                table=seat.table,
                seat=seat,
                defaults={
                    "price": seat.table.price,
                    "order_number": new_order_number
                }
            )

            if created:
                seat.remain = seat.remain - 1
                seat.save()

            return {
                "seat": seat,
                "booking": booking
            }

    def post(self, request, *args, **kwargs):
        order_number = request.POST.get("order_number", "")
        booker_name = request.POST.get("booker_name", None)
        booker_phone = request.POST.get("booker_phone", None)
        booker_comment = request.POST.get("booker_comment", None)

        booking = get_object_or_404(Booking, order_number=order_number)

        if booking.user != self.request.user:
            raise PermissionDenied()

        booking.booker_name = booker_name
        booking.booker_phone = booker_phone
        booking.booker_comment = booker_comment

        booking.save()

        return JsonResponse({}, safe=False)
