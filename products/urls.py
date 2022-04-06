from django.urls import path

from .views import MainProductView, ProductDetailView

urlpatterns = [
    path('', MainProductView.as_view()),
    path('/<int:product_id>', ProductDetailView.as_view())
]