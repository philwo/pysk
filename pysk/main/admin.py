# -*- coding: utf-8 -*-

from django.contrib import admin
from pysk.main.models import *

# Create your models here.
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("get_username", "kundennr", "anrede", "name", "land", "plz", "ort", "is_active")
    list_display_links = ("name", "get_username")
    #list_filter = ("is_active",)
    search_fields = ["user__username", "firma", "user__first_name", "user__last_name"]

class SipAccountAdmin(admin.ModelAdmin):
    list_display = ("name", "user")

class DestinationAdmin(admin.ModelAdmin):
    list_display = ("id", "name_de", "name_en")

class CDRAdmin(admin.ModelAdmin):
    list_display = ("id", "sip_account", "quellrufnr", "zielrufnr", "beginn", "dauer", "dest", "vk", "ek")

admin.site.register(Customer, CustomerAdmin)
admin.site.register(SipAccount, SipAccountAdmin)
admin.site.register(Destination, DestinationAdmin)
admin.site.register(CDR, CDRAdmin)

