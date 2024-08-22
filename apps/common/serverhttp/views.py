from django.views.generic import TemplateView

from apps.common.core.models import IPBlockedModel




class HttpRequestAttakView(TemplateView):
    template_name = 'setup.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        request = self.request
        user_language = request.LANGUAGE_CODE
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0].strip()
        else:
            ip_address = request.META.get('REMOTE_ADDR')

        if user_language not in ["es", "en"]:
            user_language = "en"

        IPBlockedModel.objects.get_or_create(
            current_ip=ip_address,
            language=user_language,
            reason=IPBlockedModel.ReasonsChoices.SERVER_HTTP_REQUEST
        )

        context['n'] = [i for i in range(1000)]
        context['ip_address'] = ip_address
        return context
