from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import CashForecast, ActualCashFlow
from .serializers import CashForecastSerializer, ActualCashFlowSerializer
from .permissions import IsCompanyUser, IsAdminOrManager

import pandas as pd
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from .models import CashForecast, ActualCashFlow
class CashForecastViewSet(viewsets.ModelViewSet):
    queryset = CashForecast.objects.all()
    serializer_class = CashForecastSerializer
    permission_classes = [IsAuthenticated, IsCompanyUser]

    def get_queryset(self):
        return self.queryset.filter(company=self.request.user.company)

class ActualCashFlowViewSet(viewsets.ModelViewSet):
    queryset = ActualCashFlow.objects.all()
    serializer_class = ActualCashFlowSerializer
    permission_classes = [IsAuthenticated, IsCompanyUser]

    def get_queryset(self):
        return self.queryset.filter(company=self.request.user.company)


def export_forecast_excel(request):
    """Export forecasts to Excel."""
    forecasts = CashForecast.objects.all().values()
    df = pd.DataFrame(forecasts)

    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = 'attachment; filename="forecasts.xlsx"'
    df.to_excel(response, index=False)
    return response


def export_forecast_pdf(request):
    """Export forecasts to PDF."""
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="forecasts.pdf"'

    pdf = canvas.Canvas(response)
    pdf.drawString(100, 800, "Forecast Report")

    y = 780
    forecasts = CashForecast.objects.all()
    for forecast in forecasts:
        pdf.drawString(100, y,
                       f"Code: {forecast.forecast_code}, Company: {forecast.company}, Forecast: {forecast.total_forecast()}")
        y -= 20

    pdf.save()
    return response