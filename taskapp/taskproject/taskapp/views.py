from django.shortcuts import render
from django.views.generic import TemplateView, FormView
from .models import Task, CheckListItem
from .forms import TaskForm


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


class TaskCreateView(FormView):
    template_name = "pages/task_create.html"
    form_class = TaskForm
    success_url = "/"

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
