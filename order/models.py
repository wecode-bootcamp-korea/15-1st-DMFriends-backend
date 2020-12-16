from django.db import models
from user.models import Address, Member,
from product.models import *
from board.models import *

class Order(models.Model):
    order_number     = models.CharField(max_length=45)
    order_status     = models.OneToOneField(
                            'OrderStatus',
                            on_delete   = models.CASCADE,
                            primary_key = True,
                            )
    address_id       = models.OneToOneField(
                            'Address',
                            on_delete   = models.CASCADE,
                            primary_key = True,
                            )
    member_id        = models.OneToOneField(
                            'Member',
                            on_delete   = models.CASCADE,
                            primary_key = True,
                            )
    delivery_message = models.CharField(max_length=500)
    order_date       = models.DateTimeField(
                            auto_now     = True, 
                            auto_now_add = True
                            )
    payments_id      = models.OneToOneField(
                            'Payment',
                            on_delete   = models.CASCADE,
                            primary_key = True,
                            )
    class Meta:
        db_table = "orders"

class Address(models.Model):
    address         = models.CharField(max_length=45)
    detail_address  = models.CharField(max_length=45)
    member_id       = models.ManyToManyField('Member', through = 'Order') 
    default         = models.BooleanField()
    created_at      = DateTimeField(auto_now=True, auto_now_add=True)
    class Meta:
        db_table = 'addresses'

class OrderStatus(models.Model):
    name = models.CharField(max_length=45)
    class Meta:
        db_table = "orderstatuses"

class Cart(models.Model):
    quantity    = models.IntegerField()
    total_price = models.DecimalField(max_digits=2)
    product_id  = models.IntegerField()
    created_at  = DateTimeField(auto_now = True, auto_now_add = True)
    order_id    = models.OneToOneField(
                        'Order',
                        on_delete   = models.CASCADE,
                        primary_key = True,
                        )
    class Meta:
        db_table = "carts"

class Payment(models.Model):
    kakao_pay_id    = models.CharField(max_length=45)
    virtual_account = models.CharField(max_length=45)
    payments_type   = models.ForeignKey('PaymentType',on_delete  = models.CASCADE, primary_key = True,)
    member_id       = models.ForeignKey('Member',on_delete  = models.CASCADE, primary_key = True,)
    payments_status = models.OneToOneField('PaymentStatus', on_delete=models.CASCADE, primary_key=True,)
    class Meta:
        db_table = 'payments'

class PaymentType(models.Model):
    name    = models.CharField(max_length=45)
    member  = models.ManyToManyField('Member', through='Payment')
    class Meta:
        db_table = 'paymenttypes'

class PaymentStatus(models.Model):
    name = models.CharField(max_length=45)
    class Meta:
        db_table = 'paymentstatuses'

