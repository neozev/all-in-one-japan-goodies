import asyncio
from django.shortcuts import render
from django.shortcuts import redirect
from .models import SavedKeyword
from .utils.scrapers import yahoo_scrape, mercari_scrape

def delete_keyword(request, keyword_id):
    SavedKeyword.objects.filter(id=keyword_id).delete()
    return redirect("home")

def save_keyword(request):
    if request.method == "POST":
        keyword = request.POST.get("keyword", "").strip()
        if keyword:
            SavedKeyword.objects.get_or_create(keyword=keyword)
    return redirect("home")

def home(request):
    saved_keywords = SavedKeyword.objects.all().order_by("keyword")
    product_info_list = []
    yahoo_list = []
    mercari_list = []

    keyword = request.GET.get("product", "").strip()
    category = request.GET.get("category")
    condition = request.GET.get("condition")
    sort = request.GET.get("sort")
    page = int(request.GET.get("page", 1))
    pricemin = request.GET.get("pricemin", None)
    pricemax = request.GET.get("pricemax", None)
    yahoo_enabled = request.GET.get("yahoo_enabled") == "on"
    mercari_enabled = request.GET.get("mercari_enabled") == "on"

    is_search = "product" in request.GET

    if is_search:
        if not keyword:
            return render(request, "core/home.html", {
                "saved_keywords": saved_keywords,
                "error": "Please enter a keyword before searching.",
            })

        if not yahoo_enabled and not mercari_enabled:
            return render(request, "core/home.html", {
                "saved_keywords": saved_keywords,
                "error": "Please select at least one store.",
            })

        # Save keyword if not empty
        if keyword:
            SavedKeyword.objects.get_or_create(keyword=keyword)

        if yahoo_enabled:
            yahoo_enabled = "on"
            yahoo_list = yahoo_scrape(keyword, category, condition, sort, page, pricemin, pricemax)

        if mercari_enabled:
            mercari_enabled = "on"
            mercari_list = asyncio.run(mercari_scrape(keyword, category, condition, sort, page, pricemin, pricemax))

        if yahoo_list or mercari_list or (yahoo_list and mercari_list):
            product_info_list += yahoo_list + mercari_list

        elif yahoo_list or mercari_list or (yahoo_list and mercari_list) == []:
            return render(request, "core/home.html", {
                    "saved_keywords": saved_keywords,
                    "error": "No items found!",
                })

        if sort == "lowprice":
            product_info_list.sort(
                key=lambda x: x.get("currentprice") or float("inf")
                )

        elif sort == "highprice":
            product_info_list.sort(
                key=lambda x: x.get("currentprice") or 0,
                reverse=True
                )

    return render(request, 'core/home.html', {
        'product_info_list': product_info_list,
        'saved_keywords': saved_keywords,
        'keyword': keyword,
        'category': category,
        'condition': condition,
        'sort': sort,
        'pricemin' : pricemin,
        'pricemax' : pricemax,
        'yahoo_enabled' : yahoo_enabled,
        'mercari_enabled' : mercari_enabled,
        'page': page
    })
