from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CashForecastViewSet, ActualCashFlowViewSet
from .views import export_forecast_excel, export_forecast_pdf

router = DefaultRouter()
router.register(r'forecasts', CashForecastViewSet)
router.register(r'actuals', ActualCashFlowViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path("export/forecasts/excel/", export_forecast_excel, name="export_forecasts_excel"),
    path("export/forecasts/pdf/", export_forecast_pdf, name="export_forecasts_pdf"),
]
