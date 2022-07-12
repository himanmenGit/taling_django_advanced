from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.core.exceptions import PermissionDenied

from ..models import Review, Booking


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    fields = ["comment", "ratings"]
    template_name = "review/create.html"
    success_url = reverse_lazy("review-history")

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


class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    model = Review
    pk_url_kwarg = "review_id"
    fields = ["comment", "ratings"]
    template_name = "review/update.html"
    success_url = reverse_lazy("review-history")

    def form_valid(self, form):
        review = self.get_object()
        if self.request.user != review.user:
            raise PermissionDenied()

        return super().form_valid(form)


class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    model = Review
    pk_url_kwarg = "review_id"
    success_url = reverse_lazy("review-history")

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user != self.object.user:
            raise PermissionDenied()
        return super().form_valid(None)


class ReviewHistoryView(LoginRequiredMixin, ListView):
    model = Review
    template_name = "review/reviews.html"
    paginate_by = 5

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)
