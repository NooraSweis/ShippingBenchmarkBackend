from django.urls import path
from shipping_benchmark.views.upload_cv_views import UploadCSV, UploadMarketRates
from shipping_benchmark.views.users_rates_views import RateSavingsAPI

urlpatterns = [
    path('upload-csv/', UploadCSV.as_view(), name='upload_csv'),
    path('upload-market-rates/', UploadMarketRates.as_view(), name='upload_market_rates'),
    path('rate-savings/', RateSavingsAPI.as_view(), name='rate_savings'),
]
