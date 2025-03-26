from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings
from django.views.static import serve


urlpatterns = [
    path('admin/', admin.site.urls),
    path('summernote/', include('django_summernote.urls')),
    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.jwt')),
    re_path(r'^auth/', include('djoser.social.urls')),
    path('core/', include('core.urls')),

    path('accounts/', include('apps.platform.accounts.urls')),
    path('', include('apps.platform.workspace.urls'))
]


urlpatterns += [re_path(r'^i18n/', include('django.conf.urls.i18n'))]
urlpatterns += [re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})]
urlpatterns += [re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT})]
