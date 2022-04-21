from django.shortcuts import render
from django.views.generic import TemplateView
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
