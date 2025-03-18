from django.contrib.auth.models import User
from django.utils.timezone import now
from django.db import models

from company.models import Company
from django.contrib.auth import get_user_model

User = get_user_model()

class DocType(models.Model):
    document_type_code = models.CharField(max_length=10, unique=True)
    document_type_name = models.CharField(max_length=255)
    starting_document_number = models.PositiveIntegerField()
    next_doc_number = models.PositiveIntegerField(null=True, blank=True)  # Auto-incremented
    company = models.ForeignKey(Company, on_delete=models.CASCADE,null=True, blank=True, related_name="document")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="doc_created_by")
    created_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="doc_modified_by")
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.document_type_code} - {self.document_type_name}"
class DocumentHistory(models.Model):
    doc_type = models.ForeignKey(DocType, on_delete=models.CASCADE, related_name="history")
    document_number = models.PositiveIntegerField()
    action = models.CharField(max_length=50,
                              choices=[("Created", "Created"), ("Updated", "Updated"), ("Deleted", "Deleted")])
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    performed_date = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.doc_type.document_type_code} - {self.document_number} - {self.action}"
class MainCategory(models.Model):
    category_code = models.CharField(max_length=50, unique=True)
    category_name = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True, related_name="category")

    username = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True, related_name="category")

    remark = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="main_created_by")
    created_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="main_modified_by")
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.category_code} - {self.category_name}"

class SubCategory(models.Model):
    """
    Stores sub-categories with validation based on Back-Office settings.
    """
    sub_category_code = models.CharField(max_length=50, unique=True, blank=True, null=True)
    sub_category_description = models.TextField()
    within_category_code = models.CharField(max_length=50)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True, related_name="subcategory")

    username = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True, related_name="subcategory")

    remark = models.TextField(blank=True, null=True)

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="sub_created_by")
    created_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="sub_modified_by")
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.sub_category_code} - {self.sub_category_description}"
class Project(models.Model):
    # Mandatory fields
    project_code = models.CharField(max_length=50, unique=True)
    project_name = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True, related_name="project")

    # Estimated Costs
    est_billing = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    est_dir_labour = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    est_dir_materials = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    est_dir_overheads = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    est_dir_noncash = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)  # Exclude from Cash Reports

    est_indir_labour = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    est_indir_materials = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    est_indir_overheads = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    est_indir_noncash = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)  # Exclude from Cash Reports

    # System Captured Fields
    username = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name="project")

    remark = models.TextField(blank=True, null=True)

    created_by = models.ForeignKey(User, related_name="created_projects", on_delete=models.SET_NULL, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, related_name="modified_projects", on_delete=models.SET_NULL, null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.project_code} - {self.project_name}"

    @property
    def cash_forecast(self):
        """Cash Forecast / Cash P/L calculation excluding NonCash fields"""
        return (
            (self.est_billing or 0)
            - (self.est_dir_labour or 0)
            - (self.est_dir_materials or 0)
            - (self.est_dir_overheads or 0)
            - (self.est_indir_labour or 0)
            - (self.est_indir_materials or 0)
            - (self.est_indir_overheads or 0)
        )

    @property
    def net_profit_loss(self):
        """Net P/L calculation including NonCash fields"""
        return self.cash_forecast - (self.est_dir_noncash or 0) - (self.est_indir_noncash or 0)
class Partie(models.Model):
    party_code = models.CharField(max_length=20, unique=True)
    party_name = models.CharField(max_length=255)
    username = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name="party")

    remark = models.TextField(blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True, related_name="party")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="party_created_by")
    created_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="party_modified_by")
    modified_date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.party_name
class GLChartOfAccount(models.Model):
    gl_acct_code = models.CharField(max_length=50, unique=True)
    gl_acct_name = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE,null=True, blank=True, related_name="gl")
    username = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name="gl")

    remark = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="gl_created_by")
    created_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="gl_modified_by")
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.gl_acct_code} - {self.gl_acct_name}"

class Bank(models.Model):
    bank_code = models.CharField(max_length=10, unique=True)
    bank_name = models.CharField(max_length=255)
    bank_swift_ifsc = models.CharField(max_length=50, blank=True, null=True)
    bank_country = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE,null=True, blank=True, related_name="bank")
    username = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True, related_name="bank")

    remark = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name="created_banks")
    created_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name="modified_banks")
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.bank_code} - {self.bank_name}"

class BankBranch(models.Model):
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name="branches")
    branch_code = models.CharField(max_length=20, unique=True)
    branch_name = models.CharField(max_length=255)
    bank_swift_ifsc = models.CharField(max_length=50, blank=True, null=True)
    bank_state = models.CharField(max_length=100, blank=True, null=True)
    bank_country = models.CharField(max_length=100)
    username = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name="bankbranches")

    remark = models.TextField(blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True, related_name="bankbranches")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="branch_created_by")
    created_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="branch_modified_by")
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Bank Branch"
        verbose_name_plural = "Bank Branches"


    def __str__(self):
        return f"{self.branch_code} - {self.branch_name} ({self.bank.bank_name})"



class CreditFacilityMaster(models.Model):
    category_code = models.CharField(max_length=50)  # "CF" as input
    credit_facility_code = models.CharField(max_length=20, unique=True)
    credit_facility_name = models.CharField(max_length=255)

    username = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True, related_name="creditfacility")
    remark = models.TextField(blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True, related_name="creditfacility")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="credit_created_by")
    created_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="credit_modified_by")
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.credit_facility_code} - {self.credit_facility_name}"

class Filter1(models.Model):
    filter_code = models.CharField(max_length=50, unique=True)  # e.g., "TVM"
    filter_description = models.CharField(max_length=255)  # e.g., "Trivandrum"
    filter_purpose = models.CharField(max_length=100)  # e.g., "Location"
    username = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True, related_name="filter1s")
    remark = models.TextField(blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True, related_name="filter1s")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="filter1_created_by")
    created_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="filter1_modified_by")
    modified_date = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.filter_code} - {self.filter_description}"
class SubFilter1(models.Model):
    sub_filter_code = models.CharField(max_length=50, unique=True)  # e.g., "P1"
    sub_filter_desc = models.CharField(max_length=255)  # e.g., "Pattom"
    filter1 = models.ForeignKey(Filter1, on_delete=models.CASCADE)  # Related to Filter-1


    remark = models.TextField(blank=True, null=True)
    username = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name="subfilter1s")

    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True, related_name="subfilter1s")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="subfilter1_created_by")
    created_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="subfilter1_modified_by")
    modified_date = models.DateTimeField(auto_now=True)



    def __str__(self):
        return f"{self.sub_filter_code} - {self.sub_filter_desc}"
class Filter2(models.Model):
    filter_code = models.CharField(max_length=50, unique=True)  # e.g., "Brand"
    filter_description = models.CharField(max_length=255)  # e.g., "Mangalam"
    filter_broad_description = models.CharField(max_length=255)  # e.g., "Spices"


    remark = models.TextField(blank=True, null=True)
    username = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name="filter2s")

    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True, related_name="filter2s")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="filter2_created_by")
    created_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="filter2_modified_by")
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.filter_code} - {self.filter_description}"
class SubFilter2(models.Model):
    sub_filter_code = models.CharField(max_length=50, unique=True)  # e.g., "Grade"
    sub_filter_description = models.CharField(max_length=255)  # e.g., "Spice Grade"
    filter2 = models.ForeignKey(Filter2, on_delete=models.CASCADE, related_name="sub_filters")  # Relation to Filter-2


    remark = models.TextField(blank=True, null=True)
    username = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name="subfilter2s")

    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True, related_name="subfilter2s")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="subfilter2_created_by")
    created_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="subfilter2_modified_by")
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.sub_filter_code} - {self.sub_filter_description}"

class CurrencyCode(models.Model):
    curr_code = models.CharField(max_length=10, unique=True, verbose_name="Currency Code")
    curr_name = models.CharField(max_length=100, verbose_name="Currency Name")

    remark = models.TextField(verbose_name="Remark", blank=True, null=True)
    username = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name="currcodes")

    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True, related_name="currcodes")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="currcodes_created_by")
    created_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="currcodes_modified_by")
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Currency Code"
        verbose_name_plural = "Currency Codes"

    def __str__(self):
        return f"{self.curr_code} - {self.curr_name}"


class CurrencyRate(models.Model):
    currency_enabled = models.BooleanField(default=True, verbose_name="Currency Enabled")  # Toggle field
    currency_code = models.CharField(max_length=10, verbose_name="Currency Code")
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=6, verbose_name="Exchange Rate")
    exchange_rate_date = models.DateField(verbose_name="Exchange Rate As on Date", null=True, blank=True)
    remark = models.TextField(verbose_name="Remark", null=True, blank=True)
    username = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name="currrates")

    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True, related_name="currrates")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="currrates_created_by")
    created_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="currrates_modified_by")
    modified_date = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.currency_code} - {self.exchange_rate} (As of {self.exchange_rate_date})"

    class Meta:
        verbose_name = "Currency Rate"
        verbose_name_plural = "Currency Rates"