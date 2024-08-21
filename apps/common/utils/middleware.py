import logging

from django.utils.translation import gettext as _

logger = logging.getLogger(__name__)


class APILogMiddleware:
    """Middleware to log API requests."""

    def __init__(self, get_response):
        """Initialize the APILogMiddleware.

        :param get_response: The function to get the response.
        :type get_response: function
        """
        self.get_response = get_response

    def __call__(self, request):
        """Handle the middleware logic.

        :param request: The HTTP request.
        :type request: HttpRequest

        :return: The HTTP response.
        :rtype: HttpResponse
        """
        host = request.get_host()

        # Check if the host starts with 'www.'
        if host.startswith('www.'):
            non_www_host = host[4:]  # Remove 'www.' from the host
            url = request.build_absolute_uri(request.get_full_path())
            non_www_url = url.replace(
                f'http://www.{host}', f'http://{non_www_host}'
            )

            # Redirect to the non-www version
            from django.http import HttpResponsePermanentRedirect
            return HttpResponsePermanentRedirect(non_www_url)

        response = self.get_response(request)
        return response
