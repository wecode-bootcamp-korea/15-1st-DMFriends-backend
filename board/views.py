import json

from django.http    import JsonResponse
from django.views   import View

from board.models   import Board, BoardImage, Comment
from user.models    import Member, BoardLike, CommentLike

# 1. 동묘프렌즈 첫 접속 - '오늘' 탭 게시물 로드
class BoardListView(View):
    def get(self, request):
        try:            
            # '오늘' 탭 목록을 위한 board 리스트 준비 (전체 게시물 개수만큼 반복)
            ## board image 준비
            ## 게시물 좋아요 수 가져오기
            ## 가장 최근의 댓글 가져오기(댓글이 아예 없는 경우 대비)
            comment_data_writer = Comment.objects.filter(board_id = 3).only('writer').order_by('-created_at').first()
            comment_data_content = Comment.objects.filter(board_id = 3).only('content').order_by('-created_at').first()
            #print(Comment.objects.filter(board_id = 3).order_by('-created_at').first().writer.nickname)
            #print(Comment.objects.filter(board_id = 3).order_by('-created_at').first().content)
            
            def check_comment(self, board_id):
                print(board_id)
                if Comment.objects.filter(board_id = board_id).exists() : 
                    data = Comment.objects.filter(board_id = board_id).order_by('-created_at').first()
                    comment_data = {
                        "writer"    : data.writer.nickname,
                        "content"   : data.content
                    }
                else:
                    comment_data = ''
                return comment_data

            
            board_list = [{
                "id"            : board.id,
                "uploader"      : board.uploader,
                "theme"         : board.theme,
                "title"         : board.title,
                "content"       : board.content,
                "created_at"    : board.created_at,
                "board_images"  : list(BoardImage.objects.filter(board_id = board.id).values('image_url')),
                "board_likes"   : BoardLike.objects.filter(board_id = board.id).count(),
                "comment"       : check_comment(self,board.id)
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
            print('a')
            return JsonResponse({'message' : 'SUCCESS', 'board_list' : boards}, status = 200)
        
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
        except ValueError:
            return JsonResponse({'message' : 'DECODE_ERROR'}, status = 400)
        except Board.DoesNotExist:
            return JsonResponse({'message' : 'NO_EXIST_DATA'}, status = 500)
        except Board.MultipleObjectsReturned:
            return JsonResponse({'message' : 'TOO_MANY_DATA'}, status = 500)



