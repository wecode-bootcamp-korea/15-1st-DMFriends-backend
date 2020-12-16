from django.db import models
from order.models import *
from board.models import *
from user.models import Member

class Category(models.Model):
    name = models.CharField(max_length=45)
    class Meta:
        db_table = "categories"

class Subcategory(models.Model):
    name        = models.CharField(max_length=45)
    category_id = models.OneToOneField(
        'Cateogory',
        on_delete   = models.CASCADE,
        primary_key = True,
    )
    class Meta:
        db_table = "categories"

class Character(models.Model):
    name = models.CharField(max_length=45)
    class Meta:
        db_table = "characters"

class Product(models.Model):
    name            = models.CharField(max_length=45, null=True)
    price           = models.DecimalField(max_digits=2)
    star_rating     = models.DecimalField(max_digits=1)
    description     = models.TextField()
    category_id     = models.OneToOneField(
                        'Category',
                        on_delete   = models.CASCADE,
                        primary_key = True,
                        )
    subcategory_id  = models.OneToOneField(
                        'Subcategory',
                        on_delete   = models.CASCADE,
                        primary_key = True,
                        )
    character_id    = models.OneToOneField(
                        'Character',
                        on_delete   = models.CASCADE,
                        primary_key = True,
                        )
    discount_id     = models.OneToOneField(
                        'Discount',
                        on_delete   = models.CASCADE,
                        primary_key = True,
                        )
    image           = models.CharField(max_length = 1000)
    created_at      = DateTimeField(
                        auto_now     = True, 
                        auto_now_add = True
                        )
    class Meta:
        db_table = "products"

class ProductImage(models.Model):
    product_id = models.ForeignKey(
                    'Product',
                    on_delete = models.CASCADE
                )
    image_url = models.CharField(max_length=2000)
    class Meta:
        db_table = "productimages"

class Discount(models.Model):
    discount_rate   = models.FloatField()
    discount_type   = models.CharField(max_length=45)
    discount_due    = DateTimeField(auto_now=True, auto_now_add=True)  
    class Meta:
        db_table = "discounts"

class Review(models.Model):
    product_id  = models.ForeignKey(
                    'Product',
                    on_delete = models.CASCADE       
                    )
    member_id   = models.ForeignKey(
                    'Member',
                    on_delete = models.CASCADE       
                    )
    content     = models.CharField(max_length=500)
    created_at  = models.DateTimeField(
                    auto_now     = True, 
                    auto_now_add = True
                    )
    star_rating = models.DecimalField(max_digits=2, decimal_places=2)   
    class Meta:
        db_table = "reviewlikes"

class RecentView(models.Model):
    product_id = models.ForeignKey('Product')
    member_id  = models.ForeignKey('Member')
    viewed_at = models.DateTimeField(auto_now=True, auto_now_add=True)
    class Meta:
        db_table = 'recentviews'

