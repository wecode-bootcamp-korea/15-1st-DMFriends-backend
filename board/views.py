import json
import datetime

from django.http    import JsonResponse
from django.views   import View

from board.models   import Board, BoardImage, Comment
from user.models    import Member, BoardLike, CommentLike
#from user.utils     import login_decorator

# 1. 동묘프렌즈 첫 접속 - '오늘' 탭 게시물 로드
class BoardListView(View):
    def check_comment(self, board_id):
        if Comment.objects.filter(board_id = board_id).exists() : 
            data = Comment.objects.filter(board_id = board_id).order_by('-created_at').first()
            comment_data = {
                "id"            : data.id,
                "writer"        : data.writer.nickname,
                "content"       : data.content,
                "content_num"   : Comment.objects.filter(board_id = board_id).count()
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
                "thumb_image"   : BoardImage.objects.filter(board_id = board.id).values_list('image_url', flat=True)[0],
                "board_images"  : list(BoardImage.objects.filter(board_id = board.id).values_list('image_url', flat=True)[1:]),
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


# 2-1. 게시물 상세조회 - 게시물 호출        
class GetBoardView(View):
    def get(self, request, board_id):
        try:
            data = Board.objects.filter(id = board_id)[0]

            # 리턴보낼 board_data 준비
            board_data = {
                "id"            : data.id,
                "uploader"      : data.uploader,
                "theme"         : data.theme,
                "title"         : data.title,
                "content"       : data.content,
                "created_at"    : data.created_at,
                "thumb_image"   : BoardImage.objects.filter(board_id = board.id).values_list('image_url', flat=True)[0],
                "board_images"  : list(BoardImage.objects.filter(board_id = board_id).values_list('image_url', flat=True)[1:]),
                "board_likes"   : BoardLike.objects.filter(board_id = board_id).count()
            }
            return JsonResponse({'message' : 'SUCCESS', 'board_list' : board_data}, status = 200)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
        except ValueError:
            return JsonResponse({'message' : 'DECODE_ERROR'}, status = 400)
        except Board.DoesNotExist:
            return JsonResponse({'message' : 'NO_EXIST_DATA'}, status = 500)    


# 2-2. 게시물 상세조회 
class CommentView(View):
    ## 1. 댓글 목록 호출(GET)
    def get(self, request):
        try:
            board_id    = request.GET.get('board_id', None)
            sort        = request.GET.get('sort', None)
            page        = int(request.GET.get("page", 1) or 1)
            page_size = 2
            limit = int(page_size * page)
            offset = int(limit - page_size) 

            if Comment.objects.filter(board_id = board_id).exists(): 
                data = Comment.objects.filter(board_id=board_id).order_by(sort).values()[offset:limit]
                comment_data = [{
                    "id"        : comment['id'],
                    "writer"    : Member.objects.get(id=comment['writer_id']).nickname,
                    "content"   : comment['content'],
                    "is_liked"  : CommentLike.objects.filter(comment_id = comment['id'], is_like = 1).count(), 
                    "created_at": comment['created_at']
                } for comment in data]
            else:
                comment_data = ''
            return JsonResponse({'message' : 'SUCCESS', 'comment_data' : comment_data, 'page' : page}, status = 200)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
        except ValueError:
            return JsonResponse({'message' : 'DECODE_ERROR'}, status = 400)
        except Comment.DoesNotExist:
            return JsonResponse({'message' : 'NO_EXIST_DATA'}, status = 500)        
        except :
            return JsonResponse({'message' : 'NO_COMMENT_EXIST'}, status = 500)

    ## 2. 댓글 작성(POST)
    #@login_decorator
    def post(self, request):
        try:
            data        = json.loads(request.body)
            board_id    = data['board_id']
            member_id   = data['member_id']
            content     = data['content']

            if content == "":
                return JsonResponse({'message' : 'COMMENT_REQUIRED'}, status=400)
            else:
                Comment.objects.create(
                    content         = content,
                    created_at      = datetime.datetime.now(),
                    board_id        = board_id,
                    writer_id       = member_id
                )
            return JsonResponse({'message' : 'SUCCESS'}, status = 201)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)          
        except :
            return JsonResponse({'message' : 'NO_COMMENT_EXIST'}, status = 500) 


# 3. 대댓글 작성
class AddSelfCommentView(View):
    #@login_decorator
    def post(self, request):
        try:
            data        = json.loads(request.body)
            board_id    = data['board_id']
            member_id   = data['member_id']
            comment_id  = data['comment_id']
            content     = data['content']

            if board_id and member_id:
                if content == "":
                    return JsonResponse({'message' : 'COMMENT_REQUIRED'}, status=400)
                elif Comment.objects.filter(id=comment_id).exists():
                    Comment.objects.create(
                        content         = content,
                        created_at      = datetime.datetime.now(),
                        board_id        = board_id,
                        self_comment_id = comment_id,
                        writer_id       = member_id
                    )
            return JsonResponse({'message' : 'SUCCESS'}, status = 201)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
        except :
            return JsonResponse({'message' : 'NO_COMMENT_EXIST'}, status = 500)


# 4. 게시물 좋아요
class LikeBoardView(View):
    #@login_decorator
    def post(self, request):
        try:
            data        = json.loads(request.body)
            board_id    = data['board_id']
            member_id   = data['member_id']

            if BoardLike.objects.filter(board_id=board_id, member_id=member_id).exists():
                if BoardLike.objects.filter(board_id=board_id, member_id=member_id)[0].is_like == 1:
                    BoardLike.objects.filter(board_id=board_id, member_id=member_id).update(is_like=0)
                    return JsonResponse(
                        {
                            'message' : 'SUCCESS', 
                            'member_id' : member_id, 
                            'like' : False
                        }, status = 200)
                else:
                    BoardLike.objects.filter(board_id=board_id, member_id=member_id).update(is_like=1)
                    return JsonResponse(
                        {
                            'message' : 'SUCCESS', 
                            'member_id' : member_id, 
                            'like' : True
                        }, status = 200)
            else:
                BoardLike.objects.create(
                    is_like     = 1,
                    board_id    = board_id,
                    member_id   = member_id
                )
                return JsonResponse(
                    {
                        'message' : 'SUCCESS', 
                        'member_id' : member_id, 
                        'like' : True
                    }, status = 201)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
        except :
            return JsonResponse({'message' : 'NO_COMMENT_EXIST'}, status = 500) 


# 5. 댓글 좋아요
class LikeCommentView(View):
    #@login_decorator
    def post(self, request):
        try:
            data        = json.loads(request.body)
            member_id   = data['member_id']
            comment_id  = data['comment_id']

            if CommentLike.objects.filter(member_id=member_id, comment_id=comment_id).exists():
                if CommentLike.objects.filter(member_id=member_id, comment_id=comment_id)[0].is_like == 1:
                    CommentLike.objects.filter(member_id=member_id, comment_id=comment_id).update(is_like=0)
                    return JsonResponse(
                        {
                            'message' : 'SUCCESS', 
                            'member_id' : member_id, 
                            'like' : False
                        }, status = 200)
                else:
                    CommentLike.objects.filter(member_id=member_id, comment_id=comment_id).update(is_like=1)
                    return JsonResponse(
                        {
                            'message' : 'SUCCESS', 
                            'member_id' : member_id, 
                            'like' : True
                        }, status = 200)
            else:
                CommentLike.objects.create(
                    is_like     = 1,
                    comment_id  = comment_id,
                    member_id   = member_id
                )
            return JsonResponse(
                {
                    'message' : 'SUCCESS', 
                    'member_id' : member_id, 
                    'like' : True
                }, status = 201)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
        except :
            return JsonResponse({'message' : 'NO_COMMENT_EXIST'}, status = 500)




