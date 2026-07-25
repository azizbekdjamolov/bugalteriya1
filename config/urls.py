from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('moliya/', include('finance.urls')),
    path('kontragentlar/', include('parties.urls')),
    path('xodimlar/', include('hr.urls')),
    path('ombor/', include('warehouse.urls')),
    path('hujjatlar/', include('documents.urls')),
    path('hisobotlar/', include('reports.urls')),
    path('bildirishnomalar/', include('notifications.urls')),
    path('accounts/', include('accounts.urls')),
    path('api/token/', include('accounts.api_urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
