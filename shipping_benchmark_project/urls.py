from django.urls import path, include

urlpatterns = [
    path('api/', include('shipping_benchmark.routes.urls')),
]
