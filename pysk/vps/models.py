# -*- coding: utf-8 -*-

from django.db import models
from time import time
from math import floor

from django.contrib.auth.models import User
from app.models import Customer
from django.utils.translation import ugettext_lazy as _

## Model classes

class Domain(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    ns1 = models.CharField(max_length=255, default="ns.inwx.de.")
    ns2 = models.CharField(max_length=255, default="ns2.inwx.de.", blank=True)
    ns3 = models.CharField(max_length=255, default="ns3.inwx.de.", blank=True)
    ns4 = models.CharField(max_length=255, blank=True)
    ns5 = models.CharField(max_length=255, blank=True)
    ns6 = models.CharField(max_length=255, blank=True)
    mx1 = models.CharField(max_length=255, blank=True)
    mx2 = models.CharField(max_length=255, blank=True)
    mx3 = models.CharField(max_length=255, blank=True)
    jabber = models.CharField(max_length=255, blank=True)
    is_gafyd = models.BooleanField(default=False)
    serial = models.IntegerField(default=0, blank=True, editable=False)
    active = models.BooleanField(default=True)
    zonehash = models.CharField(max_length=128, blank=True, editable=False)

    def __unicode__(self):
        return u"%s" % (self.name)

    def save(self, force_insert=False, force_update=False):
        from datetime import date
        t = date.today().strftime("%Y%m%d")

        # Do we already have a serial?
        if self.serial == 0:
            # No
            c = 1
        else:
            # Yes, but is it from today?
            d = str(self.serial)[:8]
            if (t != d):
                # No
                c = 1
            else:
                # Yes
                c = int(str(self.serial)[8:]) + 1

        self.serial = "%s%02i" % (t, c)
        super(Domain, self).save(force_insert, force_update)

    class Meta:
        ordering = ["name"]
        verbose_name = _(u"Domain")
        verbose_name_plural = _(u"Domains")

class NSEntry(models.Model):
    NSENTRY_TYPE_CHOICES = (
        ("A", "A"),
        ("AAAA", "AAAA"),
        ("CNAME", "CNAME"),
        ("MX", "MX"),
        ("TXT", "TXT"),
        ("SRV", "SRV"),
        ("NS", "NS"),
    )
    id = models.AutoField(primary_key=True)
    host = models.CharField(max_length=64)
    domain = models.ForeignKey(Domain)
    type = models.CharField(max_length=16, choices=NSENTRY_TYPE_CHOICES, default="A")
    value = models.CharField(max_length=64)
    port = models.IntegerField(null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)
    priority = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return u"%s.%s %s %s" % (self.host, self.domain, self.type, self.value)

    def fqdn(self):
        return (u"%s.%s." % (self.host, self.domain)).strip(".")

    class Meta:
        ordering = ["domain__name", "type", "host"]
        unique_together = (("host", "domain", "type"),)
        verbose_name = _(u"Custom DNS record")
        verbose_name_plural = _(u"Custom DNS records")

class IPAddress(models.Model):
    id = models.AutoField(primary_key=True)
    ip = models.IPAddressField(unique=True)

    def __unicode__(self):
        return u"%s" % (self.ip,)

    class Meta:
        ordering = ["ip"]
        verbose_name = _(u"IP address")
        verbose_name_plural = _(u"IP addresses")

CHOICES_FORCE_WWW = (
        ("strip", _(u"strip www subdomain")),
        ("prepend", _(u"force www subdomain")),
        ("ignore", _(u"both is okay")),
    )

class VirtualHost(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(Customer)
    name = models.CharField(max_length=255, blank=True, verbose_name=_(u"Hostname"), help_text=_(u"Sometimes also called 'subdomain' ..."))
    domain = models.ForeignKey(Domain)
    ipport = models.ForeignKey(IPAddress, verbose_name=_(u"IP"))
    active = models.BooleanField(default=True)
    force_www = models.CharField(max_length=16, choices=CHOICES_FORCE_WWW, default="ignore", verbose_name=_(u"Force WWW"))
    ssl_enabled = models.BooleanField(default=False, verbose_name=_(u"SSL enabled"))
    ssl_force = models.BooleanField(default=False, verbose_name=_(u"Force SSL"))
    ssl_cert = models.CharField(max_length=250, blank=True, verbose_name=_(u"SSL certificate"))
    ssl_key = models.CharField(max_length=250, blank=True, verbose_name=_(u"SSL Private Key"))
    enable_php = models.BooleanField(default=True, verbose_name=_(u"Enable PHP"))
    apache_config = models.TextField(blank=True, verbose_name=_(u"Apache config"))
    apache_enabled = models.BooleanField(default=True, verbose_name=_(u"Apache enabled"))
    nginx_config = models.TextField(blank=True, verbose_name=_(u"nginx config"))
    sortkey = models.CharField(max_length=255, blank=True, editable=False)

    def __unicode__(self):
        return u"%s.%s" % (self.name, self.domain)

    def save(self, force_insert=False, force_update=False):
        self.sortkey = "%s-%s" % (self.domain.name.replace(".", "-"), self.name.replace(".", "-"))
        super(VirtualHost, self).save(force_insert, force_update)

    def fqdn(self):
        return (u"%s.%s." % (self.name, self.domain)).strip(".")
    fqdn.short_description = "FQDN"

    class Meta:
        ordering = ["sortkey", "domain__name", "name"]
        unique_together = (("name", "domain"),)
        verbose_name = _(u"Webspace")
        verbose_name_plural = _(u"Webspaces")

class Alias(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, blank=True, verbose_name=_(u"Hostname"))
    domain = models.ForeignKey(Domain)
    target = models.CharField(max_length=255)
    www_alias = models.BooleanField(default=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return u"%s.%s -> %s" % (self.name, self.domain.name, self.target)

    def fqdn(self):
        return (u"%s.%s." % (self.name, self.domain)).strip(".")

    class Meta:
        ordering = ["domain__name", "name"]
        unique_together = (("name", "domain"),)
        verbose_name = _(u"HTTP forwarding")
        verbose_name_plural = _(u"HTTP forwardings")

class DirectAlias(models.Model):
    id = models.AutoField(primary_key=True)
    host = models.ForeignKey(VirtualHost)
    name = models.CharField(max_length=255, blank=True, verbose_name=_(u"Hostname"), help_text=_(u"Sometimes also called 'subdomain' ..."))
    domain = models.ForeignKey(Domain)
    active = models.BooleanField(default=True)

    def fqdn(self):
        return (u"%s.%s." % (self.name, self.domain)).strip(".")

    class Meta:
        verbose_name = _(u"Direct alias")
        verbose_name_plural = _(u"Direct aliases")

class Mailbox(models.Model):
    id = models.AutoField(primary_key=True)
    mail = models.CharField(max_length=75, verbose_name=_(u"Username"), help_text=_(u"This is the username, the part before the @ sign!"))
    domain = models.ForeignKey(Domain, help_text=_(u"Which domain should become part of the e-mail address? (This is the part after the @ sign!)"))
    password = models.CharField(max_length=64)
    quota = models.IntegerField(verbose_name=_(u"Quota"), help_text=_(u"Specify the quota of this mail account in megabytes"))
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return u"%s@%s (%s)" % (self.mail, self.domain, self.quota)

    class Meta:
        ordering = ["domain", "mail"]
        unique_together = (("mail", "domain"),)
        verbose_name = _(u"Mailbox")
        verbose_name_plural = _(u"Mailboxes")

class Forwarding(models.Model):
    id = models.AutoField(primary_key=True)
    source = models.CharField(max_length=75, verbose_name=_(u"Username"), help_text=_(u"This is the username, the part before the @ sign!"))
    domain = models.ForeignKey(Domain, help_text=_(u"Which domain should become part of the e-mail address? (This is the part after the @ sign!)"))
    target = models.CharField(max_length=200, verbose_name=_(u"Destination address"), help_text=_(u"To which destination address shall the mail be forwarded?"))
    active = models.BooleanField(default=True)

    def email(self):
        return u"%s@%s" % (self.source, self.domain)
    email.short_description = _(u"E-Mail Address")

    def __unicode__(self):
        return u"%s -> %s" % (self.email(), self.target)

    class Meta:
        ordering = ["domain", "source"]
        unique_together = (("source", "domain"),)
        verbose_name = _(u"E-Mail forwarding")
        verbose_name_plural = _(u"E-Mail forwardings")
