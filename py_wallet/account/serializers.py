from rest_framework import serializers
from account.models import User

class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','password']


class CheckBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','balance']

class UpdateBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','balance']