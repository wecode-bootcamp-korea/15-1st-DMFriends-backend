from django.db   import models
from user.models import Member

class Board(models.Model):
    uploader        = models.CharField(max_length=45)
    created_at      = models.DateTimeField(auto_now = True)
    title           = models.CharField(max_length=100, null=True)
    content         = models.CharField(max_length=150)
    theme           = models.CharField(max_length=45)
    board_comment   = models.ManyToManyField('user.Member', through='Comment')

    class Meta:
        db_table = "boards"

class BoardImage(models.Model): 
    board       = models.ForeignKey('Board', on_delete = models.SET_NULL, null=True)
    image_url   = models.CharField(max_length=2000)  

    class Meta:
        db_table = "boardimages"


class Comment(models.Model):
    writer        = models.ForeignKey('user.Member', on_delete = models.SET_NULL, null=True)
    content       = models.CharField(max_length=500)
    created_at    = models.DateTimeField(auto_now = True)
    board         = models.ForeignKey('Board', on_delete = models.SET_NULL, null=True)
    self_comment  = models.ForeignKey('self', on_delete = models.SET_NULL, null=True)

    class Meta:
        db_table = "comments"

