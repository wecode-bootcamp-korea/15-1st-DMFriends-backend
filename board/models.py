from django.db import models
from user.models import Member

class Board(models.Model):
    uploader        = models.CharField(max_length=45)
    created_at      = models.DateTimeField(auto_now = True)
    content         = models.CharField(max_length=45)
    theme           = models.CharField(max_length=45)
    class Meta:
        db_table = "boards"

class BoardImage(models.Model): 
    board_id    = models.ForeignKey(
                    'Board',
                    on_delete = models.CASCADE
                    )
    image_url   = models.CharField(max_length=2000)  
    class Meta:
        db_table = "boardimages"

class BoardLike(models.Model):
    member = models.ForeignKey('user.Member',on_delete  = models.CASCADE)
    is_like   = models.BooleanField()
    board  = models.ForeignKey('Board',on_delete  = models.CASCADE) 
    class Meta:
        db_table = "boardlikes"

class Comment(models.Model):
    writer    = models.ForeignKey('user.Member', on_delete = models.CASCADE)
    content     = models.CharField(max_length=500)
    created_at  = models.DateTimeField(
                    auto_now = True, 
                    )
    board    = models.ForeignKey(
                    'Board',
                    on_delete = models.CASCADE
                    )
    self_comment  = models.ForeignKey(
                    'self',
                    on_delete = models.CASCADE
                    )
    class Meta:
        db_table = "comments"

class CommentLike(models.Model):
    comment = models.ForeignKey('Comment',on_delete  = models.CASCADE)
    member = models.ForeignKey('user.Member',on_delete  = models.CASCADE)
    is_like = models.BooleanField()
    class Meta:
        db_table = "commentlikes"