from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser', 'date_joined']

class UpdateUserRoleSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = User
        
        fields = ['id','is_staff','is_superuser']

class SignUpSerializer(serializers.ModelSerializer):
    is_staff = serializers.BooleanField(default=False)
    is_superuser = serializers.BooleanField(default=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'is_staff', 'is_superuser']

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        is_staff = validated_data.get('is_staff', False)
        is_superuser = validated_data.get('is_superuser', False)

        # Check if the user already exists
        user_exists = User.objects.filter(username=username).exists()

        if user_exists:
            raise serializers.ValidationError({'error': 'User already exists'})

        # If the user doesn't exist, create a new one
        user = User(**validated_data)
        user.set_password(password)
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.save()

        return user

class SignInSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def to_representation(self, instance):
        # Customize the structure of the response
        return {
            'username': instance['username'],
            'email': instance['email'],  # Include additional fields if needed
            'token': instance['token'],
        }

# class UserProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserProfile
#         fields = ['id', 'user', 'user_type']

# class EquitySymbolSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EquitySymbol
#         fields = ['id', 'symbol']

# class InvestmentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Investment
#         fields = ['id', 'customer', 'asset_type', 'principal_amount', 'purchase_price', 'shares', 'investment_date', 'maturity_date', 'equity_symbol']




