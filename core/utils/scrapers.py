import requests
import time
from bs4 import BeautifulSoup
from mercapi import Mercapi
from .search import get_random_user_agent, build_yahoo_url
from .search import build_mercari_url

def get_content(url):
    session = requests.Session()
    session.headers.update({
        "User-Agent": get_random_user_agent(),
        "Accept-Language": "en-US,en;q=0.5",
        "Content-Language": "en-US",
        "Connection": "keep-alive",
    })

    response = session.get(url, timeout=15)
    return response.text

def yahoo_scrape(keyword, category, condition, sort, page, pricemin, pricemax):
    yahoo_url = build_yahoo_url(keyword=keyword, category=category, condition=condition, sort=sort, page=page, pricemin=pricemin, pricemax=pricemax)
    html = get_content(yahoo_url)
    yahoo_product_info_list = []

    MAX_RETRIES = 5
    DELAY = 1.5

    # Detects a website that is not fully loaded
    mole = "<!DOCTYPE HTML>"

    for attempt in range(MAX_RETRIES):
        print(f"Yahoo attempt {attempt + 1} / {MAX_RETRIES}...")

        if mole not in html:
            print("Results found. Proceeding...")

            yahoo_soup = BeautifulSoup(html, 'html.parser')
            items = yahoo_soup.select("li.Product, li.Item--grid")

            for item in items:
                img_tag = item.select_one("img.Item__imageData, img.Product__imageData")
                name_tag = item.select_one("h3.Product__title, span.Item__title")
                time_tag = item.select_one("dd.Product__time, div.Item__data")
                link_tag = item.find("a", class_="Product__imageLink")
                link = link_tag.get("href") if link_tag else None

                price_spans = item.find_all("span", class_="Product__priceValue")
                current_price_tag = None
                buynow_price_tag = None

                for span in price_spans:
                    classes = span.get("class", [])
                    if "u-textRed" in classes:
                        current_price_tag = span
                    else:
                        buynow_price_tag = span

                if img_tag and name_tag and current_price_tag:
                    yahoo_product_info_list.append({
                        'name': name_tag.get_text(strip=True),
                        'currentprice': int(current_price_tag.get_text(strip=True).replace(",", "").replace("円", "")),
                        'buynowprice': f"Buy now {buynow_price_tag.get_text(strip=True).replace(',', '').replace('円', '')}" if buynow_price_tag else "",
                        'image_url': img_tag.get("src", ""),
                        'time': time_tag.get_text(strip=True),
                        'link': link,
                        'source': 'yahoo'
                    })

            return yahoo_product_info_list

        print("No results found, retrying...")
        time.sleep(DELAY)
        html = get_content(yahoo_url)

    else:
        print("Max retries reached. Proceeding with last response.")
        return []


async def mercari_scrape(keyword, category, condition, sort, page, pricemin, pricemax):
    search_conditions = build_mercari_url(keyword=keyword, category=category, condition=condition, sort=sort, page=page, pricemin=pricemin, pricemax=pricemax)
    api = Mercapi()
    results = await api.search(**search_conditions)

    mercari_product_info_list = []

    for item in results.items:
        name = item.name
        price_tag = item.price
        thumbnail_url = extract_thumbnail(item)
        link = link_selector(item.id_)

        if name and price_tag and thumbnail_url and link:
            mercari_product_info_list.append({
                'name': name,
                'currentprice': int(price_tag),
                'image_url': thumbnail_url,
                'link': link,
                'source' : 'mercari'
            })

    return mercari_product_info_list

def link_selector(itemid):

    if itemid.startswith("m"):
        newlink = f"https://jp.mercari.com/item/{itemid}"

    else:
        newlink = f"https://jp.mercari.com/shops/product/{itemid}"

    return newlink

def extract_thumbnail(item):
    thumbs = item.thumbnails

    if not thumbs:
        return None

    # Case C: a single string
    if isinstance(thumbs, str):
        return thumbs

    # Case B: list of strings
    if isinstance(thumbs, list) and isinstance(thumbs[0], str):
        return thumbs[0]

    # Case A: list of objects with .url
    if hasattr(thumbs[0], "url"):
        return thumbs[0].url

    return None
