from rest_framework import viewsets
from .models import (
    DocType, DocumentHistory, MainCategory, SubCategory, Project, Partie,
    GLChartOfAccount, Bank, BankBranch, CreditFacilityMaster, Filter1,
    SubFilter1, Filter2, SubFilter2, CurrencyCode,CurrencyRate
)
from .serializers import (
    DocTypeSerializer, DocumentHistorySerializer, MainCategorySerializer,
    SubCategorySerializer, ProjectSerializer, PartySerializer,
    GLChartOfAccountSerializer, BankSerializer, BankBranchSerializer,
    CreditFacilityMasterSerializer, Filter1Serializer, SubFilter1Serializer,
    Filter2Serializer, SubFilter2Serializer, CurrencyCodeSerializer,CurrencyRateSerializer
)

class DocTypeViewSet(viewsets.ModelViewSet):
    queryset = DocType.objects.all()
    serializer_class = DocTypeSerializer

class DocumentHistoryViewSet(viewsets.ModelViewSet):
    queryset = DocumentHistory.objects.all()
    serializer_class = DocumentHistorySerializer

class MainCategoryViewSet(viewsets.ModelViewSet):
    queryset = MainCategory.objects.all()
    serializer_class = MainCategorySerializer

class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class PartyViewSet(viewsets.ModelViewSet):
    queryset = Partie.objects.all()
    serializer_class = PartySerializer

class GLChartOfAccountViewSet(viewsets.ModelViewSet):
    queryset = GLChartOfAccount.objects.all()
    serializer_class = GLChartOfAccountSerializer

class BankViewSet(viewsets.ModelViewSet):
    queryset = Bank.objects.all()
    serializer_class = BankSerializer

class BankBranchViewSet(viewsets.ModelViewSet):
    queryset = BankBranch.objects.all()
    serializer_class = BankBranchSerializer

class CreditFacilityMasterViewSet(viewsets.ModelViewSet):
    queryset = CreditFacilityMaster.objects.all()
    serializer_class = CreditFacilityMasterSerializer

class Filter1ViewSet(viewsets.ModelViewSet):
    queryset = Filter1.objects.all()
    serializer_class = Filter1Serializer

class SubFilter1ViewSet(viewsets.ModelViewSet):
    queryset = SubFilter1.objects.all()
    serializer_class = SubFilter1Serializer

class Filter2ViewSet(viewsets.ModelViewSet):
    queryset = Filter2.objects.all()
    serializer_class = Filter2Serializer

class SubFilter2ViewSet(viewsets.ModelViewSet):
    queryset = SubFilter2.objects.all()
    serializer_class = SubFilter2Serializer

class CurrencyCodeViewSet(viewsets.ModelViewSet):
    queryset = CurrencyCode.objects.all().order_by('id')
    serializer_class = CurrencyCodeSerializer
class CurrencyRateViewSet(viewsets.ModelViewSet):
    queryset = CurrencyCode.objects.all()
    serializer_class = CurrencyRateSerializer