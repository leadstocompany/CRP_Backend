from django.urls import path
from . import views

app_name = 'transactions'

urlpatterns = [
    # Forecast Templates
    path('forecast-templates/', views.forecast_templates, name='forecast_templates'),
    path('forecast-templates/create/', views.create_forecast_template, name='create_forecast_template'),
    path('forecast-templates/<uuid:template_id>/', views.forecast_template_detail, name='forecast_template_detail'),
    path('forecast-templates/<uuid:template_id>/update/', views.update_forecast_template,
         name='update_forecast_template'),

    # Actual Templates
    path('actual-templates/', views.actual_templates, name='actual_templates'),
    path('actual-templates/create/', views.create_actual_template, name='create_actual_template'),
    path('actual-templates/<uuid:template_id>/', views.actual_template_detail, name='actual_template_detail'),
    path('actual-templates/<uuid:template_id>/update/', views.update_actual_template, name='update_actual_template'),

    # Forecasts
    path('forecasts/', views.forecasts, name='forecasts'),
    path('forecasts/create/', views.create_forecast, name='create_forecast'),
    path('forecasts/<uuid:forecast_id>/', views.forecast_detail, name='forecast_detail'),
    path('forecasts/<uuid:forecast_id>/update/', views.update_forecast, name='update_forecast'),
    path('forecasts/<uuid:forecast_id>/submit/', views.submit_forecast, name='submit_forecast'),
    path('forecasts/<uuid:forecast_id>/approve/', views.approve_forecast, name='approve_forecast'),
    path('forecasts/<uuid:forecast_id>/reject/', views.reject_forecast, name='reject_forecast'),
    path('forecasts/<uuid:forecast_id>/details/', views.forecast_details, name='forecast_details'),
    path('forecasts/<uuid:forecast_id>/details/create/', views.create_forecast_detail, name='create_forecast_detail'),
    path('forecasts/<uuid:forecast_id>/details/<uuid:detail_id>/', views.forecast_detail_item,
         name='forecast_detail_item'),
    path('forecasts/<uuid:forecast_id>/details/<uuid:detail_id>/update/', views.update_forecast_detail,
         name='update_forecast_detail'),
    path('forecasts/<uuid:forecast_id>/details/<uuid:detail_id>/delete/', views.delete_forecast_detail,
         name='delete_forecast_detail'),

    # Actuals
    path('actuals/', views.actuals, name='actuals'),
    path('actuals/create/', views.create_actual, name='create_actual'),
    path('actuals/<uuid:actual_id>/', views.actual_detail, name='actual_detail'),
    path('actuals/<uuid:actual_id>/update/', views.update_actual, name='update_actual'),
    path('actuals/<uuid:actual_id>/submit/', views.submit_actual, name='submit_actual'),
    path('actuals/<uuid:actual_id>/approve/', views.approve_actual, name='approve_actual'),
    path('actuals/<uuid:actual_id>/reject/', views.reject_actual, name='reject_actual'),
    path('actuals/<uuid:actual_id>/details/', views.actual_details, name='actual_details'),
    path('actuals/<uuid:actual_id>/details/create/', views.create_actual_detail, name='create_actual_detail'),
    path('actuals/<uuid:actual_id>/details/<uuid:detail_id>/', views.actual_detail_item, name='actual_detail_item'),
    path('actuals/<uuid:actual_id>/details/<uuid:detail_id>/update/', views.update_actual_detail,
         name='update_actual_detail'),
    path('actuals/<uuid:actual_id>/details/<uuid:detail_id>/delete/', views.delete_actual_detail,
         name='delete_actual_detail'),

    # Credit Facilities
    path('credit-facilities/', views.credit_facilities, name='credit_facilities'),
    path('credit-facilities/create/', views.create_credit_facility, name='create_credit_facility'),
    path('credit-facilities/<uuid:facility_id>/', views.credit_facility_detail, name='credit_facility_detail'),
    path('credit-facilities/<uuid:facility_id>/update/', views.update_credit_facility, name='update_credit_facility'),
    path('credit-facilities/<uuid:facility_id>/approve/', views.approve_credit_facility,
         name='approve_credit_facility'),
    path('credit-facilities/<uuid:facility_id>/reject/', views.reject_credit_facility, name='reject_credit_facility'),
    path('credit-facilities/<uuid:facility_id>/cancel/', views.cancel_credit_facility, name='cancel_credit_facility'),
]