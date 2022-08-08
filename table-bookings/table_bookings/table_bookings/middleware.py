from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import render
from django.utils.deprecation import MiddlewareMixin
from django.utils.translation import gettext_lazy as _


exception_messages = {
    Http404.__name__ : _("없는 데이터입니다."),
    PermissionDenied.__name__ : _("권한이 없습니다")
}


class ExceptionMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        message = ""
        if exception.__class__.__name__ in exception_messages.keys():
            message = exception_messages[exception.__class__.__name__]

        return render(request, "error.html", {
            "message": message
        })
