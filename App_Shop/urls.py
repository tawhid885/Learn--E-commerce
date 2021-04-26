from django.urls import path
from .views import Home,ProductDetail

app_name="App_Shop"

urlpatterns = [
    path('', Home.as_view(), name ='home'),
    path('product/<pk>/', ProductDetail.as_view(), name ='product_detail'),
]