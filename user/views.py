'''
import json, bcrypt, jwt, re
import my_settings
from random

from django.views import View
from django.http import JsonResponse
from user.models import User


class SignUpView(View):
    def post(self, request):
        data            = json.loads(request.body)
        check_email     = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        check_password  = re.compile('^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,32}$')

        if not 'email' in data:
            return JsonResponse({'message':'EMAIL_ERROR'}, status=400)
                
        if not re.match(check_email, data['email']):
            return JsonResponse({'message':'BAD_EMAIL_REQUEST'}, status=400)
                
        if User.objects.filter(email = data['email']).exists():
            return JsonResponse({'message':'EXISTS_USER'}, status=409)
        
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


class LoginView(View):
    def  post(self, request):
        data = json.loads(request.body)

        if not 'email' in data or not 'password' in data:
            return JsonResponse({'message':'CHECK_DATA'}, status=400)

        users = User.objects.filter(email=data['email'])
        if not users.exists():
            return JsonResponse({'message':'INVALITD_USER'}, status=400)

        user_data = users.get()

        if bcrypt.checkpw(data['password'].encode('utf-8'), user_data.password.encode('utf-8')):
            token = jwt.encode({'user_id':user_data.id}, my_settings.SECRET_KEY, algorithm = ALGORITHM['hash']).decode('utf-8')
            return JsonResponse({'message':'SUCCESS_LOGIN', 'token':token}, status=200)

        return JsonResponse({'message':'INVALID_PASSWORD'}, status=400)

'''
