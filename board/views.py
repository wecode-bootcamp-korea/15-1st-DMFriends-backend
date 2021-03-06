import json
import datetime

from django.http    import JsonResponse
from django.views   import View

from board.models   import Board, BoardImage, Comment
from user.models    import Member, BoardLike, CommentLike
from user.utils     import login_check

# 로그인 여부에 따른 게시물 좋아요 체크
def check_boardLike(self, request, board_id):
    result = False
    if request.user:
        result = BoardLike.objects.filter(board_id= board_id, member_id = request.user.id).exists()
    return result

# 로그인 여부에 따른 댓글 좋아요 체크
def check_commentLike(self, request, comment_id):
    result = False
    if request.user:
        result = CommentLike.objects.filter(comment_id= comment_id, member_id = request.user.id).exists()
    return result

# 1. 동묘프렌즈 첫 접속 - '오늘' 탭 게시물 로드
class BoardListView(View):
    def check_comment(self, board_id):
        if Comment.objects.filter(board_id = board_id).exists(): 
            data = Comment.objects.filter(board_id = board_id).order_by('-created_at').first()
            comment_data = {
                "id"            : data.id,
                "writer"        : data.writer.nickname,
                "content"       : data.content,
                "content_num"   : Comment.objects.filter(board_id = board_id).count()
            }
        else:
            comment_data = {'content_num':0}
        return comment_data

    @login_check
    def get(self, request):
        try: 
            board_list  = [{
                "id"            : board.id,
                "uploader"      : board.uploader,
                "theme"         : board.theme,
                "title"         : board.title,
                "content"       : board.content,
                "created_at"    : board.created_at,
                "thumb_image"   : BoardImage.objects.filter(board_id = board.id).values_list('image_url', flat=True)[0],
                "board_images"  : list(BoardImage.objects.filter(board_id = board.id).values_list('image_url', flat=True)[1:]),
                "board_likes"   : BoardLike.objects.filter(board_id = board.id).count(),
                "member_liked"    : check_boardLike(self, request, board.id),
                "comment"       : BoardListView.check_comment(self, board.id)
            } for board in Board.objects.all()]  

            return JsonResponse({'message' : 'SUCCESS', 'board_list' : board_list}, status = 200)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
        except ValueError:
            return JsonResponse({'message' : 'DECODE_ERROR'}, status = 400)
        except Board.DoesNotExist:
            return JsonResponse({'message' : 'BOARD_DOES_NOT_EXIST'}, status = 404)


# 2-1. 게시물 상세조회 - 게시물 호출        
class GetBoardView(View):
    @login_check
    def get(self, request, board_id):
        try:
            data = Board.objects.get(id = board_id)
            
            # 리턴보낼 board_data 준비
            board_data = {
                "id"            : data.id,
                "uploader"      : data.uploader,
                "theme"         : data.theme,
                "title"         : data.title,
                "content"       : data.content,
                "created_at"    : data.created_at,
                "thumb_image"   : BoardImage.objects.filter(board_id = board_id).values_list('image_url', flat=True)[0],
                "board_images"  : list(BoardImage.objects.filter(board_id = board_id).values_list('image_url', flat=True)[1:]),
                "board_likes"   : BoardLike.objects.filter(board_id = board_id).count(),
                "member_liked"    : check_boardLike(self, request, board_id)
            }
            return JsonResponse({'message' : 'SUCCESS', 'board_list' : board_data}, status = 200)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
        except ValueError:
            return JsonResponse({'message' : 'DECODE_ERROR'}, status = 400)
        except Board.DoesNotExist:
            return JsonResponse({'message' : 'NO_EXIST_DATA'}, status = 404)    


# 2-2. 게시물 상세조회 
class CommentView(View):
    ## 1. 댓글 목록 호출(GET)
    @login_check
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
                    "created_at": comment['created_at'],
                    "member_liked": check_commentLike(self, request, comment['id']),
                } for comment in data]
            else:
                comment_data = ''
            return JsonResponse({'message' : 'SUCCESS', 'comment_data' : comment_data, 'page' : page}, status = 200)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
        except ValueError:
            return JsonResponse({'message' : 'DECODE_ERROR'}, status = 400)
        except Comment.DoesNotExist:
            return JsonResponse({'message' : 'COMMENT_DOES_NOT_EXIST'}, status = 404)   

    ## 2. 댓글 작성(POST)
    @login_check
    def post(self, request):
        try:
            if request.user == None:
                return JsonResponse({"message" : "INVALID_USER"}, status=400) 

            data        = json.loads(request.body)
            board_id    = data['board_id']
            content     = data['content']

            if content == "":
                return JsonResponse({'message' : 'COMMENT_REQUIRED'}, status=400)
            else:
                Comment.objects.create(
                    content         = content,
                    created_at      = datetime.datetime.now(),
                    board_id        = board_id,
                    writer_id       = request.user.id
                )
            return JsonResponse({'message' : 'SUCCESS'}, status = 201)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)   


# 3. 대댓글 작성
class AddSelfCommentView(View):
    @login_check
    def post(self, request):
        try:
            if request.user == None:
                return JsonResponse({"message" : "INVALID_USER"}, status=400) 

            data        = json.loads(request.body)
            board_id    = data['board_id']
            comment_id  = data['comment_id']
            content     = data['content']
            if content == "":
                return JsonResponse({'message' : 'COMMENT_REQUIRED'}, status=400)
            if board_id and request.user:
                if Comment.objects.filter(id=comment_id).exists():
                    Comment.objects.create(
                        content         = content,
                        created_at      = datetime.datetime.now(),
                        board_id        = board_id,
                        self_comment_id = comment_id,
                        writer_id       = request.user.id
                    )
            return JsonResponse({'message' : 'SUCCESS'}, status = 201)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
        except :
            return JsonResponse({'message' : 'NO_COMMENT_EXIST'}, status = 500)


# 4. 게시물 좋아요
class LikeBoardView(View):
    @login_check
    def post(self, request):
        try:
            if request.user == None:
                return JsonResponse({"message" : "INVALID_USER"}, status=400) 
            
            data        = json.loads(request.body)
            board_id    = data['board_id']

            if BoardLike.objects.filter(board_id=board_id, member_id=request.user.id).exists():
                if BoardLike.objects.get(board_id=board_id, member_id=request.user.id).is_like == 1:
                    BoardLike.objects.filter(board_id=board_id, member_id=request.user.id).update(is_like=0)
                    return JsonResponse(
                        {
                            'message' : 'SUCCESS', 
                            'member_id' : request.user.id, 
                            'like' : False
                        }, status = 200)
                
                BoardLike.objects.filter(board_id=board_id, member_id=request.user.id).update(is_like=1)
                return JsonResponse(
                    {
                        'message' : 'SUCCESS', 
                        'member_id' : request.user.id, 
                        'like' : True
                    }, status = 200)
            
            BoardLike.objects.create(
                is_like     = 1,
                board_id    = board_id,
                member_id   = request.user.id
            )
            return JsonResponse(
                {
                    'message' : 'SUCCESS', 
                    'member_id' : request.user.id, 
                    'like' : True
                }, status = 201)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)


# 5. 댓글 좋아요
class LikeCommentView(View):
    @login_check
    def post(self, request):
        try:
            if request.user == None:
                return JsonResponse({"message" : "INVALID_USER"}, status=400) 

            data        = json.loads(request.body)
            comment_id  = data['comment_id']

            if CommentLike.objects.filter(member_id=request.user.id, comment_id=comment_id).exists():
                if CommentLike.objects.get(member_id=request.user.id, comment_id=comment_id).is_like == 1:
                    CommentLike.objects.filter(member_id=request.user.id, comment_id=comment_id).update(is_like=0)
                    return JsonResponse(
                        {
                            'message' : 'SUCCESS', 
                            'member_id' : request.user.id, 
                            'like' : False
                        }, status = 200)
                
                CommentLike.objects.filter(member_id=request.user.id, comment_id=comment_id).update(is_like=1)
                return JsonResponse(
                    {
                        'message' : 'SUCCESS', 
                        'member_id' : request.user.id, 
                        'like' : True
                    }, status = 200)
            
            CommentLike.objects.create(
                is_like     = 1,
                comment_id  = comment_id,
                member_id   = request.user.id
            )
            return JsonResponse(
                {
                    'message' : 'SUCCESS', 
                    'member_id' : request.user.id, 
                    'like' : True
                }, status = 201)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)