import csv
import os
from datetime import datetime, date
from decimal import Decimal, InvalidOperation
from collections import defaultdict
from django.core.management.base import BaseCommand
from warden.models import Company, AccountabilityEvent, DataSource


class Command(BaseCommand):
    help = 'Load OSHA data from local CSV bulk downloads'

    def add_arguments(self, parser):
        parser.add_argument('--company', type=str, default='', help='Single company slug')
        parser.add_argument('--since', type=int, default=2018, help='Only load inspections since this year')

    def build_aliases(self):
        """Map search strings to company slugs"""
        return {
            'AMAZON.COM SERVICES': 'amazon', 'AMAZON FULFILLMENT': 'amazon',
            'AMAZON LOGISTICS': 'amazon', 'AMAZON.COM': 'amazon',
            'WHOLE FOODS MARKET': 'amazon',
            'WAL-MART': 'walmart', 'WALMART': 'walmart', 'SAM\'S CLUB': 'walmart',
            'DOLLAR GENERAL': 'dollar-general', 'DOLGENCORP': 'dollar-general',
            'TESLA': 'tesla', 'TESLA MOTORS': 'tesla',
            'TYSON FOODS': 'tyson-foods', 'TYSON FRESH MEATS': 'tyson-foods',
            'TYSON POULTRY': 'tyson-foods', 'IBP FRESH MEATS': 'tyson-foods',
            'FEDEX': 'fedex', 'FEDERAL EXPRESS': 'fedex',
            'FEDEX GROUND': 'fedex', 'FEDEX FREIGHT': 'fedex',
            'STARBUCKS': 'starbucks', 'STARBUCKS COFFEE': 'starbucks',
            'BOEING': 'boeing', 'THE BOEING COMPANY': 'boeing',
            'CHIPOTLE': 'chipotle', 'CHIPOTLE MEXICAN GRILL': 'chipotle',
            'NORFOLK SOUTHERN': 'norfolk-southern',
            'MCDONALDS': 'mcdonalds', 'MCDONALD\'S': 'mcdonalds',
            'META PLATFORMS': 'meta', 'FACEBOOK': 'meta',
            'WELLS FARGO': 'wells-fargo', 'WELLS FARGO BANK': 'wells-fargo',
            'GOOGLE': 'google', 'ALPHABET': 'google',
            'JBS USA': 'jbs', 'JBS SWIFT': 'jbs', 'JBS PACKERLAND': 'jbs',
            'PILGRIM\'S PRIDE': 'jbs', 'PILGRIMS PRIDE': 'jbs',
            'SPACE EXPLORATION TECHNOLOGIES': 'spacex', 'SPACEX': 'spacex',
            'UBER TECHNOLOGIES': 'uber',
            'APPLE INC': 'apple',
            'EXXON MOBIL': 'exxonmobil', 'EXXONMOBIL': 'exxonmobil',
            'UNITEDHEALTH': 'unitedhealth-group', 'UNITEDHEALTHCARE': 'unitedhealth-group',
            'HOME DEPOT': 'home-depot', 'THE HOME DEPOT': 'home-depot',
            'TARGET': 'target', 'TARGET STORES': 'target',
            'COSTCO': 'costco', 'COSTCO WHOLESALE': 'costco',
            'KROGER': 'kroger', 'THE KROGER': 'kroger',
            'LOWE\'S': 'lowes', 'LOWES': 'lowes',
            'GENERAL MOTORS': 'general-motors',
            'FORD MOTOR': 'ford-motor',
            'CATERPILLAR': 'caterpillar',
            'HONEYWELL': 'honeywell',
            '3M COMPANY': '3m', '3M': '3m',
            'GENERAL ELECTRIC': 'general-electric',
            'LOCKHEED MARTIN': 'lockheed-martin',
            'NORTHROP GRUMMAN': 'northrop-grumman',
            'JOHNSON & JOHNSON': 'johnson-and-johnson',
            'PROCTER & GAMBLE': 'procter-and-gamble',
            'COCA-COLA': 'coca-cola', 'THE COCA-COLA': 'coca-cola',
            'PEPSICO': 'pepsico', 'FRITO-LAY': 'pepsico', 'PEPSI': 'pepsico',
            'UNITED PARCEL SERVICE': 'united-parcel-service', 'UPS': 'united-parcel-service',
            'DEERE & COMPANY': 'deere-and-company', 'JOHN DEERE': 'deere-and-company',
            'CUMMINS': 'cummins',
            'DUKE ENERGY': 'duke-energy',
            'SOUTHERN COMPANY': 'southern-company',
            'CHEVRON': 'chevron',
            'CONOCOPHILLIPS': 'conocophillips',
            'MARATHON PETROLEUM': 'marathon-petroleum',
            'VALERO ENERGY': 'valero-energy', 'VALERO': 'valero-energy',
            'PHILLIPS 66': 'phillips-66',
            'HCA HEALTHCARE': 'hca-healthcare', 'HCA': 'hca-healthcare',
            'DAVITA': 'davita',
            'CVS HEALTH': 'cvs-health', 'CVS PHARMACY': 'cvs-health',
            'WALGREENS': 'walgreens-boots-alliance',
            'SYSCO': 'sysco',
            'CARNIVAL': 'carnival-corporation',
            'MARRIOTT': 'marriott-international',
            'HILTON': 'hilton',
        }

    def match_company(self, estab_name, aliases, slug_filter=None):
        """Match establishment name to a company slug"""
        if not estab_name:
            return None
        name_upper = estab_name.upper().strip()
        for alias, slug in aliases.items():
            if slug_filter and slug != slug_filter:
                continue
            if alias in name_upper:
                return slug
        return None

    def handle(self, *args, **kwargs):
        company_slug = kwargs['company']
        since_year = kwargs['since']

        inspection_path = os.path.join('data', 'inspection.csv')
        violation_path = os.path.join('data', 'violation.csv')

        if not os.path.exists(inspection_path) or not os.path.exists(violation_path):
            self.stdout.write(self.style.ERROR('Missing data/inspection.csv or data/violation.csv'))
            return

        aliases = self.build_aliases()
        company_cache = {c.slug: c for c in Company.objects.all()}

        # Step 1: Scan inspections, collect matching activity_nrs
        self.stdout.write('Step 1: Scanning inspections...')
        matched_inspections = {}  # activity_nr -> {inspection data}
        total_scanned = 0

        with open(inspection_path, 'r', encoding='utf-8', errors='replace') as f:
            reader = csv.DictReader(f)
            for row in reader:
                total_scanned += 1
                if total_scanned % 500000 == 0:
                    self.stdout.write(f'  Scanned {total_scanned:,} inspections, {len(matched_inspections)} matched...')

                # Date filter
                open_date_str = row.get('OPEN_DATE', '')
                if not open_date_str:
                    continue
                try:
                    year = int(open_date_str[:4])
                    if year < since_year:
                        continue
                except (ValueError, IndexError):
                    continue

                estab_name = row.get('ESTAB_NAME', '')
                slug = self.match_company(estab_name, aliases, company_slug or None)
                if not slug or slug not in company_cache:
                    continue

                activity_nr = row.get('ACTIVITY_NR', '').strip()
                if not activity_nr:
                    continue

                matched_inspections[activity_nr] = {
                    'slug': slug,
                    'estab_name': estab_name,
                    'site_city': row.get('SITE_CITY', '').strip(),
                    'site_state': row.get('SITE_STATE', '').strip(),
                    'open_date': open_date_str,
                }

        self.stdout.write(self.style.SUCCESS(
            f'  Scanned {total_scanned:,} inspections. {len(matched_inspections)} matched.'
        ))

        if not matched_inspections:
            self.stdout.write('No matching inspections found.')
            return

        # Step 2: Scan violations, group by activity_nr
        self.stdout.write('Step 2: Scanning violations...')
        violations_by_insp = defaultdict(list)
        total_viols = 0

        with open(violation_path, 'r', encoding='utf-8', errors='replace') as f:
            reader = csv.DictReader(f)
            for row in reader:
                total_viols += 1
                if total_viols % 1000000 == 0:
                    self.stdout.write(f'  Scanned {total_viols:,} violations...')

                activity_nr = row.get('ACTIVITY_NR', '').strip()
                if activity_nr in matched_inspections:
                    violations_by_insp[activity_nr].append(row)

        self.stdout.write(self.style.SUCCESS(
            f'  Scanned {total_viols:,} violations. {len(violations_by_insp)} inspections have violations.'
        ))

        # Step 3: Create events
        self.stdout.write('Step 3: Creating events...')
        created = 0
        skipped = 0

        for activity_nr, insp_data in matched_inspections.items():
            violations = violations_by_insp.get(activity_nr, [])
            if not violations:
                continue

            slug = insp_data['slug']
            company = company_cache[slug]

            # Check if already exists
            if AccountabilityEvent.objects.filter(
                company=company,
                source_document=f'OSHA Activity #{activity_nr}'
            ).exists():
                skipped += 1
                continue

            # Parse date
            try:
                open_date = datetime.fromisoformat(insp_data['open_date'].replace('Z', '')).date()
            except (ValueError, TypeError):
                try:
                    open_date = datetime.strptime(insp_data['open_date'][:10], '%Y-%m-%d').date()
                except:
                    continue

            # Location
            city = insp_data['site_city']
            state = insp_data['site_state']
            location = f"{city}, {state}" if city and state else state or city

            # Process violations
            active_violations = [v for v in violations if v.get('delete_flag', '').strip() != 'X']
            if not active_violations:
                continue

            total_penalty = Decimal('0')
            serious_count = 0
            viol_type_counts = {}
            type_labels = {
                'S': 'serious', 'W': 'willful', 'R': 'repeat',
                'O': 'other-than-serious', 'U': 'unclassified'
            }

            for v in active_violations:
                vtype = v.get('viol_type', '').strip()
                label = type_labels.get(vtype, vtype)
                viol_type_counts[label] = viol_type_counts.get(label, 0) + 1
                if vtype in ('S', 'W', 'R'):
                    serious_count += 1
                try:
                    penalty = Decimal(str(v.get('current_penalty', '0')).strip() or '0')
                    total_penalty += penalty
                except (InvalidOperation, TypeError):
                    pass

            viol_count = len(active_violations)

            # Severity
            if 'willful' in viol_type_counts:
                severity = 'critical'
            elif 'repeat' in viol_type_counts:
                severity = 'serious'
            elif serious_count > 0:
                severity = 'serious'
            else:
                severity = 'moderate'

            # Title
            if serious_count > 0:
                title = f"OSHA cited {serious_count} serious violation(s) at {location}"
            else:
                title = f"OSHA inspection found {viol_count} violation(s) at {location}"

            # Description
            type_strs = [f"{count} {vtype}" for vtype, count in viol_type_counts.items()]
            description = (
                f"OSHA inspection of {insp_data['estab_name']} at {location}. "
                f"Found {viol_count} violation(s): {', '.join(type_strs)}."
            )
            if total_penalty > 0:
                description += f" Total penalties: ${total_penalty:,.0f}."

            AccountabilityEvent.objects.create(
                company=company,
                date=open_date,
                title=title,
                description=description,
                domain='workplace',
                severity=severity,
                source_agency='OSHA / Dept of Labor',
                source_url=f'https://www.osha.gov/ords/imis/establishment.inspection_detail?id={activity_nr}',
                source_document=f'OSHA Activity #{activity_nr}',
                penalty_amount=total_penalty if total_penalty > 0 else None,
                facility_location=location,
            )
            created += 1

        # Update data sources
        slugs_updated = set(d['slug'] for d in matched_inspections.values())
        for slug in slugs_updated:
            if slug in company_cache:
                DataSource.objects.update_or_create(
                    company=company_cache[slug],
                    source_name='OSHA Enforcement Data (Bulk)',
                    defaults={
                        'source_agency': 'Dept of Labor / OSHA',
                        'source_url': 'https://enforcedata.dol.gov/',
                        'last_checked': date.today(),
                    }
                )

        self.stdout.write(self.style.SUCCESS(
            f'\nComplete: {created} events created, {skipped} skipped (already exist)'
        ))
