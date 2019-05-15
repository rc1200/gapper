from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from django.views.static import serve
from django.conf.urls import url
from . import views
from portfolio.views import IndexView, GalleryView

app_name = 'portfolio'
urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("index2", views.index2, name="index2", ),
    path("index3", views.index3, name="index3"),
    path("gallery", GalleryView.as_view(), name="gallery"),
    path("gallery3", GalleryView.as_view(), name="gallery3"),
    path("thankyou", views.thankyou, name="thankyou"),
    path("myAjax/<str:ticker>", views.myAjax, name="myAjax"),
    path('returnStockData/<str:ticker>', views.returnStockData, name='returnStockData'),
    path('returnStockDataPriceRange/<str:ticker>', views.returnStockDataPriceRange, name='returnStockDataPriceRange'),





    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

