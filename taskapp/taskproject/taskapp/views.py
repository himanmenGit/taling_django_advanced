from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, ListView
from .models import Task
from django.utils import timezone


def index(request):
    context = {}
    return render(request, "pages/index.html", context)


class TaskListView(TemplateView):
    template_name = "pages/task_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        tasks = Task.objects.filter(due__gte=timezone.now()).order_by("-due")
        context.update({
            "tasks": tasks
        })
        return context


class TaskCreateView(CreateView):
    model = Task
    fields = ["title", "type", "due"]
    template_name = "pages/task_create.html"
    success_url = "/"


class TaskPreviousListView(ListView):
    model = Task
    template_name = "pages/task_previous_list.html"
    queryset = Task.objects.filter(due__lt=timezone.now()).order_by("-due")
