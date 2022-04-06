from django.urls import path

from .views import GetCartView, PostCartView, UpdateCartView

urlpatterns = [
    path('', GetCartView.as_view()),
    path('/<int:product_id>', PostCartView.as_view()),
    path('/update/<int:cart_id>', UpdateCartView.as_view()),
] 