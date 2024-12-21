from shipping_benchmark.models.shipping_benchmark_models import UserRate, AggregatedMarketRate


def get_aggregated_market_rates(date=None, origin=None, destination=None):
    queryset = AggregatedMarketRate.objects.all()
    if date:
        queryset = queryset.filter(date=date)
    if origin:
        queryset = queryset.filter(origin=origin)
    if destination:
        queryset = queryset.filter(destination=destination)
    return queryset


def get_user_rates(user_email=None):
    if user_email:
        return UserRate.objects.filter(user_email=user_email)

    return UserRate.objects.all()
