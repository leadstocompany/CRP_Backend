import pandas as pd
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.contrib import admin
from django.db.models import Sum
from django.contrib import messages
from .models import CashForecast, ForecastLine, ActualCashFlow


class ForecastLineInline(admin.StackedInline):
    model = ForecastLine
    extra = 1
    readonly_fields = ('variance_against_actual',)

    def variance_against_actual(self, obj):
        if not obj.forecast:
            return "-"
        actuals = ActualCashFlow.objects.filter(
            company=obj.forecast.company,
            transaction_date__range=(obj.forecast.start_date, obj.forecast.end_date),
            project=obj.project,
            filter1=obj.filter1,
            sub_filter1=obj.sub_filter1,
            filter2=obj.filter2,
            sub_filter2=obj.sub_filter2,
            currency_code=obj.currency_code,
        ).aggregate(total=Sum('actual_amount'))

        actual = actuals["total"] or 0
        variance = (obj.forecast_amount or 0) - actual  # ✅ Handle NoneType issue
        return f"{variance:.2f}"

    variance_against_actual.short_description = "Variance ₹"


@admin.register(CashForecast)
class CashForecastAdmin(admin.ModelAdmin):
    list_display = (
        "forecast_code",
        "company",
        "start_date",
        "end_date",
        "duration_type",
        "created_by",
        "created_date",
        "total_forecast",
        "total_actual",
        "variance_percent_display",
    )
    search_fields = ("forecast_code",)
    list_filter = ("company", "start_date", "end_date", "duration_type")
    inlines = [ForecastLineInline]
    readonly_fields = ("created_by", "created_date")
    actions = ["calculate_variance_action", "export_forecasts_excel", "export_forecasts_pdf"]  # ✅ Added Export Actions

    def total_forecast(self, obj):
        return sum(line.forecast_amount or 0 for line in obj.lines.all())  # ✅ Handle NoneType issue

    total_forecast.short_description = "Forecast ₹"

    def total_actual(self, obj):
        actuals = ActualCashFlow.objects.filter(
            company=obj.company,
            transaction_date__range=(obj.start_date, obj.end_date)
        ).aggregate(total=Sum('actual_amount'))
        return actuals['total'] or 0

    total_actual.short_description = "Actual ₹"

    def variance_percent_display(self, obj):
        forecast = self.total_forecast(obj)
        actual = self.total_actual(obj)
        if forecast == 0:
            return "N/A"
        variance = forecast - actual
        percent = (variance / forecast) * 100
        return f"{percent:.2f}%"

    variance_percent_display.short_description = "Variance %"

    # ✅ **Custom Action to Recalculate Variance**
    @admin.action(description="Calculate Variance for Selected Forecasts")
    def calculate_variance_action(self, request, queryset):
        for forecast in queryset:
            variance_data = forecast.calculate_variance()
            self.message_user(request, f"Calculated variance for {forecast.forecast_code}: {variance_data}",
                              messages.SUCCESS)

    # ✅ **Custom Action to Export Forecasts to Excel**
    @admin.action(description="Export Selected Forecasts to Excel")
    def export_forecasts_excel(self, request, queryset):
        data = queryset.values("forecast_code", "company__company_name", "start_date", "end_date", "duration_type")
        df = pd.DataFrame(list(data))

        response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = 'attachment; filename="forecasts.xlsx"'
        df.to_excel(response, index=False)
        return response

    # ✅ **Custom Action to Export Forecasts to PDF**
    @admin.action(description="Export Selected Forecasts to PDF")
    def export_forecasts_pdf(self, request, queryset):
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="forecasts.pdf"'

        pdf = canvas.Canvas(response)
        pdf.drawString(100, 800, "Forecast Report")

        y = 780
        for forecast in queryset:
            pdf.drawString(100, y,
                           f"Code: {forecast.forecast_code}, Company: {forecast.company}, Forecast: {self.total_forecast(forecast)}")
            y -= 20

        pdf.save()
        return response
@admin.register(ActualCashFlow)
class ActualCashFlowAdmin(admin.ModelAdmin):
    list_display = ("company", "transaction_date", "project", "currency_code", "actual_amount", "created_by")
    list_filter = ("company", "transaction_date", "currency_code")
    search_fields = ("company__company_name", "project__project_name", "currency_code")
