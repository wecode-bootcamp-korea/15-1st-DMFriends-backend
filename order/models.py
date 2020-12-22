from django.db      import models
from user.models    import Member
from product.models import Product
class Order(models.Model):
    order_number      = models.CharField(max_length=45)
    order_status      = models.ForeignKey('OrderStatus', on_delete = models.SET_NULL, null=True, default = 1)    
    address           = models.ForeignKey('Address', on_delete = models.SET_NULL, null=True)
    member            = models.ForeignKey('user.Member', on_delete = models.SET_NULL, null=True)
    delivery_message  = models.CharField(max_length=500)
    order_date        = models.DateField( auto_now = True)
    payments          = models.ForeignKey( 'Payment', on_delete   = models.SET_NULL, null=True)
    class Meta:
        db_table = "orders"
class Address(models.Model):
    address         = models.CharField(max_length=45)
    detail_address  = models.CharField(max_length=45)
    member_id       = models.ManyToManyField('user.Member', through = 'Order')
    default         = models.BooleanField(default=False)
    created_at      = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'addresses'
class OrderStatus(models.Model):
    name = models.CharField(max_length=45)
    class Meta:
        db_table = "orderstatuses"
class Cart(models.Model):
    quantity    = models.IntegerField(default=0)
    total_price = models.DecimalField(max_digits= 10, decimal_places=2)
    product     = models.ForeignKey('product.Product', on_delete = models.SET_NULL, null=True, default = 1)
    created_at  = models.DateTimeField(auto_now = True)
    order       = models.ForeignKey('Order', on_delete = models.SET_NULL, null=-True, default = 1)
    class Meta:
        db_table = "carts"
class Payment(models.Model):
    kakao_pay       = models.CharField(max_length=45)
    virtual_account = models.CharField(max_length=45)
    payment_type   = models.ForeignKey('PaymentType',on_delete = models.SET_NULL, null= True, default = 1)
    member          = models.ForeignKey('user.Member',on_delete = models.SET_NULL, null= True, default = 1)
    payment_status = models.ForeignKey('PaymentStatus', on_delete = models.SET_NULL, null= True, default = 1)
    class Meta:
        db_table = 'payments'
class PaymentType(models.Model):
    name    = models.CharField(max_length=45)
    class Meta:
        db_table = 'paymenttypes'
class PaymentStatus(models.Model):
    name = models.CharField(max_length=45)
    class Meta:
        db_table = 'paymentstatuses'