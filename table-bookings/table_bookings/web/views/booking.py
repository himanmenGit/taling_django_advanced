import requests

from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView
from django.core.exceptions import PermissionDenied

from ..models import Booking, PayHistory


class BookingHistoryView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = "booking/list.html"
    paginate_by = 5

    def get_queryset(self):
        return Booking.objects.filter(
            user=self.request.user
        ).exclude(status=Booking.PayStatus.FAILED).exclude(status=Booking.PayStatus.READY)


class BookingCancelView(LoginRequiredMixin, View):
    def get(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id)

        if booking.user != self.request.user:
            raise PermissionDenied()

        if booking.status != Booking.PayStatus.PAID:
            messages.warning(request, "취소할 수 없는 예약입니다.")
            return redirect("booking-history")

        response = requests.post(
            "https://api.tosspayments.com/v1/payments/" + booking.pg_transaction_number + "/cancel",
            json={"cancelReason": "고객 예약취소"},
            headers={
                "Authorization": "Basic dGVzdF9za196WExrS0V5cE5BcldtbzUwblgzbG1lYXhZRzVSOg==",
                "Content-Type": "application/json"
            }
        )

        if response.ok:
            with transaction.atomic():
                booking.status = Booking.PayStatus.CANCELED
                booking.canceled_at = timezone.now()
                booking.seat.remain += 1
                booking.save()
                booking.seat.save()
                PayHistory.objects.create(booking=booking, amount=-booking.price)
        return redirect("booking-history")
