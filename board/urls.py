from django.urls    import path
from board.views    import (
                            BoardListView, 
                            GetBoardView, 
                            GetCommentView,
                            LikeBoardView,
                            UnLikeBoardView,
                            AddCommentView,
                            )

urlpatterns = [
    path('/main', BoardListView.as_view()),
    path('/feed/<int:board_id>', GetBoardView.as_view()),
    path('/comment', GetCommentView.as_view()),
    path('/like', LikeBoardView.as_view()),
    path('/unlike', UnLikeBoardView.as_view()),
    path('/addcomment', AddCommentView.as_view()),
]