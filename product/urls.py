from django.urls   import path
from product.views import ProductDetailView, ReviewView, ProductListView

urlpatterns = [path('/detail/<int:product_id>', ProductDetailView.as_view()),
               path('/category/<str:type>', ProductListView.as_view()),
               path('/<int:product_id>/review', ReviewView.as_view()),
]