from django.shortcuts import render
##from django.http import HttpResponse
from rest_framework.authtoken.models import Token
from rest_framework import generics,status
# from .serializers import UserProfileSerializer,EquitySymbolSerializer,InvestmentSerializer,UserSerializer,SignUpSerializer,SignInSerializer
# from .models import UserProfile,EquitySymbol,Investment
from .serializers import UserSerializer,SignUpSerializer,SignInSerializer,UpdateUserRoleSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
##

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import SignUpSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from bhdream_amc_app.permissions import IsAdminUser,IsStaffUser
# # Create your views here.
# ##def signin(request):
#     ##return HttpResponse("signin")

# ##ef signup(request):
#     ##return HttpResponse("signup")

# class UserView(generics.CreateAPIView):
#     queryset=User.objects.all()
#     serializer_class=UserSerializer

# class UserProfileView(generics.CreateAPIView):
#     queryset=UserProfile.objects.all()
#     serializer_class=UserProfileSerializer

# class EquitySymbolView(generics.CreateAPIView):
#     queryset=EquitySymbol.objects.all()
#     serializer_class=EquitySymbolSerializer

# class InvestmentView(generics.CreateAPIView):
#     queryset=Investment.objects.all()
#     serializer_class=InvestmentSerializer

# '''class SignUpView(APIView):
#     serializer_class=SignUpSerializer

#     def post(self,request,format=None):
#         if not self.request.session.exists(self.request.session.session_key):
#             self.request.session.create()
#         serializer=self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             last_name=serializer.data.get('last_name')
#             first_name=serializer.data.get('first_name')
#             username=serializer.data.get('username')
#             email=serializer.data.get('email')
#             password=serializer.data.get('password')
#             user=User(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
#             user.save()
#             return Response(SignInSerializer(user).data,status=status.HTTP_201_CREATED)
#         return Response({'Bad Request':'username or email already exist'},status=status.HTTP_400_BAD_REQUEST)'''

# '''class SignUpView(APIView):
#     serializer_class = SignUpSerializer

#     def post(self, request, format=None):
#         serializer = self.serializer_class(data=request.data)

#         if serializer.is_valid():
#             last_name=serializer.data.get('last_name')
#             first_name=serializer.data.get('first_name')
#             username = serializer.data.get('username')
#             password = serializer.data.get('password')
#             email = serializer.data.get('email')
#             user = User.objects.create_user(username=username, password=password, email=email,last_name=last_name,first_name=first_name)
#             return Response(SignInSerializer(user).data, status=status.HTTP_201_CREATED)
#         return Response({'Bad Request': 'Invalid input data'}, status=status.HTTP_400_BAD_REQUEST)'''

# '''class SignInView(APIView):
#     serializer_class = SignInSerializer

#     def post(self, request, format=None):
#         serializer = self.serializer_class(data=request.data)

#         if serializer.is_valid():
#             username = serializer.data.get('username')
#             password = serializer.data.get('password')
#             user = authenticate(username=username, password=password)

#             if user is not None:
#                 login(request, user)  # Log in the user
#                 return Response({'message': 'Successfully signed in'}, status=status.HTTP_200_OK)
        
#         return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)  ''' 
# '''class SignInView(APIView):
#     serializer_class=SignInSerializer
    
#     def post(self,request,format=None):
        
#         if not self.request.session.exists(self.request.session.session_key):
#             self.request.session.create()
#         serializer=self.serializer_class(data=request.data)
        
#         if serializer.is_valid():
#             username=serializer.data.get('username')
#             password=serializer.data.get('password')
#             queryset=User.objects.filter(username=username,password=password)
#             if queryset.exists():
#                 user=User(username=username)
#                 return Response(SignInSerializer(user).data,status=status.HTTP_202_ACCEPTED)
#         return Response({'Bad Request':'username or email already exist'},status=status.HTTP_400_BAD_REQUEST)'''
# BHDREAM_AMC_APP/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import SignUpSerializer
from jwt_utils import generate_jwt_token

class SignUpView(APIView):
    serializer_class = SignUpSerializer
    

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        try:
            if serializer.is_valid():
                first_name = serializer.validated_data.get('first_name')
                last_name = serializer.validated_data.get('last_name')
                username = serializer.validated_data.get('username')
                password = serializer.validated_data.get('password')
                email = serializer.validated_data.get('email')

                # Check if the user already exists
                user_exists = User.objects.filter(username=username).exists()

                if user_exists:
                    raise serializer.ValidationError({'error': 'User already exists'})

                # If the user doesn't exist, create a new one
                user = User.objects.create_user(username=username, email=email, password=password)
                user.first_name = first_name
                user.last_name = last_name
                user.is_staff = serializer.validated_data.get('is_staff', False)
                user.is_superuser = serializer.validated_data.get('is_superuser', False)
                user.save()

                # Generate JWT token
                token = generate_jwt_token(user)

                return Response({'token': token}, status=status.HTTP_201_CREATED)

        except serializer.ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SignInView(APIView):
    serializer_class = SignInSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = User.objects.filter(username=username).first()

            if user and user.check_password(password):
                # Authentication successful, generate JWT token
                token = generate_jwt_token(user)
                return Response({'token': token,"is_staff":user.is_staff,"is_superuser":user.is_superuser,"first_name":user.first_name}, status=status.HTTP_200_OK)

            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes([IsAdminUser])
class UpdateUserRoleView(APIView):
    serializer_class = UpdateUserRoleSerializer
    def post(self, request, format=None):
        
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            id = serializer.validated_data.get('id')
            is_staff = serializer.validated_data['is_staff']
            is_superuser = serializer.validated_data['is_superuser']

            user = User.objects.filter(id=id).first()
            if not user:
                raise serializer.ValidationError({'error': 'User not found with id {id}'})
            user.is_staff = is_staff
            user.is_superuser = is_superuser
            user.save()
            updated_user_serializer = UserSerializer(user)
            serialized_user = updated_user_serializer.data
            return Response({'message': 'success','user':serialized_user}, status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserListView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            first_name = serializer.validated_data.get('first_name')
            last_name = serializer.validated_data.get('last_name')
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            email = serializer.validated_data.get('email')
            # Check if the user already exists
            user_exists = User.objects.filter(username=username).exists()
            if user_exists:
                raise serializer.ValidationError({'error': 'User already exists'})
            # If the user doesn't exist, create a new one
            user = User.objects.create_user(username=username, email=email, password=password)
            user.first_name = first_name
            user.last_name = last_name
            user.is_staff = serializer.validated_data.get('is_staff', False)
            user.is_superuser = serializer.validated_data.get('is_superuser', False)
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)