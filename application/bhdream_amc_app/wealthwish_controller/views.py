from django.shortcuts import render
from .models import Goal,FIRE
from rest_framework.views import APIView
from .serializer import GoalSerializer, FIRERequestSerializer,FIREResponseSerializer
from rest_framework.response import Response
from portfolio_controller.models import Investment
from MoneyMetric.money_metric_insight_service import generate_portfolio,calculate_future_value_sip,calculate_duration,calculate_monthly_contribution,future_value
from rest_framework import status
from datetime import date
# Create your views here.

class GoalView(APIView):
    def get(self, request):
        user_id=request.decoded_token['user_id']
        
        goals = Goal.objects.filter(user_id=user_id)
        serializer = GoalSerializer(goals, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        data=request.data
        data["user"]=request.decoded_token.get('user_id')
        
        serializer = GoalSerializer(data=data)
        investments=Investment.objects.filter(user_id=data['user'])
        portfolio=generate_portfolio(investment_list=investments)
        current_return=portfolio.current_return
        
        if 'monthly_contribution' not in data or data['monthly_contribution'] is None:
            data['monthly_contribution']=calculate_monthly_contribution(cagr=current_return,
                                                                        future_value=data['goal_amount'],
                                                                        duration_months=data['duration_in_months'])
        elif 'goal_amount' not in data or data['goal_amount'] is None:
            data['goal_amount']=calculate_future_value_sip(cagr=current_return,
                                                           duration_months=data['duration_in_months'], 
                                                           monthly_contribution=data['monthly_contribution'])
        elif 'duration_in_months' not in data or data['duration_in_months'] is None:
            data['duration_in_months'] =calculate_duration(cagr=current_return,
                                                           monthly_contribution=data['monthly_contribution'],
                                                           future_value=data['goal_amount'])
        else:
            raise ValueError({'error': 'entered data is not right'})
        
        if serializer.is_valid():
            user = serializer.validated_data.get('user')
            name = serializer.validated_data.get('name')
            duration_in_months = serializer.validated_data.get('duration_in_months')
            monthly_contribution = serializer.validated_data.get('monthly_contribution')
            goal_amount = serializer.validated_data.get('goal_amount')
            
            goal_exists = Goal.objects.filter(user=user, name=name).exists()
            
            if goal_exists:
                raise serializer.ValidationError({'error': 'goal already exists'})
            
            goal = Goal.objects.create(user=user, 
                                       name=name,
                                       duration_in_months=duration_in_months,
                                       monthly_contribution=monthly_contribution,
                                       goal_amount=goal_amount)
            goal.save()
            goal_serializer=GoalSerializer(goal)
            return Response(goal_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request):
        try:
            name =  request.headers.get('name', None)
            goal = Goal.objects.get(name=name)
            goal.delete()
            return Response({"message": "goal deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Goal.DoesNotExist:
            return Response({"error": "goal not found"}, status=status.HTTP_404_NOT_FOUND)
        
    def put(self, request):
        try:
            user_id = request.decoded_token['user_id']
            investments = Investment.objects.filter(user_id=user_id)
            portfolio = generate_portfolio(investment_list=investments)
            current_return = portfolio.current_return
             # Get the data to be updated
            data = request.data
            # Check if the goal exists
            goal = Goal.objects.get(user_id=user_id, name=data['name'])
            # Update the goal with the new data
            if 'monthly_contribution' not in data or data['monthly_contribution'] is None:
                goal.monthly_contribution=calculate_monthly_contribution(cagr=current_return,
                                                                            future_value=data['goal_amount'],
                                                                            duration_months=data['duration_in_months'])
                goal.goal_amount=data['goal_amount']
                goal.duration_in_months=data['duration_in_months']
            elif 'goal_amount' not in data or data['goal_amount'] is None:
                goal.goal_amount=calculate_future_value_sip(cagr=current_return,
                                                               duration_months=data['duration_in_months'], 
                                                               monthly_contribution=data['monthly_contribution'])
                goal.duration_in_months=data['duration_in_months']
                goal.monthly_contribution=data['monthly_contribution']
            elif 'duration_in_months' not in data or data['duration_in_months'] is None:
                goal.duration_in_months =calculate_duration(cagr=current_return,
                                                               monthly_contribution=data['monthly_contribution'],
                                                               future_value=data['goal_amount'])
                goal.goal_amount=data['goal_amount']
                goal.monthly_contribution=data['monthly_contribution']
            else:
                raise ValueError({'error': 'entered data is not right'})
                   
            
            
            # Save the updated goal
            goal.save()
            # Return the updated goal data
            goal_serializer = GoalSerializer(goal)
            return Response(goal_serializer.data, status=status.HTTP_200_OK)

        except Goal.DoesNotExist:
            return Response({"error": "Goal not found"}, status=status.HTTP_404_NOT_FOUND)
        
class ActivateGoalView(APIView):
    def put(self, request):
        try:
            user_id = request.decoded_token['user_id']
             # Get the data to be updated
            data = request.data
            # Check if the goal exists
            goal = Goal.objects.get(user_id=user_id, name=data['name'])
            goal.is_active=data.get('is_active', False)
            if goal.is_active:
                goal.active_date=date.today().strftime("%Y-%m-%d")
            # Save the updated goal
            goal.save()
            # Return the updated goal data
            goal_serializer = GoalSerializer(goal)
            return Response(goal_serializer.data, status=status.HTTP_200_OK)

        except Goal.DoesNotExist:
            return Response({"error": "Goal not found"}, status=status.HTTP_404_NOT_FOUND)


class FIREView(APIView):
    def get(self, request):
        user_id=request.decoded_token['user_id']
        
        fire = FIRE.objects.filter(user=user_id)
        if(not fire.exists()):
            return Response(None,status=status.HTTP_204_NO_CONTENT)
        
        return Response(FIREResponseSerializer(fire.first()).data)
    
    def post(self, request):
        data=request.data
        data["user"]=request.decoded_token.get('user_id')
        
        serializer = FIRERequestSerializer(data=data)
        #investments=Fil.objects.filter(user_id=data['user'])
        #portfolio=generate_portfolio(investment_list=investments)
        #current_return=portfolio.current_return
        
       
        if serializer.is_valid():
            user = serializer.validated_data.get('user')
            duration = serializer.validated_data.get('duration')
            todays_yearly_requirement = serializer.validated_data.get('todays_yearly_requirement')
            
            f_v=future_value(principal=float(todays_yearly_requirement),time=duration)
            fire_amount=f_v/0.05                              #considering user will be able to generate atleast or more 5% after tax on corpus
            fire_plan = FIRE.objects.filter(user=user).first()

            if not fire_plan:
                fire_plan = FIRE.objects.create(
                    user=user,
                    duration=duration,
                    expected_inflation=6,
                    todays_yearly_requirement=todays_yearly_requirement,
                    FIRE_amount=fire_amount
                )
                fire_plan.save()
            fire_plan.duration=duration
            fire_plan.todays_yearly_requirement=todays_yearly_requirement
            fire_plan.FIRE_amount=fire_amount
            fire_plan.save()
            # Now fire_plan is an instance of the FIRE model, and you can pass it to the serializer
            response_serializer = FIREResponseSerializer(fire_plan)
            
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)