from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('network.urls')),
    path('', include('django_private_chat.urls'))
]
