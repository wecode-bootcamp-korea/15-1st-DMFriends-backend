from django.urls   import path
from product.views import ProductView, ReviewView, CategoryView

urlpatterns = [path('/detail/<int:product_id>', ProductView.as_view()),
               path('/category', CategoryView.as_view()),
               path('/<int:product_id>/review', ReviewView.as_view()),
]
