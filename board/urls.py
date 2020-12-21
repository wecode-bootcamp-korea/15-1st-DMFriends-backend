from django.urls    import path
from board.views    import BoardListView, GetBoardView

urlpatterns = [
    path('/index', BoardListView.as_view()),
    path('/getBoard', GetBoardView.as_view()),
]