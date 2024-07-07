# products/views.py
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import UserSerializer
from django.http import HttpResponse
from django.db.models import Sum, Max, F
import pandas as pd
from .models import Product

class SignUpView(APIView):
    def post(self, request):
        """
        Handles the HTTP POST request to create a new user.
        Args:
            request (HttpRequest): The HTTP request object containing the user data.
        Returns:
            Response: The HTTP response object containing the serialized user data if the user is successfully created,
                     or the serialized error messages if the user data is invalid.
                     If an exception occurs during the process, a response with a 500 status code and a detail message
                     is returned.
        Raises:
            None
        """
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("error: ", e)
            return Response({'detail': "something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
class LoginView(APIView):
    def post(self, request):
        """
        A function that handles the POST request for user login. 
        It validates the user credentials, generates a refresh token, 
        and returns the appropriate response including a new access token.
        """
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            user = User.objects.filter(username=username).first()
            if user and user.check_password(password):
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print("error: ", e)
            return Response({'detail': "something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def summary_report_csv(request):
    """
    A function that generates a summary report based on Product data. 
    It calculates the total revenue, top product quantity sold, and top product
    for each category. It then creates a CSV response containing this summary data.
    """
    try:
        summary = Product.objects.values('category').annotate(
            total_revenue=Sum(F('price') * F('quantity_sold')),
            top_product_quantity_sold=Max('quantity_sold'),
            top_product=F('product_name')
        ).order_by('category')

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="summary_report.csv"'
        df = pd.DataFrame(summary)
        # Write DataFrame to CSV
        df.to_csv(response, index=False, columns=['category', 'total_revenue', 'top_product', 'top_product_quantity_sold'])
        return response

    except DatabaseError as db_error:
        # Handle database connection issues
        print(f"DatabaseError occurred: {db_error}")
        return HttpResponse("Database connection error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except OperationalError as op_error:
        # Handle database operational errors
        print(f"OperationalError occurred: {op_error}")
        return HttpResponse("Database operational error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except FileNotFoundError as file_error:
        # Handle file not found errors
        print(f"FileNotFoundError occurred: {file_error}")
        return HttpResponse("File not found error", status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        # Handle any other unexpected exceptions
        print(f"Unexpected error occurred: {e}")
        return HttpResponse("Unexpected error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def summary_report(request):
    """
    A function that generates a summary report based on Product data.
    It calculates the total revenue, top product quantity sold, and top product
    for each category.
    """
    summary = Product.objects.values('category').annotate(
        total_revenue=Sum(F('price') * F('quantity_sold')),
        top_product_quantity_sold=Max('quantity_sold'),
        top_product=F('product_name')
    ).order_by('category')

    context = {
        'summary': summary,
    }

    return render(request, 'products/summary_report.html', context)
