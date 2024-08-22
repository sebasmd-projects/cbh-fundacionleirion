from datetime import timedelta

from django.conf import settings
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import TemplateView

from apps.common.core.models import IPBlockedModel
from apps.project.common.users.models import UserLoginAttemptModel

from .forms import KeyPrefixForm


# class KeyPrefixRequiredMixin:
#     MAX_ATTEMPTS = settings.MAX_KEY_ATTEMPS
#     ATTEMPT_RESET_TIME = timedelta(minutes=3600)

#     @method_decorator(csrf_protect)
#     def dispatch(self, request, *args, **kwargs):
#         key_prefix = request.session.get('key_prefix', None)
#         user_ip = request.META['REMOTE_ADDR']

#         if IPBlockedModel.objects.filter(current_ip=user_ip, is_active=True).exists():
#             return HttpResponseForbidden("Your IP has been blocked due to too many incorrect attempts.")

#         if not key_prefix:
#             return self.render_to_response({'form': KeyPrefixForm()})

#         key = settings.SECRET_KEY[:32]
#         if not key.startswith(key_prefix):
#             user_login_attempt, created = UserLoginAttemptModel.objects.get_or_create(
#                 user=request.user
#             )

#             if timezone.now() - user_login_attempt.last_attempt > self.ATTEMPT_RESET_TIME:
#                 user_login_attempt.attempts = 0

#             user_login_attempt.attempts += 1
#             user_login_attempt.save()

#             if user_login_attempt.attempts >= self.MAX_ATTEMPTS:
#                 IPBlockedModel.objects.create(
#                     current_ip=user_ip,
#                     reason=IPBlockedModel.ReasonsChoices.SECURITY_KEY_ATTEMPTS
#                 )
#                 user_login_attempt.attempts = 0
#                 user_login_attempt.save()
#                 return HttpResponseForbidden("Your IP has been blocked due to too many incorrect attempts.")

#             return HttpResponseForbidden("Invalid key")

#         return super().dispatch(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         form = KeyPrefixForm(request.POST)
#         if form.is_valid():
#             key_prefix = form.cleaned_data['key_prefix']
#             key = settings.SECRET_KEY[:32]

#             if key.startswith(key_prefix):
#                 request.session['key_prefix'] = key_prefix

#                 next_url = self.request.GET.get('next', 'core:index')
#                 return redirect(next_url)
#             else:
#                 form.add_error('key_prefix', 'Invalid key')

#         return self.render_to_response({'form': form})


class IndexTemplateView(TemplateView):
    template_name = "page/index.html"
