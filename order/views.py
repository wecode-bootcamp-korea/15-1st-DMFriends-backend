import json

from django.views     import View
from django.http      import JsonResponse
 
from .models        import (
    Order, 
    Address, 
    OrderStatus, 
    Cart, 
    Payment, 
    PaymentType, 
    PaymentStatus
)
from user.models    import Member
from product.models import Product, ProductImage
from order.models   import PaymentStatus

import random

from user.utils     import login_decorator, login_check

class CartView(View):
    #@login_decorator
    def get(self, request):
        cart = Cart.objects.all()
        result = [{
            "id"            : item.product.id,
            "name"          : item.product.name,
            "price"         : int(item.product.price),
            "quantity"      : item.quantity,
            "discount_id"   : item.product.discount_id,
            "image_url"     : item.product.productimage_set.first().image_url
        }for item in cart]

        return JsonResponse({"message" : "SUCCESS", "result" : result}, status = 200)
    
    @login_decorator
    def post(self, request):

        ORDER_STATUS_ID = 1

        data = json.loads(request.body)
            
        payment_ins, created = Payment.objects.get_or_create(
            member   = request.user,
            defaults = {
                'kakao_pay'      : 'justforcart', 
                'virtual_account': 'justforcart', 
                'payment_status' : PaymentStatus.objects.get(id=1), 
                'payment_type'   : PaymentType.objects.get(id=3)
            }
        )
        order_ins, created = Order.objects.get_or_create(       
            order_status_id = ORDER_STATUS_ID,
            member          = request.user, 
            defaults     = {
                'order_number'     : random.randint(100, 999),
                'address'          : Address.objects.get(address="justforcart"),
                
                'delivery_message' : '',
                'payments'         : payment_ins
                },
        )

        if order_ins.cart_set.filter(product_id=data['product_id']).exists():
            cart = Cart.objects.get(order=order_ins, product_id= data['product_id'])
            cart.quantity += 1
            cart.total_price = cart.product.price * int(cart.quantity)
            cart.save()

            return JsonResponse({"message" : "SUCCESS"}, status = 200)
        product_ins = Product.objects.get(id=data["product_id"])
        price_ins   = product_ins.price
        
        Cart.objects.create(quantity=data["quantity"], created_at=00000, product=product_ins, total_price=price_ins, order=order_ins)             
        
        return JsonResponse({"message" : "SUCCESS"}, status = 200)
    
    @login_decorator
    def delete(self, request):
        product_ids = request.GET.getlist('product_id', None)
        for id in product_ids:
            Cart.objects.filter(product_id=id).delete()
        return JsonResponse({"message" : "SUCCESS"}, status = 200)

class CartModifyView(View):

    @login_decorator
    def post(self, request, cart_id): 
        data = json.loads(request.body)

        cart = Cart.objects.get(id= cart_id)
        cart.quantity = data["quantity"]
        cart.total_price = cart.product.price * int(data["quantity"])
        cart.save()

        return JsonResponse({'message' : 'SUCCESS'}, status = 200)

    @login_decorator
    def delete(self, request, cart_id): #장바구니에서 직접 삭제하기 (Path parameter)
        data = json.loads(request.body)        
        order_ins = Order.objects.get(member_id=request.user)
        cart_product=order_ins.cart_set.filter(product_id=data['product_id'])
        cart_product.delete()
        return JsonResponse({'message':'DELETE'})
