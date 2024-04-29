from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import CountryWhitelist
import requests
import json


@login_required
def index(request):
    addr = request.META.get("REMOTE_ADDR")
    #res = requests.get(f"http://ip-api.com/json/{addr}")
    res = requests.get(f"http://ip-api.com/json/91.204.161.34")
    location_data_one = res.text
    location_data = json.loads(location_data_one)

    print(location_data)
    whitelisted_countries = [
        country.country_name for country in CountryWhitelist.objects.all()
    ]

    print(whitelisted_countries)
    if location_data["country"] in whitelisted_countries:

        return render(
            request,
            "index.html",
            {"data": location_data, "countries": whitelisted_countries},
        )
    else:
        return redirect("/error/")


def error_view(request):
    return render(request, "error.html")
