from django.urls import path
from .views import checkout,payment,complete,purchase,order_view

app_name = "App_Payment"

urlpatterns = [
    path('checkout/',checkout,name = "checkout"),
    path('pay/',payment,name = "payment"),
    path('status/',complete,name = "complete"),
    path('purchase/<val_id>/<tran_id>/',purchase,name = "purchase"),
    path('orders/',order_view,name = "orders"),
]