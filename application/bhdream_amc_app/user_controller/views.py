from django.shortcuts import render
##from django.http import HttpResponse
from rest_framework.authtoken.models import Token
from rest_framework import generics,status
from .serializers import UserProfileSerializer,EquitySymbolSerializer,InvestmentSerializer,UserSerializer,SignUpSerializer,SignInSerializer
from .models import UserProfile,EquitySymbol,Investment
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
##

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
# Create your views here.
##def signin(request):
    ##return HttpResponse("signin")

##ef signup(request):
    ##return HttpResponse("signup")

class UserView(generics.CreateAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer

class UserProfileView(generics.CreateAPIView):
    queryset=UserProfile.objects.all()
    serializer_class=UserProfileSerializer

class EquitySymbolView(generics.CreateAPIView):
    queryset=EquitySymbol.objects.all()
    serializer_class=EquitySymbolSerializer

class InvestmentView(generics.CreateAPIView):
    queryset=Investment.objects.all()
    serializer_class=InvestmentSerializer

'''class SignUpView(APIView):
    serializer_class=SignUpSerializer

    def post(self,request,format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid():
            last_name=serializer.data.get('last_name')
            first_name=serializer.data.get('first_name')
            username=serializer.data.get('username')
            email=serializer.data.get('email')
            password=serializer.data.get('password')
            user=User(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
            user.save()
            return Response(SignInSerializer(user).data,status=status.HTTP_201_CREATED)
        return Response({'Bad Request':'username or email already exist'},status=status.HTTP_400_BAD_REQUEST)'''

'''class SignUpView(APIView):
    serializer_class = SignUpSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            last_name=serializer.data.get('last_name')
            first_name=serializer.data.get('first_name')
            username = serializer.data.get('username')
            password = serializer.data.get('password')
            email = serializer.data.get('email')
            user = User.objects.create_user(username=username, password=password, email=email,last_name=last_name,first_name=first_name)
            return Response(SignInSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response({'Bad Request': 'Invalid input data'}, status=status.HTTP_400_BAD_REQUEST)'''

'''class SignInView(APIView):
    serializer_class = SignInSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            username = serializer.data.get('username')
            password = serializer.data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)  # Log in the user
                return Response({'message': 'Successfully signed in'}, status=status.HTTP_200_OK)
        
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)  ''' 
'''class SignInView(APIView):
    serializer_class=SignInSerializer
    
    def post(self,request,format=None):
        
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        serializer=self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            username=serializer.data.get('username')
            password=serializer.data.get('password')
            queryset=User.objects.filter(username=username,password=password)
            if queryset.exists():
                user=User(username=username)
                return Response(SignInSerializer(user).data,status=status.HTTP_202_ACCEPTED)
        return Response({'Bad Request':'username or email already exist'},status=status.HTTP_400_BAD_REQUEST)'''
class SignUpView(APIView):
    serializer_class = SignUpSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            first_name=serializer.validated_data.get('first_name')
            last_name=serializer.validated_data.get('last_name')
            is_employee=serializer.validated_data.get('isEmployee')
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            email = serializer.validated_data.get('email')

            user, created = User.objects.get_or_create(username=username, email=email)
            user.set_password(password)
            user.save()

            token, created = Token.objects.get_or_create(user=user)

            return Response({'token': token.key}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.authtoken.views import ObtainAuthToken

class SignInView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(SignInView, self).post(request, *args, **kwargs)
        return response
    
@permission_classes([IsAuthenticated])
class ProtectedResourceView(APIView):
    def get(self, request, format=None):
        # The user is authenticated via the token if they reach this view
        user = request.user  # This is the user associated with the token

        # You can access the user's information and perform actions based on the user
        response_data = {
            "message": "This is a protected resource",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        }

        return Response(response_data)