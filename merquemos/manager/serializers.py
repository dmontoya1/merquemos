from rest_framework import serializers
from .models import AppPolicy, FAQCategory, FAQItem, State, City


class AppPolicySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AppPolicy
        fields = ('privacy_policy', 'terms_and_conditions')


class FAQCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = FAQCategory
        fields = ('name',)


class FAQItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = FAQItem
        fields = ('question', 'answer')


class StateSerializer(serializers.ModelSerializer):

    class Meta:
        model = State
        fields = ('name',)


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = ('name',)