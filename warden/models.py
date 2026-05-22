from django.db import models


class Industry(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "industries"


class Company(models.Model):
    name = models.CharField(max_length=300)
    slug = models.SlugField(unique=True)
    legal_name = models.CharField(max_length=500, blank=True)
    industry = models.ForeignKey(Industry, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True)

    # Entity mapping fields (manual for now)
    osha_establishment_ids = models.JSONField(default=list, blank=True)
    epa_facility_ids = models.JSONField(default=list, blank=True)
    sec_cik = models.CharField(max_length=20, blank=True)
    fec_committee_ids = models.JSONField(default=list, blank=True)

    # Metadata
    employee_count = models.IntegerField(null=True, blank=True)
    headquarters = models.CharField(max_length=300, blank=True)
    stock_ticker = models.CharField(max_length=10, blank=True)
    website = models.URLField(blank=True)

    # Accountability summary
    risk_level = models.CharField(
        max_length=20,
        choices=[
            ('elevated', 'Elevated Concern'),
            ('mixed', 'Mixed Record'),
            ('limited', 'Limited Issues'),
            ('insufficient', 'Insufficient Data'),
        ],
        default='insufficient'
    )
    summary_line = models.TextField(blank=True)
    pattern_summary = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "companies"


class DataSource(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='data_sources')
    source_name = models.CharField(max_length=200)
    source_agency = models.CharField(max_length=200)
    source_url = models.URLField(blank=True)
    last_checked = models.DateField()
    coverage_start = models.DateField(null=True, blank=True)
    coverage_end = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.company.name} — {self.source_name}"


class AccountabilityEvent(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='events')

    date = models.DateField()
    title = models.CharField(max_length=500)
    description = models.TextField()

    domain = models.CharField(
        max_length=30,
        choices=[
            ('workplace', 'Workplace Safety'),
            ('environmental', 'Environmental'),
            ('governance', 'Governance'),
            ('labor', 'Labor Relations'),
            ('political', 'Political Spending'),
            ('consumer', 'Consumer Protection'),
        ]
    )
    severity = models.CharField(
        max_length=20,
        choices=[
            ('critical', 'Critical'),
            ('serious', 'Serious'),
            ('moderate', 'Moderate'),
            ('minor', 'Minor'),
            ('informational', 'Informational'),
        ]
    )

    source_agency = models.CharField(max_length=200)
    source_url = models.URLField(blank=True)
    source_document = models.CharField(max_length=300, blank=True)

    penalty_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    facility_location = models.CharField(max_length=300, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.date} — {self.company.name} — {self.title}"


class Subsidiary(models.Model):
    parent = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='subsidiaries')
    name = models.CharField(max_length=500)
    aliases = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"{self.name} (subsidiary of {self.parent.name})"

    class Meta:
        verbose_name_plural = "subsidiaries"


class SnapshotStat(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='snapshot_stats')
    label = models.CharField(max_length=200)
    value = models.CharField(max_length=100)
    context = models.CharField(max_length=300, blank=True)
    source_url = models.URLField(blank=True)
    sort_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['sort_order']

    def __str__(self):
        return f"{self.company.name} — {self.label}: {self.value}"


# Add to AccountabilityEvent when ready for migration
# record_type choices for future use:
# government_enforcement - OSHA citation, EPA fine, etc
# public_settlement - Corporate-wide settlement, consent decree
# administrative_citation - Recordkeeping violation, administrative action
# labor_complaint - NLRB complaint, union grievance
# layoff_notice - WARN Act filing
