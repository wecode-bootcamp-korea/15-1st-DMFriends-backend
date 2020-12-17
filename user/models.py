from django.db      import models
from product.models import Product

class Member(models.Model):
    email             = models.EmailField(max_length=100, unique=True)
    nickname          = models.CharField(max_length=20)
    privacy_agreement = models.BooleanField(default=False)
    anonymous         = models.BooleanField(default=False)
    random_number     = models.CharField(max_length=45)
    password          = models.CharField(max_length=100)
    board_like        = models.ManyToManyField('board.Board', through='board.BoardLike')
    comment_like      = models.ManyToManyField('board.Comment', through='board.CommentLike')
    
    class Meta:
        db_table = 'members'

class RecentView(models.Model):
    product     = models.ForeignKey('product.Product',on_delete = models.SET_NULL, null=True)
    member      = models.ForeignKey('Member',on_delete = models.SET_NULL, null=True)
    viewed_at   = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'recentviews'