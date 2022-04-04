from django.urls import path

from .views import MainProductView

urlpatterns = [
    path('', MainProductView.as_view()),
]