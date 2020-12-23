import json, bcrypt, jwt, re, random

from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.views import View
from django.http import JsonResponse, HttpResponse

import my_settings
from user.utils import login_decorator
from user.models import Member, RecentView, BoardLike, CommentLike, EmailCheck
from board.models import Board, Comment

class EmailCheckView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            email = data.get('email', None)           
            random_token = random.randint(10000, 100000)

            if email:
                validate_email(email)
                                   
            if EmailCheck.objects.filter(email = email).exists():
                return JsonResponse({'message': 'EXISTS_USER'}, status=409)

            EmailCheck.objects.create(
                email = email,       
                random_token = random_token
            )
            mail_subject = "[DM] 회원가입 인증 메일입니다."
            content = f"이메일 인증에 성공하셨습니다.\n\n인증번호는 {random_token}"
            emailsend = EmailMessage(mail_subject, content, to=[data['email']])
            emailsend.send()

            return JsonResponse({'email': 'SENT'}, status=201)  
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

class VerificationCodeView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            if EmailCheck.objects.filter(email=data['email']).exists():
                email = EmailCheck.objects.get(email = data['email'])
                if email.random_token == data['random_token']:
                    email.delete()
                    return JsonResponse({'code': 'ACCEPT'}, status=200)
                return JsonResponse({'message': 'DENY'}, status=400)
            return JsonResponse({'message': 'DENY'}, status=400)   
                 
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            email = data['email']

            if Member.objects.filter(nickname = data.get('nickname')).exists():
                return JsonResponse({'message': 'EXISTS_NICKNAME'}, status=409)

            hashed_password = bcrypt.hashpw(data.get('password').encode('UTF-8'), bcrypt.gensalt()).decode()
            
            Member.objects.create(
                email    = email,
                password = hashed_password,
                nickname = data['nickname']
            )
            return JsonResponse({'message': 'SUCCESS'}, status=201)
            
        except ValidationError:
            return JsonResponse({'message': 'INVALID_EMAIL'}, status=400)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

class LoginView(View):
    def post(self, request):
        data = json.loads(request.body)

        if not 'email' in data or not 'password' in data:
            return JsonResponse({'message':'CHECK_DATA'}, status=400)

        members = Member.objects.filter(email=data['email'])
        if not members.exists():
            return JsonResponse({'message':'INVALITD_USER'}, status=400)

        member_data = members.get()

        if bcrypt.checkpw(data['password'].encode('utf-8'), member_data.password.encode('utf-8')):
            token = jwt.encode({'member_id':member_data.id}, my_settings.SECRET_KEY, my_settings.ALGORITHM).decode('utf-8')
            return JsonResponse({'message':'SUCCESS_LOGIN', 'token':token}, status=200)

        return JsonResponse({'message': 'INVALID_PASSWORD'}, status=400)

class BoardLikeView(View):
    @login_decorator
    def post(self, request):
        data = json.loads(request.body)

        if not BoardLike.objects.filter(board_id=data['board_id'], member_id=request.user).exists():
            BoardLike.objects.create(
                member_id = request.user.id,
                board     = Board.objects.get(id=data['board_id']),
                is_like   = 1
            )
            return JsonResponse({'message': 'ADD'}, status=200)
    @login_decorator
    def delete(self, request):
        data             = json.loads(request.body)  
        delete_boardlike = BoardLike.objects.get(board_id=data['board_id'], member_id=request.user, is_like=data['is_like'])
        delete_boardlike.delete()
        return JsonResponse({'message':'DELETE'})

class CommentLikeView(View):
    @login_decorator
    def post(self, request):
        data = json.loads(request.body)
        print('1')
        print(request.user)

        if not CommentLike.objects.filter(comment_id=data['comment_id'], member_id =request.user).exists():
            CommentLike.objects.create(
                member    = request.user.id,
                comment   = Comment.objects.get(id=data['comment_id']),
                is_like   = 1
            )
            return JsonResponse({'message': 'ADD'}, status=200)
    @login_decorator
    def delete(self, request):
        data               = json.loads(request.body) 
        delete_commentlike = CommentLike.objects.get(comment_id=data['comment_id'], member_id=request.user,)
        delete_comementlike.delete()
        return JsonResponse({'message':'DELETE'})

class RecentView(View):
    @login_decorator
    def POST(self, request):        
        data = json.loads(request.body)
        if not RecentView.objects.filter(product_id=product_id, member_id=request.user).exists():
            RecentView.objects.create(
                member_id   = request.user,
                product_id  = Product.objects.get(id=data['product_id']), 
            )
            return JsonResponse({'message': 'RECENTVIEWED_ADD'}, status=200)
    @login_decorator
    def GET(self, request):
        recentviews         = Recentview.objects.filter(member_id=request.user).order_by('viewed_at')[:10]
        recentview_products = recentviews.product
        
        result = [{
            'name': item.name,
            'id': item.id,
            'price': item.price,
            'image_url': item.image_url,        
        }for item in recentview_products]

        return JsonResponse({'message': 'SUCCESS', 'result': result}, status = 200)
    @login_decorator    
    def delete(self, request):
        delete_recentview = RecentView.objects.get(product_id=data['product_id'], member_id=request.user)
        delete_recentview.delete()
        return JsonResponse({'message':'DELETE'})