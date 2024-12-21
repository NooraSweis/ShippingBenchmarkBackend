from shipping_benchmark.repositories.shipping_benchmark_repository import get_user_rates, get_aggregated_market_rates

def calculate_savings(user_email):
    user_rates = get_user_rates(user_email=user_email)
    market_data = get_aggregated_market_rates()

    results = []
    for user_rate in user_rates:
        for market_entry in market_data:
            if (
                user_rate.origin == market_entry.origin
                and user_rate.destination == market_entry.destination
                and user_rate.effective_date <= market_entry.date <= user_rate.expiry_date
            ):
                savings = {
                    "date": market_entry.date,
                    "origin": market_entry.origin,
                    "destination": market_entry.destination,
                    "user_price": float(user_rate.price),
                    "min_price": float(market_entry.min_price),
                    "percentile_10_price": float(market_entry.percentile_10_price),
                    "median_price": float(market_entry.median_price),
                    "percentile_90_price": float(market_entry.percentile_90_price),
                    "max_price": float(market_entry.max_price),
                    "potential_savings_min_price": (market_entry.min_price - user_rate.price)
                    * user_rate.annual_volume,
                    "potential_savings_percentile_10_price": (
                        market_entry.percentile_10_price - user_rate.price
                    )
                    * user_rate.annual_volume,
                    "potential_savings_median_price": (
                        market_entry.median_price - user_rate.price
                    )
                    * user_rate.annual_volume,
                    "potential_savings_percentile_90_price": (
                        market_entry.percentile_90_price - user_rate.price
                    )
                    * user_rate.annual_volume,
                    "potential_savings_max_price": (
                        market_entry.max_price - user_rate.price
                    )
                    * user_rate.annual_volume,
                }
                results.append(savings)
    return results
