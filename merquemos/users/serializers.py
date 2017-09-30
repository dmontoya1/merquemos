from rest_framework import serializers
from .models import User, Address


class AddressSerializer(serializers.ModelSerializer):
    city_name = serializers.ReadOnlyField(source='city.name', read_only=True)

    class Meta:
        model = Address
        fields = ('pk', 'city_name', 'name', 'phone_number', 'label', 'directions')

class AddressCreateSerializer(serializers.ModelSerializer):
    user = serializers.CharField(required=False)

    class Meta:
        model = Address
        fields = ('user', 'city', 'name', 'phone_number', 'label', 'directions')

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone_number')