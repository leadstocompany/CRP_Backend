from rest_framework import serializers
from .models import (
    DocType, DocumentHistory, MainCategory, SubCategory, Project, Partie,
    GLChartOfAccount, Bank, BankBranch, CreditFacilityMaster, Filter1,
    SubFilter1, Filter2, SubFilter2, CurrencyCode,CurrencyRate
)

class DocTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocType
        fields = '__all__'

class DocumentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentHistory
        fields = '__all__'

class MainCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MainCategory
        fields = '__all__'

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class PartySerializer(serializers.ModelSerializer):
    class Meta:
        model = Partie
        fields = '__all__'

class GLChartOfAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = GLChartOfAccount
        fields = '__all__'

class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = '__all__'

class BankBranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankBranch
        fields = '__all__'

class CreditFacilityMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditFacilityMaster
        fields = '__all__'

class Filter1Serializer(serializers.ModelSerializer):
    class Meta:
        model = Filter1
        fields = '__all__'

class SubFilter1Serializer(serializers.ModelSerializer):
    class Meta:
        model = SubFilter1
        fields = '__all__'

class Filter2Serializer(serializers.ModelSerializer):
    class Meta:
        model = Filter2
        fields = '__all__'

class SubFilter2Serializer(serializers.ModelSerializer):
    class Meta:
        model = SubFilter2
        fields = '__all__'

class CurrencyCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencyCode
        fields = '__all__'

class CurrencyRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencyRate
        fields = '__all__'
