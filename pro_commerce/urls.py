from django.urls import path
import pro_commerce.views
from pro_commerce.views import custom_404_view
from django.conf.urls.static import static
from django.conf import settings
handler404 = custom_404_view

app_name="pro_commerce"
urlpatterns = [
    path('',pro_commerce.views.homepage,name='homepage'),

    path('details/product/<int:product_id>/',pro_commerce.views.detail,name='product_detail'),

    path('contact',pro_commerce.views.contacts,name='contact'),
    path('apropos',pro_commerce.views.about,name='apropos'),
    path('categorie/<slug:category_slug>/', pro_commerce.views.products_by_category, name='products_by_category'),

    # path('category/<int:category_id>/', pro_commerce.views.products_by_category, name='products_by_category'),
    # path('subcategory/<int:subcategory_id>/', pro_commerce.views.products_by_subcategory, name='products_by_subcategory'),
    path('sous-categorie/<slug:subcategory_slug>/', pro_commerce.views.products_by_subcategory, name='products_by_subcategory'),

]
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL,
#                           document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
