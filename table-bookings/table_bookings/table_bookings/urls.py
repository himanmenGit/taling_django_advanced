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

from web.views.main import IndexView, SearchView, SearchJsonView
from web.views.users import RegisterView, LoginView, LogoutView, VerificationView
from web.views.restaurant import RestaurantView, BookingView, PayView

urlpatterns = [
    path('admin/', admin.site.urls),

    path("", IndexView.as_view(), name="index"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("verify/", VerificationView.as_view(), name="verification"),

    path("search/", SearchView.as_view(), name="search"),
    path("search/json/", SearchJsonView.as_view(), name="search-json"),

    path("restaurant/<int:restaurant_id>/", RestaurantView.as_view(), name="restaurant-view"),
    path("restaurant/<int:restaurant_id>/booking/<int:seat_id>", BookingView.as_view(), name="booking"),

    path("restaurant/confirm/<str:status>", PayView.as_view(), name="payment"),

    path("oauth/", include("allauth.urls")),
    # path('__debug__/', include('debug_toolbar.urls')),
]
