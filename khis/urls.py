from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('khis/account/', include("account.urls")),
    path('khis/schedule/', include("schedule.urls")),
    path('khis/appointment/', include("appointment.urls")),
    path('khis/patient-registration/', include("registration.urls")),
    path('khis/practitioner-registration/',
         include("practitioner_registration.urls")),
    path('khis/consultations/', include("ocs.urls")),
    path('khis/patient/', include("patient.urls")),
    path('khis/procedure/', include("procedure.urls")),
    path('khis/procedure-fee/', include("procedure_fee.urls")),
    path('khis/chat/', include("chat.urls")),
]
