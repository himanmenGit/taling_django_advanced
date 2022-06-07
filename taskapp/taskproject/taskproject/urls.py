"""taskproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from taskapp import views
from taskapp.views import (
    TaskListView, TaskCreateView, TaskPreviousListView, TaskDetailView, CheckListCreateView, CheckListUpdateView,
    CheckListDeleteView, TaskDeleteView
)

urlpatterns = [
    # path("", views.index, name="index"),
    path("", TaskListView.as_view(), name="index"),
    path("task/", TaskCreateView.as_view(), name="create-task"),
    path("previous/", TaskPreviousListView.as_view(), name="previous"),
    path("task/<int:task_id>/", TaskDetailView.as_view(), name="view-task"),
    path("task/<int:task_id>/item/", CheckListCreateView.as_view(), name="create-item"),
    path("task/<int:task_id>/item/<int:check_id>/", CheckListUpdateView.as_view(), name="check-item"),
    path("task/<int:task_id>/delete/", TaskDeleteView.as_view(), name="delete-task"),
    path("task/<int:task_id>/item/<int:check_id>/delete/", CheckListDeleteView.as_view(), name="delete-item"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
