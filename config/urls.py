from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('', include('apps.trips.urls')),
    path('auth/', include('apps.accounts.urls')),
    path('agency/', include('apps.agency.urls')),
    path('bookings/', include('apps.bookings.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
    path('api/v1/', include('apps.trips.api_urls')),
    path('api/v1/auth/token/', obtain_auth_token, name='api_token_auth'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = 'apps.accounts.views.error_404'
handler500 = 'apps.accounts.views.error_500'
