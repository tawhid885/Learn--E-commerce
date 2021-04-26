from django.urls import path

from .views import add_to_card, cart_view, remove_from_cart, increase_cart, decrease_cart

app_name = 'App_Order'


urlpatterns = [ 
    path('add/<int:pk>/', add_to_card, name="add"),
    path('cart/', cart_view, name="cart"),
    path('remove/<int:pk>/', remove_from_cart, name="remove"),
    path('increase/<int:pk>/', increase_cart, name="increase"),
    path('decrease/<int:pk>/', decrease_cart, name="decrease"),
]