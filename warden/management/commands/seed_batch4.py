from django.core.management.base import BaseCommand
from datetime import date
from decimal import Decimal
from warden.models import (
    Industry, Company, AccountabilityEvent, DataSource, SnapshotStat
)


class Command(BaseCommand):
    help = 'Seed Meta, Wells Fargo, Google, JBS, SpaceX, Uber, Apple, ExxonMobil'

    def handle(self, *args, **kwargs):
        tech, _ = Industry.objects.get_or_create(slug='technology', defaults={'name': 'Technology'})
        banking, _ = Industry.objects.get_or_create(slug='banking', defaults={'name': 'Banking & Financial Services'})
        meat, _ = Industry.objects.get_or_create(slug='meatpacking', defaults={'name': 'Meatpacking & Food Processing'})
        aero, _ = Industry.objects.get_or_create(slug='aerospace', defaults={'name': 'Aerospace & Defense'})
        transport, _ = Industry.objects.get_or_create(slug='rideshare', defaults={'name': 'Rideshare & Gig Economy'})
        oil, _ = Industry.objects.get_or_create(slug='oil-gas', defaults={'name': 'Oil & Gas'})
        consumer_tech, _ = Industry.objects.get_or_create(slug='consumer-tech', defaults={'name': 'Consumer Technology'})

        companies_data = [
            # ==================== META ====================
            {
                'slug': 'meta',
                'company': {
                    'name': 'Meta', 'legal_name': 'Meta Platforms, Inc.',
                    'industry': tech, 'employee_count': 67000,
                    'description': 'Parent company of Facebook, Instagram, and WhatsApp. Underwent largest mass layoffs in tech history in 2022-2023, eliminating approximately 21,000 positions.',
                    'headquarters': 'Menlo Park, CA', 'stock_ticker': 'META',
                    'website': 'https://www.meta.com', 'risk_level': 'mixed',
                    'summary_line': 'Approximately 21,000 employees laid off in two rounds (2022-2023). FTC imposed record $5 billion penalty for privacy violations. 158 WARN Act notices filed affecting 12,000+ workers.',
                    'pattern_summary': 'Unprecedented workforce reduction of approximately 25% in two waves — 11,000 in November 2022 and 10,000 beginning March 2023. FTC levied largest-ever penalty against any company ($5 billion) for deceiving users about privacy controls and violating a 2012 consent decree. Pattern of aggressive growth followed by rapid contraction with significant human cost.',
                },
                'stats': [
                    {'label': 'Total layoffs (2022-2023)', 'value': '~21,000', 'context': '11,000 (Nov 2022) + 10,000 (Mar 2023)', 'sort_order': 1},
                    {'label': 'WARN Act notices filed', 'value': '158', 'context': 'From Jan 2017 to May 2026', 'sort_order': 2},
                    {'label': 'FTC privacy penalty', 'value': '$5B', 'context': 'Largest FTC penalty ever — 2019', 'sort_order': 3},
                ],
                'events': [
                    {
                        'date': date(2023, 3, 14), 'title': 'Meta announces second round of layoffs — 10,000 additional employees',
                        'description': 'CEO Mark Zuckerberg announced elimination of 10,000 more positions across recruiting, business, and technology teams. Layoffs rolled out in waves through March, April, and May 2023. Combined with November 2022 cuts, approximately 25% of workforce eliminated.',
                        'domain': 'labor', 'severity': 'critical', 'source_agency': 'SEC Filing (8-K)',
                        'source_url': 'https://www.sec.gov/Archives/edgar/data/0001326801/000132680123000035/meta-20230314.htm',
                        'penalty_amount': None, 'facility_location': 'Corporate-wide',
                    },
                    {
                        'date': date(2022, 11, 9), 'title': 'Meta lays off 11,000 employees — 13% of workforce',
                        'description': 'Largest mass layoff in Meta history. CEO cited macroeconomic downturn, increased competition, and ads signal loss. Employees received 16 weeks base severance plus two additional weeks per year of service.',
                        'domain': 'labor', 'severity': 'critical', 'source_agency': 'SEC Filing (8-K)',
                        'source_url': 'https://www.sec.gov/Archives/edgar/data/0001326801/000132680122000116/nov092022exhibit991.htm',
                        'penalty_amount': None, 'facility_location': 'Corporate-wide',
                    },
                    {
                        'date': date(2019, 7, 24), 'title': 'FTC imposes record $5 billion penalty on Facebook for privacy violations',
                        'description': 'Largest penalty ever imposed by the FTC on any company. Facebook violated its privacy promises to consumers and a 2012 FTC consent order. Company deceived users about their ability to control personal information privacy. New restrictions imposed on business operations.',
                        'domain': 'consumer', 'severity': 'critical', 'source_agency': 'FTC',
                        'source_url': 'https://www.ftc.gov/news-events/news/press-releases/2019/07/ftc-imposes-5-billion-penalty-sweeping-new-privacy-restrictions-facebook',
                        'penalty_amount': Decimal('5000000000'), 'facility_location': 'Corporate-wide',
                    },
                ],
                'sources': [
                    {'source_name': 'SEC Filings (8-K)', 'source_agency': 'SEC', 'source_url': 'https://www.sec.gov/', 'last_checked': date(2025, 5, 22)},
                    {'source_name': 'WARN Act Notices', 'source_agency': 'State Labor Departments', 'source_url': 'https://www.warntracker.com/company/meta-facebook', 'last_checked': date(2025, 5, 22)},
                    {'source_name': 'FTC Enforcement Actions', 'source_agency': 'FTC', 'source_url': 'https://www.ftc.gov/', 'last_checked': date(2025, 5, 22)},
                ],
            },
            # ==================== WELLS FARGO ====================
            {
                'slug': 'wells-fargo',
                'company': {
                    'name': 'Wells Fargo', 'legal_name': 'Wells Fargo & Company',
                    'industry': banking, 'employee_count': 227000,
                    'description': 'One of the largest banks in the United States. Subject of one of the most extensive corporate fraud scandals in American banking history.',
                    'headquarters': 'San Francisco, CA', 'stock_ticker': 'WFC',
                    'website': 'https://www.wellsfargo.com', 'risk_level': 'elevated',
                    'summary_line': 'Created approximately 3.5 million unauthorized accounts. Over $4.5 billion in cumulative regulatory penalties. Operated under Federal Reserve asset cap from 2018 to 2025. 11 former executives subject to OCC enforcement actions.',
                    'pattern_summary': 'Systemic consumer fraud driven by aggressive sales culture and incentive structures. Employees created millions of unauthorized accounts over a multi-year period. Regulatory response included unprecedented Fed asset cap limiting company growth, billions in CFPB penalties, OCC consent orders, and DOJ fines. Pattern of violations extended beyond fake accounts to auto-loan insurance overcharges, mortgage abuses, and improper fee practices.',
                },
                'stats': [
                    {'label': 'Unauthorized accounts created', 'value': '3.5M+', 'context': 'Deposit and credit card accounts', 'sort_order': 1},
                    {'label': 'CFPB penalty (2022)', 'value': '$3.7B', 'context': '$2B consumer restitution + $1.7B fine', 'sort_order': 2},
                    {'label': 'Executives subject to OCC action', 'value': '11', 'context': 'Including CEO, fines totaling $60M+', 'sort_order': 3},
                    {'label': 'Fed asset cap duration', 'value': '7 years', 'context': '2018-2025', 'sort_order': 4},
                ],
                'events': [
                    {
                        'date': date(2025, 1, 15), 'title': 'OCC fines three former Wells Fargo executives $18.5M over fake accounts scandal',
                        'description': 'OCC banned former community bank group risk officer from banking industry for life with $10M penalty. Two additional executives fined $7M and $1.5M. Actions are last OCC penalties against 11 executives linked to fake accounts scandal.',
                        'domain': 'governance', 'severity': 'serious', 'source_agency': 'OCC',
                        'source_url': 'https://www.occ.treas.gov/', 'penalty_amount': Decimal('18500000'), 'facility_location': 'Corporate-wide',
                    },
                    {
                        'date': date(2022, 12, 20), 'title': 'CFPB orders Wells Fargo to pay $3.7 billion for widespread consumer abuses',
                        'description': 'CFPB ordered $2 billion in consumer restitution and $1.7 billion civil penalty for illegal practices across auto lending, mortgage servicing, and deposit accounts. Violations caused billions of dollars in financial harm including wrongful vehicle repossessions and home foreclosures.',
                        'domain': 'consumer', 'severity': 'critical', 'source_agency': 'CFPB',
                        'source_url': 'https://www.consumerfinance.gov/', 'penalty_amount': Decimal('3700000000'), 'facility_location': 'Corporate-wide',
                    },
                    {
                        'date': date(2018, 4, 1), 'title': 'Wells Fargo pays $1 billion settlement to CFPB and OCC for auto-loan and mortgage abuses',
                        'description': 'Settlement resolved issues related to auto-loan insurance overcharges (customers forced to pay for unnecessary insurance, some lost vehicles) and mortgage interest rate lock extension fees improperly charged to borrowers.',
                        'domain': 'consumer', 'severity': 'critical', 'source_agency': 'CFPB / OCC',
                        'source_url': 'https://www.consumerfinance.gov/', 'penalty_amount': Decimal('1000000000'), 'facility_location': 'Corporate-wide',
                    },
                    {
                        'date': date(2018, 2, 2), 'title': 'Federal Reserve imposes unprecedented asset cap on Wells Fargo',
                        'description': 'Fed ordered Wells Fargo to cap total assets at approximately $1.95 trillion until the company sufficiently improves governance and controls. Most significant Fed enforcement action against a major bank in modern history. Cap remained in effect until June 2025.',
                        'domain': 'governance', 'severity': 'critical', 'source_agency': 'Federal Reserve',
                        'source_url': 'https://www.federalreserve.gov/', 'penalty_amount': None, 'facility_location': 'Corporate-wide',
                    },
                    {
                        'date': date(2016, 9, 8), 'title': 'CFPB fines Wells Fargo $185M for secretly opening millions of unauthorized accounts',
                        'description': 'Employees opened over 2 million unauthorized deposit and credit card accounts to meet sales targets. CFPB levied $100M penalty (largest to date), OCC fined $35M, Los Angeles fined $50M. Over 5,300 employees terminated. CEO John Stumpf subsequently resigned.',
                        'domain': 'consumer', 'severity': 'critical', 'source_agency': 'CFPB / OCC',
                        'source_url': 'https://www.consumerfinance.gov/about-us/newsroom/consumer-financial-protection-bureau-fines-wells-fargo-100-million-widespread-illegal-practice-secretly-opening-unauthorized-accounts/',
                        'penalty_amount': Decimal('185000000'), 'facility_location': 'Corporate-wide',
                    },
                ],
                'sources': [
                    {'source_name': 'CFPB Enforcement Actions', 'source_agency': 'CFPB', 'source_url': 'https://www.consumerfinance.gov/', 'last_checked': date(2025, 5, 22)},
                    {'source_name': 'OCC Consent Orders', 'source_agency': 'OCC', 'source_url': 'https://www.occ.treas.gov/', 'last_checked': date(2025, 5, 22)},
                    {'source_name': 'Federal Reserve Orders', 'source_agency': 'Federal Reserve', 'source_url': 'https://www.federalreserve.gov/', 'last_checked': date(2025, 5, 22)},
                    {'source_name': 'Congressional Research Service', 'source_agency': 'Library of Congress', 'source_url': 'https://www.congress.gov/crs-product/IF11129', 'last_checked': date(2025, 5, 22)},
                ],
            },
            # ==================== GOOGLE ====================
            {
                'slug': 'google',
                'company': {
                    'name': 'Google (Alphabet)', 'legal_name': 'Alphabet Inc.',
                    'industry': tech, 'employee_count': 183000,
                    'description': 'Parent company of Google, the dominant search engine, advertising platform, and cloud services provider. Also operates YouTube, Android, and Waymo.',
                    'headquarters': 'Mountain View, CA', 'stock_ticker': 'GOOGL',
                    'website': 'https://www.google.com', 'risk_level': 'mixed',
                    'summary_line': 'DOJ won antitrust case finding Google maintained illegal monopoly in search (August 2024). Approximately 12,000 employees laid off in January 2023. NLRB found violations related to worker organizing and employee speech.',
                    'pattern_summary': 'Federal antitrust ruling determined Google illegally maintained monopoly power in search through exclusive distribution agreements worth billions annually. Concurrent with monopoly finding, company underwent significant workforce reduction. NLRB actions found violations of employee rights to organize and discuss workplace conditions.',
                },
                'stats': [
                    {'label': 'DOJ antitrust ruling', 'value': 'Monopoly', 'context': 'Illegal monopoly in search — August 2024', 'sort_order': 1},
                    {'label': 'Layoffs (Jan 2023)', 'value': '12,000', 'context': 'Approximately 6% of global workforce', 'sort_order': 2},
                ],
                'events': [
                    {
                        'date': date(2024, 8, 5), 'title': 'Federal judge rules Google illegally maintained monopoly in search',
                        'description': 'U.S. District Judge Amit Mehta ruled that Google violated antitrust law by maintaining an illegal monopoly in the search market. Court found Google paid billions annually (estimated $26B+ in 2021) to Apple, Samsung, and browser makers to be the default search engine, foreclosing competition.',
                        'domain': 'governance', 'severity': 'critical', 'source_agency': 'DOJ / U.S. District Court (D.C.)',
                        'source_url': 'https://www.justice.gov/', 'penalty_amount': None, 'facility_location': 'Washington, DC (Federal Court)',
                    },
                    {
                        'date': date(2023, 1, 20), 'title': 'Google lays off approximately 12,000 employees — 6% of global workforce',
                        'description': 'CEO Sundar Pichai announced elimination of approximately 12,000 roles across the company. Affected employees in the US received 16 weeks severance plus two weeks for each additional year of tenure. Layoffs part of broader tech industry workforce contraction.',
                        'domain': 'labor', 'severity': 'serious', 'source_agency': 'SEC Filing / Public Announcement',
                        'source_url': 'https://www.sec.gov/', 'penalty_amount': None, 'facility_location': 'Corporate-wide',
                    },
                ],
                'sources': [
                    {'source_name': 'DOJ Antitrust Division', 'source_agency': 'DOJ', 'source_url': 'https://www.justice.gov/', 'last_checked': date(2025, 5, 22)},
                    {'source_name': 'SEC Filings', 'source_agency': 'SEC', 'source_url': 'https://www.sec.gov/', 'last_checked': date(2025, 5, 22)},
                    {'source_name': 'NLRB Decisions', 'source_agency': 'NLRB', 'source_url': 'https://www.nlrb.gov/', 'last_checked': date(2025, 5, 22)},
                ],
            },
            # ==================== JBS ====================
            {
                'slug': 'jbs',
                'company': {
                    'name': 'JBS', 'legal_name': 'JBS USA Holdings, Inc.',
                    'industry': meat, 'employee_count': 250000,
                    'description': 'Largest meat processing company in the world. US subsidiary operates beef, pork, and poultry processing plants across multiple states.',
                    'headquarters': 'Greeley, CO', 'stock_ticker': 'JBSAY',
                    'website': 'https://www.jbssa.com', 'risk_level': 'elevated',
                    'summary_line': 'Pled guilty to federal price-fixing charges with $52.5M criminal fine. Connected to child labor investigations through subcontractor PSSI which employed 100+ children at JBS and other meatpacking facilities. History of OSHA violations at processing plants.',
                    'pattern_summary': 'Antitrust violations in beef pricing combined with workplace safety and child labor concerns across processing operations. DOJ price-fixing prosecution part of broader investigation into meatpacking industry collusion. Child labor enforcement at JBS facilities revealed children as young as 13 cleaning equipment with hazardous chemicals through subcontractor networks.',
                },
                'stats': [
                    {'label': 'Price-fixing criminal fine', 'value': '$52.5M', 'context': 'DOJ antitrust — pled guilty', 'sort_order': 1},
                    {'label': 'Child labor connection', 'value': 'PSSI', 'context': 'Subcontractor employed 100+ children at meatpacking plants', 'sort_order': 2},
                ],
                'events': [
                    {
                        'date': date(2024, 4, 1), 'title': 'JBS subsidiary Pilgrim\'s Pride completes price-fixing guilty plea and $107M penalty',
                        'description': 'Pilgrim\'s Pride, a JBS subsidiary that is the second-largest chicken producer in the US, pled guilty to conspiracy to fix prices and rig bids for broiler chicken products. Combined with parent company JBS\'s $52.5M beef price-fixing fine, total antitrust penalties exceeded $150M.',
                        'domain': 'governance', 'severity': 'critical', 'source_agency': 'DOJ Antitrust Division',
                        'source_url': 'https://www.justice.gov/', 'penalty_amount': Decimal('107000000'), 'facility_location': 'Corporate-wide',
                    },
                    {
                        'date': date(2023, 2, 17), 'title': 'DOL fines subcontractor PSSI $1.5M for employing 100+ children at JBS and other meatpacking plants',
                        'description': 'Packers Sanitation Services Inc. (PSSI), which provided cleaning services at JBS and other meatpacking facilities, fined for employing over 100 children as young as 13 to clean equipment with hazardous chemicals at plants in eight states.',
                        'domain': 'labor', 'severity': 'critical', 'source_agency': 'DOL Wage and Hour Division',
                        'source_url': 'https://www.dol.gov/', 'penalty_amount': Decimal('1500000'), 'facility_location': 'Multiple states (8)',
                    },
                ],
                'sources': [
                    {'source_name': 'DOJ Antitrust Division', 'source_agency': 'DOJ', 'source_url': 'https://www.justice.gov/', 'last_checked': date(2025, 5, 22)},
                    {'source_name': 'DOL Wage and Hour Division', 'source_agency': 'Dept of Labor', 'source_url': 'https://www.dol.gov/', 'last_checked': date(2025, 5, 22)},
                    {'source_name': 'OSHA Inspections', 'source_agency': 'OSHA', 'source_url': 'https://www.osha.gov/', 'last_checked': date(2025, 5, 22)},
                ],
            },
            # ==================== SPACEX ====================
            {
                'slug': 'spacex',
                'company': {
                    'name': 'SpaceX', 'legal_name': 'Space Exploration Technologies Corp.',
                    'industry': aero, 'employee_count': 13000,
                    'description': 'Private aerospace manufacturer and space transportation company. Operates launch facilities in Texas, Florida, and California.',
                    'headquarters': 'Hawthorne, CA', 'stock_ticker': '',
                    'website': 'https://www.spacex.com', 'risk_level': 'mixed',
                    'summary_line': 'Fired employees who circulated open letter criticizing CEO conduct — NLRB filed complaint finding terminations unlawful. Multiple OSHA investigations at Starbase facility in Texas. DOJ sued for hiring discrimination against refugees and asylum seekers.',
                    'pattern_summary': 'Pattern of retaliatory action against employees who raised workplace concerns. NLRB found SpaceX unlawfully terminated workers for protected concerted activity. Company challenged NLRB\'s constitutionality in federal court rather than engage with labor board process. Concurrent DOJ discrimination lawsuit alleged company illegally refused to hire non-US citizens and non-permanent residents.',
                },
                'stats': [
                    {'label': 'Employees fired for open letter', 'value': '8', 'context': 'NLRB found terminations unlawful', 'sort_order': 1},
                    {'label': 'DOJ hiring discrimination suit', 'value': 'Active', 'context': 'Alleged discrimination against refugees/asylum seekers', 'sort_order': 2},
                ],
                'events': [
                    {
                        'date': date(2024, 1, 3), 'title': 'NLRB files complaint alleging SpaceX illegally fired employees for open letter',
                        'description': 'NLRB complaint alleges SpaceX unlawfully terminated eight employees who drafted and circulated an open letter in June 2022 criticizing CEO Elon Musk\'s public conduct and calling for the company to enforce its harassment policies. SpaceX challenged NLRB\'s constitutionality in federal court.',
                        'domain': 'labor', 'severity': 'serious', 'source_agency': 'NLRB',
                        'source_url': 'https://www.nlrb.gov/', 'penalty_amount': None, 'facility_location': 'Hawthorne, CA',
                    },
                    {
                        'date': date(2023, 8, 24), 'title': 'DOJ sues SpaceX for hiring discrimination against refugees and asylum seekers',
                        'description': 'Department of Justice filed lawsuit alleging SpaceX discriminated against asylum seekers and refugees in hiring from at least September 2018 to May 2022. Company allegedly discouraged asylum seekers and refugees from applying and refused to hire or consider them.',
                        'domain': 'labor', 'severity': 'serious', 'source_agency': 'DOJ',
                        'source_url': 'https://www.justice.gov/', 'penalty_amount': None, 'facility_location': 'Corporate-wide',
                    },
                ],
                'sources': [
                    {'source_name': 'NLRB Complaints', 'source_agency': 'NLRB', 'source_url': 'https://www.nlrb.gov/', 'last_checked': date(2025, 5, 22)},
                    {'source_name': 'DOJ Civil Rights Division', 'source_agency': 'DOJ', 'source_url': 'https://www.justice.gov/', 'last_checked': date(2025, 5, 22)},
                    {'source_name': 'OSHA Inspections', 'source_agency': 'OSHA', 'source_url': 'https://www.osha.gov/', 'last_checked': date(2025, 5, 22)},
                ],
            },
            # ==================== UBER ====================
            {
                'slug': 'uber',
                'company': {
                    'name': 'Uber', 'legal_name': 'Uber Technologies, Inc.',
                    'industry': transport, 'employee_count': 32800,
                    'description': 'Rideshare and delivery platform operating in 70+ countries. Central figure in worker classification debates globally.',
                    'headquarters': 'San Francisco, CA', 'stock_ticker': 'UBER',
                    'website': 'https://www.uber.com', 'risk_level': 'mixed',
                    'summary_line': 'Multiple state and international enforcement actions over driver classification as independent contractors vs employees. $100M+ in settlements across jurisdictions. Subject of ongoing regulatory actions regarding worker protections, benefits, and minimum wage compliance.',
                    'pattern_summary': 'Persistent regulatory conflict over driver employment classification across multiple jurisdictions. Business model premised on classifying drivers as independent contractors despite significant operational control. Pattern of regulatory settlements followed by continued classification disputes in new jurisdictions.',
                },
                'stats': [
                    {'label': 'Worker classification settlements', 'value': '$100M+', 'context': 'Across multiple states and countries', 'sort_order': 1},
                    {'label': 'Active classification disputes', 'value': 'Multiple', 'context': 'Ongoing in US, EU, and UK jurisdictions', 'sort_order': 2},
                ],
                'events': [
                    {
                        'date': date(2023, 6, 13), 'title': 'Uber pays $290M to settle New York driver wage theft claims',
                        'description': 'New York Attorney General reached $290 million settlement with Uber over allegations the company shortchanged drivers on earnings by deducting sales taxes and fees from driver pay rather than from passenger fares. Affected approximately 100,000 current and former drivers.',
                        'domain': 'labor', 'severity': 'critical', 'source_agency': 'New York Attorney General',
                        'source_url': 'https://ag.ny.gov/', 'penalty_amount': Decimal('290000000'), 'facility_location': 'New York',
                    },
                    {
                        'date': date(2022, 3, 17), 'title': 'UK Supreme Court upholds ruling that Uber drivers are workers, not contractors',
                        'description': 'UK Supreme Court unanimously ruled Uber drivers are workers entitled to minimum wage, holiday pay, and other protections. Court found Uber\'s characterization of drivers as independent contractors did not reflect the reality of the working relationship.',
                        'domain': 'labor', 'severity': 'serious', 'source_agency': 'UK Supreme Court',
                        'source_url': '', 'penalty_amount': None, 'facility_location': 'United Kingdom',
                    },
                ],
                'sources': [
                    {'source_name': 'State Attorney General Actions', 'source_agency': 'State AGs', 'source_url': '', 'last_checked': date(2025, 5, 22)},
                    {'source_name': 'DOL Worker Classification', 'source_agency': 'Dept of Labor', 'source_url': 'https://www.dol.gov/', 'last_checked': date(2025, 5, 22)},
                ],
            },
            # ==================== APPLE ====================
            {
                'slug': 'apple',
                'company': {
                    'name': 'Apple', 'legal_name': 'Apple Inc.',
                    'industry': consumer_tech, 'employee_count': 161000,
                    'description': 'Consumer technology company. World\'s most valuable public company. Operates retail stores and manages global supply chain manufacturing relationships.',
                    'headquarters': 'Cupertino, CA', 'stock_ticker': 'AAPL',
                    'website': 'https://www.apple.com', 'risk_level': 'mixed',
                    'summary_line': 'NLRB found violations related to restricting employee use of workplace communication tools. DOJ filed landmark antitrust lawsuit alleging illegal smartphone monopoly. Supply chain labor controversies in manufacturing partner facilities.',
                    'pattern_summary': 'Federal antitrust action alleges Apple illegally maintained smartphone monopoly through restrictive practices. NLRB enforcement found violations of employee rights to discuss wages and working conditions through workplace tools. Long-running supply chain labor concerns at contract manufacturer facilities, particularly Foxconn operations in China.',
                },
                'stats': [
                    {'label': 'DOJ antitrust lawsuit', 'value': 'Active', 'context': 'Filed March 2024 — alleging smartphone monopoly', 'sort_order': 1},
                    {'label': 'NLRB violations found', 'value': 'Yes', 'context': 'Restricted employee speech on workplace tools', 'sort_order': 2},
                ],
                'events': [
                    {
                        'date': date(2024, 3, 21), 'title': 'DOJ files landmark antitrust lawsuit alleging Apple maintains illegal smartphone monopoly',
                        'description': 'Department of Justice and 16 state attorneys general filed civil antitrust lawsuit alleging Apple illegally maintains a monopoly in the smartphone market by selectively imposing contractual restrictions on developers, degrading cross-platform experiences, and limiting competitive threats.',
                        'domain': 'governance', 'severity': 'critical', 'source_agency': 'DOJ Antitrust Division',
                        'source_url': 'https://www.justice.gov/', 'penalty_amount': None, 'facility_location': 'Washington, DC (Federal Court)',
                    },
                    {
                        'date': date(2024, 1, 1), 'title': 'NLRB finds Apple violated labor law by restricting employee workplace communications',
                        'description': 'NLRB found Apple violated federal labor law by maintaining overly broad rules restricting employee use of Slack and other workplace communication tools to discuss wages, hours, and working conditions. Violations identified at multiple retail and corporate locations.',
                        'domain': 'labor', 'severity': 'moderate', 'source_agency': 'NLRB',
                        'source_url': 'https://www.nlrb.gov/', 'penalty_amount': None, 'facility_location': 'Corporate-wide',
                    },
                ],
                'sources': [
                    {'source_name': 'DOJ Antitrust Division', 'source_agency': 'DOJ', 'source_url': 'https://www.justice.gov/', 'last_checked': date(2025, 5, 22)},
                    {'source_name': 'NLRB Decisions', 'source_agency': 'NLRB', 'source_url': 'https://www.nlrb.gov/', 'last_checked': date(2025, 5, 22)},
                ],
            },
            # ==================== EXXONMOBIL ====================
            {
                'slug': 'exxonmobil',
                'company': {
                    'name': 'ExxonMobil', 'legal_name': 'Exxon Mobil Corporation',
                    'industry': oil, 'employee_count': 62000,
                    'description': 'Largest publicly traded oil and gas company in the United States. Major producer, refiner, and marketer of petroleum products globally.',
                    'headquarters': 'Spring, TX', 'stock_ticker': 'XOM',
                    'website': 'https://www.exxonmobil.com', 'risk_level': 'elevated',
                    'summary_line': 'Subject of multiple state attorney general lawsuits alleging consumer deception about climate change risks. EPA enforcement history at refineries and chemical plants. SEC settlement over climate-related asset valuation disclosures.',
                    'pattern_summary': 'Prolonged legal exposure from state AG climate deception lawsuits alleging company misled public and investors about climate risks despite internal knowledge. EPA enforcement actions at refinery and petrochemical operations for air quality and emissions violations. Environmental liability across decades of operations including Superfund site involvement.',
                },
                'stats': [
                    {'label': 'Active state AG climate lawsuits', 'value': 'Multiple', 'context': 'Alleging consumer deception about climate risks', 'sort_order': 1},
                    {'label': 'EPA enforcement history', 'value': 'Extensive', 'context': 'Refinery and chemical plant violations', 'sort_order': 2},
                ],
                'events': [
                    {
                        'date': date(2024, 9, 1), 'title': 'California AG climate deception lawsuit against ExxonMobil proceeds',
                        'description': 'California Attorney General\'s lawsuit alleging ExxonMobil engaged in decades-long campaign to deceive the public about climate change risks continued through discovery. State alleges company promoted fossil fuels while its own scientists documented climate risks from the 1970s onward.',
                        'domain': 'consumer', 'severity': 'serious', 'source_agency': 'California Attorney General',
                        'source_url': 'https://oag.ca.gov/', 'penalty_amount': None, 'facility_location': 'California (State Court)',
                    },
                    {
                        'date': date(2019, 12, 10), 'title': 'New York AG loses climate fraud case but increases regulatory scrutiny',
                        'description': 'New York Supreme Court ruled in ExxonMobil\'s favor in AG\'s lawsuit alleging the company defrauded investors by maintaining two sets of books for climate risk projections. Despite the ruling, the case intensified regulatory scrutiny of fossil fuel industry climate disclosures.',
                        'domain': 'governance', 'severity': 'moderate', 'source_agency': 'New York Attorney General',
                        'source_url': 'https://ag.ny.gov/', 'penalty_amount': None, 'facility_location': 'New York (State Court)',
                    },
                ],
                'sources': [
                    {'source_name': 'EPA Enforcement Actions', 'source_agency': 'EPA', 'source_url': 'https://www.epa.gov/', 'last_checked': date(2025, 5, 22)},
                    {'source_name': 'State AG Climate Litigation', 'source_agency': 'State AGs', 'source_url': '', 'last_checked': date(2025, 5, 22)},
                    {'source_name': 'SEC Filings', 'source_agency': 'SEC', 'source_url': 'https://www.sec.gov/', 'last_checked': date(2025, 5, 22)},
                ],
            },
        ]

        for data in companies_data:
            company, _ = Company.objects.get_or_create(slug=data['slug'], defaults=data['company'])

            for s in data['stats']:
                SnapshotStat.objects.get_or_create(company=company, label=s['label'], defaults={**s, 'source_url': ''})

            for e in data['events']:
                AccountabilityEvent.objects.get_or_create(company=company, date=e['date'], title=e['title'], defaults=e)

            for s in data['sources']:
                DataSource.objects.get_or_create(company=company, source_name=s['source_name'], defaults=s)

            self.stdout.write(self.style.SUCCESS(
                f'Seeded {company.name}: {company.events.count()} events, '
                f'{company.snapshot_stats.count()} stats, '
                f'{company.data_sources.count()} sources'
            ))
