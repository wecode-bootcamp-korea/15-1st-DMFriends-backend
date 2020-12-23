import json, bcrypt, jwt, re

from django.http import JsonResponse
from my_settings import SECRET_KEY, ALGORITHM
from user.models import Member, RecentView, BoardLike, CommentLike


def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization', None)
            payload = jwt.decode(access_token, SECRET_KEY, algorithm=ALGORITHM)
            user = Member.objects.get(id=payload['member_id'])
            request.user = user

        except Member.DoesNotExist:
            return JsonResponse({"message" : "INVALID_USER"}, status=400)
        except jwt.exceptions.DecodeError:
            return JsonResponse({"message" : "INVALID_TOKEN"}, status=400)
            
        return func(self, request, *args, **kwargs)
    return wrapper