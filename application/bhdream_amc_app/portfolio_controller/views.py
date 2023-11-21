from django.shortcuts import render
from rest_framework.views import APIView
from .models import Investment,Equity
from .serializers import EquitySerializer,InvestmentSerializer
from rest_framework.response import Response
from django.db.models import Q
from rest_framework import status
from MoneyMetric.money_metric_insight_service import generate_portfolio,get_optimised_portfolio
from MoneyMetric.serializer import PortfolioDTOSerializer
from MoneyMetric.dto import PortfolioDTO
# Create your views here.
class EquityView(APIView):
    def get(self, request):
        Equities = Equity.objects.all()
        serializer = EquitySerializer(Equities, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EquitySerializer(data=request.data)
        if serializer.is_valid():
            symbol = serializer.validated_data.get('symbol')
            title = serializer.validated_data.get('title')
            
            if symbol is None or not symbol.strip() or title is None or not title.strip():
                raise serializer.ValidationError({'error': 'symbol or title cant be empty'})
            # Check if the user already exists
            equity_exists = Equity.objects.filter(Q(symbol=symbol) | Q(title=title)).exists()
            if equity_exists:
                raise serializer.ValidationError({'error': 'Equity already exists'})
            # If the user doesn't exist, create a new one
            equity = Equity.objects.create(symbol=symbol, title=title)
            equity.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        try:
            symbol = request.GET.get('symbol')
            equity = Equity.objects.get(symbol=symbol)
            equity.delete()
            return Response({"message": "equity deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Equity.DoesNotExist:
            return Response({"error": "equity not found"}, status=status.HTTP_404_NOT_FOUND)

class InvestmentView(APIView):
    def post(self, request, format=None):
        data=request.data
        data['user']=request.decoded_token.get('user_id')
        serializer = InvestmentSerializer(data=request.data)
        try:
            if serializer.is_valid():
                user = serializer.validated_data.get('user')
                equity = serializer.validated_data.get('equity')
                investment_date = serializer.validated_data.get('investment_date')
                shares = serializer.validated_data.get('shares')
                purchase_price = serializer.validated_data.get('purchase_price')

                # If the user doesn't exist, create a new one
                investment = Investment.objects.create(user=user, equity=equity, investment_date=investment_date, shares=shares, purchase_price=purchase_price)
                investment.save()

                return Response({'message': "investment added"}, status=status.HTTP_201_CREATED)

        except serializer.ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        user_id = request.decoded_token.get('user_id')  # Assuming the header key is 'id'

        if not user_id:
            return Response({"error": "User ID not provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_id = int(user_id)
        except ValueError:
            return Response({"error": "Invalid User ID "}, status=status.HTTP_400_BAD_REQUEST)

        investments = Investment.objects.filter(user_id=user_id)
        serializer = InvestmentSerializer(investments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request):
        try:
            id =  request.headers.get('id') 
            investment = Investment.objects.get(id=id)
            investment.delete()
            return Response({"message": "investment deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Equity.DoesNotExist:
            return Response({"error": "investment not found"}, status=status.HTTP_404_NOT_FOUND)

class PortfolioView(APIView):
    def get(self, request):
        user_id = request.decoded_token.get('user_id')  # Assuming the header key is 'id'

        if not user_id:
            return Response({"error": "User ID not provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_id = int(user_id)
        except ValueError:
            return Response({"error": "Invalid User ID "}, status=status.HTTP_400_BAD_REQUEST)

        investments = Investment.objects.filter(user_id=user_id)
        portfolio= generate_portfolio(investment_list=investments)
        serializer = PortfolioDTOSerializer(portfolio)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PortfolioOptimizationView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data

        # Deserialize the input data using the PortfolioDTOSerializer
        serializer = PortfolioDTOSerializer(data=data)
        if serializer.is_valid():
            # Use the validated data to create a PortfolioDTO instance
            portfolio_dto = PortfolioDTO.from_dict(serializer.validated_data)
            optimized_portfolio=get_optimised_portfolio(portfolio=portfolio_dto)
            # Now, you can use the 'portfolio_dto' object as needed in your application logic
            serializer = PortfolioDTOSerializer(optimized_portfolio)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Invalid data provided"}, status=status.HTTP_400_BAD_REQUEST)