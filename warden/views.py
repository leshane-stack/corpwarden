from django.shortcuts import render, get_object_or_404
from .models import Company, AccountabilityEvent


def home(request):
    companies = Company.objects.filter(events__isnull=False).distinct().order_by('name')
    recent_events = AccountabilityEvent.objects.select_related('company').order_by("-date")[:5]
    return render(request, 'warden/home.html', {
        'companies': companies,
        'recent_events': recent_events,
    })


def company_detail(request, slug):
    company = get_object_or_404(Company, slug=slug)
    events = company.events.all()
    stats = company.snapshot_stats.all()
    sources = company.data_sources.all()
    return render(request, 'warden/company_detail.html', {
        'company': company,
        'events': events,
        'stats': stats,
        'sources': sources,
    })


def event_detail(request, slug, event_id):
    company = get_object_or_404(Company, slug=slug)
    event = get_object_or_404(AccountabilityEvent, id=event_id, company=company)
    related_events = company.events.exclude(id=event.id)[:5]
    return render(request, 'warden/event_detail.html', {
        'company': company,
        'event': event,
        'related_events': related_events,
    })

from django.http import HttpResponse

def robots_txt(request):
    lines = [
        "User-agent: *",
        "Allow: /",
        "Sitemap: https://www.corpwarden.com/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
