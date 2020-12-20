from django.urls   import path
from product.views import ProductView, ReviewView, CategoryView

urlpatterns = [path('product/<int:id>', ProductView.as_view()),
               path('product/category', CategoryView.as_view()),
               path('product/<int:id>/review', ReviewView.as_view()),
]