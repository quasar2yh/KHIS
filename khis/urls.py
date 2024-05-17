from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('khis/account/', include("account.urls")),
    path('khis/', include("ocs.urls")),
]