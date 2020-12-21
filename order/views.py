import json

from django.views     import View
from django.http      import JsonResponse
 
from .models        import Order, Address, OrderStatus, Cart, Payment, PaymentType, PaymentStatus
from user.models    import Member
from product.models import Product


class CartView(View): #quantity만 업데이트할 수 있게 하고 나머지는 productview로 이동
    def post(self, request):
        data             = json.loads(request.body)
        #user = User.objects.get(id=request.user.id) 
        # order_status_ins = OrderStatus.objects.only('id').get(name='오더 전')
        # address_ins      = Address.objects.only('id').get(id=1)  #address가 없는 id로 설정
        # member_ins       = Member.objects.only('id').get(id=1)   #데코레이터 써야함
        # payment_ins      = Payment.objects.only('id').get(id=1)  #payment가없는 id로 설정
        # Order.objects.create(order_number=1, order_status=order_status_ins, address=address_ins, member=member_ins, delivery_message='', order_date=00000, payments=payment_ins)
        
        order_ins   = Order.objects.only('id').latest('id')  
        product_ins = Product.objects.only('id').get(id=117)    #데코레이터 써야할 듯...?
        price_ins   = Product.objects.only('price').get(id=117) #데코레이터 써야할 듯...?
        Cart.objects.create(quantity=data["quantity"], created_at=00000, product=product_ins, total_price=price_ins, order=order_ins) 
        
        return JsonResponse({'message' : 'OK'}, status = 200)

#     def get(self, request):
#             return JsonResponse({'message' : 'OK'}, status = 200)


# class OrderView(View):
#     def post(self, request):
#         Order.objects.create() # --> I think this needs to be update 

#         return JsonResponse({'message' : 'OK'}, status = 200)


