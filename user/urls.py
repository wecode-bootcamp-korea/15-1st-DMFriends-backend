from django.urls import path
from user.views  import SignUpView, LoginView, EmailCheckView, VerificationCodeView, BoardLikeView, CommentLikeView, RecentView

urlpatterns=[
    path('/signup', SignUpView.as_view()),
    path('/login', LoginView.as_view()),
    path('/email-check', EmailCheckView.as_view()),
    path('/verification', VerificationCodeView.as_view()),
    path('/boardlike', BoardLikeView.as_view()),
    path('/commentlike', CommentLikeView.as_view()),
    path('/recentview',RecentView.as_view()),
]

