from django.urls   import path
from product.views import ProductView, ReviewView, CategoryView

urlpatterns = [path('/detail/<int:product_id>', ProductView.as_view()),
               path('product/category', CategoryView.as_view()),
               path('product/<int:id>/review', ReviewView.as_view()),
]
