from django.urls    import path
from board.views    import (
                            BoardListView, 
                            GetBoardView, 
                            CommentView,
                            AddSelfCommentView,
                            LikeBoardView,
                            LikeCommentView,
                            )

urlpatterns = [
    path('/main'                , BoardListView.as_view()),
    path('/feed/<int:board_id>' , GetBoardView.as_view()),
    path('/comment'             , CommentView.as_view()),
    path('/addselfcomment'      , AddSelfCommentView.as_view()),
    path('/like'                , LikeBoardView.as_view()),
    path('/likecomment'         , LikeCommentView.as_view()),
]