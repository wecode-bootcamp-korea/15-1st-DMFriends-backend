from django.urls   import path
from order.views import AddToCartView, CartView  #OrderView

urlpatterns = [path('/addtocart', AddToCartView.as_view()),
               path('/cart',      CartView.as_view()),
            #    path('/order',     OrderView.as_view()),
]