from django.db import models
from user.models import Member,

class Board(models.Model):
    uploader        = models.CharField(max_length=45)
    created_at      = models.DateTimeField(auto_now = True)
    content         = models.CharField(max_length=45)
    theme = models.CharField(max_length=45)
    
    class Meta:
        db_table = "boards"

class BoardImage(models.Model):
    board       = models.ForeignKey('Board', on_delete = models.SET_NULL, null = True)
    image_url   = models.URLField(max_length=2000)
    
    class Meta:
        db_table = "boardimages"

class BoardLike(models.Model):
    member      = models.ForeignKey('user.Member',on_delete = models.SET_NULL, null = True)
    is_like     = models.BooleanField(default=False)
    board       = models.ForeignKey('Board',on_delete = models.SET_NULL, null = True)
    
    class Meta:
        db_table = "boardlikes"

class Comment(models.Model):
    member          = models.ForeignKey('user.Member',on_delete = models.SET_NULL, null = True)
    content         = models.CharField(max_length=500)
    created_at      = models.DateTimeField(auto_now = True)
    board           = models.ForeignKey('Board', on_delete=models.SET_NULL, null=True)
    self_comment    = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
    
    
    class Meta:
        db_table = "comments"

class CommentLike(models.Model):
    comment     = models.ForeignKey('Comment',on_delete = models.SET_NULL, null = True)
    member      = models.ForeignKey('user.Member',on_delete = models.SET_NULL, null = True)
    is_like     = models.BooleanField(default=False)
    
    class Meta:
        db_table = "commentlikes"
