from django.urls    import path
from board.views    import IndexView, GetBoardView

urlpatterns = [
    path('/index', IndexView.as_view()),
    path('/getBoard', GetBoardView.as_view()),
]