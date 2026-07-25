"""
Rollarga asoslangan ruxsatlarni tekshirish uchun yordamchi dekorator/mixin.
"""
from functools import wraps
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


def role_required(*allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                raise PermissionDenied
            if request.user.is_super_admin or request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            raise PermissionDenied("Sizda ushbu bo'limga kirish huquqi yo'q.")
        return _wrapped
    return decorator


class RoleRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    allowed_roles = []

    def test_func(self):
        u = self.request.user
        return u.is_authenticated and (u.is_super_admin or u.role in self.allowed_roles)


def readonly_block(request):
    """Auditor rolidagi foydalanuvchi yozish amallarini bajara olmasligi uchun."""
    return getattr(request.user, 'is_readonly', False)
