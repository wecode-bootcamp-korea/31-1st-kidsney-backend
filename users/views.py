import json, bcrypt, jwt, datetime

from django.http import JsonResponse
from django.views import View
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.conf import settings

from utilities.validators import validate_email, validate_password, validate_phone_number
from .models import User

class SignUpView(View):
    def post(self, request):
        try:
            data          = json.loads(request.body)
            email         = data['email']
            password      = data['password']
            phone_number  = data['phone_number']

            validate_email(email)
            validate_password(password)
            validate_phone_number(phone_number)

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

            validate_email(email)
            validate_password(password)
            
            user = User.objects.get(email = email)

            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({'message' : 'INVALID_USER'}, status = 401)
            
            access_token = jwt.encode({'id' : user.id, 'iat' : datetime.datetime.utcnow(), 'exp':datetime.datetime.utcnow() + datetime.timedelta(days=2)}, settings.SECRET_KEY, settings.ALGORITHM)
            return JsonResponse({'message' : 'SUCCESS', 'token': access_token}, status = 200)
      
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
        except ValidationError as e:
            return JsonResponse({'message': e.message}, status = 400)
        except User.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_USER'}, status = 401)
        