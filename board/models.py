from django.db import models
from order.models import *
from product.models import *
from user.models import Member

class Board(models.Model):
    uploader        = models.CharField(max_length=45)
    created_at      = models.DateTimeField(
                        auto_now     = True, 
                        auto_now_add = True
                        )
    board_image_id  = ForeignKey(
                        'BoardImage'
                        on_delete = models.CASCADE
                        )
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
    member_id = models.ForeignKey('Member')
    is_like   = models.BooleanField()
    board_id  = models.ForeignKey('Board') 
    class Meta:
        db_table = "boardlikes"

class Comment(models.Model):
    content     = models.CharField(max_length=500)
    created_at  = models.DateTimeField(
                    auto_now     = True, 
                    auto_now_add = True
                    )
    member_id   = models.ForeignKey(
                    'Member',
                    on_delete = models.CASCADE
                    )
    board_id    = models.ForeignKey(
                    'Board',
                    on_delete = models.CASCADE
                    )
    comment_id  = models.ForeignKey(
                    'self',
                    on_delete = models.CASCADE
                    )
    class Meta:
        db_table = "comments"

class CommentLike(models.Model):
    comment_id = models.ForeignKey('Comment',)
    member_id = models.ForeignKey('Member')
    is_like = models.BooleanField()
    class Meta:
        db_table = "commentlikes"


