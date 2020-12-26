from django.urls import path
from user.views  import SignUpView, LoginView, EmailCheckView, VerificationCodeView, RecentViews

urlpatterns=[
    path('/signup', SignUpView.as_view()),
    path('/login', LoginView.as_view()),
    path('/email-check', EmailCheckView.as_view()),
    path('/verification', VerificationCodeView.as_view()),
    path('/recentview',RecentViews.as_view()),
]

