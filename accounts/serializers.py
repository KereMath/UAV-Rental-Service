from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

CustomUser = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid credentials")
# serializers.py
from rest_framework import serializers
from .models import UAV
from .models import UAVListing

class UAVListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UAVListing
        fields = ['price'] 
        depth = 1     

class UAVSerializer(serializers.ModelSerializer):
    rental_status = serializers.CharField(read_only=True, source='current_rental_status')
    rental_id = serializers.IntegerField(read_only=True, source='current_rental_id')
    listing = UAVListingSerializer(read_only=True)
    is_listed = serializers.SerializerMethodField()


    def get_is_listed(self, obj):
        return UAVListing.objects.filter(uav=obj).exists()
    class Meta:
        model = UAV
        fields = ['id', 'brand', 'model', 'weight', 'category', 'rental_status', 'rental_id', 'listing', 'is_listed']
from rest_framework import serializers
from .models import UAVListing




from rest_framework import serializers
from .models import RentalRecord

class RentalRecordSerializer(serializers.ModelSerializer):
    uav = UAVSerializer(read_only=True)  
    user = serializers.StringRelatedField() 

    class Meta:
        model = RentalRecord
        fields = ['id', 'uav', 'user', 'start_date', 'end_date', 'status']


