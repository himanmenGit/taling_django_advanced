import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from django.db.models.signals import post_save
from django.dispatch import receiver

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialAccount


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    nickname = models.CharField(null=False, max_length=30)
    profile_image = models.ImageField(upload_to="uploads/%Y/%m/%d/", null=True)
    verified = models.BooleanField(default=False)


class UserVerification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.CharField(null=False, max_length=200, unique=True)
    verified = models.BooleanField(default=False)
    expired_at = models.DateTimeField(null=False)
    verified_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=False)


class Category(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, null=False)


class Restaurant(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    main_image = models.ForeignKey("RestaurantImage", related_name="main_image", null=True, on_delete=models.CASCADE)
    address = models.CharField(max_length=300, db_index=True)
    phone = models.CharField(max_length=20)
    visible = models.BooleanField(default=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    menu_info = models.TextField(null=True)
    description = models.TextField(null=True)


class RestaurantImage(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    image = models.ImageField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)


class RestaurantTable(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    class Weekday(models.TextChoices):
        MONDAY = "MON", _("월요일"),
        TUESDAY = "TUE", _("화요일"),
        WEDNESDAY = "WED", _("수요일")
        THURDAY = "THU", _("목요일"),
        FRIDAY = "FRI", _("금요일"),
        SATURDAY = "SAT", _("토요일"),
        SUNDAY = "SUN", _("일요일")

    weekday = models.CharField(max_length=3, choices=Weekday.choices, default=Weekday.MONDAY)
    time = models.TimeField()
    available = models.IntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        unique_together = ["restaurant", "weekday", "time"]


class Recommendation(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    sort = models.IntegerField(default=9999)
    visible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)


class AvailableSeat(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    table = models.ForeignKey(RestaurantTable, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    remain = models.IntegerField(default=-1)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        unique_together = ["restaurant", "table", "datetime"]


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    table = models.ForeignKey(RestaurantTable, on_delete=models.CASCADE)
    seat = models.ForeignKey(AvailableSeat, on_delete=models.CASCADE)

    class PayMethod(models.TextChoices):
        CARD = "CARD", _("카드"),

    class PayStatus(models.TextChoices):
        READY = "READY", _("결제대기"),
        PAID = "PAID", _("결제완료"),
        FAILED = "FAILED", _("예약실패"),
        CANCELED = "CANCELED", _("예약취소"),

    order_number = models.CharField(max_length=20)
    pg_transaction_number = models.CharField(max_length=50, null=True, default=None)
    method = models.CharField(max_length=4, choices=PayMethod.choices, default=PayMethod.CARD)
    status = models.CharField(max_length=10, choices=PayStatus.choices, default=PayStatus.READY)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    paid_at = models.DateTimeField(null=True, default=None)
    canceled_at = models.DateTimeField(null=True, default=None)

    booker_name = models.CharField(max_length=20, default=None, null=True)
    booker_phone = models.CharField(max_length=20, default=None, null=True)
    booker_comment = models.CharField(max_length=200, default=None, null=True)


class PayHistory(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True, null=True)


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        user.username = user.email[:30]

        if User.objects.filter(username=user.username).exists():
            user.username = str(uuid.uuid4())
        return user


@receiver(post_save, sender=User)
def on_save_user(sender, instance, **kwargs):
    profile = UserProfile.objects.filter(user=instance).first()
    social_account = SocialAccount.objects.filter(user=instance).first()

    # 소셜 계정일 경우 프로필을 생성 해 준다.
    if profile is None and social_account is not None:
        nickname = instance.email.split("@")[0]
        UserProfile.objects.create(
            user=instance,
            nickname=nickname,
            profile_image=None,
            verified=True
        )
