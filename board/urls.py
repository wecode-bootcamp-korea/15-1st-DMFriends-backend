from django.urls    import path
from board.views    import BoardListView

urlpatterns = [
    path('/index', BoardListView.as_view()),
]