from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
from shipping_benchmark.models.shipping_benchmark_models import UserRate, MarketRate


class UploadCSV(APIView):
    def post(self, request):
        user_email = request.data.get('user_email')
        file = request.FILES.get('file')

        # Validate presence of email and file
        if not user_email:
            return Response({"error": "User email is required"}, status=status.HTTP_400_BAD_REQUEST)
        if not file:
            return Response({"error": "File is required"}, status=status.HTTP_400_BAD_REQUEST)
        if not file.name.endswith('.xlsx'):
            return Response({"error": "File is not an Excel file"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Read the Excel file
            data = pd.read_excel(file)

            # Define the required columns
            required_columns = {
                'origin', 'destination', 'effective_date',
                'expiry_date', 'price', 'annual_volume'
            }

            # Check for missing columns
            missing_columns = required_columns - set(data.columns)
            if missing_columns:
                return Response(
                    {"error": f"Missing required fields: {missing_columns}."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Check for NaN values
            if data.isnull().values.any():
                return Response(
                    {"error": "CSV contains missing values."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Add user_email to each row and save to the database
            records = [
                UserRate(
                    user_email=user_email,
                    origin=row['origin'],
                    destination=row['destination'],
                    effective_date=row['effective_date'],
                    expiry_date=row['expiry_date'],
                    price=row['price'],
                    annual_volume=row['annual_volume']
                )
                for _, row in data.iterrows()
            ]
            UserRate.objects.bulk_create(records)

            return Response({"message": "Data uploaded successfully."}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class UploadMarketRates(APIView):
    def post(self, request):
        # Get the uploaded Excel file
        file = request.FILES.get('file')

        if not file:
            return Response({"error": "File is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Read the Excel file using pandas
            data = pd.read_excel(file)

            # Define required columns
            required_columns = {'date', 'origin', 'destination', 'price'}

            # Check if all required columns are present
            missing_columns = required_columns - set(data.columns)
            if missing_columns:
                return Response(
                    {"error": f"Missing required columns: {missing_columns}."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Add rows to the database
            records = [
                MarketRate(
                    date=datetime.strptime(row['date'], "%Y-%m-%d %H:%M:%S %Z").strftime("%Y-%m-%d"),
                    origin=row['origin'],
                    destination=row['destination'],
                    price=row['price']
                )
                for _, row in data.iterrows()
            ]

            # Use bulk_create to insert records efficiently
            MarketRate.objects.bulk_create(records)

            return Response(
                {
                    "message": "Data uploaded successfully."
                },
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
