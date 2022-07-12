from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.core.exceptions import PermissionDenied

from ..models import Review, Restaurant, Booking


class ReviewCreateView(CreateView):
    model = Review
    fields = ["comment", "ratings"]
    template_name = "review/create.html"
    success_url = reverse_lazy("booking-history")

    def form_valid(self, form):
        booking_id = self.kwargs["booking_id"]
        booking = get_object_or_404(Booking, id=booking_id)
        if booking.review:
            raise PermissionDenied()
        if booking.user != self.request.user:
            raise PermissionDenied()
        if booking.seat.datetime > timezone.now():
            raise PermissionDenied()

        data = form.save(commit=False)
        data.user = self.request.user
        data.restaurant = booking.restaurant
        data.save()
        booking.review = data
        booking.save()

        return super().form_valid(form)
