# core/middleware.py

import threading

_user = threading.local()

class CurrentEmployeeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if hasattr(request.user, 'employee'):
            _user.value = request.user.employee
        else:
            _user.value = None
        response = self.get_response(request)
        return response

def get_current_employee():
    return getattr(_user, 'value', None)
