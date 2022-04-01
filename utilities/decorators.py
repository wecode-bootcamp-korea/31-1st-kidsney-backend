import jwt

from django.http import JsonResponse
from django.conf import settings

from users.models import User

def check_token(func):
    def wrapper(self, request):
        try:
            access_token = request.headers.get('Authorization')
            payload      = jwt.decode(access_token, settings.SECRET_KEY, settings.ALGORITHM)
            request.user = User.objects.get(id = payload["id"])
             
        except jwt.exceptions.DecodeError:
            return JsonResponse({"message" : "INVALID_USER"}, status = 401)
        except User.DoesNotExist:
            return JsonResponse({"message" : "INVALID_USER"}, status = 401)
        except jwt.ExpiredSignatureError:
            return JsonResponse({"message": "EXPIRED_TOKEN"}, status = 401)
        return func(self, request)
    return wrapper