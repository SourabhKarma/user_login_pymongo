from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django_mongo.settings import db

from rest_framework.permissions import AllowAny
from .serializer import CustomUserSerializer
from rest_framework.throttling import ScopedRateThrottle

import secrets
import bcrypt


# Create your views here.



# ++++++++++++++++++++++   LOGIN +++++++++++++++++++++

collection = db['< your_collection_name >'] 


class CreateUserView(APIView):
    

    authentication_classes = []
    permission_classes = [AllowAny]
    throttle_scope = 'login_scope'
    throttle_classes = [ScopedRateThrottle,]
    

    def post(self, request):
        print("Received request data:", request.data)
        serializer = CustomUserSerializer(data=request.data)

        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            password = serializer.validated_data['password']
            
            

            if not phone_number or not password:
                return Response({'error': 'Please provide both phone number and password'}, status=status.HTTP_400_BAD_REQUEST)

            existing_user = self.get_by_phone_number(phone_number)

            if existing_user:
                print("Failed to create user")
                return Response({'error': 'User with this phone number already exists'}, status=status.HTTP_400_BAD_REQUEST)

            self.create_user(phone_number,password)

            user = self.get_by_phone_number(phone_number)
            
            if user is None:
                return Response({'error': 'Failed to create user'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # print(user)
            
            




            return Response({"auth_token":user["auth_token"],
                'message': 'User registration successful',
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




    def create_auth_token(self):
        return secrets.token_urlsafe(32)




    def create_user(self, phone_number, password,):

        users_collection = collection
        
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        user_data = {
            'phone_number': phone_number,
            'password': hashed_password.decode('utf-8'),
            'auth_token': self.create_auth_token(), 
        }

        users_collection.insert_one(user_data)

    def get_by_phone_number(self, phone_number):

        users_collection = collection

        return users_collection.find_one({'phone_number': phone_number})






# ++++++++++++++++++++++   Profile +++++++++++++++++++++




class ProfileView(APIView):
    def get(self, request):
        auth_token = request.headers.get('Authorization') 

        if not auth_token:
            return Response({'error': 'Authentication token is required'}, status=status.HTTP_401_UNAUTHORIZED)

        user = self.get_user_by_token(auth_token)

        if not user:
            return Response({'error': 'Invalid or expired authentication token'}, status=status.HTTP_401_UNAUTHORIZED)

        profile_data = {
            'phone_number': user.get('phone_number'),
            'password': user.get('password'),
            'auth_token': user.get('auth_token'),
        }

        return Response(profile_data, status=status.HTTP_200_OK)

    def get_user_by_token(self,auth_token):


        users_collection = collection
        


        user = users_collection.find_one({'auth_token': auth_token})
        return user



# ++++++++++++++++++++++   LOGOUT +++++++++++++++++++++


class LogoutView(APIView):
    def post(self, request):
        auth_token = request.headers.get('Authorization') 

        if not auth_token:
            return Response({'error': 'Authentication token is required'}, status=status.HTTP_401_UNAUTHORIZED)

        self.clear_user_sessions_and_tokens(auth_token)

        return Response({'message': 'Logout successfully , Token has been removed'}, status=status.HTTP_200_OK)
    
    def clear_user_sessions_and_tokens(self,auth_token):

        users_collection = collection

        users_collection.update_one(
            {'auth_token': auth_token},
            {'$unset': {'sessions': '', 'auth_token': None}}
        )










