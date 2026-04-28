from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps


class AgencyRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not request.user.is_agency_manager:
            messages.error(request, 'Access denied. Agency manager account required.')
            return redirect('home')
        try:
            agency = request.user.agency
            if not agency.is_approved:
                return redirect('agency:pending')
        except Exception:
            return redirect('agency:register')
        return super().dispatch(request, *args, **kwargs)


def agency_required(view_func):
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_agency_manager:
            messages.error(request, 'Access denied.')
            return redirect('home')
        try:
            agency = request.user.agency
            if not agency.is_approved:
                return redirect('agency:pending')
        except Exception:
            return redirect('agency:register')
        return view_func(request, *args, **kwargs)
    return wrapper
