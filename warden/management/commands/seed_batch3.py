from django.core.management.base import BaseCommand
from datetime import date
from decimal import Decimal
from warden.models import (
    Industry, Company, AccountabilityEvent, DataSource, SnapshotStat
)


class Command(BaseCommand):
    help = 'Seed Starbucks, Boeing, Chipotle, Norfolk Southern, McDonalds'

    def handle(self, *args, **kwargs):
        food, _ = Industry.objects.get_or_create(slug='restaurants', defaults={'name': 'Restaurants & Food Service'})
        aero, _ = Industry.objects.get_or_create(slug='aerospace', defaults={'name': 'Aerospace & Defense'})
        rail, _ = Industry.objects.get_or_create(slug='railroads', defaults={'name': 'Railroads & Freight'})
        qsr, _ = Industry.objects.get_or_create(slug='quick-service', defaults={'name': 'Quick-Service Restaurants'})

        # ==================== STARBUCKS ====================
        sbux, _ = Company.objects.get_or_create(
            slug='starbucks',
            defaults={
                'name': 'Starbucks',
                'legal_name': 'Starbucks Corporation',
                'industry': food,
                'description': 'Global coffeehouse chain operating 35,000+ stores worldwide. Largest target of NLRB unfair labor practice charges in modern history.',
                'employee_count': 381000,
                'headquarters': 'Seattle, WA',
                'stock_ticker': 'SBUX',
                'website': 'https://www.starbucks.com',
                'risk_level': 'elevated',
                'summary_line': 'NLRB administrative law judges have found Starbucks committed more than 400 labor law violations. 771 unfair labor practice charges docketed since 2021. NLRB found company showed "general disregard for employees\' fundamental statutory rights."',
                'pattern_summary': 'Largest documented campaign of unfair labor practices against a single employer in modern NLRB history. Pattern of retaliatory terminations, benefit withholding from union stores, surveillance, and threatened store closures. Enforcement escalated from individual store complaints to corporate-wide policy findings. Over 125 new ULP charges filed since January 2025 under current CEO.',
            }
        )

        sbux_stats = [
            {'label': 'NLRB labor law violations found', 'value': '400+', 'context': 'By administrative law judges since 2021', 'sort_order': 1},
            {'label': 'Unfair labor practice charges', 'value': '771', 'context': 'Docketed by NLRB regional offices as of Feb 2024', 'sort_order': 2},
            {'label': 'New ULP charges (2025)', 'value': '125+', 'context': 'Filed since January 2025', 'sort_order': 3},
        ]
        for s in sbux_stats:
            SnapshotStat.objects.get_or_create(company=sbux, label=s['label'], defaults={**s, 'source_url': ''})

        sbux_events = [
            {
                'date': date(2025, 3, 27),
                'title': 'NLRB affirms Starbucks violated labor law with store closure threats',
                'description': 'Board affirmed ALJ finding that store manager violated Section 8(a)(1) by making statements suggesting unionization could lead to store closures without providing factual basis. Decision in Starbucks Corp v. Workers United, 374 N.L.R.B. No. 23.',
                'domain': 'labor', 'severity': 'moderate',
                'source_agency': 'NLRB',
                'source_url': 'https://www.nlrb.gov/',
                'penalty_amount': None, 'facility_location': 'National',
            },
            {
                'date': date(2024, 12, 16),
                'title': 'NLRB finds Starbucks committed 60+ violations at Buffalo stores where organizing began',
                'description': 'NLRB ruled Starbucks committed more than 60 violations of labor law at the Buffalo, NY stores where the Workers United organizing campaign originated. Board stated "the severity and pervasiveness of the Respondent\'s unfair labor practices demonstrate a general disregard for its employees\' fundamental statutory rights."',
                'domain': 'labor', 'severity': 'critical',
                'source_agency': 'NLRB',
                'source_url': 'https://www.nlrb.gov/',
                'penalty_amount': None, 'facility_location': 'Buffalo, NY',
            },
            {
                'date': date(2023, 10, 2),
                'title': 'NLRB ALJ rules Starbucks adopted corporate-wide antiunion benefits policy',
                'description': 'Administrative law judge found Starbucks adopted a corporate-wide policy of conditioning eligibility for increased wages and benefits on employees refraining from union representation. Company withheld new benefits from unionized stores while granting them to non-union locations.',
                'domain': 'labor', 'severity': 'critical',
                'source_agency': 'NLRB',
                'source_url': 'https://www.nlrb.gov/',
                'penalty_amount': None, 'facility_location': 'Corporate-wide',
            },
            {
                'date': date(2023, 5, 1),
                'title': 'NLRB ALJ rules Starbucks illegally fired five Memphis workers for union organizing',
                'description': 'Administrative law judge ruled Starbucks violated federal labor law when it terminated five of the seven "Memphis 7" workers who were organizing a union at their store. Case reached the Supreme Court on the question of NLRB injunction powers.',
                'domain': 'labor', 'severity': 'serious',
                'source_agency': 'NLRB',
                'source_url': 'https://www.nlrb.gov/',
                'penalty_amount': None, 'facility_location': 'Memphis, TN',
            },
            {
                'date': date(2023, 3, 1),
                'title': 'NLRB ALJ finds Starbucks guilty of "egregious and widespread misconduct" in Buffalo',
                'description': 'Administrative law judge found Starbucks engaged in egregious and widespread misconduct and showed a general disregard for employees\' fundamental rights during the Buffalo, NY union organizing campaign that began in 2021.',
                'domain': 'labor', 'severity': 'critical',
                'source_agency': 'NLRB',
                'source_url': 'https://www.nlrb.gov/',
                'penalty_amount': None, 'facility_location': 'Buffalo, NY',
            },
        ]
        for e in sbux_events:
            AccountabilityEvent.objects.get_or_create(company=sbux, date=e['date'], title=e['title'], defaults=e)

        for s in [
            {'source_name': 'NLRB Decisions & Orders', 'source_agency': 'NLRB', 'source_url': 'https://www.nlrb.gov/', 'last_checked': date(2025, 5, 22)},
            {'source_name': 'Senate HELP Committee Report', 'source_agency': 'U.S. Senate', 'source_url': 'https://www.help.senate.gov/', 'last_checked': date(2025, 5, 22)},
        ]:
            DataSource.objects.get_or_create(company=sbux, source_name=s['source_name'], defaults=s)

        # ==================== BOEING ====================
        boeing, _ = Company.objects.get_or_create(
            slug='boeing',
            defaults={
                'name': 'Boeing',
                'legal_name': 'The Boeing Company',
                'industry': aero,
                'description': 'Major aerospace manufacturer producing commercial airliners, defense systems, and space vehicles. Operates manufacturing facilities across Washington, South Carolina, and other states.',
                'employee_count': 170000,
                'headquarters': 'Arlington, VA',
                'stock_ticker': 'BA',
                'website': 'https://www.boeing.com',
                'risk_level': 'elevated',
                'summary_line': 'FAA proposed $3.1M+ in fines for safety violations including the January 2024 door plug blowout. 32 whistleblower complaints filed with OSHA since 2020. DOJ rejected initial fraud plea deal in December 2024. Senate investigation found employees feel pressure to prioritize speed over quality.',
                'pattern_summary': 'Systemic safety and quality failures spanning manufacturing, oversight, and corporate culture. FAA identified hundreds of quality system violations at 737 factory. Internal survey found only 47% of employees agreed schedule pressures do not lower standards. Whistleblower allegations of manufacturing shortcuts on 787 and 777 programs. Pattern of prioritizing production speed and delivery schedules over safety compliance.',
            }
        )

        boeing_stats = [
            {'label': 'FAA proposed fines (2025)', 'value': '$3.1M+', 'context': 'Safety violations Sept 2023 - Feb 2024', 'sort_order': 1},
            {'label': 'OSHA whistleblower complaints', 'value': '32', 'context': 'Filed since 2020', 'sort_order': 2},
            {'label': 'Quality system violations (FAA)', 'value': 'Hundreds', 'context': 'At 737 factory in Renton, WA', 'sort_order': 3},
            {'label': 'Employee safety culture survey', 'value': '47%', 'context': 'Agreed schedule pressures do not lower standards (May 2024)', 'sort_order': 4},
        ]
        for s in boeing_stats:
            SnapshotStat.objects.get_or_create(company=boeing, label=s['label'], defaults={**s, 'source_url': ''})

        boeing_events = [
            {
                'date': date(2025, 9, 12),
                'title': 'FAA proposes $3.1M+ in fines against Boeing for safety violations',
                'description': 'FAA identified hundreds of quality system violations at Boeing 737 factory in Renton, WA and subcontractor Spirit AeroSystems in Wichita, KS. Violations included an employee pressuring a safety inspector to sign off on a 737 Max to meet delivery schedule despite non-compliance. Penalties cover violations from Sept 2023 through Feb 2024.',
                'domain': 'workplace', 'severity': 'critical',
                'source_agency': 'FAA',
                'source_url': 'https://www.faa.gov/',
                'penalty_amount': Decimal('3100000'), 'facility_location': 'Renton, WA; Wichita, KS',
            },
            {
                'date': date(2024, 12, 5),
                'title': 'Federal judge rejects Boeing fraud plea deal over 737 MAX crashes',
                'description': 'U.S. judge rejected Boeing\'s agreement to plead guilty to conspiracy to defraud the FAA in connection with the two fatal 737 MAX crashes that killed 346 people (Lion Air 2018, Ethiopian Airlines 2019). Judge cited DOJ policy concerns about independent compliance monitoring.',
                'domain': 'governance', 'severity': 'critical',
                'source_agency': 'DOJ / U.S. District Court',
                'source_url': 'https://www.justice.gov/',
                'penalty_amount': None, 'facility_location': 'Washington, DC (Federal Court)',
            },
            {
                'date': date(2024, 9, 25),
                'title': 'Senate investigation reveals Boeing employees feel pressure to prioritize speed over safety',
                'description': 'Senate Permanent Subcommittee on Investigations hearing presented new documents showing Boeing personnel continue to feel pressure to prioritize production speed over quality. May 2024 internal survey found only 47% of respondents agreed schedule pressures do not cause teams to lower standards.',
                'domain': 'workplace', 'severity': 'serious',
                'source_agency': 'U.S. Senate PSI',
                'source_url': 'https://www.hsgac.senate.gov/',
                'penalty_amount': None, 'facility_location': 'Corporate-wide',
            },
            {
                'date': date(2024, 3, 19),
                'title': 'Senate obtains whistleblower allegations of "potentially catastrophic" 787 manufacturing defects',
                'description': 'Senate Subcommittee obtained documents from a current Boeing quality engineer alleging the company took shortcuts in 787 production, including faulty engineering and evaluation of data allowing potentially defective parts. Whistleblower also reported assembly defects in 777 aircraft.',
                'domain': 'workplace', 'severity': 'critical',
                'source_agency': 'U.S. Senate PSI',
                'source_url': 'https://www.hsgac.senate.gov/',
                'penalty_amount': None, 'facility_location': 'Multiple manufacturing facilities',
            },
            {
                'date': date(2024, 1, 5),
                'title': 'Alaska Airlines 737 MAX 9 door plug blows out during flight',
                'description': 'A paneled-over emergency exit door plug on an Alaska Airlines Boeing 737 MAX 9 blew out shortly after takeoff from Portland, Oregon. 171 passengers and 6 crew aboard. No serious injuries. NTSB investigation found lapses in Boeing manufacturing and FAA oversight led to the incident.',
                'domain': 'workplace', 'severity': 'critical',
                'source_agency': 'NTSB / FAA',
                'source_url': 'https://www.ntsb.gov/',
                'penalty_amount': None, 'facility_location': 'Portland, OR (flight) / Renton, WA (manufacturing)',
            },
        ]
        for e in boeing_events:
            AccountabilityEvent.objects.get_or_create(company=boeing, date=e['date'], title=e['title'], defaults=e)

        for s in [
            {'source_name': 'FAA Enforcement Actions', 'source_agency': 'FAA', 'source_url': 'https://www.faa.gov/', 'last_checked': date(2025, 5, 22)},
            {'source_name': 'NTSB Investigation Reports', 'source_agency': 'NTSB', 'source_url': 'https://www.ntsb.gov/', 'last_checked': date(2025, 5, 22)},
            {'source_name': 'Senate PSI Investigation', 'source_agency': 'U.S. Senate', 'source_url': 'https://www.hsgac.senate.gov/', 'last_checked': date(2025, 5, 22)},
            {'source_name': 'DOJ Criminal Proceedings', 'source_agency': 'Dept of Justice', 'source_url': 'https://www.justice.gov/', 'last_checked': date(2025, 5, 22)},
            {'source_name': 'OSHA Whistleblower Complaints', 'source_agency': 'OSHA', 'source_url': 'https://www.osha.gov/', 'last_checked': date(2025, 5, 22)},
        ]:
            DataSource.objects.get_or_create(company=boeing, source_name=s['source_name'], defaults=s)

        # ==================== CHIPOTLE ====================
        chipotle, _ = Company.objects.get_or_create(
            slug='chipotle',
            defaults={
                'name': 'Chipotle',
                'legal_name': 'Chipotle Mexican Grill, Inc.',
                'industry': qsr,
                'description': 'Fast-casual restaurant chain operating 3,500+ locations. Repeat target of state child labor enforcement actions across multiple jurisdictions.',
                'employee_count': 120000,
                'headquarters': 'Newport Beach, CA',
                'stock_ticker': 'CMG',
                'website': 'https://www.chipotle.com',
                'risk_level': 'elevated',
                'summary_line': 'Over $9.4M in child labor penalties across Massachusetts, New Jersey, and Washington DC. More than 44,000 alleged child labor violations identified across multiple states. Federal DOL citation for assigning minors to operate hazardous equipment.',
                'pattern_summary': 'Persistent pattern of child labor violations across multiple states spanning 2020 to present. Violations consistently involve minors working past legal hours, exceeding weekly hour limits, and working without required permits. Scale of violations — over 44,000 alleged across three states alone — suggests systemic scheduling and compliance failures rather than isolated incidents.',
            }
        )

        chipotle_stats = [
            {'label': 'Cumulative child labor penalties', 'value': '$9.4M+', 'context': 'Massachusetts, New Jersey, Washington DC', 'sort_order': 1},
            {'label': 'Alleged violations (NJ alone)', 'value': '30,660', 'context': 'Identified in 2020 state audit', 'sort_order': 2},
            {'label': 'Alleged violations (MA)', 'value': '13,253', 'context': 'Across 50+ locations', 'sort_order': 3},
        ]
        for s in chipotle_stats:
            SnapshotStat.objects.get_or_create(company=chipotle, label=s['label'], defaults={**s, 'source_url': ''})

        chipotle_events = [
            {
                'date': date(2023, 8, 28),
                'title': 'Chipotle pays $322,400 to settle DC child labor violations — 800+ violations identified',
                'description': 'Washington DC Attorney General found over 800 potential violations of child labor law at Chipotle locations over three years. Most involved scheduling minors for later or longer hours than permitted. Investigation triggered by violations found in other states.',
                'domain': 'labor', 'severity': 'serious',
                'source_agency': 'DC Office of the Attorney General',
                'source_url': 'https://oag.dc.gov/',
                'penalty_amount': Decimal('322400'), 'facility_location': 'Washington, DC (20 locations)',
            },
            {
                'date': date(2022, 9, 20),
                'title': 'Chipotle pays $7.75M to New Jersey for 30,660 child labor violations',
                'description': 'New Jersey Department of Labor audit identified approximately 30,660 alleged violations impacting minors at Chipotle locations across the state. Historic settlement — largest child labor penalty in New Jersey history. Company required to implement comprehensive compliance plan across 85 NJ locations.',
                'domain': 'labor', 'severity': 'critical',
                'source_agency': 'NJ Dept of Labor / Attorney General',
                'source_url': 'https://www.nj.gov/labor/',
                'penalty_amount': Decimal('7750000'), 'facility_location': 'New Jersey (85 locations)',
            },
            {
                'date': date(2020, 12, 30),
                'title': 'DOL fines Chipotle for assigning minors to operate hazardous trash compactors',
                'description': 'Federal investigation found Chipotle assigned five minor employees to repeatedly load and operate trash and cardboard compactors at Commerce, CA location. Minors assigned to compactor teams three times daily regardless of age. $27,150 in civil penalties.',
                'domain': 'labor', 'severity': 'serious',
                'source_agency': 'DOL Wage and Hour Division',
                'source_url': 'https://www.dol.gov/newsroom/releases/whd/whd20201230',
                'penalty_amount': Decimal('27150'), 'facility_location': 'Commerce, CA',
            },
            {
                'date': date(2020, 1, 28),
                'title': 'Massachusetts fines Chipotle $1.37M for 13,253 child labor violations',
                'description': 'Largest child labor penalty ever issued by the state. Violations included minors working past midnight, exceeding 48 hours per week, and working without permits. Teenagers reported hours prevented them from keeping up with schoolwork. Total settlement closer to $2M including sick time violations.',
                'domain': 'labor', 'severity': 'critical',
                'source_agency': 'Massachusetts Attorney General',
                'source_url': 'https://www.mass.gov/orgs/office-of-the-attorney-general',
                'penalty_amount': Decimal('1370000'), 'facility_location': 'Massachusetts (50+ locations)',
            },
        ]
        for e in chipotle_events:
            AccountabilityEvent.objects.get_or_create(company=chipotle, date=e['date'], title=e['title'], defaults=e)

        for s in [
            {'source_name': 'DOL Wage and Hour Division', 'source_agency': 'Dept of Labor', 'source_url': 'https://www.dol.gov/', 'last_checked': date(2025, 5, 22)},
            {'source_name': 'State Attorney General Actions', 'source_agency': 'State AGs (MA, NJ, DC)', 'source_url': '', 'last_checked': date(2025, 5, 22)},
        ]:
            DataSource.objects.get_or_create(company=chipotle, source_name=s['source_name'], defaults=s)

        # ==================== NORFOLK SOUTHERN ====================
        ns, _ = Company.objects.get_or_create(
            slug='norfolk-southern',
            defaults={
                'name': 'Norfolk Southern',
                'legal_name': 'Norfolk Southern Corporation',
                'industry': rail,
                'description': 'Class I freight railroad operating approximately 19,300 route miles across 22 eastern states. Subject of major federal investigation following East Palestine, Ohio derailment.',
                'employee_count': 19000,
                'headquarters': 'Atlanta, GA',
                'stock_ticker': 'NSC',
                'website': 'https://www.nscorp.com',
                'risk_level': 'elevated',
                'summary_line': 'February 2023 East Palestine, Ohio train derailment released hazardous chemicals including vinyl chloride, triggering federal emergency response. Subject of DOJ enforcement action, EPA emergency orders, and NTSB investigation finding systemic safety failures.',
                'pattern_summary': 'East Palestine derailment exposed systemic deficiencies in hazardous materials safety protocols, train inspection practices, and emergency response preparedness. NTSB investigation identified overheated bearing as cause with failures in detection systems. Federal scrutiny extended to industry-wide practices including train length, staffing, and inspection frequency. Company reached $600M+ settlement with affected residents.',
            }
        )

        ns_stats = [
            {'label': 'East Palestine settlement', 'value': '$600M+', 'context': 'Class action settlement with affected residents', 'sort_order': 1},
            {'label': 'EPA emergency orders', 'value': 'Multiple', 'context': 'Hazardous materials cleanup and monitoring', 'sort_order': 2},
            {'label': 'Hazardous chemicals released', 'value': '5+', 'context': 'Including vinyl chloride (known carcinogen)', 'sort_order': 3},
        ]
        for s in ns_stats:
            SnapshotStat.objects.get_or_create(company=ns, label=s['label'], defaults={**s, 'source_url': ''})

        ns_events = [
            {
                'date': date(2024, 6, 25),
                'title': 'NTSB releases final report on East Palestine derailment — finds systemic safety failures',
                'description': 'National Transportation Safety Board final report identified an overheated wheel bearing as the cause of the derailment. Report found failures in Norfolk Southern\'s bearing detection systems, inadequate train inspection protocols, and insufficient emergency response planning for hazardous materials. NTSB issued recommendations for industry-wide safety improvements.',
                'domain': 'workplace', 'severity': 'critical',
                'source_agency': 'NTSB',
                'source_url': 'https://www.ntsb.gov/',
                'penalty_amount': None, 'facility_location': 'East Palestine, OH',
            },
            {
                'date': date(2024, 2, 1),
                'title': 'Norfolk Southern reaches $600M+ class action settlement with East Palestine residents',
                'description': 'Company agreed to pay over $600 million to settle class action lawsuit filed by residents of East Palestine and surrounding communities affected by the February 2023 derailment and hazardous chemical release.',
                'domain': 'consumer', 'severity': 'critical',
                'source_agency': 'U.S. District Court',
                'source_url': '',
                'penalty_amount': Decimal('600000000'), 'facility_location': 'East Palestine, OH',
            },
            {
                'date': date(2023, 3, 31),
                'title': 'EPA issues emergency order requiring Norfolk Southern to fund full cleanup',
                'description': 'EPA ordered Norfolk Southern to pay for the complete cleanup of contamination from the East Palestine derailment and controlled release of hazardous chemicals. Order required ongoing environmental monitoring and health screenings for affected residents.',
                'domain': 'environmental', 'severity': 'critical',
                'source_agency': 'EPA',
                'source_url': 'https://www.epa.gov/',
                'penalty_amount': None, 'facility_location': 'East Palestine, OH',
            },
            {
                'date': date(2023, 2, 3),
                'title': 'Norfolk Southern train derails in East Palestine, OH — releases vinyl chloride and hazardous chemicals',
                'description': '38-car derailment including 11 cars carrying hazardous materials. Controlled release and burn of vinyl chloride, a known carcinogen, ordered to prevent uncontrolled explosion. Approximately 1,500 residents evacuated. Contamination affected air, water, and soil in surrounding communities.',
                'domain': 'environmental', 'severity': 'critical',
                'source_agency': 'NTSB / EPA / FRA',
                'source_url': 'https://www.ntsb.gov/',
                'penalty_amount': None, 'facility_location': 'East Palestine, OH',
            },
        ]
        for e in ns_events:
            AccountabilityEvent.objects.get_or_create(company=ns, date=e['date'], title=e['title'], defaults=e)

        for s in [
            {'source_name': 'NTSB Investigation', 'source_agency': 'NTSB', 'source_url': 'https://www.ntsb.gov/', 'last_checked': date(2025, 5, 22)},
            {'source_name': 'EPA Enforcement Orders', 'source_agency': 'EPA', 'source_url': 'https://www.epa.gov/', 'last_checked': date(2025, 5, 22)},
            {'source_name': 'Federal Railroad Administration', 'source_agency': 'FRA', 'source_url': 'https://railroads.dot.gov/', 'last_checked': date(2025, 5, 22)},
        ]:
            DataSource.objects.get_or_create(company=ns, source_name=s['source_name'], defaults=s)

        # ==================== McDONALD'S ====================
        mcd, _ = Company.objects.get_or_create(
            slug='mcdonalds',
            defaults={
                'name': "McDonald's",
                'legal_name': "McDonald's Corporation",
                'industry': qsr,
                'description': 'Largest quick-service restaurant chain globally. Operates through franchisees who employ the majority of workers across 13,000+ US locations.',
                'employee_count': 150000,
                'headquarters': 'Chicago, IL',
                'stock_ticker': 'MCD',
                'website': 'https://www.mcdonalds.com',
                'risk_level': 'mixed',
                'summary_line': 'Franchise network subject to DOL child labor investigations involving more than 4,000 violations across the industry. Multiple franchisees cited for minors working excessive hours and operating hazardous equipment. Over 13,000 minor-aged workers affected industry-wide between 2017 and 2021.',
                'pattern_summary': 'Child labor violations concentrated in franchise operations where corporate oversight of labor scheduling is limited. DOL identified more than 4,000 violations involving over 13,000 minor-aged workers in the broader restaurant industry between 2017 and 2021, with multiple McDonald\'s franchisees among those cited. Pattern reflects industry-wide pressure to fill labor gaps with teenage workers post-pandemic.',
            }
        )

        mcd_stats = [
            {'label': 'Franchisee child labor cases', 'value': 'Multiple', 'context': 'DOL citations across multiple states', 'sort_order': 1},
            {'label': 'Industry minor worker violations', 'value': '4,000+', 'context': 'DOL found 2017-2021 across restaurant industry', 'sort_order': 2},
        ]
        for s in mcd_stats:
            SnapshotStat.objects.get_or_create(company=mcd, label=s['label'], defaults={**s, 'source_url': ''})

        mcd_events = [
            {
                'date': date(2022, 12, 6),
                'title': 'DOL cites Pittsburgh McDonald\'s franchisee for child labor violations involving 100+ minors',
                'description': 'McDonald\'s franchisee Santonastasso Enterprises LLC accused of child labor violations involving more than 100 employees aged 14-15. DOL Wage and Hour Division investigated scheduling and work hour compliance at Pittsburgh-area locations.',
                'domain': 'labor', 'severity': 'serious',
                'source_agency': 'DOL Wage and Hour Division',
                'source_url': 'https://www.dol.gov/',
                'penalty_amount': None, 'facility_location': 'Pittsburgh, PA',
            },
        ]
        for e in mcd_events:
            AccountabilityEvent.objects.get_or_create(company=mcd, date=e['date'], title=e['title'], defaults=e)

        for s in [
            {'source_name': 'DOL Wage and Hour Division', 'source_agency': 'Dept of Labor', 'source_url': 'https://www.dol.gov/', 'last_checked': date(2025, 5, 22)},
            {'source_name': 'OSHA Inspections', 'source_agency': 'OSHA', 'source_url': 'https://www.osha.gov/', 'last_checked': date(2025, 5, 22)},
        ]:
            DataSource.objects.get_or_create(company=mcd, source_name=s['source_name'], defaults=s)

        # Summary
        for company in [sbux, boeing, chipotle, ns, mcd]:
            self.stdout.write(self.style.SUCCESS(
                f'Seeded {company.name}: {company.events.count()} events, '
                f'{company.snapshot_stats.count()} stats, '
                f'{company.data_sources.count()} sources'
            ))
