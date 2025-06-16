"""Opera_CTN URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import debug_toolbar
from django.contrib import admin
from django.conf import settings
from django.urls import path,include,re_path
from django.conf.urls.static import static
from django.views.static import serve
from ctn_bpf import views

from django.conf.urls.i18n import i18n_patterns
from ctn_bpf.urls import (
    ajax_urls_patterns,
    gestionnaire_url_patterns,
    save_url_patterns,
    filter_urls,
    log_urls,
)
# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import StructureViewSet

# router = DefaultRouter()
# router.register(r'structures', StructureViewSet)
"""
from webpages import views
handler404 = views.error_404
handler500 = views.error_500
"""
urlpatterns = [
    path('', include('ctn_bpf.urls')),
    path('website/', include('websites.urls')),
    path('BeinInfo/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
    path('ajax/', include(ajax_urls_patterns)),
    path('gestionnaire/', include(gestionnaire_url_patterns)),
    path('save/', include(save_url_patterns)),
    path('filter/', include(filter_urls)),
    path('log/', include(log_urls)),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT,}),]
urlpatterns += [re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT,}),]

handler404 = views.error_404
handler500 = views.error_500
