from django.db import models

class UserRate(models.Model):
    user_email = models.EmailField()
    origin = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    effective_date = models.DateField()
    expiry_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    annual_volume = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'users_rates'



class MarketRate(models.Model):
    date = models.DateField()
    origin = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'market_rates'

class AggregatedMarketRate(models.Model):
    date = models.DateField()
    origin = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    min_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    percentile_10_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    median_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    percentile_90_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    max_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        db_table = 'aggregated_market_rates'
