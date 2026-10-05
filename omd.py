from collections import Counter
from typing import Any


MOSCOW = {201, 202, 203, 204}
KAZAN = {203, 204, 205, 206}
QUERIES = [
    'чехол',
    'iphone',
    'чехол',
    'наушники',
    'iphone',
    'iphone',
    'кабель',
    'чехол',
    'iphone',
]
ORDERS = [
    {'id': 1, 'buyer': 'anya', 'status': 'delivered', 'amount': 900},
    {'id': 2, 'buyer': 'boris', 'status': 'returned', 'amount': 4_500},
    {'id': 3, 'buyer': 'anya', 'status': 'delivered', 'amount': 1_500},
    {'id': 4, 'buyer': 'vera', 'status': 'delivered', 'amount': 3_200},
    {'id': 5, 'buyer': 'boris', 'status': 'delivered', 'amount': 700},
    {'id': 6, 'buyer': 'gleb', 'status': 'returned', 'amount': 2_100},
]
DAYS = [
    {'day': 'пн', 'orders': 20, 'revenue': 40_000, 'returns': 2},
    {'day': 'вт', 'orders': 16, 'revenue': 19_200, 'returns': 4},
    {'day': 'ср', 'orders': 25, 'revenue': 55_000, 'returns': 1},
    {'day': 'чт', 'orders': 10, 'revenue': 12_000, 'returns': 3},
    {'day': 'пт', 'orders': 30, 'revenue': 48_000, 'returns': 3},
]
REVIEWS = [
    {'id': 1, 'product': 'Чехол', 'stars': 5},
    {'id': 1, 'product': 'Чехол', 'stars': 3},
    {'id': 1, 'product': 'Чехол', 'stars': 4},
    {'id': 2, 'product': 'Наушники', 'stars': 2},
    {'id': 2, 'product': 'наушники', 'stars': 2},
    {'id': 2, 'product': 'НАУШНИКИ', 'stars': 5},
    {'id': 3, 'product': 'Планшет', 'stars': 5},
    {'id': 4, 'product': 'Колонка', 'stars': 4},
    {'id': 4, 'product': 'Колонка', 'stars': 4},
    {'id': 5, 'product': 'Кабель', 'stars': 1},
]


def compare_warehouse_data(
    first_warehouse: set[int],
    second_warehouse: set[int],
) -> tuple[set[int], set[int], set[int], int]:
    common_items = first_warehouse.intersection(second_warehouse)
    only_first_items = first_warehouse.difference(second_warehouse)
    only_second_items = second_warehouse.difference(first_warehouse)
    count_different_items = len(first_warehouse.union(second_warehouse))

    return (
        common_items,
        only_first_items,
        only_second_items,
        count_different_items,
    )


def analyze_queries(
    queries: list[str],
) -> tuple[int, Counter[str], str, float, list[str]]:
    total_queries = len(queries)
    query_counts = Counter(queries)
    top_query, top_count = query_counts.most_common(1)[0]
    top_query_share = top_count / total_queries
    single_queries = [
        query for query, count in query_counts.items() if count == 1
    ]

    return (
        total_queries,
        query_counts,
        top_query,
        top_query_share,
        single_queries,
    )


def analyze_orders(
    orders: list[dict[str, Any]],
) -> tuple[int, set[str], int, float]:
    returned_orders = [
        order for order in orders if order['status'] == 'returned'
    ]
    delivered_orders = [
        order for order in orders if order['status'] == 'delivered'
    ]

    returned_sum = sum(order['amount'] for order in returned_orders)
    returned_buyers = {order['buyer'] for order in returned_orders}
    delivered_count = len(delivered_orders)
    delivered_sum = sum(order['amount'] for order in delivered_orders)
    avg_bill = delivered_sum / delivered_count

    return (
        returned_sum,
        returned_buyers,
        delivered_count,
        avg_bill,
    )


def analyze_days(
    days: list[dict[str, Any]],
) -> tuple[int, str, dict[str, float], list[str]]:
    total_revenue = sum(day['revenue'] for day in days)

    day_max_revenue = ''
    max_revenue = 0
    for day in days:
        if day['revenue'] > max_revenue:
            max_revenue = day['revenue']
            day_max_revenue = day['day']

    revenue_per_order = {
        day['day']: day['revenue'] / day['orders'] for day in days
    }
    high_return_days = [
        day['day'] for day in days
        if day['returns'] / day['orders'] > 0.2
    ]

    return (
        total_revenue,
        day_max_revenue,
        revenue_per_order,
        high_return_days,
    )


def analyze_reviews(
    reviews: list[dict[str, Any]],
) -> tuple[dict[str, float], str, int, float]:
    stars_product: dict[str, list[int]] = {}
    for review in reviews:
        product = review['product'].lower()
        if product not in stars_product:
            stars_product[product] = []
        stars_product[product].append(review['stars'])

    avg_stars = {
        product: sum(stars) / len(stars)
        for product, stars in stars_product.items()
    }

    worst_product = ''
    worst_avg = float('inf')
    for product, stars in stars_product.items():
        if len(stars) >= 2 and avg_stars[product] < worst_avg:
            worst_avg = avg_stars[product]
            worst_product = product

    low_reviews_count = sum(review['stars'] <= 2 for review in reviews)
    low_reviews_share = low_reviews_count / len(reviews)

    return (
        avg_stars,
        worst_product,
        low_reviews_count,
        low_reviews_share,
    )


if __name__ == '__main__':
    # task 1
    print(compare_warehouse_data(MOSCOW, KAZAN))

    # task 2
    print(analyze_queries(QUERIES))

    # task 3
    print(analyze_orders(ORDERS))

    # task 4
    print(analyze_days(DAYS))

    # task 5
    print(analyze_reviews(REVIEWS))
