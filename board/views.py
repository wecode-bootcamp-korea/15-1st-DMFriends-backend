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
                "board_images"  : list(BoardImage.objects.filter(board_id = board.id).values_list('image_url', flat=True)),
                "board_likes"   : BoardLike.objects.filter(board_id = board.id).count(),
                "comment"       : BoardListView.check_comment(self, board.id)
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
        
# 2. 게시물 상세조회
class GetBoardView(View):
    def get_comments(self, request, board_id):
        sort = request.GET.get('sort', None)
        if Comment.objects.filter(board_id = board_id).exists(): 
            data = Comment.objects.filter(board_id=board_id).order_by(sort).values()
            comment_data = [{
                "id"        : comment['id'],
                "writer"    : Member.objects.get(id=comment['writer_id']).nickname,
                "content"   : comment['content'],
                "is_liked"  : CommentLike.objects.filter(comment_id = comment['id'], is_like = 1).count(), 
                "created_at": comment['created_at']
            } for comment in data]
        else:
            comment_data = ''
        #print(comment_data)
        return comment_data

    def get(self, request):
        try:
            board_id = request.GET.get('board_id', None)
            orderby = request.GET.get('orderby', None)

            data = Board.objects.filter(id = board_id)[0]

            # 리턴보낼 board_data 준비
            board_data = {
                "id"            : data.id,
                "uploader"      : data.uploader,
                "theme"         : data.theme,
                "title"         : data.title,
                "content"       : data.content,
                "created_at"    : data.created_at,
                "board_images"  : list(BoardImage.objects.filter(board_id = board_id).values_list('image_url', flat=True)),
                "board_likes"   : BoardLike.objects.filter(board_id = board_id).count(),
                "comment"       : GetBoardView.get_comments(self, request, board_id)
            }
            return JsonResponse({'message' : 'SUCCESS', 'board_list' : board_data}, status = 200)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
        except ValueError:
            return JsonResponse({'message' : 'DECODE_ERROR'}, status = 400)
        except Board.DoesNotExist:
            return JsonResponse({'message' : 'NO_EXIST_DATA'}, status = 500)
        except Board.MultipleObjectsReturned:
            return JsonResponse({'message' : 'TOO_MANY_DATA'}, status = 500)
        

