import json
import decimal

from django.views  import View
from django.http   import JsonResponse
from django.db.models import Q
 
from .models      import  (
    Category,
    Subcategory, 
    Product, 
    ProductImage, 
    Discount, 
    Review
)

from user.models  import Member #login_decorator


class ProductListView(View):
    def get(self, request):
            category_seq    = request.GET.get('category', None)
            subcategory_seq = request.GET.get('subcategory', None)
            sort            = request.GET.get('sort', None)

            products = Product.objects.filter(Q(category=category_seq) | Q (subcategory=subcategory_seq), id__range=(1,40)).order_by(sort).values()
            
            filtered_products = [{
                "id"            : item["id"],
                "name"          : item["name"],
                "price"         : int(item["price"]),
                "star_rating"   : item["star_rating"],
                "description"   : item["description"],
                "category_id"   : item["category_id"],
                "subcategory_id": item["subcategory_id"],
                "discount_id"   : item["discount_id"],
                "image_url"     : list(ProductImage.objects.filter(product_id = item["id"]).values_list('image_url', flat=True)),
                "created_at"    : item["created_at"],
            }for item in products]

            return JsonResponse({"message" : "SUCCESS", "result" : filtered_products}, status = 200)
            
class ProductDetailView(View):
    def get(self, request, product_id):
            if Product.objects.filter(id=product_id).exists():
                products =  Product.objects.filter(id=product_id).values()

                product_list = [{
                    "id"            : item["id"],
                    "name"          : item["name"],
                    "price"         : item["price"],
                    "star_rating"   : item["star_rating"],
                    "description"   : item["description"],
                    "category_id"   : item["category_id"],
                    "subcategory_id": item["subcategory_id"],
                    "discount_id"   : item["discount_id"],
                    "image_url"     : item["image_url"],
                    "created_at"    : item["created_at"],
                    "images_slider" : list(ProductImage.objects.filter(product_id = item["id"]).values_list('image_url', flat=True))
                }for item in products]            
                
                return JsonResponse({"result" : product_list}, status = 200)
            return JsonResponse({"message" : "PRODUCT_DOES_NOT_EXIST"}, status=404)
#한국어 인코딩이 안됨

class ReviewView(View):
    #@login_decorator
    def post(self, request, product_id):
        data = json.loads(request.body)
        member_ins = Member.objects.get(id=request.user.id)

        if Product.objects.filter(id=product_id).exists():
            member_ins = Member.objects.get(id=member_ins) 
            Review.objects.create(star_rating=data['star_rating'], created_at=data['created_at'] , product=product_id, member=member_ins, content = data['content']) 

        return JsonResponse({"message" : "SUCCESS", "result" : data}, status = 200)
