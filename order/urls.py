from django.urls   import path
from order.views import CartView, CartModifyView

urlpatterns = [path('/cart',                  CartView.as_view()),
               path('/cart/<int:cart_id>', CartModifyView.as_view()),
               ]