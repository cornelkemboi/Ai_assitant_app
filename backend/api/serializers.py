from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Document


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'original_file', 'user', 'upload_date']
        read_only_fields = ['user']

    def create(self, validated_data):
        document = Document.objects.create(**validated_data)
        return document
