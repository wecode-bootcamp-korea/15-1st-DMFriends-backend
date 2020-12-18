import json, bcrypt, jwt, re
import my_settings

from django.views import View
from django.http import JsonResponse
from user.models import User


class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            check_email = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
            #적어도 하나의 대문자,(?=.*?[A-Z]), 영문 소문자 1 자 이상 (?=.*?[a-z]), 적어도 하나의 숫자(?=.*?[0-9]), 하나 이상의 특수 문자(?=.*?[#?!@$%^&*-]),최소 길이 8 에서 32까지.{8,32}
            check_password  = re.compile('^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,32}$')

            if not 'email' in data:
                return JsonResponse({'message':'EMAIL_ERROR'}, status=400)
                    
            if not re.match(check_email, data['email']):
                return JsonResponse({'message':'BAD_EMAIL_REQUEST'}, status=400)
                    
            if User.objects.filter(email = data['email']).exists():
                return JsonResponse({'message': 'EXISTS_USER'}, status=409)
            
            if password.notequals(confirmPassword):
                return JsonResponse({'message':'NOT_MATCHED'}, status=400)
            
            if not re.match(check_password, data['password']):
                return JsonResponse({'message':'INVALID_PASSWORD'}, status=400)
            
            if User.objects.filter(nick_name = data['nick_name']).exists():
                return JsonResponse({'message':'EXISTS_NICKNAME'}, status=409)
            
            hashed_password = bcrypt.hashpw(data['password'].encode('UTF-8'), bcrypt.gensalt()).decode()
            
            User(
                email           = data.get('email'),
                hashed_password = data.get('hashed_password'),
                nick_name       = data.get('nick_name'),
                ).save()
            return JsonResponse({'message': 'SUCCESS'}, status=201)
            
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status = 400)
        