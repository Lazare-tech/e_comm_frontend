from django.urls import path
import pro_commerce.views
from django.conf.urls.static import static
from django.conf import settings

app_name="pro_commerce"
urlpatterns = [
    path('',pro_commerce.views.homepage,name='homepage'),
    path('details',pro_commerce.views.detail,name='detail'),
    path('contact',pro_commerce.views.contacts,name='contact'),
    path('apropos',pro_commerce.views.about,name='apropos')
]
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL,
#                           document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
