from django.contrib import messages
from django.shortcuts import HttpResponseRedirect, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView
from django.views import View

from ..forms import RegisterForm, LoginForm
from ..models import UserProfile


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
    def get(self, requesr):
        auth.logout(requesr)
        return redirect(reverse("index"))
