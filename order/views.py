import json

from django.views     import View
from django.http      import JsonResponse
 
from .models        import Order, Address, OrderStatus, Cart, Payment, PaymentType, PaymentStatus
from user.models    import Member
from product.models import Product


class AddToCartView(View):
    #@login_decorator
    def post(self, request):
        data = json.loads(request.body)

        if Cart.objects.filter(product_id=data["product_id"]).exists():
            quantity = Cart.objects.filter(product_id=data["product_id"]).values_list("quantity", flat=True)[0]
            quantity += 1
            total_price = quantity*Product.objects.filter(id=data["product_id"]).values_list("price", flat=True)[0]
            Cart.objects.filter().update(quantity=quantity, total_price=total_price)
            return JsonResponse({"message" : "SUCCESS", "result" : '장바구니에 같은 상품이 추가되었습니다'}, status = 200)

        else:
            member_ins       = Member.objects.get(id=1) #임시로 1번!
            order_status_ins = OrderStatus.objects.only('id').get(name='오더 전')
            address_ins      = Address.objects.only('id').get(address='justforcart')
            payment_ins      = Payment.objects.only('id').get(kakao_pay='justforcart', id=1) 
            Order.objects.create(order_number=1, order_status=order_status_ins, address=address_ins, member=member_ins, delivery_message='', order_date=00000, payments=payment_ins)
            
            order_ins   = Order.objects.only('id').latest('id')  
            product_ins = Product.objects.only('id').get(id=data["product_id"])
            total_price = int(data["quantity"])*Product.objects.filter(id=data["product_id"]).values_list("price", flat=True)[0]

            Cart.objects.create(quantity=data["quantity"], created_at=00000, product=product_ins, total_price=total_price, order=order_ins) 
            return JsonResponse({"message" : "SUCCESS", "result" : '장바구니에 상품이 담겼습니다'}, status = 200)

class CartView(View):
    def post(self, request):
        data = json.loads(request.body)

        if data["delete"] == True:
            Cart.objects.filter(product_id=data["product_id"]).delete()
            return JsonResponse({'message' : 'SUCCESS', "result" : '장바구니에서 상품을 삭제했습니다'}, status = 200)
            


        total_price = int(data["quantity"])*Product.objects.filter(id=data["product_id"]).values_list("price", flat=True)[0]
        Cart.objects.filter(product_id=data["product_id"]).update(quantity=data["quantity"], total_price=total_price)        
        return JsonResponse({'message' : 'SUCCESS', "result" : '장바구니에서 상품의 갯수가 변경되었습니다'}, status = 200)

# 결제창은 추가구현사항으로 프론트와 상의했습니다!
# class OrderView(View):
#     def post(self, request):
#         data = json.loads(request.body)
#         member_ins = Member.objects.get(id=1) #임시로 1번!

#         Cart.objects.filter(product_id=data["product_id"]).update(quantity=data["quantity"], total_price=3000)
        
#         if data["address"]:
#             Address.objects.create(address=data["address"], detail_address=data["detail_address"], default=data["default"], member_id=member_ins, created_at=000000)
#             address_ins = Address.objects.only('id').latest('id')  
#         paymentstatus_ins = PaymentStatus.objects.get(id=2)

#         Payment.objects.update(payment_status=paymentstatus_ins, )
#         Order.objects.update(delivery_message=data["delivery_message"],order_date=000000, address=address_ins, member=member_ins, order_status=, payments=)
#         return JsonResponse({'message' : 'OK'}, status = 200)


