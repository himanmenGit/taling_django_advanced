from django.views.generic import ListView

from ..models import Booking


class BookingHistoryView(ListView):
    model = Booking
    template_name = "history/list.html"
    paginate_by = 5

    def get_queryset(self):
        return Booking.objects.filter(
            user=self.request.user
        ).exclude(status=Booking.PayStatus.FAILED).exclude(status=Booking.PayStatus.READY)
