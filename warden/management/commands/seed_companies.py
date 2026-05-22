from django.core.management.base import BaseCommand
from datetime import date
from decimal import Decimal
from warden.models import (
    Industry, Company, AccountabilityEvent, DataSource, SnapshotStat
)


class Command(BaseCommand):
    help = 'Seed Walmart, Dollar General, Tesla, and Tyson Foods'

    def handle(self, *args, **kwargs):
        # Industries
        retail, _ = Industry.objects.get_or_create(slug='retail', defaults={'name': 'Retail'})
        discount, _ = Industry.objects.get_or_create(slug='discount-retail', defaults={'name': 'Discount Retail'})
        auto, _ = Industry.objects.get_or_create(slug='automotive-ev', defaults={'name': 'Automotive & EV Manufacturing'})
        meat, _ = Industry.objects.get_or_create(slug='meatpacking', defaults={'name': 'Meatpacking & Food Processing'})

        # ==================== WALMART ====================
        walmart, _ = Company.objects.get_or_create(
            slug='walmart',
            defaults={
                'name': 'Walmart',
                'legal_name': 'Walmart Inc.',
                'industry': retail,
                'description': 'Largest private employer in the United States. Operates retail stores, warehouses, and distribution centers nationwide.',
                'employee_count': 2100000,
                'headquarters': 'Bentonville, AR',
                'stock_ticker': 'WMT',
                'website': 'https://www.walmart.com',
                'risk_level': 'mixed',
                'summary_line': 'History of repeat OSHA violations across retail and warehouse locations. Significant WARN Act layoff activity with 224 notices affecting 36,800+ workers since 2004. Ongoing restructuring of corporate and technology workforce.',
            }
        )

        walmart_stats = [
            {'label': 'WARN notices since 2004', 'value': '224', 'context': 'Affecting 36,841 workers across 36 states', 'sort_order': 1},
            {'label': 'Recent corporate layoffs', 'value': '1,500+', 'context': '2025 — tech, e-commerce, and advertising roles', 'sort_order': 2},
            {'label': 'OSHA enforcement pattern', 'value': 'Repeat', 'context': 'Cited for similar hazards across multiple states', 'sort_order': 3},
        ]
        for s in walmart_stats:
            SnapshotStat.objects.get_or_create(company=walmart, label=s['label'], defaults={**s, 'source_url': ''})

        walmart_events = [
            {
                'date': date(2026, 4, 3),
                'title': 'WARN notice filed for 90 employees at Worcester, MA location',
                'description': 'Walmart filed WARN Act notice with Massachusetts Department of Labor for 90 employees at Worcester facility, effective May 29, 2026.',
                'domain': 'labor',
                'severity': 'moderate',
                'source_agency': 'Massachusetts Dept of Labor',
                'source_url': 'https://mass.gov/info-details/worker-adjustment-and-retraining-notification-act-warn',
                'penalty_amount': None,
                'facility_location': 'Worcester, MA',
            },
            {
                'date': date(2025, 5, 1),
                'title': 'Walmart cuts approximately 1,500 corporate roles across tech and e-commerce',
                'description': 'Walmart laid off approximately 1,500 corporate employees targeting technology, e-commerce fulfillment, and advertising teams. WARN filings disclosed 381 layoffs in Sunnyvale and 106 at San Bruno Global Tech office in California.',
                'domain': 'labor',
                'severity': 'serious',
                'source_agency': 'California EDD / WARN Act',
                'source_url': '',
                'penalty_amount': None,
                'facility_location': 'Sunnyvale, CA; San Bruno, CA; Bentonville, AR',
            },
            {
                'date': date(2023, 2, 24),
                'title': 'Federal panel upholds OSHA citation for hazardous shelving at Johnstown warehouse',
                'description': 'Occupational Safety and Health Review Commission affirmed that Walmart violated federal workplace safety standards at its warehouse in Johnstown, NY when stored merchandise fell onto and seriously injured an employee in 2017. Walmart litigated the $10,000 citation for years.',
                'domain': 'workplace',
                'severity': 'moderate',
                'source_agency': 'OSHRC / Dept of Labor',
                'source_url': 'https://www.dol.gov/newsroom/releases/sol?page=15',
                'penalty_amount': Decimal('10000'),
                'facility_location': 'Johnstown, NY',
            },
            {
                'date': date(2013, 1, 1),
                'title': 'Walmart settles OSHA violations for blocked exits and safety failures across multiple stores',
                'description': 'Walmart agreed to settlement resolving long-standing violations related to blocked exits, inadequate training, and poor safety practices across multiple retail locations. $190,000 in penalties covering violations at 2,800 stores.',
                'domain': 'workplace',
                'severity': 'serious',
                'source_agency': 'OSHA',
                'source_url': 'https://www.osha.gov/',
                'penalty_amount': Decimal('190000'),
                'facility_location': 'Multiple locations (2,800 stores)',
            },
            {
                'date': date(2012, 2, 13),
                'title': 'OSHA cites Walmart for 24 repeat and serious violations at Rochester supercenter',
                'description': 'OSHA identified fall hazards, obstructed exit routes, absence of lockout/tagout procedures, unguarded machinery, and lack of PPE training. Violations were substantially similar to hazards found at nine other Walmart locations across eight states.',
                'domain': 'workplace',
                'severity': 'serious',
                'source_agency': 'OSHA',
                'source_url': 'https://www.osha.gov/',
                'penalty_amount': Decimal('365500'),
                'facility_location': 'Rochester, NY',
            },
        ]
        for e in walmart_events:
            AccountabilityEvent.objects.get_or_create(company=walmart, date=e['date'], title=e['title'], defaults=e)

        walmart_sources = [
            {'source_name': 'OSHA Inspections & Citations', 'source_agency': 'Dept of Labor / OSHA', 'source_url': 'https://www.osha.gov/', 'last_checked': date(2025, 5, 22)},
            {'source_name': 'WARN Act Notices', 'source_agency': 'State Labor Departments', 'source_url': 'https://www.warntracker.com/company/walmart', 'last_checked': date(2025, 5, 22)},
            {'source_name': 'OSHRC Decisions', 'source_agency': 'OSHRC', 'source_url': 'https://www.oshrc.gov/', 'last_checked': date(2025, 5, 22)},
        ]
        for s in walmart_sources:
            DataSource.objects.get_or_create(company=walmart, source_name=s['source_name'], defaults=s)

        # ==================== DOLLAR GENERAL ====================
        dg, _ = Company.objects.get_or_create(
            slug='dollar-general',
            defaults={
                'name': 'Dollar General',
                'legal_name': 'Dollar General Corp.',
                'industry': discount,
                'description': 'Discount retailer operating 19,000+ stores nationwide. First company added to OSHA Severe Violator Enforcement Program.',
                'employee_count': 173000,
                'headquarters': 'Goodlettsville, TN',
                'stock_ticker': 'DG',
                'website': 'https://www.dollargeneral.com',
                'risk_level': 'elevated',
                'summary_line': 'Most-cited retailer in OSHA history. First company placed on OSHA severe violator list. Over $21M in cumulative OSHA fines since 2017 across 243+ inspections. Corporate-wide settlement reached July 2024 with potential fines of $100,000/day for non-compliance.',
            }
        )

        dg_stats = [
            {'label': 'Cumulative OSHA fines since 2017', 'value': '$21M+', 'context': 'Across 243+ inspections nationwide', 'sort_order': 1},
            {'label': 'Corporate-wide settlement', 'value': '$12M', 'context': 'July 2024 — hazard correction within 48 hours required', 'sort_order': 2},
            {'label': 'OSHA severe violator status', 'value': '1st', 'context': 'First company added to OSHA SVEP list (2023)', 'sort_order': 3},
            {'label': 'Open NLRB unfair labor practice cases', 'value': '13', 'context': 'As of February 2025', 'sort_order': 4},
        ]
        for s in dg_stats:
            SnapshotStat.objects.get_or_create(company=dg, label=s['label'], defaults={**s, 'source_url': ''})

        dg_events = [
            {
                'date': date(2024, 7, 11),
                'title': 'OSHA reaches $12M corporate-wide settlement requiring systematic safety changes',
                'description': 'Settlement resolves existing contested and open federal OSHA inspections for blocked emergency exits, electrical panels, fire extinguishers, and unsafe storage. Dollar General must correct hazards within 48 hours and submit proof. Failure subjects company to $100,000/day fines up to $500,000.',
                'domain': 'workplace',
                'severity': 'critical',
                'source_agency': 'OSHA / Dept of Labor',
                'source_url': 'https://www.osha.gov/news/newsreleases/national/07112024-0',
                'penalty_amount': Decimal('12000000'),
                'facility_location': 'Corporate-wide (19,000+ stores)',
            },
            {
                'date': date(2023, 7, 13),
                'title': 'OSHA cites Dollar General for 8 violations at two Tampa-area stores, proposes $342K penalties',
                'description': 'Inspectors found exit routes blocked, electrical hazards, no working employee restroom, and uncovered sewer drain at Brandon store. Emergency exit blocked by rolling containers at Dade City store. Three repeat, two serious, and three other-than-serious violations.',
                'domain': 'workplace',
                'severity': 'serious',
                'source_agency': 'OSHA',
                'source_url': 'https://www.osha.gov/news/newsreleases/region4/07132023',
                'penalty_amount': Decimal('342282'),
                'facility_location': 'Brandon, FL; Dade City, FL',
            },
            {
                'date': date(2023, 6, 2),
                'title': 'OSHA cites Dollar General for 8 repeat violations in Alabama and Florida, proposes $1.1M penalties',
                'description': 'Inspectors again found blocked exits, fire extinguishers, and electrical panels at multiple stores. Since 2017, company has faced 240+ inspections. In Alabama, Florida, and Georgia alone, nearly $9 million in penalties assessed between Feb 2022 and April 2023.',
                'domain': 'workplace',
                'severity': 'critical',
                'source_agency': 'OSHA',
                'source_url': 'https://www.osha.gov/news/newsreleases/region4/06022023',
                'penalty_amount': Decimal('1098292'),
                'facility_location': 'Alabama; Florida',
            },
            {
                'date': date(2023, 4, 20),
                'title': 'OSHA cites Dollar General for continued fire and entrapment hazards at Orlando-area store',
                'description': 'Federal inspectors again found employees exposed to fire and entrapment hazards from blocked exits and unsafe storage at an Orlando-area Dollar General location.',
                'domain': 'workplace',
                'severity': 'serious',
                'source_agency': 'OSHA',
                'source_url': 'https://www.osha.gov/news/newsreleases/national/04202023',
                'penalty_amount': None,
                'facility_location': 'Orlando, FL area',
            },
            {
                'date': date(2023, 1, 1),
                'title': 'Dollar General becomes first company added to OSHA Severe Violator Enforcement Program',
                'description': 'OSHA expanded the reach of its safety enforcement program and added Dollar General as the first company to the severe violator list, reflecting the pattern of repeated violations across hundreds of store locations.',
                'domain': 'workplace',
                'severity': 'critical',
                'source_agency': 'OSHA',
                'source_url': 'https://www.osha.gov/',
                'penalty_amount': None,
                'facility_location': 'Corporate-wide',
            },
            {
                'date': date(2023, 1, 1),
                'title': 'NLRB rules Dollar General engaged in unfair labor practices against organizing workers',
                'description': 'National Labor Relations Board ruled Dollar General engaged in "blatant hallmark unfair labor practices" against workers attempting to organize in Connecticut, including unlawful termination, surveillance, interrogation, and threatening store closures.',
                'domain': 'labor',
                'severity': 'serious',
                'source_agency': 'NLRB',
                'source_url': 'https://www.nlrb.gov/',
                'penalty_amount': None,
                'facility_location': 'Connecticut',
            },
        ]
        for e in dg_events:
            AccountabilityEvent.objects.get_or_create(company=dg, date=e['date'], title=e['title'], defaults=e)

        dg_sources = [
            {'source_name': 'OSHA Inspections & Enforcement', 'source_agency': 'Dept of Labor / OSHA', 'source_url': 'https://www.osha.gov/', 'last_checked': date(2025, 5, 22)},
            {'source_name': 'OSHA News Releases', 'source_agency': 'OSHA', 'source_url': 'https://www.osha.gov/news', 'last_checked': date(2025, 5, 22)},
            {'source_name': 'NLRB Decisions', 'source_agency': 'NLRB', 'source_url': 'https://www.nlrb.gov/', 'last_checked': date(2025, 5, 22)},
            {'source_name': 'SEC Proxy Filings (PX14A6G)', 'source_agency': 'SEC', 'source_url': 'https://www.sec.gov/cgi-bin/browse-edgar?company=dollar+general', 'last_checked': date(2025, 5, 22)},
        ]
        for s in dg_sources:
            DataSource.objects.get_or_create(company=dg, source_name=s['source_name'], defaults=s)

        # ==================== TESLA ====================
        tesla, _ = Company.objects.get_or_create(
            slug='tesla',
            defaults={
                'name': 'Tesla',
                'legal_name': 'Tesla, Inc.',
                'industry': auto,
                'description': 'Electric vehicle manufacturer and energy company. Operates manufacturing facilities including Fremont, CA and Austin, TX Gigafactory.',
                'employee_count': 140000,
                'headquarters': 'Austin, TX',
                'stock_ticker': 'TSLA',
                'website': 'https://www.tesla.com',
                'risk_level': 'elevated',
                'summary_line': 'Active OSHA citations including worker fatality investigation. Federal EEOC lawsuit for systemic racial harassment at Fremont facility. California civil rights agency lawsuit alleging racially segregated workplace. Multiple discrimination settlements.',
            }
        )

        tesla_stats = [
            {'label': 'OSHA citations (2024-2025)', 'value': '4+', 'context': 'Including worker fatality investigation at Austin Gigafactory', 'sort_order': 1},
            {'label': 'Active federal discrimination lawsuits', 'value': '2', 'context': 'EEOC and California CRD — both ongoing', 'sort_order': 2},
            {'label': 'Discrimination jury verdict (2023)', 'value': '$3.2M', 'context': 'Owen Diaz case — original jury awarded $137M in 2021', 'sort_order': 3},
        ]
        for s in tesla_stats:
            SnapshotStat.objects.get_or_create(company=tesla, label=s['label'], defaults={**s, 'source_url': ''})

        tesla_events = [
            {
                'date': date(2025, 3, 6),
                'title': 'OSHA cites Tesla $49,650 for three violations following worker electrocution death',
                'description': 'OSHA issued three serious citations at maximum penalty ($16,550 each) after contract electrician Victor Joe Gomez Sr. was electrocuted while inspecting electrical panels at Austin Gigafactory in August 2024. Violations included failure to provide PPE, failure to advise employees on energized circuit locations, and allowing inspection of equipment that was not de-energized.',
                'domain': 'workplace',
                'severity': 'critical',
                'source_agency': 'OSHA / Dept of Labor',
                'source_url': 'https://www.osha.gov/',
                'penalty_amount': Decimal('49650'),
                'facility_location': 'Austin, TX (Gigafactory)',
            },
            {
                'date': date(2024, 1, 1),
                'title': 'OSHA cites Tesla for chromium overexposure and inadequate training',
                'description': 'Citation issued for overexposing workers to hexavalent chromium and failing to train employees about chemical hazards. Hexavalent chromium exposure is associated with occupational asthma, eye irritation, and increased cancer risk.',
                'domain': 'workplace',
                'severity': 'serious',
                'source_agency': 'OSHA',
                'source_url': 'https://www.osha.gov/',
                'penalty_amount': None,
                'facility_location': 'Manufacturing facility',
            },
            {
                'date': date(2024, 3, 15),
                'title': 'Tesla settles Owen Diaz racial discrimination lawsuit after two jury trials',
                'description': 'Confidential settlement reached in long-running racial discrimination case. First jury trial in 2021 awarded $137M (later reduced to $15M by judge). Second trial in 2023 awarded $3.2M. Diaz alleged colleagues used racial slurs, created racist graffiti, and told him to "go back to Africa" while working at Fremont factory.',
                'domain': 'labor',
                'severity': 'serious',
                'source_agency': 'U.S. District Court, Northern District of California',
                'source_url': 'https://www.eeoc.gov/',
                'penalty_amount': Decimal('3200000'),
                'facility_location': 'Fremont, CA',
            },
            {
                'date': date(2023, 9, 28),
                'title': 'EEOC sues Tesla for systemic racial harassment and retaliation at Fremont facility',
                'description': 'Federal lawsuit alleges that since at least 2015, Black employees at Fremont manufacturing facilities endured racial slurs, swastikas, threats, and nooses on equipment and in common areas. EEOC found employees who reported harassment faced terminations, transfers, and adverse employment actions.',
                'domain': 'labor',
                'severity': 'critical',
                'source_agency': 'EEOC',
                'source_url': 'https://www.eeoc.gov/newsroom/eeoc-sues-tesla-racial-harassment-and-retaliation',
                'penalty_amount': None,
                'facility_location': 'Fremont, CA',
            },
            {
                'date': date(2022, 2, 9),
                'title': 'California Civil Rights Department sues Tesla for systemic racial discrimination',
                'description': 'California CRD (formerly DFEH) filed civil complaint alleging systemic race discrimination, hostile work environment, and pay equity violations at Fremont plant. Complaint alleges Tesla maintained a "racially segregated" workplace. Case remains in litigation.',
                'domain': 'labor',
                'severity': 'critical',
                'source_agency': 'California Civil Rights Dept',
                'source_url': 'https://calcivilrights.ca.gov/',
                'penalty_amount': None,
                'facility_location': 'Fremont, CA',
            },
        ]
        for e in tesla_events:
            AccountabilityEvent.objects.get_or_create(company=tesla, date=e['date'], title=e['title'], defaults=e)

        tesla_sources = [
            {'source_name': 'OSHA Inspections & Citations', 'source_agency': 'Dept of Labor / OSHA', 'source_url': 'https://www.osha.gov/', 'last_checked': date(2025, 5, 22)},
            {'source_name': 'EEOC Lawsuit & Press Releases', 'source_agency': 'EEOC', 'source_url': 'https://www.eeoc.gov/', 'last_checked': date(2025, 5, 22)},
            {'source_name': 'California CRD Enforcement', 'source_agency': 'California Civil Rights Dept', 'source_url': 'https://calcivilrights.ca.gov/', 'last_checked': date(2025, 5, 22)},
            {'source_name': 'SEC Filings (10-Q, DEF 14A)', 'source_agency': 'SEC', 'source_url': 'https://www.sec.gov/cgi-bin/browse-edgar?company=tesla', 'last_checked': date(2025, 5, 22)},
        ]
        for s in tesla_sources:
            DataSource.objects.get_or_create(company=tesla, source_name=s['source_name'], defaults=s)

        # ==================== TYSON FOODS ====================
        tyson, _ = Company.objects.get_or_create(
            slug='tyson-foods',
            defaults={
                'name': 'Tyson Foods',
                'legal_name': 'Tyson Foods, Inc.',
                'industry': meat,
                'description': 'Largest meat and poultry processor in the United States. Operates processing plants and distribution facilities across multiple states.',
                'employee_count': 142000,
                'headquarters': 'Springdale, AR',
                'stock_ticker': 'TSN',
                'website': 'https://www.tysonfoods.com',
                'risk_level': 'elevated',
                'summary_line': 'Ongoing DOL investigations into child labor violations at multiple facilities. Pattern of OSHA citations for hazardous conditions including amputation hazards and chemical exposure. Worker fatality at Dakota City plant in 2025.',
            }
        )

        tyson_stats = [
            {'label': 'Active federal child labor investigations', 'value': '2+', 'context': 'DOL Wage and Hour Division — Arkansas, Virginia facilities', 'sort_order': 1},
            {'label': 'OSHA violations (2023)', 'value': '20', 'context': 'Across 12 facilities in 7 states', 'sort_order': 2},
            {'label': 'Worker fatality (2025)', 'value': '1', 'context': 'Dakota City, NE — lockout/tagout failure', 'sort_order': 3},
            {'label': 'Child labor penalty (assessed)', 'value': '$90.8K', 'context': 'Maximum civil penalty — Green Forest, AR facility', 'sort_order': 4},
        ]
        for s in tyson_stats:
            SnapshotStat.objects.get_or_create(company=tyson, label=s['label'], defaults={**s, 'source_url': ''})

        tyson_events = [
            {
                'date': date(2025, 6, 3),
                'title': 'OSHA fines Tyson $27,790 after worker death at Dakota City plant',
                'description': 'Maintenance worker was fatally injured when a machine lowered onto him after an electronic sensor activated while he was lying underneath performing work. OSHA found Tyson had not ensured authorized employees were trained in correct lockout procedures. Two violations identified.',
                'domain': 'workplace',
                'severity': 'critical',
                'source_agency': 'OSHA / Dept of Labor',
                'source_url': 'https://www.osha.gov/',
                'penalty_amount': Decimal('27790'),
                'facility_location': 'Dakota City, NE',
            },
            {
                'date': date(2024, 9, 1),
                'title': 'DOL searches two Tyson plants in Arkansas following child labor tips',
                'description': 'Department of Labor investigators searched Tyson plants in Rogers and Green Forest, Arkansas after receiving anonymous tips about school-age children working at the facilities. Court documents unsealed showing photographs of alleged minors entering and exiting plants.',
                'domain': 'labor',
                'severity': 'critical',
                'source_agency': 'DOL Wage and Hour Division',
                'source_url': 'https://www.dol.gov/',
                'penalty_amount': None,
                'facility_location': 'Rogers, AR; Green Forest, AR',
            },
            {
                'date': date(2023, 9, 25),
                'title': 'DOL opens investigation into child labor at Tyson and Perdue Farms',
                'description': 'Department of Labor launched investigations into whether migrant children are among those cleaning slaughterhouses owned by Tyson and Perdue. Investigation followed New York Times Magazine report detailing children working overnight cleaning blood, grease, and feathers with acid and pressure hoses. First time DOL attempted to hold parent companies jointly liable for subcontractor child labor violations.',
                'domain': 'labor',
                'severity': 'critical',
                'source_agency': 'DOL Wage and Hour Division',
                'source_url': 'https://www.dol.gov/',
                'penalty_amount': None,
                'facility_location': 'Eastern Shore, VA',
            },
            {
                'date': date(2023, 2, 1),
                'title': 'DOL finds child labor violations at Tyson facilities as part of multi-state investigation',
                'description': 'DOL investigation found illegal child labor in 13 meat processing facilities in eight states, including Tyson Foods facilities. Six cases of illegal child labor found at Tyson Green Forest, AR facility ($90,828 penalty — maximum allowed). One case at Goodlettsville, TN facility ($15,138 penalty).',
                'domain': 'labor',
                'severity': 'critical',
                'source_agency': 'DOL Wage and Hour Division',
                'source_url': 'https://www.dol.gov/',
                'penalty_amount': Decimal('105966'),
                'facility_location': 'Green Forest, AR; Goodlettsville, TN',
            },
            {
                'date': date(2023, 1, 1),
                'title': 'OSHA finds 20 violations at 12 Tyson facilities across seven states',
                'description': 'OSHA inspections identified 20 violations at Tyson facilities in Indiana, Missouri, Iowa, Arkansas, Nebraska, North Carolina, and Texas. Initial fines totaled over $230,000.',
                'domain': 'workplace',
                'severity': 'serious',
                'source_agency': 'OSHA',
                'source_url': 'https://www.osha.gov/',
                'penalty_amount': Decimal('230407'),
                'facility_location': 'IN, MO, IA, AR, NE, NC, TX',
            },
            {
                'date': date(2016, 8, 16),
                'title': 'OSHA fines Tyson $263K for 17 violations including amputation hazards at Texas plant',
                'description': 'Investigation initiated after worker lost finger in unguarded conveyor belt at Center, TX chicken processing plant. OSHA found two repeated and 15 serious violations including amputation hazards, high carbon dioxide exposure, peracetic acid exposure without PPE, obstructed fire exits, and improper drainage.',
                'domain': 'workplace',
                'severity': 'serious',
                'source_agency': 'OSHA',
                'source_url': 'https://www.osha.gov/',
                'penalty_amount': Decimal('263498'),
                'facility_location': 'Center, TX',
            },
        ]
        for e in tyson_events:
            AccountabilityEvent.objects.get_or_create(company=tyson, date=e['date'], title=e['title'], defaults=e)

        tyson_sources = [
            {'source_name': 'OSHA Inspections & Citations', 'source_agency': 'Dept of Labor / OSHA', 'source_url': 'https://www.osha.gov/', 'last_checked': date(2025, 5, 22)},
            {'source_name': 'DOL Wage and Hour Division', 'source_agency': 'Dept of Labor', 'source_url': 'https://www.dol.gov/', 'last_checked': date(2025, 5, 22)},
            {'source_name': 'SEC Proxy Filings (PX14A6G)', 'source_agency': 'SEC', 'source_url': 'https://www.sec.gov/cgi-bin/browse-edgar?company=tyson+foods', 'last_checked': date(2025, 5, 22)},
            {'source_name': 'Federal Court Records', 'source_agency': 'U.S. Courts', 'source_url': 'https://www.uscourts.gov/', 'last_checked': date(2025, 5, 22)},
        ]
        for s in tyson_sources:
            DataSource.objects.get_or_create(company=tyson, source_name=s['source_name'], defaults=s)

        # Summary
        for company in [walmart, dg, tesla, tyson]:
            self.stdout.write(self.style.SUCCESS(
                f'Seeded {company.name}: {company.events.count()} events, '
                f'{company.snapshot_stats.count()} stats, '
                f'{company.data_sources.count()} sources'
            ))
