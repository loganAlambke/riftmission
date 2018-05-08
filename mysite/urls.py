from django.contrib import admin
from django.urls import path, include

urlpatterns = [
	path('rift_missions/', include('rift_missions.urls')),
    path('admin/', admin.site.urls),
]
