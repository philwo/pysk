# -*- coding: utf-8 -*-

from django.contrib import admin
from pysk.vps.models import *

## Utility classes

class ForeignKeyFilter(object):
    def formfield_for_dbfield(self, db_field, **kwargs):
        # Only show the foreign key objects from the rendered filter.
        filters = getattr(self, 'foreignkey_filters', None)
        if filters and db_field.name in filters:
            kwargs['queryset'] = filters[db_field.name](get_current_user())
        return admin.ModelAdmin.formfield_for_dbfield(self, db_field, **kwargs)

## Admin classes

class DomainAdmin(admin.ModelAdmin):
    def queryset(self, request):
        if request.user.is_superuser:
            return Domain.objects.all()
        return Domain.objects.filter(owner=request.user)

    list_display = ("owner", "name", "mx1", "serial", "active")
    list_display_links = ("name",)
    fieldsets = (
        (None, {
            "fields": ("name", "owner", "active")
        }),
        ("Nameservers", {
            "fields": ("ns1", "ns2", "ns3", "ns4", "ns5", "ns6")
        }),
        ("Mail Exchange", {
            "fields": ("mx1", "mx2", "mx3")
        }),
        ("Special options", {
            "fields": ("is_gafyd", )
        })
    )

class NSEntryAdmin(admin.ModelAdmin):
    def queryset(self, request):
        if request.user.is_superuser:
            return NSEntry.objects.all()
        return NSEntry.objects.filter(domain__owner=request.user)

    list_display = ("owner", "fqdn", "type", "value")
    #list_display = ("owner", "host", "domain", "type", "value")
    list_display_links = ("fqdn",)
    #list_display_links = ("host", "domain",)
    fieldsets = (
        (None, {
            "fields": ("host", "domain", "type", "value")
        }),
        ("SRV records", {
            "fields": ("port", "weight", "priority")
        }),
    )

class IPAddressInline(admin.StackedInline):
    def queryset(self, request):
        if request.user.is_superuser:
            return IPAddress.objects.all()
        return IPAddress.objects.filter(server__owner=request.user)

    model = IPAddress
    fk_name = "server"
    extra = 1

class ServerAdmin(admin.ModelAdmin):
    def queryset(self, request):
        if request.user.is_superuser:
            return Server.objects.all()
        return Server.objects.filter(owner=request.user)

    list_display = ("owner", "id", "fqdn", "main_ip", "active")
    list_display_links = ("id", "fqdn")
    inlines = [
        IPAddressInline,
    ]

class AliasAdmin(admin.ModelAdmin):
    def queryset(self, request):
        if request.user.is_superuser:
            return Alias.objects.all()
        return Alias.objects.filter(owner=request.user)

    list_display = ("owner", "fqdn", "target", "active")
    list_display_links = ("fqdn",)

class MailboxAdmin(admin.ModelAdmin):
    def queryset(self, request):
        if request.user.is_superuser:
            return Mailbox.objects.all()
        return Mailbox.objects.filter(owner=request.user)

    list_display = ("owner", "mail", "domain", "quota", "active")
    list_display_links = ("mail", "domain")

class ForwardingAdmin(admin.ModelAdmin):
    def queryset(self, request):
        if request.user.is_superuser:
            return Forwarding.objects.all()
        return Forwarding.objects.filter(owner=request.user)

    list_display = ("owner", "source", "domain", "target", "active")
    list_display_links = ("source", "domain")

class DirectAliasInline(admin.TabularInline):
    def queryset(self, request):
        if request.user.is_superuser:
            return DirectAlias.objects.all()
        return DirectAlias.objects.filter(host__owner=request.user)

    model = DirectAlias
    extra = 3

class HostConfigInline(admin.StackedInline):
    def queryset(self, request):
        if request.user.is_superuser:
            return HostConfig.objects.all()
        return HostConfig.objects.filter(host__owner=request.user)

    model = HostConfig
    extra = 1

class VirtualHostAdmin(admin.ModelAdmin):
    def queryset(self, request):
        if request.user.is_superuser:
            return VirtualHost.objects.all()
        return VirtualHost.objects.filter(owner=request.user)

    list_display = ("owner", "fqdn", "dns_ip", "active")
    #list_display = ("owner", "fqdn", "dns_ip", "active", "check_availability")
    list_display_links = ("fqdn",)
    inlines = [HostConfigInline, DirectAliasInline]

admin.site.register(Domain, DomainAdmin)
admin.site.register(NSEntry, NSEntryAdmin)
admin.site.register(Server, ServerAdmin)
admin.site.register(Alias, AliasAdmin)
admin.site.register(Mailbox, MailboxAdmin)
admin.site.register(Forwarding, ForwardingAdmin)
admin.site.register(VirtualHost, VirtualHostAdmin)

