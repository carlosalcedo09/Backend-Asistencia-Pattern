# middleware.py

from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.core.exceptions import PermissionDenied

class CustomPermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if isinstance(exception, PermissionDenied):
            return render(request, 'admin/403.html', status=401)  
        return None