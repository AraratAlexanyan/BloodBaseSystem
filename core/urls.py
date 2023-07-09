from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from core import settings

urlpatterns = [

                  path('admin/', admin.site.urls),
                  path('', include('user.urls')),
                  path('', include('blood.urls')),
                  # path("__debug__/", include("debug_toolbar.urls")),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
