from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _

class LoginGroupRequiredMixin(UserPassesTestMixin, LoginRequiredMixin):
    group_required = None
    redirect_url = None

    def test_func(self):
        if self.group_required is None:
            raise ValueError(_("group_required attribute not set"))
        user = self.request.user
        return user.is_superuser or user.groups.filter(name=self.group_required).exists()

    def handle_no_permission(self):
        if self.redirect_url:
            return redirect(self.redirect_url)
        raise PermissionDenied(_("You do not have permission to view this page"))
