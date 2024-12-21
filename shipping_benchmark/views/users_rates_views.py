from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from shipping_benchmark.components.users_rates_component import calculate_savings

class RateSavingsAPI(APIView):
    def get(self, request):
        try:
            user_email = request.query_params.get('user_email')

            if not user_email:
                return Response(
                    {"error": "user_email query parameter is required."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            data = calculate_savings(user_email)
            return Response({"results": data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
