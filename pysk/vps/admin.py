# -*- coding: utf-8 -*-

from django.contrib import admin
from pysk.vps.models import *

from django.utils.translation import ugettext_lazy as _

## Admin classes

class DomainAdmin(admin.ModelAdmin):
    list_display = ("name", "mx1", "serial", "active",)
    list_display_links = ("name",)
    fieldsets = (
        (None, {
            "fields": ("name", "active")
        }),
        (_(u"Nameservers"), {
            "fields": ("ns1", "ns2", "ns3", "ns4", "ns5", "ns6")
        }),
        (_(u"Mail Exchange"), {
            "fields": ("mx1", "mx2", "mx3")
        }),
        (_(u"Jabber Server"), {
            "fields": ("jabber",)
        }),
        (_(u"Special options"), {
            "classes": ("collapse",),
            "fields": ("is_gafyd",)
        })
    )

class NSEntryAdmin(admin.ModelAdmin):
    list_display = ("fqdn", "type", "value",)
    list_display_links = ("fqdn",)
    fieldsets = (
        (None, {
            "fields": ("host", "domain", "type", "value")
        }),
        (_(u"SRV records"), {
            "classes": ("collapse",),
            "fields": ("port", "weight", "priority")
        }),
    )

class IPAddressAdmin(admin.ModelAdmin):
    list_display = ("ip",)

class AliasAdmin(admin.ModelAdmin):
    list_display = ("fqdn", "target", "active",)
    list_display_links = ("fqdn",)

class MailboxAdmin(admin.ModelAdmin):
    list_display = ("mail", "domain", "quota", "active",)
    list_display_links = ("mail", "domain",)

class ForwardingAdmin(admin.ModelAdmin):
    list_display = ("email", "target", "active",)
    list_display_links = ("email",)

class DirectAliasInline(admin.TabularInline):
    model = DirectAlias
    extra = 3

class VirtualHostAdmin(admin.ModelAdmin):
    list_display = ("fqdn", "ipport", "ssl_cert", "ssl_key", "force_www", "ssl_enabled", "ssl_force", "apache_enabled", "active",)
    list_display_links = ("fqdn",)
    inlines = [DirectAliasInline]
    fieldsets = (
        (None, {
            "fields": ("name", "domain", "ipport", "active")
        }),
        (_(u"nginx Webserver"), {
            "fields": ("force_www", "nginx_config", )
        }),
        (_(u"Apache Webserver"), {
            "fields": ("apache_enabled", "apache_config")
        }),
        (_(u"SSL"), {
            "fields": ("ssl_enabled", "ssl_force", "ssl_cert", "ssl_key")
        }),
    )

admin.site.register(Domain, DomainAdmin)
admin.site.register(NSEntry, NSEntryAdmin)
admin.site.register(IPAddress, IPAddressAdmin)
admin.site.register(Alias, AliasAdmin)
admin.site.register(Mailbox, MailboxAdmin)
admin.site.register(Forwarding, ForwardingAdmin)
admin.site.register(VirtualHost, VirtualHostAdmin)
