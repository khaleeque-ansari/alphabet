import re
import warnings

from django import http
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.core.mail import mail_managers
from django.urls import is_valid_path
from django.utils.cache import (
    cc_delim_re, get_conditional_response, set_response_etag,
)
from django.utils.deprecation import MiddlewareMixin, RemovedInDjango21Warning
from django.utils.encoding import force_text
from django.utils.six.moves.urllib.parse import urlparse


class CommonMiddleware(MiddlewareMixin):
    response_redirect_class = http.HttpResponsePermanentRedirect

    def process_request(self, request):
        """
        Check for denied User-Agents and rewrite the URL based on
        settings.APPEND_SLASH and settings.PREPEND_WWW
        """

        # Check for denied User-Agents
        if 'HTTP_USER_AGENT' in request.META:
            for user_agent_regex in settings.DISALLOWED_USER_AGENTS:
                if user_agent_regex.search(request.META['HTTP_USER_AGENT']):
                    raise PermissionDenied('Forbidden user agent')

        # Check for a redirect based on settings.PREPEND_WWW
        host = request.get_host()
        must_prepend = settings.PREPEND_WWW and host and not host.startswith('www.')
        redirect_url = ('%s://www.%s' % (request.scheme, host)) if must_prepend else ''

        # Check if a slash should be appended
        if self.should_redirect_with_slash(request):
            path = self.get_full_path_with_slash(request)
        else:
            path = request.get_full_path()

        # Return a redirect if necessary
        if redirect_url or path != request.get_full_path():
            redirect_url += path
            return self.response_redirect_class(redirect_url)
