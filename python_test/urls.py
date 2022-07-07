from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('calendar/', include('calendar.urls')),
    path('rest/v1/calendar/', include('calender.urls')),
]
