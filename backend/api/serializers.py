from rest_framework import serializers
from .models import User, Accounts, Banks, History

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'is_active', 'is_staff', 'password', 'first_name', 'last_name','email']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accounts
        fields = '__all__'

class BanksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banks
        fields = '__all__'

class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = '__all__'