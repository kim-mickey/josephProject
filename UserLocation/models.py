from django.db import models


# Create your models here.
class CountryWhitelist(models.Model):
    country_name = models.CharField(max_length=100, unique=True)
    country_code = models.CharField(max_length=3, unique=True) # iso3 country code

    def __str__(self) -> str:
        return f"{self.country_name} - {self.country_code}"
