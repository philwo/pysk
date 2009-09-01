from django.db import models
from django.contrib.auth.models import User
from time import time
from math import floor

## Utility classes

class ForeignKeyFilter(object):
    def formfield_for_dbfield(self, db_field, **kwargs):
        # Only show the foreign key objects from the rendered filter.
        filters = getattr(self, 'foreignkey_filters', None)
        if filters and db_field.name in filters:
            kwargs['queryset'] = filters[db_field.name](get_current_user())
        return admin.ModelAdmin.formfield_for_dbfield(self, db_field, **kwargs)

## Model classes

class Domain(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    owner = models.ForeignKey(User)
    ns1 = models.CharField(max_length=255, default="ns.inwx.de.")
    ns2 = models.CharField(max_length=255, default="ns2.inwx.de.", blank=True)
    ns3 = models.CharField(max_length=255, default="ns3.inwx.de.", blank=True)
    ns4 = models.CharField(max_length=255, blank=True)
    ns5 = models.CharField(max_length=255, blank=True)
    ns6 = models.CharField(max_length=255, blank=True)
    mx1 = models.CharField(max_length=255, default="mail.igowo.de.", blank=True)
    mx2 = models.CharField(max_length=255, blank=True)
    mx3 = models.CharField(max_length=255, blank=True)
    is_gafyd = models.BooleanField(default=False)
    serial = models.IntegerField(default=0, blank=True, editable=False)
    active = models.BooleanField(default=True)
    zonehash = models.CharField(max_length=128, blank=True, editable=False)

    def __unicode__(self):
        return u"%s" % (self.name)

    #def fmtuser(self):
        #return u"%s (%s %s)"

    def save(self):
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
        super(Domain, self).save()

    class Meta:
        ordering = ["owner", "name"]

class NSEntry(models.Model):
    NSENTRY_TYPE_CHOICES = (
        ("A", "A"),
        ("AAAA", "AAAA"),
        ("CNAME", "CNAME"),
        ("MX", "MX"),
        ("TXT", "TXT"),
        ("SRV", "SRV"),
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

    def owner(self):
        return self.domain.owner

    def fqdn(self):
        return (u"%s.%s." % (self.host, self.domain)).strip(".")

    class Meta:
        ordering = ["domain__owner", "domain__name", "type", "host"]
        #ordering = ["domain__owner", "type"]
        unique_together = (("host", "domain", "type"),)
        verbose_name = "Custom DNS record"
        verbose_name_plural = "Custom DNS records"

class Server(models.Model):
    id = models.IntegerField(primary_key=True, help_text="Muss immer &gt; 100 sein!")
    hostname = models.CharField(max_length=64, unique=True)
    domain = models.ForeignKey(Domain)
    owner = models.ForeignKey(User)
    active = models.BooleanField(default=True)
    main_ip = models.ForeignKey("IPAddress", unique=True, related_name="server_main_ips", blank=True, null=True)

    def __unicode__(self):
        return self.fqdn()

    def fqdn(self):
        return (u"%s.%s." % (self.hostname, self.domain)).strip(".")
    fqdn.short_description = "FQDN"
    fqdn.admin_order_field = "domain"

    def save(self):
        super(Server, self).save()

    class Meta:
        ordering = ["id"]

IP_CONFIG_CHOICES = (
    ("apache", "Apache Webserver"),
    ("nginx", "nginx (Load-Balancer only ATM)"),
    ("custom", "Custom App"),
)

class IPAddress(models.Model):
    id = models.AutoField(primary_key=True)
    server = models.ForeignKey(Server, related_name="ipaddress_set")
    ip = models.IPAddressField()
    port = models.IntegerField()
    sslcert = models.CharField(max_length=250, blank=True)
    sslca = models.CharField(max_length=250, blank=True)
    sslkey = models.CharField(max_length=250, blank=True)
    configtype = models.CharField(max_length=250, default="apache", choices=IP_CONFIG_CHOICES)
    parent_ip = models.ForeignKey("IPAddress", blank=True, null=True)

    def __unicode__(self):
        return u"%s:%s (%s)" % (self.ip, self.port, self.server.fqdn())

    class Meta:
        unique_together = (("ip", "port", "parent_ip"),)
        ordering = ["ip", "port"]

class VirtualHost(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField("Hostname", max_length=255, blank=True)
    domain = models.ForeignKey(Domain)
    owner = models.ForeignKey(User)
    ipports = models.ManyToManyField(IPAddress, through="HostConfig")
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return u"%s.%s" % (self.name, self.domain)

    def fqdn(self):
        return (u"%s.%s." % (self.name, self.domain)).strip(".")
    fqdn.short_description = "FQDN"

    def dns_ip(self):
        qset = HostConfig.objects.filter(host=self, publish_dns=True)
        if len(qset) > 0:
            return qset[0].ipport
        else:
            return u""
    dns_ip.short_description = "DNS-published IP"

    def check_availability(self):
        import urllib2
        try:
            response = urllib2.urlopen('http://%s/'  % (self.fqdn(),))
            return u"OK"
        except urllib2.HTTPError, e:
            return u"HTTP Error %s" % (e.code,)
        except urllib2.URLError, e:
            return u"URL Error"
    check_availability.short_description = "HTTP Availability"

    class Meta:
        ordering = ["owner", "domain__name", "name"]
        unique_together = (("name", "domain"),)

class HostConfig(models.Model):
    id = models.AutoField(primary_key=True)
    host = models.ForeignKey(VirtualHost)
    ipport = models.ForeignKey(IPAddress)
    config = models.TextField(blank=True)
    publish_dns = models.BooleanField(default=True)
    active = models.BooleanField(default=True)

class Alias(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField("Hostname", max_length=64, blank=True)
    domain = models.ForeignKey(Domain)
    owner = models.ForeignKey(User)
    target = models.CharField(max_length=255)
    wildcard = models.BooleanField(default=True)
    www_alias = models.BooleanField(default=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return u"%s.%s -> %s" % (self.name, self.domain.name, self.target)

    def fqdn(self):
        return (u"%s.%s." % (self.name, self.domain)).strip(".")

    class Meta:
        ordering = ["owner", "domain__name", "name"]
        unique_together = (("name", "domain"),)
        verbose_name = "Domain alias"
        verbose_name_plural = "Domain aliases"

class DirectAlias(models.Model):
    id = models.AutoField(primary_key=True)
    host = models.ForeignKey(VirtualHost)
    ipport = models.ForeignKey(IPAddress)
    name = models.CharField("Hostname", max_length=64, blank=True)
    domain = models.ForeignKey(Domain)
    active = models.BooleanField(default=True)

    def fqdn(self):
        return (u"%s.%s." % (self.name, self.domain)).strip(".")

class Mailbox(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User)
    mail = models.CharField(max_length=75)
    domain = models.ForeignKey(Domain)
    password = models.CharField(max_length=64)
    quota = models.IntegerField()
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return u"%s: %s@%s (%s)" % (self.owner.username, self.mail, self.domain, self.quota)

    class Meta:
        ordering = ["owner", "domain", "mail"]
        unique_together = (("mail", "domain"),)
        verbose_name_plural = "Mailboxes"

class Forwarding(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User)
    source = models.CharField(max_length=75)
    domain = models.ForeignKey(Domain)
    target = models.CharField(max_length=200)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return u"%s@%s -> %s" % (self.source, self.domain, self.target)

    class Meta:
        ordering = ["owner", "domain", "source"]
        unique_together = (("source", "domain"),)

