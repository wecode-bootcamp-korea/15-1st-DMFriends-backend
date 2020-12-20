import json, bcrypt, jwt, re
import my_settings

from django.db.models import Q
from .utils import token_check
from django.views import View
from django.http import JsonResponse, HttpResponse
from user.models import Member, RecentView, BoardLike, CommentLike
from board.models. import Board
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            
            if not validate_email(email):
                raise ValidationError('INVALID_EMAIL')
                    
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
            return JsonResponse({'message': 'VALIDATION_EMAIL'}, status=400)

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

        def login_decorator(func):
            def wrapper(self, request, *args, **kwargs):
            try:
                auth_token = request.headers.get('Authorization', None)
                payload = jwt.decode(auth_token, my_settings.SECRET_KEY, my_settings.ALGORITHM)
                request.user = Member.objects.get(id=payload['member_id'])
                return func(self, request, *args, **kwargs)

            except User.DoesNotExist:
                return JsonResponse({"message" : "INVALID_MEMBER"}, status=400)
            except jwt.exceptions.DecodeError:
                return JsonResponse({"message" : "INVALID_TOKEN"}, status=400)
            
        return wrapper

class BoardLikeView(View):
    @login_decorator
    def post(self, request):
        data = json.loads(request.body)

        if not BoardLike.objects.filter(board_id=request.data['board.id'], member_id=request.user.id).exist():
            BoardLike.objects.create(
                member =request.user,
                board=Board.objects.get(id=data['board_id'])
            )
            return JsonResponse({'message': 'ADD'}, status=200)
        delete_like = BoardLike.objects.get(board_id=data['board_id'], member_id=request.user.id)
        delete_like.delete()

        return JsonResponse({'message':'DELETE'})

class CommentLikeView(View):
    @login_decorator
    def post(self, request):
        data = json.loads(request.body)

        if not CommentLike.objects.filter(comment_id=request.data['comment.id'], member_id=request.user.id).exist():
            CommentLike.objects.create(
                member =request.user,
                comment=Comment.objects.get(id=data['comment_id'])
            )
            return JsonResponse({'message': 'ADD'}, status=200)
        delete_like = CommentLike.objects.get(comment_id=data['comment_id'], member_id=request.user.id)
        delete_like.delete()

        return JsonResponse({'message':'DELETE'})

class RecentView(View):
    @login_decorator
    def get(self, request):        
        product_id = request.GET.get('product_id')
        member_id = request.GET.get('member_id')

        if RecentView.objects.filter(product_id=product_id, member_id=member_id).exist():
            RecentView.objects.create(
                member_id=member_id,
                product_id=product_id  
            )
            viewed_at = RecentView.objects.all().order_by('-viewed_at')[0:50]
            return JsonResponse(['message':'RECENTVIEWED ADD'],status=200)
        

