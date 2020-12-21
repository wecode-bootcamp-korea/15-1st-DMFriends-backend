import json

from django.http    import JsonResponse
from django.views   import View

from board.models   import Board, BoardImage, Comment
from user.models    import Member, BoardLike, CommentLike

# 1. 동묘프렌즈 첫 접속 - '오늘' 탭 게시물 로드
class BoardListView(View):
    def check_comment(self, board_id):
        if Comment.objects.filter(board_id = board_id).exists() : 
            data = Comment.objects.filter(board_id = board_id).order_by('-created_at').first()
            comment_data = {
                "writer"    : data.writer.nickname,
                "content"   : data.content
            }
        else:
            comment_data = ''
        return comment_data

    def get(self, request):
        try: 
            board_list = [{
                "id"            : board.id,
                "uploader"      : board.uploader,
                "theme"         : board.theme,
                "title"         : board.title,
                "content"       : board.content,
                "created_at"    : board.created_at,
                "board_images"  : list(BoardImage.objects.filter(board_id = board.id).values('image_url')),
                "board_likes"   : BoardLike.objects.filter(board_id = board.id).count(),
                "comment"       : BoardListView.check_comment(self,board.id)
            } for board in Board.objects.all()]  
            return JsonResponse({'message' : 'SUCCESS', 'board_list' : board_list}, status = 200)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
        except ValueError:
            return JsonResponse({'message' : 'DECODE_ERROR'}, status = 400)
        except Board.DoesNotExist:
            return JsonResponse({'message' : 'NO_EXIST_DATA'}, status = 500)
        except Board.MultipleObjectsReturned:
            return JsonResponse({'message' : 'TOO_MANY_DATA'}, status = 500)
        
# 2. 게시물 조회 - 하나의 게시물 & 댓글 & 좋아요 - select_related() 사용해볼것?
class GetBoardView(View):
    def get(self, request):
        try:
            
            return JsonResponse({'message' : 'SUCCESS', 'board_list' : boards}, status = 200)
        
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
        except ValueError:
            return JsonResponse({'message' : 'DECODE_ERROR'}, status = 400)
        except Board.DoesNotExist:
            return JsonResponse({'message' : 'NO_EXIST_DATA'}, status = 500)
        except Board.MultipleObjectsReturned:
            return JsonResponse({'message' : 'TOO_MANY_DATA'}, status = 500)



