from datetime import timedelta

from django.contrib import messages
from django.shortcuts import redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import FormView, UpdateView
from django.views import View

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.hashers import check_password

from allauth.socialaccount.models import SocialAccount

from ..forms import RegisterForm, LoginForm, ProfileForm, PasswordForm
from ..models import UserProfile, UserVerification
from ..utils import create_email_key


def send_verification_mail(reqeust, user, receiver):
    key = create_email_key(user.id)
    link = "http://" + reqeust.get_host() + reverse("verification") + "?key=" + key

    expired_at = timezone.now() + timedelta(days=3)
    UserVerification.objects.create(user=user, key=key, expired_at=expired_at)

    email_context = {
        "link": link
    }
    msg_plain = render_to_string("email/verification.txt", email_context)
    msg_html = render_to_string("email/verification.html", email_context)

    send_mail(
        "이메일 인증을 완료해주세요.", msg_plain,
        "jade@studypie.co",
        [receiver],
        html_message=msg_html,
        fail_silently=True
    )


class RegisterView(FormView):
    template_name = "users/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("index")

    # clena()이 끝나고 난 뒤 호출됨
    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        nickname = form.cleaned_data.get("nickname")
        profile_image = form.cleaned_data.get("profile_image")

        user = User.objects.create_user(username=email, email=email, password=password)
        UserProfile.objects.create(user=user, nickname=nickname, profile_image=profile_image)

        send_verification_mail(self.request, user, email)

        return super().form_valid(form)


class LoginView(FormView):
    template_name = "users/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")

        user = auth.authenticate(username=email, password=password)

        if user is not None:
            auth.login(self.request, user)
            return super().form_valid(form)
        else:
            messages.warning(self.request, "계정 혹은 비밀번호를 확인해주세요.")
            return redirect(reverse("login"))


class LogoutView(View):
    def get(self, request):
        auth.logout(request)
        return redirect(reverse("index"))


class VerificationView(View):
    def get(self, request):
        key = request.GET.get("key", "")
        verification = UserVerification.objects.get(key=key)
        current = timezone.now()

        if verification.expired_at > current:
            verification.verified = True
            verification.verified_at = current
            verification.save()

            user = verification.user
            user.userprofile.verified = True
            user.userprofile.save()

            messages.success(self.request, "인증이 완료되었습니다.")
        else:
            messages.warning(self.request, "인증을 다시 시도해주세요")

        return redirect(reverse("index"))


class ProfileView(UpdateView):
    form_class = ProfileForm
    template_name = "users/profile.html"
    success_url = reverse_lazy("profile")

    def get_object(self, queryset=None):
        return UserProfile.objects.get(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        social_account = SocialAccount.objects.filter(user=self.request.user).first()
        context["is_social_login"] = social_account is not None
        return context


class PasswordView(FormView):
    form_class = PasswordForm
    template_name = "users/password.html"
    success_url = reverse_lazy("profile")

    def form_valid(self, form):
        old_password = form.cleaned_data.get("old_password")
        new_password = form.cleaned_data.get("new_password")
        confirm_password = form.cleaned_data.get("confirm_password")

        if new_password != confirm_password:
            messages.warning(self.request, "2개의 비밀번호가 일치하지 않습니다")
            return redirect(reverse("password"))
        elif not check_password(self.request.user.password, old_password):
            messages.warning(self.request, "기존 비밀번호가 일치하지 않습니다.")
            return redirect(reverse("password"))
        else:
            messages.warning(self.request, "비밀번호가 수정되었습니다.")
            self.request.user.set_password(new_password)
            self.request.user.save()
            return super().form_valid(form)
