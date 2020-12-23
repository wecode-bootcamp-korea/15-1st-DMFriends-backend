import json

from django.views     import View
from django.http      import JsonResponse
 
from .models        import Order, Address, OrderStatus, Cart, Payment, PaymentType, PaymentStatus
from user.models    import Member
from product.models import Product, ProductImage
import random
#from user.utils     import login_decorator

def product_list(self, product_id, message):

    cart_single_product   = Cart.objects.get(product_id=product_id)
    product_added = cart_single_product.product

    result = {
        "message"       : message,
        "id"            : product_added.id,
        "name"          : product_added.name,
        "price"         : int(product_added.price),
        "quantity"      : cart_single_product.quantity,
        "discount_id"   : product_added.discount_id,
        "image_url"     : str(ProductImage.objects.filter(product_id = product_added.id).values_list('image_url', flat=True)),
                }
    return result


class CartView(View):
    def get(self, request):
        cart_all_product = Cart.objects.values_list('product_id', flat=True).distinct()
        all_products = [{item: product_list(self, item, '')} for item in cart_all_product]

        return JsonResponse({"message" : "SUCCESS", "result" : all_products}, status = 200)
    
    #@login_decorator
    def post(self, request):
        data = json.loads(request.body)

        order_ins, created = Order.objects.get_or_create(          
            order_status_id = OrderStatus.objects.get(id=1),
            defaults     = {
                'order_number'     : random.randint(100, 999),
                'address'          : Address.objects.get(address="justforcart"),
                'member'           : Member.objects.get(id=1), #임시로 1번!
                'delivery_message' : '', 
                'order_date'       : 00000, 
                'payments'         : Payment.objects.get(kakao_pay="justforcart")
                },
        )

        if order_ins.cart_set.filter(product_id=data['product_id']).exists():
            cart = Cart.objects.get(order=order_ins, product_id= data['product_id'])
            cart.quantity += 1
            cart.total_price = cart.product.price * int(cart.quantity)
            cart.save()

            return JsonResponse({"message" : "SUCCESS", "result" : '장바구니에 동일한 상품이 추가되었습니다'}, status = 200)

        else:
            product_ins = Product.objects.get(id=data["product_id"])
            price_ins   = product_ins.price
            
            Cart.objects.create(quantity=data["quantity"], created_at=00000, product=product_ins, total_price=price_ins, order=order_ins)             
            
            return JsonResponse({"message" : "SUCCESS", "result" : '장바구니에 상품이 담겼습니다'}, status = 200)
    
    def delete(self, request): #장바구니 버튼 누를때 삭제하기 (QuerySet)
        product_id = request.GET.get('product_id', None)
        Cart.objects.filter(product_id=product_id).delete()
        return JsonResponse({"message" : "SUCCESS", "result" : '장바구니에서 상품이 삭제되었습니다'}, status = 200)



class CartModifyView(View):

    #@login_decorator
    def post(self, request, cart_id): 
        data = json.loads(request.body)

        cart = Cart.objects.get(id= cart_id)
        cart.quantity = data["quantity"]
        cart.total_price = cart.product.price * int(data["quantity"])
        cart.save()

        modified_product_info = product_list(self, cart.product_id, "장바구니에서 상품의 갯수가 변경되었습니다")

        return JsonResponse({'message' : 'SUCCESS', "result" : modified_product_info}, status = 200)

    def delete(self, request, cart_id): #장바구니에서 직접 삭제하기 (Path parameter)
        Cart.objects.filter(id=cart_id).delete()
        return JsonResponse({"message" : "SUCCESS", "result" : '장바구니에서 상품이 삭제되었습니다'}, status = 200)






# 결제창은 추가구현사항으로 프론트와 상의했습니다!
# class OrderView(View):
#     def post(self, request):
#        data = json.loads(request.body)
#        member_ins = Member.objects.get(id=1) #임시로 1번!
#         
#        if data["delete"] == True:
#            Cart.objects.filter(product_id=data["product_id"]).delete()
#            return JsonResponse({'message' : 'SUCCESS', "result" : '장바구니에서 상품을 삭제했습니다'}, status = 200)
            
#        total_price = int(data["quantity"])*Product.objects.filter(id=data["product_id"]).values_list("price", flat=True)[0]
#        Cart.objects.filter(product_id=data["product_id"]).update(quantity=data["quantity"], total_price=total_price)        
         
#         Cart.objects.filter(order_id=)
#         order_number_ins = Order.objects()
#         if data["address"]:
#             Address.objects.create(address=data["address"], detail_address=data["detail_address"], default=data["default"], member_id=member_ins, created_at=000000)
#             address_ins = Address.objects.only('id').latest('id')    
#         paymentstatus_ins = PaymentStatus.objects.get(id=2)
#         paymenttype_ins = PaymentType.objects.get(name=data["paymenttype"])
#         Payment.objects.create(member=member_ins, payment_status=paymentstatus_ins, payment_type = paymenttype_ins )
#         payment_ins = Payment.objects.only('id').latest('id')
#         orderstatus_ins = Order.objects.only('id').get(id=2)
#         Order.objects.filter(order_number=order_number_ins).update(delivery_message=data["delivery_message"],order_date=000000, address=address_ins, member=member_ins, order_status=orderstatus_ins, payments=payment_ins)
#         return JsonResponse({'message' : 'OK'}, status = 200)


