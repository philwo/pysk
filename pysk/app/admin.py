# -*- coding: utf-8 -*-

from django.contrib import admin
from pysk.app.models import *

class CustomerAdmin(admin.ModelAdmin):
    list_display = ("get_username", "kundennr", "anrede", "name", "land", "plz", "ort", "is_active")
    list_display_links = ("name", "get_username")
    #list_filter = ("is_active",)
    search_fields = ["user__username", "firma", "user__first_name", "user__last_name"]

admin.site.register(Customer, CustomerAdmin)
