import requests
import json
import time
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from django.core.management.base import BaseCommand
from warden.models import Company, AccountabilityEvent, DataSource
from collections import defaultdict


API_BASE = "https://apiprod.dol.gov/v4/get/OSHA"
API_KEY = "UJZ7dij3Ih8faol2vZosIqR4SfqaduiluEKIjahMXg0"


class Command(BaseCommand):
    help = 'Scrape OSHA enforcement data via DOL API'

    def add_arguments(self, parser):
        parser.add_argument('--company', type=str, default='', help='Single company slug')
        parser.add_argument('--limit', type=int, default=0, help='Limit companies to process')

    def api_request(self, endpoint, params=None, retries=3):
        """Make a request to the DOL API with retry on rate limit"""
        url = f"{API_BASE}/{endpoint}/json"
        if params is None:
            params = {}
        params['X-API-KEY'] = API_KEY

        for attempt in range(retries):
            try:
                response = requests.get(url, params=params, timeout=60)
                if response.status_code == 204:
                    return []
                if response.status_code == 429:
                    wait = 30 * (attempt + 1)
                    self.stdout.write(f"  Rate limited. Waiting {wait}s...")
                    time.sleep(wait)
                    continue
                response.raise_for_status()
                return response.json()
            except requests.exceptions.HTTPError as e:
                if '429' in str(e):
                    wait = 30 * (attempt + 1)
                    self.stdout.write(f"  Rate limited. Waiting {wait}s...")
                    time.sleep(wait)
                    continue
                self.stdout.write(self.style.ERROR(f"API error: {e}"))
                return []
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"API error: {e}"))
                return []
        return []

    def search_inspections(self, search_name):
        """Search for inspections by establishment name"""
        filter_obj = json.dumps({
            "and": [
                {"field": "estab_name", "operator": "like", "value": f"%{search_name}%"},
                {"field": "open_date", "operator": "gt", "value": "2018-01-01"}
            ]
        })
        params = {
            'limit': 100,
            'filter_object': filter_obj,
            'sort': 'desc',
            'sort_by': 'open_date',
        }
        return self.api_request('inspection', params)

    def get_violations_batch(self, activity_nrs):
        """Get violations for multiple inspections at once"""
        if not activity_nrs:
            return {}

        # Use 'in' operator to batch
        filter_obj = json.dumps({
            "field": "activity_nr",
            "operator": "in",
            "value": [int(a) for a in activity_nrs]
        })
        params = {
            'limit': 10000,
            'filter_object': filter_obj,
        }

        data = self.api_request('violation', params)
        if not data or not isinstance(data, list):
            return {}

        # Group by activity_nr
        grouped = defaultdict(list)
        for v in data:
            grouped[str(v.get('activity_nr', ''))].append(v)

        return grouped

    def handle(self, *args, **kwargs):
        company_slug = kwargs['company']
        limit = kwargs['limit']

        if company_slug:
            companies = Company.objects.filter(slug=company_slug)
        else:
            companies = Company.objects.exclude(risk_level='insufficient').order_by('name')
            if limit:
                companies = companies[:limit]

        self.stdout.write(f"Processing {companies.count()} companies")

        search_names = {
            'amazon': ['AMAZON.COM SERVICES', 'AMAZON FULFILLMENT'],
            'walmart': ['WAL-MART', 'WALMART'],
            'dollar-general': ['DOLLAR GENERAL', 'DOLGENCORP'],
            'tesla': ['TESLA'],
            'tyson-foods': ['TYSON FOODS', 'TYSON FRESH MEATS'],
            'fedex': ['FEDEX', 'FEDERAL EXPRESS'],
            'starbucks': ['STARBUCKS'],
            'boeing': ['BOEING'],
            'chipotle': ['CHIPOTLE'],
            'norfolk-southern': ['NORFOLK SOUTHERN'],
            'mcdonalds': ['MCDONALDS'],
            'meta': ['META PLATFORMS'],
            'wells-fargo': ['WELLS FARGO'],
            'google': ['GOOGLE'],
            'jbs': ['JBS USA', 'JBS SWIFT'],
            'spacex': ['SPACE EXPLORATION'],
            'uber': ['UBER TECHNOLOGIES'],
            'apple': ['APPLE INC'],
            'exxonmobil': ['EXXON MOBIL', 'EXXONMOBIL'],
            'unitedhealth-group': ['UNITEDHEALTH', 'UNITEDHEALTHCARE'],
        }

        total_created = 0
        total_skipped = 0

        for company in companies:
            names = search_names.get(company.slug, [company.name.upper()])
            company_events = 0

            for search_name in names:
                self.stdout.write(f"\nSearching: {search_name} ({company.name})")

                inspections = self.search_inspections(search_name)
                if not inspections or not isinstance(inspections, list):
                    self.stdout.write("  No inspections found")
                    continue

                self.stdout.write(f"  Found {len(inspections)} inspections")

                # Filter out already-imported inspections
                new_inspections = []
                for insp in inspections:
                    activity_nr = str(insp.get('activity_nr', ''))
                    if not AccountabilityEvent.objects.filter(
                        company=company,
                        source_document=f'OSHA Activity #{activity_nr}'
                    ).exists():
                        new_inspections.append(insp)
                    else:
                        total_skipped += 1

                if not new_inspections:
                    self.stdout.write("  All inspections already imported")
                    continue

                self.stdout.write(f"  {len(new_inspections)} new inspections to check")

                # Batch violation lookup — chunks of 20
                for i in range(0, len(new_inspections), 20):
                    chunk = new_inspections[i:i+20]
                    activity_nrs = [str(insp['activity_nr']) for insp in chunk]

                    self.stdout.write(f"  Fetching violations for batch {i//20 + 1}...")
                    violations_by_insp = self.get_violations_batch(activity_nrs)
                    time.sleep(2)  # Rate limit between batches

                    for insp in chunk:
                        activity_nr = str(insp['activity_nr'])
                        violations = violations_by_insp.get(activity_nr, [])

                        # Skip inspections with no violations
                        if not violations:
                            continue

                        # Parse date
                        open_date_str = insp.get('open_date', '')
                        try:
                            open_date = datetime.fromisoformat(str(open_date_str).replace('Z', '')).date()
                        except (ValueError, TypeError):
                            continue

                        # Location
                        city = str(insp.get('site_city', '')).strip()
                        state = str(insp.get('site_state', '')).strip()
                        location = f"{city}, {state}" if city and state else state or city
                        estab_name = str(insp.get('estab_name', '')).strip()

                        # Process violations
                        active_violations = [v for v in violations if v.get('delete_flag') != 'X']
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
                            vtype = str(v.get('viol_type', '')).strip()
                            label = type_labels.get(vtype, vtype)
                            viol_type_counts[label] = viol_type_counts.get(label, 0) + 1
                            if vtype in ('S', 'W', 'R'):
                                serious_count += 1
                            try:
                                penalty = Decimal(str(v.get('current_penalty', 0) or 0))
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
                            f"OSHA inspection of {estab_name} at {location}. "
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
                        total_created += 1
                        company_events += 1

            if company_events > 0:
                DataSource.objects.update_or_create(
                    company=company,
                    source_name='OSHA Enforcement Data (Automated)',
                    defaults={
                        'source_agency': 'Dept of Labor / OSHA',
                        'source_url': 'https://enforcedata.dol.gov/',
                        'last_checked': date.today(),
                    }
                )
                self.stdout.write(self.style.SUCCESS(
                    f"  {company.name}: {company_events} new events"
                ))
            else:
                self.stdout.write(f"  {company.name}: no violations found")

        self.stdout.write(self.style.SUCCESS(
            f"\nOSHA scrape complete: {total_created} created, {total_skipped} skipped"
        ))
