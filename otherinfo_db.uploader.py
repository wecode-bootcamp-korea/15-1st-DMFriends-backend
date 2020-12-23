import os
import django
import csv
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dmfriends.settings")
django.setup()

from order.models import Payment, PaymentStatus, PaymentType, Address, OrderStatus
from user.models import Member

a1 = PaymentStatus(name="결제 진행 전")
a2 = PaymentStatus(name="결제 진행 중")
a3 = PaymentStatus(name="결제 완료")
a4 = PaymentStatus(name="결제 취소")
PaymentStatus.objects.bulk_create([a1, a2, a3, a4])

a1 = PaymentType(name="카카오페이")
a2 = PaymentType(name="무통장입금")
a3 = PaymentType(name="N/A")
PaymentType.objects.bulk_create([a1, a2, a3])

Address.objects.create(address = 'justforcart', detail_address = '', default = 0, created_at = 201023)
Member.objects.create(email = '', nickname = '', privacy_agreement = 1, anonymous = 0, random_number = 0, password = '')

member_ins = Member.objects.only('id').get(id=1)
paymentstatus_ins = PaymentStatus.objects.only('id').get(name="결제 진행 전")
paymenttype_ins = PaymentType.objects.only('id').get(name="N/A")
Payment.objects.create(kakao_pay='justforcart', virtual_account='justforcart', member=member_ins, payment_status=paymentstatus_ins, payment_type=paymenttype_ins)

a1 = OrderStatus(name="오더 전")
a2 = OrderStatus(name="오더 진행 중")
a3 = OrderStatus(name="오더 완료")
a4 = OrderStatus(name="오더 취소")

OrderStatus.objects.bulk_create([a1, a2, a3])

