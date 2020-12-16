from django.db import models
from user.models import *
from product.models import *
from board.models import *

class Order(models.Model):
    order_number     = models.CharField(max_length=45)
    order_status     = models.OneToOneField(
                            'OrderStatus',
                            on_delete   = models.CASCADE,
                            )
    address_id       = models.OneToOneField(
                            'Address',
                            on_delete   = models.CASCADE,
                            )
    member_id        = models.OneToOneField(
                            'user.Member',
                            on_delete   = models.CASCADE,
                            )
    delivery_message = models.CharField(max_length=500)
    order_date       = models.DateTimeField(
                            auto_now = True,
                            )
    payments_id      = models.OneToOneField(
                            'Payment',
                            on_delete   = models.CASCADE,
                            )
    class Meta:
        db_table = "orders"

class Address(models.Model):
    address         = models.CharField(max_length=45)
    detail_address  = models.CharField(max_length=45)
    member_id       = models.ManyToManyField('user.Member', through = 'Order')
    default         = models.BooleanField()
    created_at      = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'addresses'

class OrderStatus(models.Model):
    name = models.CharField(max_length=45)
    class Meta:
        db_table = "orderstatuses"

class Cart(models.Model):
    quantity    = models.IntegerField()
    total_price = models.DecimalField(max_digits= 7, decimal_places=2)
    product_id  = models.IntegerField()
    created_at  = models.DateTimeField(auto_now = True)
    order_id    = models.OneToOneField(
                        'Order',
                        on_delete   = models.CASCADE,
                        )
    class Meta:
        db_table = "carts"

class Payment(models.Model):
    kakao_pay_id    = models.CharField(max_length=45)
    virtual_account = models.CharField(max_length=45)
    payments_type   = models.ForeignKey('PaymentType',on_delete  = models.CASCADE)
    member_id       = models.ForeignKey('user.Member',on_delete  = models.CASCADE)
    payments_status = models.OneToOneField('PaymentStatus', on_delete=models.CASCADE)
    class Meta:
        db_table = 'payments'

class PaymentType(models.Model):
    name    = models.CharField(max_length=45)
    member  = models.ManyToManyField('user.Member', through='Payment')
    class Meta:
        db_table = 'paymenttypes'

class PaymentStatus(models.Model):
    name = models.CharField(max_length=45)
    class Meta:
        db_table = 'paymentstatuses'

