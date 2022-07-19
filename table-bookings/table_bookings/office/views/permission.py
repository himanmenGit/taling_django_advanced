from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

from ..models import RestaurantPermission
from web.models import Restaurant, Booking


class BookingPermissionRequiredMixin(PermissionRequiredMixin):
    check_permission_path_variable = None

    def has_manager(self):
        if self.request.user.is_superuser:
            return True

        groups = self.request.user.groups.all()

        if any(group.name == "manager" for group in groups):
            return True

        return False

    def get_booking_has_perms(self):
        if self.has_manager():
            return Booking.objects.all()

        restaurants = Restaurant.objects.filter(restaurantpermission__user=self.request.user).all()
        return Booking.objects.filter(restaurant__in=restaurants)

    def has_permission(self):
        has_perms = super().has_permission()

        if self.check_permission_path_variable and not self.has_manager():
            booking_id = self.kwargs.get(self.check_permission_path_variable)
            booking = get_object_or_404(Booking, id=booking_id)

            try:
                RestaurantPermission.objects.get(restaurant=booking.restaurant, user=self.request.user)
            except ObjectDoesNotExist:
                return False

        return has_perms
