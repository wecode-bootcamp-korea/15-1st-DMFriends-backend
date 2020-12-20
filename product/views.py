import json

from django.views     import View
from django.http      import JsonResponse
from django.shortcuts import render
 
from .models  import Category, Subcategory, Product, ProductImage, Discount, Review
from user.models import Member

class ProductView(View):
    def get(self, request, id):
        try:
            if Product.objects.filter(id=id) == "": #아무것도 반환하지 않을때 조건을 어떻게 명시해야하나
                raise ValueError
            product_list =  list(Product.objects.filter(id=id).values())
            return JsonResponse({"message" : "SUCCESS", "result" : product_list}, status = 200) #리스트로 반환되는데 괜찮은건가
        except ValueError:
            return JsonResponse({'message' : 'ObjectDoesNotExist'}, status = 400)
#한국어 인코딩이 안됨

class CategoryView(View):
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
    def post(self, request):
        data        = json.loads(request.body)
        
        product_ins = Product.objects.only('id').get(id=data["product"])
        member_ins  = Member.objects.only('id').get(id=data["member"])
        Review.objects.create(star_rating=data['star_rating'], created_at=data['created_at'] , product=product_ins, member=member_ins, content = data['content']) 

        return JsonResponse({"message" : "SUCCESS", "result" : data}, status = 200)