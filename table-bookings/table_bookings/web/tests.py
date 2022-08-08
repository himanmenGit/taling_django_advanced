from django.test import TestCase
from django.test import Client
from django.urls import reverse

from .models import Booking, Restaurant, Category
from .templatetags.booking_tags import convert_status_korean


class BookingTagsTest(TestCase):
    def setUp(self) -> None:
        self.cases = [
            (Booking.PayStatus.READY, "결제 대기"),
            (Booking.PayStatus.PAID, "예약 완료"),
            (Booking.PayStatus.FAILED, "예약 실패"),
            (Booking.PayStatus.CANCELED, "예약 취소"),
        ]

    def test__convert_status_korean(self):
        for case in self.cases:
            result = convert_status_korean(case[0])
            self.assertEqual(case[1], result)


class SearchViewTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.test_restaurant = []
        category = Category.objects.create(name="한식")
        self.test_restaurant.append(
            Restaurant.objects.create(name="테스트", category=category, address="서울시 중구", phone="020000"),
        )
        self.test_restaurant.append(
            Restaurant.objects.create(name="아무거나", category=category, address="서울시 강남구", phone="020000")
        )

    def test_get(self):
        keyword = "테스트"
        response = self.client.get(reverse("search"), {"keyword": keyword})
        self.assertTemplateUsed(response, "main/search.html")

        for item in self.test_restaurant:
            if keyword in item.name:
                self.assertContains(response, f'<div class="card" id="restaurant-{item.id}">', status_code=200)
            else:
                self.assertNotContains(response, f'<div class="card" id="restaurant-{item.id}">', status_code=200)