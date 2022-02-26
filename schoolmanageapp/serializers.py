from rest_framework.serializers import ModelSerializer,Serializer,FloatField,ImageField,DecimalField,CharField,ChoiceField,DateField,SerializerMethodField
from .models import *
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.core.exceptions import ValidationError
from datetime import timedelta
from rest_framework import serializers


ACCOUNT_TYPE = (('1','Superadmin'),
                ('2','teacher'),
                ('3','Student'))


class RegisterSerializer(serializers.ModelSerializer):
	first_name = serializers.CharField(error_messages={"required": "first name Key is required", "blank": "first name is required"},max_length=400)
	last_name=serializers.CharField(error_messages={"required": "last name Key is required", "blank": "last name is required"},max_length=400)
	email = serializers.CharField(error_messages={"required": "Email Key is required", "blank": "Email is required"},max_length=100)
	username = serializers.CharField(error_messages={"required": "username key is required", "blank": "username is required"},max_length=100)
	password = serializers.CharField(error_messages={"required": "password key is required", "blank": "password is required"},max_length=100)
	account_type = serializers.ChoiceField(error_messages={"required": "device_type key is required", "blank": "device_type is required"},choices=ACCOUNT_TYPE)
	def validate(self,data):
		username=data.get('username')
		email=data.get('email')
		password=data.get('password')
		if User.objects.filter(username=username).exists():
			raise ValidationError("username is already exists.")
		if User.objects.filter(email=email).exists():
			raise ValidationError("Email is already exists. ")	
		return data
	def create(self, validated_data):
		first_name=validated_data.get('first_name')
		last_name=validated_data.get('last_name')
		email=validated_data.get('email')
		username=validated_data.get('username')
		password=validated_data.get('password')
		account_type=validated_data.get('account_type')
		user=User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email)
		user.set_password(password)
		user.save()
		UA=UserAccount.objects.create(user=user)
		UA.account_type=account_type
		UA.save()
		return validated_data




class AddStudRegisterSerializer(serializers.ModelSerializer):
	first_name = serializers.CharField(error_messages={"required": "first name Key is required", "blank": "first name is required"},max_length=400)
	last_name=serializers.CharField(error_messages={"required": "last name Key is required", "blank": "last name is required"},max_length=400)
	email = serializers.CharField(error_messages={"required": "Email Key is required", "blank": "Email is required"},max_length=100)
	username = serializers.CharField(error_messages={"required": "username key is required", "blank": "username is required"},max_length=100)
	password = serializers.CharField(error_messages={"required": "password key is required", "blank": "password is required"},max_length=100)
	def validate(self,data):
		username=data.get('username')
		email=data.get('email')
		password=data.get('password')
		if User.objects.filter(username=username).exists():
			raise ValidationError("username is already exists.")
		if User.objects.filter(email=email).exists():
			raise ValidationError("Email is already exists. ")	
		return data
	def create(self, validated_data):
		first_name=validated_data.get('first_name')
		last_name=validated_data.get('last_name')
		email=validated_data.get('email')
		username=validated_data.get('username')
		password=validated_data.get('password')
		account_type=validated_data.get('account_type')
		user=User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email)
		user.set_password(password)
		user.save()
		UA=UserAccount.objects.create(user=user)
		UA.account_type="3"
		UA.save()
		return validated_data


class ViewUserAccountSerializer(serializers.ModelSerializer):
	username=SerializerMethodField()
	first_name=SerializerMethodField()
	last_name=SerializerMethodField()
	email=SerializerMethodField()
	def get_username(self,instance):
		return instance.User.username
	def get_first_name(self,instance):
		return instance.User.first_name
	def get_last_name(self,instance):
		return instance.User.last_name			
	def get_email(self,instance):
		return instance.User.email	
	class Meta:
		model = UserAccount
		fields = [
				'username',
				'first_name',
				'last_name',
				'email',
				'account_type'
					]	