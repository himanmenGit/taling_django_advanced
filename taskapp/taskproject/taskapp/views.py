from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, ListView, DetailView
from .models import Task, CheckListItem
from django.utils import timezone
from django.core.paginator import Paginator


def index(request):
    context = {}
    return render(request, "pages/index.html", context)


class TaskListView(TemplateView):
    template_name = "pages/task_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        tasks = Task.objects.filter(due__gte=timezone.now()).order_by("-due")
        paginator = Paginator(tasks, 1)
        page_number = self.request.GET.get("page", 1)
        paging = paginator.get_page(page_number)
        context.update({
            "paging": paging
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
    paginate_by = 4


class TaskDetailView(DetailView):
    model = Task
    template_name = "pages/task_detail.html"
    pk_url_kwarg = "task_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["checklists"] = CheckListItem.objects.filter(task=kwargs.get("object")).all()
        return context
