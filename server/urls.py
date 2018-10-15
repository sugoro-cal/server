from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from . import settings
from app.views import index


urlpatterns = [
    path('', index, name='index'),
    path('app/', include("app.urls")),
    path('auth/', include("django.contrib.auth.urls")),
    path('auth/', include("signup.urls")),
    path('profile/', include("users.urls")),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
