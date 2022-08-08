from django.urls import path
from django.views.decorators.cache import cache_page

from .views.main import IndexView, SearchView, SearchJsonView
from .views.users import RegisterView, LoginView, LogoutView, VerificationView, ProfileView, PasswordView
from .views.restaurant import RestaurantView, RestaurantBookingView, RestaurantPayView
from .views.booking import BookingHistoryView, BookingCancelView
from .views.reviews import ReviewCreateView, ReviewUpdateView, ReviewDeleteView, ReviewHistoryView

urlpatterns = [
    # main
    # path("", cache_page(60*15)(IndexView.as_view()), name="index"),
    path("", IndexView.as_view(), name="index"),

    # user
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("verify/", VerificationView.as_view(), name="verification"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("password/", PasswordView.as_view(), name="password"),

    # search
    path("search/", SearchView.as_view(), name="search"),
    path("search/json/", SearchJsonView.as_view(), name="search-json"),

    # restaurant
    path("restaurant/<int:restaurant_id>/", RestaurantView.as_view(), name="restaurant-view"),
    path("restaurant/<int:restaurant_id>/seat/<int:seat_id>", RestaurantBookingView.as_view(),
         name="restaurant-booking"),
    path("restaurant/confirm/<str:status>", RestaurantPayView.as_view(), name="restaurant-payment"),

    # booking
    path("booking/", BookingHistoryView.as_view(), name="booking-history"),
    path("booking/<int:booking_id>/cancel/", BookingCancelView.as_view(), name="booking-cancel"),

    # review
    path("review/", ReviewHistoryView.as_view(), name="review-history"),
    path("review/booking/<int:booking_id>/", ReviewCreateView.as_view(), name="review-create"),
    path("review/<int:review_id>/update/", ReviewUpdateView.as_view(), name="review-update"),
    path("review/<int:review_id>/delete/", ReviewDeleteView.as_view(), name="review-delete"),
]
