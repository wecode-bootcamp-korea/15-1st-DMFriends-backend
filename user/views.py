import json, bcrypt, jwt, re
import my_settings

from django.views import View
from django.http import JsonResponse, HttpResponse
from user.models import Member, RecentView
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

#CHECK_EMAIL= re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
CHECK_PASSWORD = re.compile('^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,32}$')

class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            
            if not validate_email(email):
                raise ValidationError('INVALID_EMAIL')

            if not re.match(CHECK_PASSWORD, password):
                return JsonResponse({'message':'INVALID_PASSWORD'}, status=400)
                    
            if Member.objects.filter(email = email).exists():
                return JsonResponse({'message': 'EXISTS_USER'}, status=409)    
            
            if Member.objects.filter(nickname = data['nickname']).exists():
                return JsonResponse({'message':'EXISTS_NICKNAME'}, status=409)
            
            hashed_password = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt()).decode()
            
            Member.objects.create(
                email    = email,
                password = hashed_password,
                nickname = data.get('nickname'),
                )
            return JsonResponse({'message': 'SUCCESS'}, status=201)
            
        except ValidationError:
            return JsonResponse({'message': 'VALIDATION_ERROR'}, status=400)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
