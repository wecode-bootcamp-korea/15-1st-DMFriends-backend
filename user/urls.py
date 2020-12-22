from django.urls import path
<<<<<<< HEAD
from user.views  import SignUpView, LoginView, EmailCheckView, VerificationCodeView

urlpatterns=[
    path('/signup', SignUpView.as_view()),
    path('/login', LoginView.as_view()),
    path('/echeck', EmailCheckView.as_view()),
    path('/vcode', VerificationCodeView.as_view()),

=======
>>>>>>> c6720d2aa84aeba86a41de8bb00bc8eef763e98d
]

