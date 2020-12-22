from django.urls import path
from user.views  import SignUpView, LoginView, EmailCheckView, VerificationCodeView

urlpatterns=[
    path('/signup', SignUpView.as_view()),
    path('/login', LoginView.as_view()),
    path('/echeck', EmailCheckView.as_view()),
    path('/vcode', VerificationCodeView.as_view()),

]

