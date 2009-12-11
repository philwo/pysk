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
    fieldsets = (
        (None, {
            "fields": ("active",)
        }),
        (_(u"Source"), {
            "fields": ("source", "domain")
        }),
        (_(u"Destination"), {
            "fields": ("target",)
        }),
    )

class DirectAliasInline(admin.TabularInline):
    model = DirectAlias
    extra = 3

class VirtualHostAdmin(admin.ModelAdmin):
    list_display = ("fqdn", "owner", "ipport", "ssl_cert", "ssl_key", "force_www", "ssl_enabled", "ssl_force", "apache_enabled", "active",)
    list_display_links = ("fqdn",)
    inlines = [DirectAliasInline]
    fieldsets = (
        (None, {
            "fields": ("name", "domain", "owner", "ipport", "active")
        }),
        (_(u"Features"), {
            "fields": ("enable_php", "php_config")
        }),
        (_(u"nginx Webserver"), {
            "fields": ("force_www", "nginx_config")
        }),
        (_(u"Apache Webserver"), {
            "fields": ("apache_enabled", "apache_config")
        }),
        (_(u"SSL"), {
            "fields": ("ssl_enabled", "ssl_force", "ssl_cert", "ssl_key")
        }),
    )

class PHPExtensionInline(admin.TabularInline):
    model = PHPExtension
    extra = 1
    
class PHPConfigInline(admin.StackedInline):
    model = PHPConfig
    extra = 1

class PHPExtensionAdmin(admin.ModelAdmin):
    list_display = ("enabled","name",)
    list_editable = ("enabled",)
    list_display_links = ("name",)

class PHPConfigAdmin(admin.ModelAdmin):
    list_display = ("name",)
    list_display_links = ("name",)
    fieldsets = (
        (None, {
            "fields": ("name",)
        }),
        (_(u"Language features"), {
            "fields": ("short_open_tag", "allow_call_time_pass_reference", "session_bug_compat_42", "session_bug_compat_warn")
        }),
        (_(u"Limits"), {
            "fields": ("max_execution_time", "max_input_time", "memory_limit", "post_max_size", "upload_max_filesize")
        }),
        (_(u"Error reporting"), {
            "fields": ("error_reporting", "display_errors", "display_startup_errors", "log_errors", "track_errors", "html_errors")
        }),
    )

class ServerConfigAdmin(admin.ModelAdmin):
    fieldsets = (
        (_(u"PHP config"), {
            "fields": ("default_php_config",)
        }),
    )

admin.site.register(Domain, DomainAdmin)
admin.site.register(NSEntry, NSEntryAdmin)
admin.site.register(IPAddress, IPAddressAdmin)
admin.site.register(Alias, AliasAdmin)
admin.site.register(Mailbox, MailboxAdmin)
admin.site.register(Forwarding, ForwardingAdmin)
admin.site.register(VirtualHost, VirtualHostAdmin)
admin.site.register(PHPExtension, PHPExtensionAdmin)
admin.site.register(PHPConfig, PHPConfigAdmin)
admin.site.register(ServerConfig, ServerConfigAdmin)
