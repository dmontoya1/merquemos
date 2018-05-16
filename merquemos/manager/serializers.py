from rest_framework import serializers
from .models import (
    AppPolicy, FAQCategory,
    FAQItem, State, City,
    ContactMessage
)


class AppPolicySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AppPolicy
        fields = ('privacy_policy', 'terms_and_conditions')

class FAQCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = FAQCategory
        fields = ('pk', 'name')

class FAQItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = FAQItem
        fields = ('question', 'answer')

class StateSerializer(serializers.ModelSerializer):

    class Meta:
        model = State
        fields = ('id', 'name')

class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = ('id', 'name', 'state')

class ContactMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContactMessage
        fields = ('title', 'content')