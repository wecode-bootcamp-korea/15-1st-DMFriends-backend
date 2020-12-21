import json

from django.http    import JsonResponse
from django.views   import View

from board.models   import Board, BoardImage, Comment
from user.models    import Member, BoardLike, CommentLike

# 1. 동묘프렌즈 첫 접속 - '오늘' 탭 게시물 로드
class BoardListView(View):
    def get(self, request):
        try:
            board_data  = Board.objects.all()
            boards       = []
            # 전체 게시물 개수만큼 반복
            for i in board_data:
                board_id    = i.id
                # 가장 최근의 댓글 목록[0] 가져오기
                comments      = []
                ## 1. 해당 게시물의 댓글 id 추출
                comment_list = Comment.objects.filter(
                                    board_id = board_id
                                )
                comment_ids = []
                for j in range(len(comment_list)):
                    comment_ids.append(comment_list[j].id)
                ## 2. 각 댓글의 좋아요 수 sum list 중 가장 큰 값 추출 
                comment_sums = {} 
                for j in range(len(comment_ids)):
                    comment_sums[comment_ids[j]] = CommentLike.objects.filter(comment_id =comment_ids[j]).count()
                # 3. 댓글이 아예 없는 경우 대비하기
                if comment_ids:
                    best_comment_id = max(comment_sums, key = comment_sums.get)
                    comment_data = comment_list.filter(id = best_comment_id)
                    # 댓글이 있을 경우 board 리스트에 담을 준비
                    if comment_data:
                        member_id = comment_data[0].writer_id
                        comments.append({
                            'comment_num'   : len(comment_data),
                            'writer'        : Member.objects.filter(id = comment_data[0].writer_id)[0].nickname,
                            'content'       : comment_data[0].content
                        })
                # board image 준비
                board_images        = []
                board_image_data    = BoardImage.objects.filter(board_id = board_id)
                for k in range(len(board_image_data)):
                    board_images.append(
                        board_image_data[k].image_url
                    )
                # 게시물 좋아요 수 가져오기
                board_likes = BoardLike.objects.filter(board_id = board_id)
                
                # '오늘' 탭 목록을 위한 board 리스트 준비
                boards.append({
                    'board_id'      : i.id,
                    'uploader'      : i.uploader,
                    'theme'         : i.theme,
                    'title'         : i.title,
                    'content'       : i.content,
                    'created_at'    : i.created_at,
                    'comment'       : comments,
                    'board_image'   : board_images,
                    'board_likes'   : len(board_likes)
                })
            return JsonResponse({'message' : 'SUCCESS', 'board_list' : boards}, status = 200)

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



