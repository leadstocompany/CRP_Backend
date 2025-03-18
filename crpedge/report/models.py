from django.db import models
from company.models import Company  # Assuming Company model is in the 'company' app
from master.models import (  # Assuming master models are in the 'masters' app
    MainCategory, SubCategory, Project, Partie, GLChartOfAccount,
    Bank, BankBranch, CreditFacilityMaster, Filter1, SubFilter1, Filter2, SubFilter2,
    CurrencyCode, CurrencyRate
)

class ReportConfiguration(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    report_name = models.CharField(max_length=100)

    # Filter relationships
    main_category = models.ForeignKey(MainCategory, on_delete=models.SET_NULL, null=True, blank=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)
    party = models.ForeignKey(Partie, on_delete=models.SET_NULL, null=True, blank=True)
    gl_coa = models.ForeignKey(GLChartOfAccount, on_delete=models.SET_NULL, null=True, blank=True)
    bank = models.ForeignKey(Bank, on_delete=models.SET_NULL, null=True, blank=True)
    bank_branch = models.ForeignKey(BankBranch, on_delete=models.SET_NULL, null=True, blank=True)
    credit_facility = models.ForeignKey(CreditFacilityMaster, on_delete=models.SET_NULL, null=True, blank=True)
    filter1 = models.ForeignKey(Filter1, on_delete=models.SET_NULL, null=True, blank=True)
    sub_filter1 = models.ForeignKey(SubFilter1, on_delete=models.SET_NULL, null=True, blank=True)
    filter2 = models.ForeignKey(Filter2, on_delete=models.SET_NULL, null=True, blank=True)
    sub_filter2 = models.ForeignKey(SubFilter2, on_delete=models.SET_NULL, null=True, blank=True)
    curr_code = models.ForeignKey(CurrencyCode, on_delete=models.SET_NULL, null=True, blank=True)
    curr_rate = models.ForeignKey(CurrencyRate, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.company.company_name} - {self.report_name}"