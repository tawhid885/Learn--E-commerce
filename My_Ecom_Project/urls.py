from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('App_Shop.urls', namespace='App_Shop')),
    path('account/',include('App_Login.urls', namespace='App_login')),
    path('shop/',include('App_Order.urls', namespace='App_Order')),
    path('payment/',include('App_Payment.urls', namespace='App_Payment')),
]


#To Show Media File

from django.conf import settings
from django.contrib.staticfiles.urls import static,staticfiles_urlpatterns

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

