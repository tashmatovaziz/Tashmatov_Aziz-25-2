from django.contrib import admin
from products.models import Products, Hashtag, Review

admin.site.register(Products)
admin.site.register(Hashtag)
admin.site.register(Review)