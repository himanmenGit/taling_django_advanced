"""table_bookings URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from web.views.main import IndexView, SearchView, SearchJsonView
from web.views.users import RegisterView, LoginView, LogoutView, VerificationView, ProfileView, PasswordView
from web.views.restaurant import RestaurantView, RestaurantBookingView, RestaurantPayView
from web.views.booking import BookingHistoryView, BookingCancelView
from web.views.reviews import ReviewCreateView, ReviewUpdateView, ReviewDeleteView, ReviewHistoryView

urlpatterns = [
    path('admin/', admin.site.urls),

    # main
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
    path("restaurant/<int:restaurant_id>/seat/<int:seat_id>", RestaurantBookingView.as_view(), name="restaurant-booking"),
    path("restaurant/confirm/<str:status>", RestaurantPayView.as_view(), name="restaurant-payment"),

    # booking
    path("booking/", BookingHistoryView.as_view(), name="booking-history"),
    path("booking/<int:booking_id>/cancel/", BookingCancelView.as_view(), name="booking-cancel"),

    # review
    path("review/", ReviewHistoryView.as_view(), name="review-history"),
    path("review/booking/<int:booking_id>/", ReviewCreateView.as_view(), name="review-create"),
    path("review/<int:review_id>/update/", ReviewUpdateView.as_view(), name="review-update"),
    path("review/<int:review_id>/delete/", ReviewDeleteView.as_view(), name="review-delete"),

    path("oauth/", include("allauth.urls")),
    # path('__debug__/', include('debug_toolbar.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
