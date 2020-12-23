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
        order_status_id = OrderStatus.objects.get(id=1)
        order_ins, created = Order.objects.get_or_create(       
            order_status_id = order_status_id,
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

            return JsonResponse({"message" : "SUCCESS"}, status = 200)
        product_ins = Product.objects.get(id=data["product_id"])
        price_ins   = product_ins.price
        
        Cart.objects.create(quantity=data["quantity"], created_at=00000, product=product_ins, total_price=price_ins, order=order_ins)             
        
        return JsonResponse({"message" : "SUCCESS", "result" : '장바구니에 상품이 담겼습니다'}, status = 200)
    
    def delete(self, request):
        product_ids = request.GET.getlist('product_id', None)
        for id in product_ids:
            Cart.objects.filter(product_id=id).delete()
        return JsonResponse({"message" : "SUCCESS"}, status = 200)



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