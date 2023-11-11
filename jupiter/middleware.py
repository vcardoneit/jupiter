import logging
from django.utils import timezone


class UserAccessLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger('django')

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated:
            log_message = f"User '{request.user}' accessed '{request.path}' at {timezone.now()}."
            self.logger.info(log_message)

        return response
