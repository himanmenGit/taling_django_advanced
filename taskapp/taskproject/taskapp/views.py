from django.shortcuts import render, redirect, resolve_url
from django.views import View
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView
from django.views.generic.detail import SingleObjectMixin
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


# class TaskDetailView(DetailView):
#     model = Task
#     template_name = "pages/task_detail.html"
#     pk_url_kwarg = "task_id"
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["checklists"] = CheckListItem.objects.filter(task=kwargs.get("object")).all()
#         return context

class TaskDetailView(SingleObjectMixin, ListView):
    model = Task
    template_name = "pages/task_detail.html"
    pk_url_kwarg = "task_id"
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(Task.objects.all())
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return CheckListItem.objects.filter(task=self.object).all()


class CheckListCreateView(CreateView):
    model = CheckListItem
    fields = ["content"]
    template_name = "pages/checklist_create.html"
    success_url = "/task/{0}/"

    def get_success_url(self):
        return self.success_url.format(str(self.kwargs.get("task_id")))

    def form_valid(self, form):
        data = form.save(commit=False)
        data.task = Task.objects.get(id=self.kwargs.get("task_id"))
        data.save()
        return redirect(self.get_success_url())


class CheckListUpdateView(View):
    model = CheckListItem
    success_url = "/task/{0}/"
    pk_url_kwarg = "check_id"

    def get_success_url(self):
        return resolve_url("view-task", task_id=str(self.kwargs.get("task_id")))

    def get_object(self):
        return self.model.objects.get(id=self.kwargs.get(self.pk_url_kwarg))

    def get(self, request, *args, **kwargs):
        data = self.get_object()
        data.checked = not data.checked
        data.save()
        return redirect(self.get_success_url())


# class CheckListUpdateView(UpdateView):
#     model = CheckListItem
#     # fields = ["checked"]
#     # template_name = "pages/checklist_update.html"
#     success_url = "/task/{0}/"
#     pk_url_kwarg = "check_id"
#
#     def get(self, request, *args, **kwargs):
#         data = super().get_object()
#         data.checked = not data.checked
#         data.save()
#         return redirect(self.get_success_url())
#
#     def get_success_url(self):
#         return resolve_url("view-task", task_id=str(self.kwargs.get("task_id")))
#


class CheckListDeleteView(DeleteView):
    model = CheckListItem
    template_name = "pages/checklist_delete.html"
    success_url = "/task/{0}/"
    pk_url_kwarg = "check_id"

    def get_success_url(self):
        return resolve_url("view-task", task_id=str(self.kwargs.get("task_id")))


class TaskDeleteView(DeleteView):
    model = Task
    template_name = "pages/task_delete.html"
    success_url = "/"
    pk_url_kwarg = "task_id"
