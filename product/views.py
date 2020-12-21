import json

from django.views     import View
from django.http      import JsonResponse
 
from .models     import  (
    Category,
    Subcategory, 
    Product, 
    ProductImage, 
    Discount, 
    Review
)
from user.models import Member, login_decorator

class ProductDetailView(View):
    def get(self, request, product_id):
            if Product.objects.filter(id=product_id).exists():
                product =  list(Product.objects.filter(id=product_id).values())
                return JsonResponse({"result" : product_list}, status = 200)
            return JsonResponse({"message" : "PRODUCT_DOES_NOT_EXIST"}, status=404)
#한국어 인코딩이 안됨

    def get(self, request):
            category_seq    = request.GET.get('category', None)
            subcategory_seq = request.GET.get('subcategory', None)
            sort            = request.GET.get('sort', None)

            if subcategory_seq == None:
                product_list =  list(Product.objects.filter(category=category_seq).order_by(sort).values())
            else:
                product_list =  list(Product.objects.filter(category=category_seq, subcategory=subcategory_seq).order_by(sort).values())

            return JsonResponse({"message" : "SUCCESS", "result" : product_list}, status = 200)

class ReviewView(View):
    @login_decorator #데코레이터가 user앱에 있어서 머지되었다는 가정하에 코드를 짰습니다.
    def post(self, request, id):
        data        = json.loads(request.body)
        
        if Product.objects.filter(id=product_id).exists():
            member_ins = Member.objects.get(id=request.user.id) 
            Review.objects.create(star_rating=data['star_rating'], created_at=data['created_at'] , product=product_id, member=member_ins, content = data['content']) 

        return JsonResponse({"message" : "SUCCESS", "result" : data}, status = 200)
