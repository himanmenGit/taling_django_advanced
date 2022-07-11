from django import template
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
