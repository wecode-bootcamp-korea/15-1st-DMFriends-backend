from django.db import models
from order.models import *
from product.models import *
from board.models import *


class Member(models.Model):
    email             = models.EmailField(max_length=100)
    nickname          = models.CharField(max_length=20)
    privacy_agreement = models.BooleanField()
    anonymous         = models.BooleanField()
    random_number     = models.CharField(max_length=45)
    password          = models.CharField(max_length=100)
    board             = models.ManyToManyField('board.Board', through='board.BoardLike')
    comment           = models.ManyToManyField('board.Comment', through='board.CommentLike')
    product           = models.ManyToManyField('product.Product', through='product.RecentView')
    
    class Meta:

        db_table = 'members'















































