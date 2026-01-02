import random
from mercapi.requests import SearchRequestData
from urllib.parse import urlencode

categories = {
    "Cars and Motorcycles": {"yahoo": 26318, "mercari": 1318},
    "Fashion": {"yahoo": 23000, "mercari": 3088},
    "Baby Products": {"yahoo": 24202, "mercari": 3},
    "Toys and Games": {"yahoo": 25464, "mercari": 1328},
    "Hobby": {"yahoo": 24242, "mercari": 6386},
    "Tickets": {"yahoo": 2084043920, "mercari": 1027},
    "Books": {"yahoo": 21600, "mercari": 5},
    "Computers": {"yahoo": 23336, "mercari": 7},
    "Audio Video Equipment": {"yahoo": 23632, "mercari": 3888},
    "Sports and Leisure": {"yahoo": 24698, "mercari": 8},
    "Beauty": {"yahoo": 42177, "mercari": 6},
    "Food and Drinks": {"yahoo": 23976, "mercari": 1844},
    "Furniture and Interior": {"yahoo": 24198, "mercari": 4},
    }

yahoo_conditions = {
    "New and used": "1,2",
    "new": "1",
    "used": "2",
    }

yahoo_sort = {
    "newest": {"s1": "featured", "o1": "d"},
    "time": {"s1": "end", "o1": "a"},
    "lowprice": {"s1": "cbids", "o1": "a"},
    "highprice": {"s1": "cbids", "o1": "d"},
    }

mercari_conditions = {
    "New and used": [1, 2, 3, 4, 5, 6],
    "new": [1],
    "used": [2, 3, 4, 5, 6],
    }

mercari_sort = {
    "newest": (SearchRequestData.SortBy.SORT_CREATED_TIME,
               SearchRequestData.SortOrder.ORDER_DESC),
    "time": (SearchRequestData.SortBy.SORT_CREATED_TIME,
             SearchRequestData.SortOrder.ORDER_DESC),
    "lowprice": (SearchRequestData.SortBy.SORT_PRICE,
                 SearchRequestData.SortOrder.ORDER_ASC),
    "highprice": (SearchRequestData.SortBy.SORT_PRICE,
                  SearchRequestData.SortOrder.ORDER_DESC),
    }

def build_yahoo_url(keyword, category=None, condition=None, sort=None, page=None, pricemin=None, pricemax=None):
    base = "https://auctions.yahoo.co.jp/search/search"

    params = {
        "p": keyword,
        "va": keyword,
        "is_postage_mode": 0,
        "rc_ng": 1,
        "mode": 1,
        "n": 100,
    }

    if pricemin:
        params["min"] = pricemin
    if pricemax:
        params["max"] = pricemax
    if pricemin and pricemax:
        params["price_type"] = "currentprice"

    # Category (optional)
    if category in categories:
        params["auccat"] = categories[category]["yahoo"]

     # Condition
    if condition in yahoo_conditions:
        params["istatus"] = yahoo_conditions[condition]

    # Sorting
    if sort in yahoo_sort:
        params.update(yahoo_sort[sort])

    # Pagination
    params["b"] = 1 if page <= 1 else (page - 1) * 100 + 1

    return f"{base}?{urlencode(params)}"

def build_mercari_url(keyword, category=None, condition=None, sort=None, page=None, pricemin=None, pricemax=None):

    mercari_params = {
        "query": keyword,
        "price_min": pricemin,
        "price_max": pricemax,
        "categories": [],
        "item_conditions": [],
        "status": [SearchRequestData.Status.STATUS_ON_SALE],
        "page_token" : f"v1:{max(page - 1, 0)}",
    }

    # Category (optional)
    if category in categories:
        mercari_params["categories"] = [categories[category]['mercari']]

    # condition
    if condition in mercari_conditions:
        mercari_params["item_conditions"] = mercari_conditions[condition]

    # Sort Options
    sort_by, sort_order = mercari_sort.get(
        sort,
        (SearchRequestData.SortBy.SORT_SCORE,
         SearchRequestData.SortOrder.ORDER_DESC),
    )

    mercari_params["sort_by"] = sort_by
    mercari_params["sort_order"] = sort_order

    return mercari_params

def get_random_user_agent():

    USER_AGENTS = [

        # Windows Chrome
        (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),

        # MacOS Safari
        (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/605.1.15 (KHTML, like Gecko) "
            "Version/17.0 Safari/605.1.15"
        ),

        # Android Chrome
        (
            "Mozilla/5.0 (Linux; Android 12; Pixel 6) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/123.0.0.0 Mobile Safari/537.36"
        ),

        # iPhone Safari
        (
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
            "AppleWebKit/605.1.15 (KHTML, like Gecko) "
            "Version/17.0 Mobile/15E148 Safari/604.1"
        ),

        # Windows Firefox
        (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) "
            "Gecko/20100101 Firefox/122.0"
        ),
    ]

    return random.choice(USER_AGENTS)
