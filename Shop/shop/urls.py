from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "shop"

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('create_product/', views.create_product, name='create_product'),
    path('update_product/', views.update_product, name='update_product'),
    path('favotite_list/', views.favorite_list, name='favorite_list'),
    path('add_favorite/<int:product_id>/', views.add_favorite, name='add_favorite'),
    path('remove_favorite/<int:product_id>/', views.remove_favorite, name='remove_favorite'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
