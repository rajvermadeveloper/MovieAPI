from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.authentication import JWTAuthentication
from accounts.models import BlacklistedAccessToken
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse

class CheckBlacklistMiddleware(MiddlewareMixin):
    def process_request(self, request):
        auth = JWTAuthentication()
        try:
            user_auth_tuple = auth.authenticate(request)
            if user_auth_tuple is not None:
                user, token = user_auth_tuple
                if BlacklistedAccessToken.objects.filter(token=str(token)).exists():
                    return JsonResponse({'error': 'authentication failed'})
        except Exception as e:
            pass  # Handle exceptions as needed

        return None
