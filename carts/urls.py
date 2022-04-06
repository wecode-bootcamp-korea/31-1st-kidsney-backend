from django.urls import path

from .views import CartView, UpdateCartView

urlpatterns = [
    path('', CartView.as_view()),
    path('/products/<int:product_id>', CartView.as_view()),
    path('/<int:cart_id>', UpdateCartView.as_view()),
] 