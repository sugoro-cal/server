from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from . import settings
from app.views import index, explain


urlpatterns = [
    path('', index, name='index'),
    path('explain/', explain, name='explain'),
    path('app/', include("app.urls")),
    path('accounts/', include("django.contrib.auth.urls")),
    path('accounts/', include("signup.urls")),
    path('profile/', include("users.urls")),
]

handler404 = 'app.views.error_404'

if settings.DEBUG:
    urlpatterns += [path('admin/', admin.site.urls)]
    import debug_toolbar
    urlpatterns += [path('', include(debug_toolbar.urls))]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
