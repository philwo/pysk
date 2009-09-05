# -*- coding: utf-8 -*-

from django.contrib import admin
from pysk.voip.models import *

class SipAccountAdmin(admin.ModelAdmin):
    list_display = ("name", "user")

class DestinationAdmin(admin.ModelAdmin):
    list_display = ("id", "name_de", "name_en")

class CDRAdmin(admin.ModelAdmin):
    list_display = ("id", "sip_account", "quellrufnr", "zielrufnr", "beginn", "dauer", "dest", "vk", "ek")

admin.site.register(SipAccount, SipAccountAdmin)
admin.site.register(Destination, DestinationAdmin)
admin.site.register(CDR, CDRAdmin)
