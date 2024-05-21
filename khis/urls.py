from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('khis/account/', include("account.urls")),
    path('khis/schedule/', include("schedule.urls")),
    path('khis/appointment/', include("appointment.urls")),
    path('khis/patient-registration/', include("registration.urls")),
    path('khis/consultations/', include("ocs.urls")),
]
