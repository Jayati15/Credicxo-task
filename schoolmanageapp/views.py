from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK,HTTP_400_BAD_REQUEST
from .serializers import *

from datetime import datetime,timedelta



def get_serializer_errors(serializer):
    error_keys = list(serializer.errors.keys())
    if error_keys:
        error_msg = serializer.errors[error_keys[0]]
        return {'error':error_msg[0]}
    else:
        return serializer.errors




def check_blank_or_null(data):
	status=True
	for x in data:
		if x=="" or x==None:
			status=False
			break
		else:
			pass					
	return status        


#This API is only for Admin,
#Admin can able to Create any kind account
class RegisterApiView(APIView):
	permission_classes = (IsAuthenticated,)
 
	def post(self, request):
		if UserAccount.objects.get(user=request.user).account_type == "1":
			serializer = RegisterSerializer(data=request.data)
			if serializer.is_valid():
				serializer.save()
				return Response({"message": "Registered Successfully"}, status=HTTP_200_OK)
			else:
				return Response(get_serializer_errors(serializer), status=HTTP_400_BAD_REQUEST)
		else:
			return Response({"error":"You are Not admin"},status=HTTP_400_BAD_REQUEST)


#this API is only used for Admin .
#admin can filter Account by Account Type.
class ViewUserAccount(APIView):
	permission_classes = (IsAuthenticated,)
	def get(self, request):
		if UserAccount.objects.get(user=request.user).account_type == "1":
			UA=UserAccount.objects.all()
			serializer=ViewUserAccountSerializer(UA,many=True)
			return Response({"students":serializer.data},status=HTTP_200_OK)
		else:
			return Response({"error":"You are Not admin"},status=HTTP_400_BAD_REQUEST)
	
	def post(self, request):
		account_type=request.data.get("account_type")
		if UserAccount.objects.get(user=request.user).account_type == "1":
			UA=UserAccount.objects.filter(account_type=account_type)
			serializer=ViewUserAccountSerializer(UA,many=True)
			return Response({"students":serializer.data},status=HTTP_200_OK)
		else:
			return Response({"error":"You are Not admin"},status=HTTP_400_BAD_REQUEST)
	




#This API only for Teacher can create Student account
#this Teacher can view all students
class ViewAndAddstudentApiView(APIView):
	permission_classes = (IsAuthenticated,)
	def post(self, request):
		if UserAccount.objects.get(user=request.user).account_type == "2":
			serializer = AddStudRegisterSerializer(data=request.data)
			if serializer.is_valid():
				serializer.save()
				return Response({"message": "Registered Successfully"}, status=HTTP_200_OK)
			else:
				return Response(get_serializer_errors(serializer), status=HTTP_400_BAD_REQUEST)
		else:
			return Response({"error":"You are Not Teacher"},status=HTTP_400_BAD_REQUEST)

	
	def get(self, request):
		if UserAccount.objects.get(user=request.user).account_type == "2":
			UA=UserAccount.objects.filter(account_type="3")
			serializer=ViewUserAccountSerializer(UA,many=True)
			return Response({"students":serializer.data},status=HTTP_200_OK)
		else:
			return Response({"error":"You are Not Teacher"},status=HTTP_400_BAD_REQUEST)
	

					


#This API is only for student
#Student can view his profile
class StudentProfile(APIView):
	permission_classes = (IsAuthenticated,)
	def get(self, request):
		if UserAccount.objects.get(user=request.user).account_type == "3":
			UA=UserAccount.objects.get(User=request.user)
			serializer=ViewUserAccountSerializer(UA,many=False)
			return Response({"students":serializer.data},status=HTTP_200_OK)
		else:
			return Response({"error":"You are Not Teacher"},status=HTTP_400_BAD_REQUEST)




#This API is for every User(student,teacher,and admin)
#We can integrate This API with send_mail function
#we send otp throuh mail.
#Otp is only valid for 30 minutes
class SendOtpToForgetPassword(APIView):
	permission_classes = (AllowAny, )
	def post(self, request):
		username = request.data.get('username')
		if User.objects.filter(username=username).exists():
			user=User.objects.get(username=username)
			if forget_otp.objects.filter(user=user).exists():
				sot=forget_otp.objects.get(user=user)
				sot.delete()	
			otp=1234
			sotp=forget_otp.objects.create(user=user,otp=otp)
			sotp.expire=datetime.now()+timedelta(minutes=30)       
			sotp.save()
			return Response({'message':"Otp sent successfully"},status=HTTP_200_OK)
		else:
			return Response({"message":"username does not exists"},status=HTTP_400_BAD_REQUEST)	



#It will verify otp and change password.
class VerifyForgetpasswordOtp(APIView):
	permission_classes = (AllowAny, )
	def post(self,request):
		context={}
		username = request.data.get("username")
		otp_value=request.data.get('otp_value')
		password=request.data.get("password")
		if check_blank_or_null([username,otp_value]) and User.objects.filter(username=username).exists():
			user=User.objects.get(username=username)
			if forget_otp.objects.filter(user=user,expire__gte=datetime.now(),otp=otp_value).exists():
				sotp=forget_otp.objects.get(user=user,expire__gte=datetime.now(),otp=otp_value)
				if sotp.attempt < 5:
					sotp.save()
					user.set_password(password)
					user.save()
					context['message']="password has been changed"
					return Response(context, status=HTTP_200_OK)
				else:
					context['message']="You have used all attempt.Please resend your otp"	
					return Response(context, status=HTTP_400_BAD_REQUEST)
			else:
				sotp=forget_otp.objects.get(user=user)
				sotp.attempt+=1
				sotp.save()
				context['message']="Incorrect Otp"
				return Response(context, status=HTTP_400_BAD_REQUEST)
		else:
			context['message']="User Account is not exists."
			return Response(context, status=HTTP_400_BAD_REQUEST)		

	

# Create your views here.
