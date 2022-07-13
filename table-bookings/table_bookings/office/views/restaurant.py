from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from web.models import Restaurant, RestaurantImage


class RestaurantListView(ListView):
    model = Restaurant
    paginate_by = 10
    template_name = "office/restaurant/list.html"
    ordering = ["-created_at"]


class RestaurantCreateView(CreateView):
    model = Restaurant
    fields = ["name", "category", "address", "phone", "menu_info", "description"]
    template_name = "office/restaurant/create.html"
    success_url = reverse_lazy("office-restaurant-list")

    def form_valid(self, form):
        data = form.save(commit=False)
        data.save()

        image_data = self.request.FILES.get("main_image")

        if image_data:
            image = RestaurantImage(
                restaurant=data,
                image=image_data
            )
            image.save()
            data.main_image = image
            data.save()

        return super().form_valid(form)


class RestaurantUpdateView(UpdateView):
    model = Restaurant
    pk_url_kwarg = "restaurant_id"
    fields = ["name", "category", "address", "phone", "menu_info", "description"]
    template_name = "office/restaurant/update.html"
    success_url = reverse_lazy("office-restaurant-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = self.object
        return context

    def form_valid(self, form):
        data = form.save(commit=False)
        data.save()

        image_data = self.request.FILES.get("main_image")

        if image_data:
            image = RestaurantImage(
                restaurant=data,
                image=image_data
            )
            image.save()
            data.main_image = image
            data.save()
        return super().form_valid(form)


class RestaurantDeleteView(DeleteView):
    model = Restaurant
    pk_url_kwarg = "restaurant_id"
    template_name = "office/restaurant/delete.html"
    success_url = reverse_lazy("office-restaurant-list")
