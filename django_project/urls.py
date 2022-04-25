from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
import web.urls
import api.urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api.urls)),
    path('', include(web.urls)),
]
