from django.db import models
from product.models import Product
from board.models import Board, Comment


class Member(models.Model):
    email             = models.EmailField(max_length=100)
    nickname          = models.CharField(max_length=20)
    privacy_agreement = models.BooleanField(default=False)
    anonymous         = models.BooleanField(default=False)
    random_number     = models.CharField(max_length=45)
    password          = models.CharField(max_length=100)
    board_like        = models.ManyToManyField('board.Board', through='board.BoardLike')
    board_comment     = models.ManyToManyField('board.Board',through= 'board.Comment')
    comment_like      = models.ManyToManyField('board.Comment', through='board.CommentLike')
    product           = models.ManyToManyField('product.Product', through='product.RecentView')
    
    class Meta:
        db_table = 'members'















































