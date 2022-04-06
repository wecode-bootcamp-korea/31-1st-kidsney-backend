from django.urls import path

from .views import SignUpView, SignInView, WishListView, PostWishView

urlpatterns = [
    path('/signup', SignUpView.as_view()),
    path('/signin', SignInView.as_view()),
    path('/wishlist', WishListView.as_view()),
    path('/wishlist/<int:product_id>', PostWishView.as_view()),
]