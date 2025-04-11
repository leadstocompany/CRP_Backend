from django.db import models
from django.conf import settings
from django.db.models import Sum
from master.models import Project, Filter1, SubFilter1, Filter2, SubFilter2
from company.models import Company

User = settings.AUTH_USER_MODEL

class CashForecast(models.Model):
    DURATION_CHOICES = [
        ('D', 'Day'),
        ('W', 'Week'),
        ('M', 'Month'),
    ]

    duration_type = models.CharField(max_length=1, choices=DURATION_CHOICES, default='M')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="cash_forecasts")
    forecast_code = models.CharField(max_length=50, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="forecasts_created")
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.forecast_code} ({self.company.company_code})"

    def calculate_variance(self):
        """Calculate variance for each forecast line against actual cash flows."""
        for line in self.lines.all():
            actuals = ActualCashFlow.objects.filter(
                company=self.company,
                transaction_date__range=(self.start_date, self.end_date),
                project=line.project,
                currency_code=line.currency_code,
            ).aggregate(Sum('actual_amount'))

            actual = actuals["actual_amount__sum"] or 0
            line.variance = line.forecast_amount - actual
            line.save()


class ForecastLine(models.Model):
    forecast = models.ForeignKey(CashForecast, on_delete=models.CASCADE, related_name="lines")  # ✅ Fixed related_name
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, related_name="forecast_lines")
    filter1 = models.ForeignKey(Filter1, on_delete=models.SET_NULL, null=True, related_name="forecast_lines")
    sub_filter1 = models.ForeignKey(SubFilter1, on_delete=models.SET_NULL, null=True, related_name="forecast_lines")
    filter2 = models.ForeignKey(Filter2, on_delete=models.SET_NULL, null=True, related_name="forecast_lines")
    sub_filter2 = models.ForeignKey(SubFilter2, on_delete=models.SET_NULL, null=True, related_name="forecast_lines")
    currency_code = models.CharField(max_length=10)
    forecast_amount = models.DecimalField(max_digits=15, decimal_places=2)
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = (
            'forecast', 'project', 'filter1', 'sub_filter1', 'filter2', 'sub_filter2', 'currency_code'
        )


class ActualCashFlow(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="actual_cashflows")
    transaction_date = models.DateField()
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, related_name="actual_cashflows")
    filter1 = models.ForeignKey(Filter1, on_delete=models.SET_NULL, null=True, related_name="actual_cashflows")
    sub_filter1 = models.ForeignKey(SubFilter1, on_delete=models.SET_NULL, null=True, related_name="actual_cashflows")
    filter2 = models.ForeignKey(Filter2, on_delete=models.SET_NULL, null=True, related_name="actual_cashflows")
    sub_filter2 = models.ForeignKey(SubFilter2, on_delete=models.SET_NULL, null=True, related_name="actual_cashflows")
    currency_code = models.CharField(max_length=10)
    actual_amount = models.DecimalField(max_digits=15, decimal_places=2)
    remarks = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="actuals_created")
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_date} - {self.actual_amount}"
