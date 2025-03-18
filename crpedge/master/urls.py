from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DocTypeViewSet, DocumentHistoryViewSet, MainCategoryViewSet,
    SubCategoryViewSet, ProjectViewSet, PartyViewSet, GLChartOfAccountViewSet,
    BankViewSet, BankBranchViewSet, CreditFacilityMasterViewSet, Filter1ViewSet,
    SubFilter1ViewSet, Filter2ViewSet, SubFilter2ViewSet, CurrencyCodeViewSet
)

router = DefaultRouter()
router.register(r'doc-types', DocTypeViewSet)
router.register(r'document-histories', DocumentHistoryViewSet)
router.register(r'main-categories', MainCategoryViewSet)
router.register(r'sub-categories', SubCategoryViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'partie', PartyViewSet)
router.register(r'gl-accounts', GLChartOfAccountViewSet)
router.register(r'banks', BankViewSet)
router.register(r'bank-branches', BankBranchViewSet)
router.register(r'credit-facilities', CreditFacilityMasterViewSet)
router.register(r'filters-1', Filter1ViewSet)
router.register(r'sub-filters-1', SubFilter1ViewSet)
router.register(r'filters-2', Filter2ViewSet)
router.register(r'sub-filters-2', SubFilter2ViewSet)
router.register(r'currencies', CurrencyCodeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
