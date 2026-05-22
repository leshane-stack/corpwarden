from django.core.management.base import BaseCommand
from datetime import date
from decimal import Decimal
from warden.models import (
    Industry, Company, AccountabilityEvent, DataSource, SnapshotStat
)


class Command(BaseCommand):
    help = 'Seed Amazon accountability data'

    def handle(self, *args, **kwargs):
        # Industry
        industry, _ = Industry.objects.get_or_create(
            slug='ecommerce-logistics',
            defaults={'name': 'E-commerce & Logistics'}
        )

        # Company
        company, _ = Company.objects.get_or_create(
            slug='amazon',
            defaults={
                'name': 'Amazon',
                'legal_name': 'Amazon.com Services LLC',
                'industry': industry,
                'description': 'Global e-commerce and cloud computing company. Second-largest private employer in the United States.',
                'employee_count': 1500000,
                'headquarters': 'Seattle, WA',
                'stock_ticker': 'AMZN',
                'website': 'https://www.amazon.com',
                'risk_level': 'elevated',
                'summary_line': 'Persistent pattern of OSHA enforcement actions across warehouse facilities. Injury rates significantly above industry average. Subject to the first major multi-site OSHA investigation in over a decade.',
            }
        )

        # Snapshot Stats
        stats = [
            {
                'label': 'OSHA facilities investigated',
                'value': '10+',
                'context': 'Multi-site investigation began summer 2022',
                'source_url': 'https://www.osha.gov/news/newsreleases/osha-national-news-release/20241219',
                'sort_order': 1,
            },
            {
                'label': 'Warehouse injury rate vs industry',
                'value': '75%',
                'context': 'Higher than non-Amazon warehouses (2023 OSHA data)',
                'source_url': '',
                'sort_order': 2,
            },
            {
                'label': 'Serious injury rate vs industry',
                'value': '2x',
                'context': 'More than twice non-Amazon warehouse average',
                'source_url': '',
                'sort_order': 3,
            },
            {
                'label': 'Corporate-wide OSHA settlement',
                'value': '$145K',
                'context': 'Dec 2024 — ergonomic measures required nationwide',
                'source_url': 'https://www.osha.gov/news/newsreleases/osha-national-news-release/20241219',
                'sort_order': 4,
            },
        ]

        for s in stats:
            SnapshotStat.objects.get_or_create(
                company=company,
                label=s['label'],
                defaults=s
            )

        # Accountability Events
        events = [
            {
                'date': date(2025, 7, 10),
                'title': 'California Labor Commissioner cites Amazon $5.9M for warehouse labor violations',
                'description': 'Amazon.com Services LLC cited for violating California\'s Warehouse Worker Protection Act (AB 701) at two Inland Empire facilities (ONT8 and ONT9). Penalties of $1.2M at ONT9 and $4.7M at ONT8.',
                'domain': 'workplace',
                'severity': 'critical',
                'source_agency': 'California Labor Commissioner',
                'source_url': 'https://warehouseworkers.org/amazon-cited-for-labor-violations/',
                'penalty_amount': Decimal('5900000'),
                'facility_location': 'Ontario, CA (Inland Empire)',
            },
            {
                'date': date(2024, 12, 19),
                'title': 'OSHA reaches corporate-wide settlement requiring ergonomic measures at all facilities',
                'description': 'Settlement resolves 10 cases across facilities in NY, FL, ID, PA, CO, IL, and NJ. Amazon required to conduct ergonomic risk assessments, implement engineering controls, and allow OSHA access for two years. First major multi-site OSHA settlement in over a decade.',
                'domain': 'workplace',
                'severity': 'serious',
                'source_agency': 'OSHA / Dept of Labor',
                'source_url': 'https://www.osha.gov/news/newsreleases/osha-national-news-release/20241219',
                'penalty_amount': Decimal('145000'),
                'facility_location': 'Corporate-wide (7 states)',
            },
            {
                'date': date(2023, 6, 25),
                'title': 'OSHA cites Amazon for 14 recordkeeping violations at six facilities',
                'description': 'Citations for failing to properly record work-related injuries and illnesses at warehouses in FL, IL, NY, CO, and ID. Violations included misclassifying injuries, failing to record within required timeframes, and not providing timely records to OSHA.',
                'domain': 'workplace',
                'severity': 'serious',
                'source_agency': 'OSHA',
                'source_url': 'https://www.staffingindustry.com/news/global-daily-news/osha-cites-amazon-record-keeping-violations',
                'penalty_amount': Decimal('29008'),
                'facility_location': 'FL, IL, NY, CO, ID',
            },
            {
                'date': date(2023, 2, 23),
                'title': 'OSHA cites Amazon Colorado Springs facility — 7th location found ignoring known hazards',
                'description': 'Delivery station processing 5,000-10,000 packages per hour cited for exposing workers to ergonomic hazards. Inspection initiated after employee complaint of musculoskeletal disorders and blocked fire exits.',
                'domain': 'workplace',
                'severity': 'serious',
                'source_agency': 'OSHA / Dept of Labor',
                'source_url': 'https://www.dol.gov/newsroom/releases/osha/osha20230223-0',
                'penalty_amount': Decimal('15625'),
                'facility_location': 'Colorado Springs, CO',
            },
            {
                'date': date(2023, 1, 18),
                'title': 'OSHA cites Amazon at three facilities following US Attorney referrals',
                'description': 'Citations issued for serious violations of the OSH Act at facilities in New Windsor, NY; Waukegan, IL; and Deltona, FL. Referrals came from US Attorney\'s Office for the Southern District of New York. Workers exposed to ergonomic hazards from high-frequency lifting, heavy weights, and awkward postures. Deltona facility also cited for struck-by hazards.',
                'domain': 'workplace',
                'severity': 'critical',
                'source_agency': 'OSHA / DOJ (SDNY)',
                'source_url': 'https://www.justice.gov/usao-sdny/pr/amazon-cited-osha-based-sdny-referrals-serious-violations-exposed-workers-safety',
                'penalty_amount': None,
                'facility_location': 'New Windsor, NY; Waukegan, IL; Deltona, FL',
            },
            {
                'date': date(2022, 7, 1),
                'title': 'OSHA opens multi-site investigation across 10 Amazon facilities',
                'description': 'Federal workplace safety regulators launch first major multi-site investigation in over a decade, targeting ergonomic hazards and injury rates at Amazon warehouse operations across the country.',
                'domain': 'workplace',
                'severity': 'serious',
                'source_agency': 'OSHA',
                'source_url': 'https://www.osha.gov/news/newsreleases/osha-national-news-release/20241219',
                'penalty_amount': None,
                'facility_location': 'Multiple states',
            },
        ]

        for e in events:
            AccountabilityEvent.objects.get_or_create(
                company=company,
                date=e['date'],
                title=e['title'],
                defaults=e
            )

        # Data Sources
        sources = [
            {
                'source_name': 'OSHA Inspections & Citations',
                'source_agency': 'Dept of Labor / OSHA',
                'source_url': 'https://www.osha.gov/ords/imis/establishment.html',
                'last_checked': date(2025, 5, 22),
            },
            {
                'source_name': 'DOL News Releases',
                'source_agency': 'Dept of Labor',
                'source_url': 'https://www.dol.gov/newsroom/releases',
                'last_checked': date(2025, 5, 22),
            },
            {
                'source_name': 'DOJ Press Releases (SDNY)',
                'source_agency': 'Dept of Justice',
                'source_url': 'https://www.justice.gov/usao-sdny',
                'last_checked': date(2025, 5, 22),
            },
            {
                'source_name': 'California Labor Commissioner Citations',
                'source_agency': 'California DLSE',
                'source_url': 'https://www.dir.ca.gov/dlse/',
                'last_checked': date(2025, 5, 22),
            },
        ]

        for s in sources:
            DataSource.objects.get_or_create(
                company=company,
                source_name=s['source_name'],
                defaults=s
            )

        self.stdout.write(self.style.SUCCESS(
            f'Seeded Amazon: {company.events.count()} events, '
            f'{company.snapshot_stats.count()} stats, '
            f'{company.data_sources.count()} sources'
        ))
