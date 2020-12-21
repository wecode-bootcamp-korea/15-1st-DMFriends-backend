from django.db   import models
  
class Category(models.Model):
    name = models.CharField(max_length=45)
    
    class Meta:
        db_table = "categories"

class Subcategory(models.Model):
    name     = models.CharField(max_length=45)
    category = models.ForeignKey('Category',on_delete = models.SET_NULL, null=True)
    
    class Meta:
        db_table = "subcategories"

class Product(models.Model):
    name            = models.CharField(max_length=45, null=True)
    price           = models.DecimalField(max_digits= 7, decimal_places=2)
    star_rating     = models.DecimalField(max_digits= 3, decimal_places=1)
    description     = models.TextField(null=True)
    category        = models.ForeignKey('Category', on_delete = models.SET_NULL, null=True)
    subcategory     = models.ForeignKey('Subcategory', on_delete = models.SET_NULL, null=True)
    discount        = models.ForeignKey('Discount', on_delete = models.SET_NULL, null=True)
    image_url       = models.URLField(max_length = 2000, null=True)
    created_at      = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "products"

class ProductImage(models.Model):
    product     = models.ForeignKey('Product', on_delete = models.SET_NULL, null=True)
    image_url   = models.URLField(max_length=2000)
    
    class Meta:
        db_table = "productimages"

class Discount(models.Model):
    discount_rate   = models.DecimalField(max_digits= 3, decimal_places=1)
    discount_type   = models.CharField(max_length=45)
    discount_due    = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "discounts"

class Review(models.Model):
    product     = models.ForeignKey('Product', on_delete = models.SET_NULL, null=True)
    member      = models.ForeignKey('user.Member', on_delete = models.SET_NULL, null=True)
    content     = models.CharField(max_length=500)
    created_at  = models.DateTimeField(auto_now = True)
    star_rating = models.DecimalField(max_digits= 3, decimal_places=1)
    
    class Meta:
        db_table = "reviews"

