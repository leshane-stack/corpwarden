from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from warden.sitemaps import CompanySitemap, EventSitemap, StaticSitemap
from warden.views import robots_txt

sitemaps = {
    'companies': CompanySitemap,
    'events': EventSitemap,
    'static': StaticSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('robots.txt', robots_txt, name='robots_txt'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('', include('warden.urls')),
]
