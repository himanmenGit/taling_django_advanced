from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from .models import Task, CheckListItem


def index(request):
    context = {}
    return render(request, "pages/index.html", context)


class TaskListView(TemplateView):
    template_name = "pages/task_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        tasks = Task.objects.all()
        context.update({
            "tasks": tasks
        })
        return context


class TaskCreateView(CreateView):
    model = Task
    fields = ["title", "type", "due"]
    template_name = "pages/task_create.html"
    success_url = "/"
