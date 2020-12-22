import json, bcrypt, jwt, re
from user.models import Member, RecentView, BoardLike, CommentLike

def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            auth_token = request.headers.get('Authorization', None)
            payload = jwt.decode(auth_token, my_settings.SECRET_KEY, my_settings.ALGORITHM)
            request.user = Member.objects.get(id=payload['user'])

        except Member.DoesNotExist:
            return JsonResponse({"message" : "INVALID_USER"}, status=400)
        except jwt.exceptions.DecodeError:
            return JsonResponse({"message" : "INVALID_TOKEN"}, status=400)
            
        return func(self, request, *args, **kwargs)
    return wrapper