from django import template
from django.utils import timezone

from ..models import Booking

register = template.Library()


@register.filter(name="convert_status_korean")
def convert_status_korean(status: Booking.PayStatus):
    if status == Booking.PayStatus.READY:
        return "결제 대기"
    elif status == Booking.PayStatus.CANCELED:
        return "예약 취소"
    elif status == Booking.PayStatus.FAILED:
        return "예약 실패"
    elif status == Booking.PayStatus.PAID:
        return "예약 완료"
    return ""


@register.filter(name="is_available_review")
def is_available_review(booking: Booking):
    now = timezone.now()
    return booking.status == Booking.PayStatus.PAID and booking.seat.datetime < now and booking.review is None
