from django.core.management.base import BaseCommand
from datetime import date
from decimal import Decimal
from warden.models import (
    Industry, Company, AccountabilityEvent, DataSource, SnapshotStat
)


class Command(BaseCommand):
    help = 'Seed FedEx and UnitedHealthcare'

    def handle(self, *args, **kwargs):
        logistics, _ = Industry.objects.get_or_create(slug='logistics', defaults={'name': 'Freight & Logistics'})
        health, _ = Industry.objects.get_or_create(slug='health-insurance', defaults={'name': 'Health Insurance'})

        # ==================== FEDEX ====================
        fedex, _ = Company.objects.get_or_create(
            slug='fedex',
            defaults={
                'name': 'FedEx',
                'legal_name': 'FedEx Corporation',
                'industry': logistics,
                'description': 'Global shipping and logistics company. Employs approximately 505,000 workers across package delivery, freight, and supply chain operations.',
                'employee_count': 505000,
                'headquarters': 'Memphis, TN',
                'stock_ticker': 'FDX',
                'website': 'https://www.fedex.com',
                'risk_level': 'mixed',
                'summary_line': 'Significant workforce restructuring with 74 WARN notices affecting 9,275 workers since 2001. Major facility closures and layoffs accelerated in 2024-2025 as part of network consolidation. Workforce reduced 7.7% between 2022 and 2024.',
                'pattern_summary': 'Accelerating workforce reductions tied to network consolidation and automation strategy. 23 WARN filings affecting 3,714 workers across 13 states in 2024-2026 alone. Multiple facility closures concentrated in Texas and Tennessee. Shift from B2C e-commerce toward B2B operations contributing to structural job elimination.',
            }
        )

        fedex_stats = [
            {'label': 'WARN notices (2024-2026)', 'value': '23', 'context': 'Affecting 3,714 workers across 13 states', 'sort_order': 1},
            {'label': 'Total WARN notices since 2001', 'value': '74', 'context': 'Affecting 9,275 workers', 'sort_order': 2},
            {'label': 'Workforce reduction (2022-2024)', 'value': '7.7%', 'context': 'From 547,000 to 505,000 employees', 'sort_order': 3},
        ]
        for s in fedex_stats:
            SnapshotStat.objects.get_or_create(company=fedex, label=s['label'], defaults={**s, 'source_url': ''})

        fedex_events = [
            {
                'date': date(2025, 12, 5),
                'title': 'FedEx closes Coppell, TX facility — 856 employees laid off',
                'description': 'FedEx Supply Chain Logistics & Electronics center in Coppell, Texas permanently closed, eliminating all 856 positions. Layoffs implemented in phases beginning January 2026 with full closure in April. Part of broader network restructuring.',
                'domain': 'labor',
                'severity': 'serious',
                'source_agency': 'Texas Workforce Commission / WARN Act',
                'source_url': 'https://www.twc.texas.gov/',
                'penalty_amount': None,
                'facility_location': 'Coppell, TX',
            },
            {
                'date': date(2025, 11, 7),
                'title': 'FedEx announces layoffs at five facilities impacting 843 employees',
                'description': 'WARN Act notices filed for layoffs across five FedEx facilities as part of ongoing network consolidation and operational restructuring.',
                'domain': 'labor',
                'severity': 'serious',
                'source_agency': 'State Labor Departments / WARN Act',
                'source_url': '',
                'penalty_amount': None,
                'facility_location': 'Multiple facilities',
            },
            {
                'date': date(2025, 3, 31),
                'title': 'FedEx files WARN notice for mass layoff at Lebanon, TN facility',
                'description': 'FedEx notified Tennessee Department of Labor & Workforce Development of planned mass layoff at Lebanon facility. Law firm investigating potential WARN Act violations related to notice timing.',
                'domain': 'labor',
                'severity': 'moderate',
                'source_agency': 'Tennessee Dept of Labor',
                'source_url': 'https://www.tn.gov/workforce.html',
                'penalty_amount': None,
                'facility_location': 'Lebanon, TN',
            },
            {
                'date': date(2025, 5, 1),
                'title': 'FedEx lays off 305 employees at Fort Worth supply chain facility',
                'description': 'Over half the workforce at FedEx Supply Chain Logistics and Electronics facility in Fort Worth eliminated. Part of broader operational restructuring targeting technology and supply chain roles.',
                'domain': 'labor',
                'severity': 'moderate',
                'source_agency': 'Texas Workforce Commission / WARN Act',
                'source_url': 'https://www.twc.texas.gov/',
                'penalty_amount': None,
                'facility_location': 'Fort Worth, TX',
            },
            {
                'date': date(2024, 12, 8),
                'title': 'FedEx announces facility closures amid network overhaul',
                'description': 'FedEx disclosed plans for additional facility closures and workforce reductions as part of multi-year network consolidation. Total workforce reduced from 547,000 to approximately 505,000 between 2022 and 2024 — a 7.7% reduction.',
                'domain': 'labor',
                'severity': 'serious',
                'source_agency': 'SEC Filings / Public Announcements',
                'source_url': 'https://www.sec.gov/',
                'penalty_amount': None,
                'facility_location': 'Corporate-wide',
            },
        ]
        for e in fedex_events:
            AccountabilityEvent.objects.get_or_create(company=fedex, date=e['date'], title=e['title'], defaults=e)

        fedex_sources = [
            {'source_name': 'WARN Act Notices', 'source_agency': 'State Labor Departments', 'source_url': 'https://www.warntracker.com/company/fedex', 'last_checked': date(2025, 5, 22)},
            {'source_name': 'OSHA Inspections', 'source_agency': 'Dept of Labor / OSHA', 'source_url': 'https://www.osha.gov/', 'last_checked': date(2025, 5, 22)},
            {'source_name': 'SEC Filings', 'source_agency': 'SEC', 'source_url': 'https://www.sec.gov/', 'last_checked': date(2025, 5, 22)},
        ]
        for s in fedex_sources:
            DataSource.objects.get_or_create(company=fedex, source_name=s['source_name'], defaults=s)

        # ==================== UNITEDHEALTHCARE ====================
        uhc, _ = Company.objects.get_or_create(
            slug='unitedhealth-group',
            defaults={
                'name': 'UnitedHealth Group',
                'legal_name': 'UnitedHealth Group Incorporated',
                'industry': health,
                'description': 'Parent company of UnitedHealthcare, the nation\'s largest health insurer. Operates health insurance, pharmacy benefits (Optum), and care management services.',
                'employee_count': 440000,
                'headquarters': 'Minnetonka, MN',
                'stock_ticker': 'UNH',
                'website': 'https://www.unitedhealthgroup.com',
                'risk_level': 'elevated',
                'summary_line': 'DOL lawsuit and $20.25M settlement over systematic claims denials. Federal class action proceeding over AI algorithm used to deny Medicare Advantage coverage with alleged 90% error rate. Senate investigation found prior authorization denial rate more than doubled after AI deployment.',
                'pattern_summary': 'Escalating regulatory and legal scrutiny over automated claims denial practices. DOL sued subsidiary UMR for systematically denying emergency and drug screening claims without review. Separate class action alleges AI tool nH Predict overrode physician decisions to deny post-acute care to elderly patients. Senate investigation documented denial rate increase from 10.9% to 22.7% after AI implementation. Federal court ordered broad discovery into AI-driven claims processes in March 2025.',
            }
        )

        uhc_stats = [
            {'label': 'DOL settlement (2025)', 'value': '$20.25M', 'context': 'Systematic claims denials by UMR subsidiary', 'sort_order': 1},
            {'label': 'AI denial error rate (alleged)', 'value': '90%', 'context': 'nH Predict algorithm — per class action lawsuit', 'sort_order': 2},
            {'label': 'Prior auth denial rate increase', 'value': '2x', 'context': '10.9% to 22.7% after AI deployment (2020-2022)', 'sort_order': 3},
            {'label': 'Active federal lawsuits', 'value': '2+', 'context': 'DOL settlement + AI denial class action proceeding', 'sort_order': 4},
        ]
        for s in uhc_stats:
            SnapshotStat.objects.get_or_create(company=uhc, label=s['label'], defaults={**s, 'source_url': ''})

        uhc_events = [
            {
                'date': date(2026, 3, 9),
                'title': 'Federal court orders UnitedHealth to produce broad discovery in AI claims denial case',
                'description': 'Magistrate judge directed UnitedHealthcare to turn over expansive set of documents in Estate of Lokken v. UnitedHealth Group class action. Court rejected UnitedHealth\'s efforts to limit discovery scope, ruling that pre-2019 records are relevant to establishing baseline before AI deployment.',
                'domain': 'consumer',
                'severity': 'serious',
                'source_agency': 'U.S. District Court, District of Minnesota',
                'source_url': '',
                'penalty_amount': None,
                'facility_location': 'Minneapolis, MN (Federal Court)',
            },
            {
                'date': date(2025, 2, 13),
                'title': 'Federal judge allows AI denial class action to proceed against UnitedHealthcare',
                'description': 'Court denied UnitedHealthcare\'s motion to dismiss key claims in Estate of Lokken v. UnitedHealth Group. Breach of contract and good faith claims allowed to move forward. Judge described UHG\'s claims denial appeals process as "futile" with likelihood of causing "irreparable injury."',
                'domain': 'consumer',
                'severity': 'serious',
                'source_agency': 'U.S. District Court, District of Minnesota',
                'source_url': '',
                'penalty_amount': None,
                'facility_location': 'Minneapolis, MN (Federal Court)',
            },
            {
                'date': date(2025, 2, 11),
                'title': 'UnitedHealth pays $20.25M to settle DOL lawsuit over systematic claims denials',
                'description': 'Settlement resolved DOL lawsuit alleging subsidiary UMR improperly denied thousands of emergency department and drug screening claims without assessing their merit. UMR "applied no standard and simply denied all the claims" for urinary drug screening. Company required to reprocess denied claims.',
                'domain': 'consumer',
                'severity': 'critical',
                'source_agency': 'Dept of Labor',
                'source_url': 'https://www.dol.gov/',
                'penalty_amount': Decimal('20250000'),
                'facility_location': 'Corporate-wide',
            },
            {
                'date': date(2024, 10, 1),
                'title': 'Senate investigation finds UnitedHealthcare denial rate doubled after AI deployment',
                'description': 'Senate Permanent Subcommittee on Investigations released report finding UnitedHealthcare\'s prior authorization denial rate for post-acute care jumped from 10.9% in 2020 to 22.7% in 2022 after implementing automated review processes. Skilled nursing denials increased nine-fold compared to 2019.',
                'domain': 'consumer',
                'severity': 'critical',
                'source_agency': 'U.S. Senate Permanent Subcommittee on Investigations',
                'source_url': '',
                'penalty_amount': None,
                'facility_location': 'Washington, DC',
            },
            {
                'date': date(2023, 11, 1),
                'title': 'Class action lawsuit filed alleging AI algorithm used to deny Medicare Advantage claims',
                'description': 'Families of two deceased Medicare Advantage beneficiaries filed class action alleging UnitedHealth, UnitedHealthcare, and naviHealth used AI tool nH Predict to systematically deny post-acute care claims. Lawsuit alleges 90% error rate on AI-driven denials. Plaintiffs include 91-year-old recovering from fractures and 74-year-old stroke patient.',
                'domain': 'consumer',
                'severity': 'critical',
                'source_agency': 'U.S. District Court, District of Minnesota',
                'source_url': '',
                'penalty_amount': None,
                'facility_location': 'Minneapolis, MN (Federal Court)',
            },
            {
                'date': date(2023, 8, 2),
                'title': 'Department of Labor sues UMR subsidiary over systematic emergency claims denials',
                'description': 'DOL filed complaint alleging UMR, a UnitedHealth subsidiary and largest third-party administrator in the U.S., improperly denied thousands of emergency department and drug screening claims without assessing their merit. UMR administers plans for approximately 2,140 self-funded employers.',
                'domain': 'consumer',
                'severity': 'critical',
                'source_agency': 'Dept of Labor',
                'source_url': 'https://www.dol.gov/',
                'penalty_amount': None,
                'facility_location': 'Corporate-wide',
            },
        ]
        for e in uhc_events:
            AccountabilityEvent.objects.get_or_create(company=uhc, date=e['date'], title=e['title'], defaults=e)

        uhc_sources = [
            {'source_name': 'DOL Enforcement Actions', 'source_agency': 'Dept of Labor', 'source_url': 'https://www.dol.gov/', 'last_checked': date(2025, 5, 22)},
            {'source_name': 'Federal Court Records (D. Minn.)', 'source_agency': 'U.S. Courts', 'source_url': 'https://www.uscourts.gov/', 'last_checked': date(2025, 5, 22)},
            {'source_name': 'Senate Subcommittee Reports', 'source_agency': 'U.S. Senate', 'source_url': 'https://www.hsgac.senate.gov/subcommittees/investigations/', 'last_checked': date(2025, 5, 22)},
            {'source_name': 'SEC Filings', 'source_agency': 'SEC', 'source_url': 'https://www.sec.gov/', 'last_checked': date(2025, 5, 22)},
        ]
        for s in uhc_sources:
            DataSource.objects.get_or_create(company=uhc, source_name=s['source_name'], defaults=s)

        for company in [fedex, uhc]:
            self.stdout.write(self.style.SUCCESS(
                f'Seeded {company.name}: {company.events.count()} events, '
                f'{company.snapshot_stats.count()} stats, '
                f'{company.data_sources.count()} sources'
            ))
