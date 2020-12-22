from django.db      import models
from product.models import Product

class Member(models.Model):
    email             = models.EmailField(max_length=100, unique=True)
    nickname          = models.CharField(max_length=20, null=True)
    privacy_agreement = models.BooleanField(default=False)
    anonymous         = models.BooleanField(default=False)
    random_number     = models.CharField(max_length=45)
    password          = models.CharField(max_length=200, null=True)
    random_token      = models.IntegerField(null=True)
    board_like        = models.ManyToManyField('board.Board', through='BoardLike')
    comment_like      = models.ManyToManyField('board.Comment', through='CommentLike')
    member_recentview = models.ManyToManyField('product.Product', through='RecentView')
    
    class Meta:
        db_table = 'members'
    
class BoardLike(models.Model):
    member  = models.ForeignKey('Member',on_delete = models.SET_NULL, null=True)
    is_like = models.BooleanField()
    board   = models.ForeignKey('board.Board',on_delete = models.SET_NULL, null=True) 

    class Meta:
        db_table = "boardlikes"

class CommentLike(models.Model):
    comment = models.ForeignKey('board.Comment',on_delete = models.SET_NULL, null=True)
    member  = models.ForeignKey('Member',on_delete = models.SET_NULL, null=True)
    is_like = models.BooleanField()

    class Meta:
        db_table = "commentlikes"

class RecentView(models.Model):
    product     = models.ForeignKey('product.Product',on_delete = models.SET_NULL, null=True)
    member      = models.ForeignKey('Member',on_delete = models.SET_NULL, null=True)
    viewed_at   = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'recentviews'