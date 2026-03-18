from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps
from django.contrib.auth.models import User
from .models import UserProfile

def role_required(allowed_roles):
    """
    Decorator for views that checks that the user is logged in and has the given role.
    Raises PermissionDenied if the user does not have the required role.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
                
            # Allow superusers to access admin views
            if request.user.is_superuser and 'admin' in allowed_roles:
                return view_func(request, *args, **kwargs)
                
            try:
                profile = request.user.userprofile
                if profile.role in allowed_roles:
                    return view_func(request, *args, **kwargs)
                else:
                    messages.error(request, f"Access denied. You must be an {', '.join(allowed_roles)} to view this page.")
                    # Redirect based on their actual role if possible, or landing
                    if profile.role == 'student':
                        return redirect('student_dashboard')
                    elif profile.role == 'adviser':
                        return redirect('adviser_dashboard')
                    elif profile.role == 'admin':
                        return redirect('admin_dashboard')
                    else:
                        return redirect('landing')
            except UserProfile.DoesNotExist:
                # Fallback for old users without profile
                if request.user.is_superuser and 'admin' in allowed_roles:
                    return view_func(request, *args, **kwargs)
                messages.error(request, "User profile is incomplete. Please register again.")
                return redirect('login')
                
        return _wrapped_view
    return decorator
