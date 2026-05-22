from django.contrib.sitemaps import Sitemap
from .models import Company, AccountabilityEvent


class CompanySitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Company.objects.all()

    def location(self, obj):
        return f'/company/{obj.slug}/'

    def lastmod(self, obj):
        return obj.updated_at


class EventSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.6

    def items(self):
        return AccountabilityEvent.objects.all()

    def location(self, obj):
        return f'/company/{obj.company.slug}/event/{obj.id}/'

    def lastmod(self, obj):
        return obj.created_at


class StaticSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 1.0

    def items(self):
        return ['/']

    def location(self, item):
        return item
