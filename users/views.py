import json, bcrypt, jwt

from django.http import JsonResponse
from django.views import View
from django.db import IntegrityError
from django.forms import ValidationError
from django.conf import settings

from utilities.validators import email_validate, password_validate, phone_number_validate
from .models import User

class SignUpView(View):
    def post(self, request):
        try:
            data          = json.loads(request.body)
            email         = data['email']
            password      = data['password']
            phone_number  = data['phone_number']

            email_validate(email)
            password_validate(password)
            phone_number_validate(phone_number)

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            User.objects.create(
                first_name    = data['first_name'],
                last_name     = data['last_name'],
                email         = email,
                password      = hashed_password,
                phone_number  = phone_number,
                date_of_birth = data["date_of_birth"]
            )

            return JsonResponse({'message' : 'CREATED'}, status = 201)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
        except IntegrityError:
            return JsonResponse({'message' : 'THIS_EMAIL_ALREADY_EXIST.'}, status = 400)
        except ValidationError as e:
            return JsonResponse({'message': e.message}, status = 400)

class SignInView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            email    = data['email']
            password = data['password']

            email_validate(email)
            password_validate(password)
            
            user = User.objects.get(email = email)

            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({'message' : 'INVALID_USER'}, status = 400)
            
            access_token = jwt.encode({'id' : user.id}, settings.SECRET_KEY, settings.ALGORITHM)
            return JsonResponse({'message' : 'SUCCESS', 'token': access_token}, status = 200)
            
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
        except ValidationError as e:
            return JsonResponse({'message': e.message}, status = 400)
        except User.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_USER'}, status = 400)