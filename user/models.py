from django.db import models
from order.models import *
from product.models import *
from board.models import *


class Member(models.Model):
    def random_number():
        return str(random.randit(1000,9999))
    email             = models.EmailField(max_length=100)
    nickname          = models.CharField(max_length=20)
    privacy_agreement = models.BooleanField()
    anonymous         = models.BooleanField()
    random_number     = models.CharField(max_length=45, default = random_number)
    password          = models.CharField(max_length=100)
    board             = models.ManyToManyField('Board', through='BoardLike')
    comment           = models.ManyToManyField('Comment', through='CommentLike')
    product           = models.ManyToManyField('Product', through='RecentView')
    class Meta:
        db_table = 'members'
















































