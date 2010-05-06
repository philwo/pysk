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
    host = models.CharField(max_length=64, blank=True)
    domain = models.ForeignKey(Domain)
    type = models.CharField(max_length=16, choices=NSENTRY_TYPE_CHOICES, default="A")
    value = models.CharField(max_length=512)
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
    php_config = models.ForeignKey("PHPConfig", null=True, blank=True)
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
    password = models.CharField(max_length=256)
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
    source = models.CharField(max_length=75, verbose_name=_(u"Username"), help_text=_(u"This is the username, the part before the @ sign! Leave blank for catch-all."), blank=True)
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

class PHPConfig(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=75, unique=True, verbose_name=_(u"Config name"))
    short_open_tag = models.BooleanField(verbose_name=_(u"Short open tag"), help_text=_(u"""
    <strong>This directive determines whether or not PHP will recognize code between
    <? and ?> tags as PHP source which should be processed as such.</strong><br /><br />
    It's been recommended for several years that you not use the short tag "short cut" and
    instead to use the full <?php and ?> tag combination. With the wide spread use
    of XML and use of these tags by other languages, the server can become easily
    confused and end up parsing the wrong code in the wrong context. But because
    this short cut has been a feature for such a long time, it's currently still
    supported for backwards compatibility, but we recommend you don't use them.<br /><br />
    
    see <a href="http://php.net/short-open-tag">http://php.net/short-open-tag</a>
    """))
    max_execution_time = models.IntegerField(verbose_name=_(u"Max. execution time"), help_text=_(u"""
    <strong>Maximum execution time of each script, in seconds</strong><br /><br />
    
    see <a href="http://php.net/max-execution-time">http://php.net/max-execution-time</a>
    """))
    max_input_time = models.IntegerField(verbose_name=_(u"Max. input time"), help_text=_(u"""
    <strong>Maximum amount of time each script may spend parsing request data.</strong><br /><br />
    
    It's a good idea to limit this time on productions servers in order to eliminate unexpectedly
    long running scripts.<br /><br />
    
    see <a href="http://php.net/max-input-time">http://php.net/max-input-time</a>
    """))
    memory_limit = models.CharField(max_length=20, verbose_name=_(u"Memory limit"), help_text=_(u"""
    <strong>Maximum amount of memory a script may consume (128MB)</strong><br /><br />
    
    see <a href="http://php.net/memory-limit">http://php.net/memory-limit</a>
    """))
    post_max_size = models.CharField(max_length=20, verbose_name=_(u"POST request max. size"), help_text=_(u"""
    <strong>Maximum size of POST data that PHP will accept.</strong><br /><br />
    
    see <a href="http://php.net/post-max-size">http://php.net/post-max-size</a>
    """))
    upload_max_filesize = models.CharField(max_length=20, verbose_name=_(u"File-upload max. filesize"), help_text=_(u"""
    <strong>Maximum allowed size for uploaded files.</strong><br /><br />
    
    see <a href="http://php.net/upload-max-filesize">http://php.net/upload-max-filesize</a>
    """))
    allow_call_time_pass_reference = models.BooleanField(verbose_name=_(u"Allow call time pass reference"), help_text=_(u"""
    <strong>This directive allows you to enable and disable warnings which PHP will issue
    if you pass a value by reference at function call time.</strong><br /><br />
    
    Passing values by
    reference at function call time is a deprecated feature which will be removed
    from PHP at some point in the near future. The acceptable method for passing a
    value by reference to a function is by declaring the reference in the functions
    definition, not at call time. This directive does not disable this feature, it
    only determines whether PHP will warn you about it or not. These warnings
    should enabled in development environments only.
    
    see <a href="http://php.net/allow-call-time-pass-reference">http://php.net/allow-call-time-pass-reference</a>
    """))
    error_reporting = models.CharField(max_length=100, verbose_name=_(u"Error reporting"), help_text=_(u"""
    <strong>This directive informs PHP of which errors, warnings and notices you would like
    it to take action for.</strong><br /><br />
    
    The recommended way of setting values for this
    directive is through the use of the error level constants and bitwise
    operators. The error level constants are below here for convenience as well as
    some common settings and their meanings.<br /><br />
    
    <strong>Error Level Constants:</strong><br /><br />
    E_ALL: All errors and warnings (includes E_STRICT as of PHP 6.0.0)<br /><br />
    E_ERROR: fatal run-time errors<br /><br />
    E_RECOVERABLE_ERROR: almost fatal run-time errors<br /><br />
    E_WARNING: run-time warnings (non-fatal errors)<br /><br />
    E_PARSE: compile-time parse errors<br /><br />
    E_NOTICE: run-time notices (these are warnings which often result from a bug in your code, but it's possible that it was
    intentional (e.g., using an uninitialized variable and relying on the fact it's automatically initialized to an empty string)<br /><br />
    E_STRICT: run-time notices, enable to have PHP suggest changes to your code which will ensure the best interoperability and forward compatibility of your code<br /><br />
    E_CORE_ERROR: fatal errors that occur during PHP's initial startup<br /><br />
    E_CORE_WARNING: warnings (non-fatal errors) that occur during PHP's initial startup<br /><br />
    E_COMPILE_ERROR: fatal compile-time errors<br /><br />
    E_COMPILE_WARNING: compile-time warnings (non-fatal errors)<br /><br />
    E_USER_ERROR: user-generated error message<br /><br />
    E_USER_WARNING: user-generated warning message<br /><br />
    E_USER_NOTICE: user-generated notice message<br /><br />
    E_DEPRECATED: warn about code that will not work in future versions of PHP<br /><br />
    E_USER_DEPRECATED: user-generated deprecation warnings<br /><br />
    
    <strong>Common Values:</strong><br /><br />
    E_ALL & ~E_NOTICE  (Show all errors, except for notices and coding standards warnings.)<br /><br />
    E_ALL & ~E_NOTICE | E_STRICT  (Show all errors, except for notices)<br /><br />
    E_COMPILE_ERROR|E_RECOVERABLE_ERROR|E_ERROR|E_CORE_ERROR  (Show only errors)<br /><br />
    E_ALL | E_STRICT  (Show all errors, warnings and notices including coding standards.)<br /><br />
    """))
    display_errors = models.BooleanField(verbose_name=_(u"Display errors"), help_text=_(u"""
    <strong>This directive controls whether or not and where PHP will output errors,
    notices and warnings too.</strong><br /><br />
    
    Error output is very useful during development, but
    it could be very dangerous in production environments. Depending on the code
    which is triggering the error, sensitive information could potentially leak
    out of your application such as database usernames and passwords or worse.
    It's recommended that errors be logged on production servers rather than
    having the errors sent to STDOUT.<br /><br />

    see <a href="http://php.net/display-errors">http://php.net/display-errors</a>
    """))
    display_startup_errors = models.BooleanField(verbose_name=_(u"Display start-up errors"), help_text=_(u"""
    <strong>The display of errors which occur during PHP's startup sequence are handled
    separately from display_errors.</strong><br /><br />
    
    PHP's default behavior is to suppress those
    errors from clients. Turning the display of startup errors on can be useful in
    debugging configuration problems. But, it's strongly recommended that you
    leave this setting off on production servers.<br /><br />
    
    see <a href="http://php.net/display-startup-errors">http://php.net/display-startup-errors</a>
    """))
    log_errors = models.BooleanField(verbose_name=_(u"Log errors to file"), help_text=_(u"""
    <strong>Besides displaying errors, PHP can also log errors to locations such as a
    server-specific log, STDERR, or a location specified by the error_log
    directive found below.</strong><br /><br />
    
    While errors should not be displayed on productions
    servers they should still be monitored and logging is a great way to do that.<br /><br />

    see <a href="http://php.net/log-errors">http://php.net/log-errors</a>
    """))
    track_errors = models.BooleanField(verbose_name=_(u"Track errors in variable"), help_text=_(u"""
    <strong>Store the last error/warning message in $php_errormsg (boolean).</strong><br /><br />
    
    Setting this value
    to On can assist in debugging and is appropriate for development servers. It should
    however be disabled on production servers.<br /><br />

    see <a href="http://php.net/track-errors">http://php.net/track-errors</a>
    """))
    html_errors = models.BooleanField(verbose_name=_(u"Link to documentation on error"), help_text=_(u"""
    <strong>When PHP displays or logs an error, it has the capability of inserting html
    links to documentation related to that error.</strong><br /><br />
    
    This directive controls whether
    those HTML links appear in error messages or not. For performance and security
    reasons, it's recommended you disable this on production servers.<br /><br />

    see <a href="http://php.net/html-errors">http://php.net/html-errors</a>
    """))
    session_bug_compat_42 = models.BooleanField(verbose_name=_(u"Stay compatible with session bug (~ PHP 4.2)"), help_text=_(u"""
    <strong>PHP 4.2 and less have an undocumented feature/bug that allows you to
    to initialize a session variable in the global scope, even when register_globals
    is disabled.</strong><br /><br />
    
    PHP 4.3 and later will warn you, if this feature is used.
    You can disable the feature and the warning separately. At this time,
    the warning is only displayed, if bug_compat_42 is enabled. This feature
    introduces some serious security problems if not handled correctly. It's
    recommended that you do not use this feature on production servers. But you
    should enable this on development servers and enable the warning as well. If you
    do not enable the feature on development servers, you won't be warned when it's
    used and debugging errors caused by this can be difficult to track down.<br /><br />

    see <a href="http://php.net/session.bug-compat-42">http://php.net/session.bug-compat-42</a>
    """))
    session_bug_compat_warn = models.BooleanField(verbose_name=_(u"Warn on use of session bug (~ PHP 4.2)"), help_text=_(u"""
    <strong>This setting controls whether or not you are warned by PHP when initializing a
    session value into the global space.</strong><br /><br />

    session.bug_compat_42 must be enabled before
    these warnings can be issued by PHP. See the directive above for more information.<br /><br />

    see <a href="http://php.net/session.bug-compat-warn">http://php.net/session.bug-compat-warn</a>
    """))
    
    def __unicode__(self):
        return u"%s" % (self.name,)

    class Meta:
        ordering = ["name"]
        verbose_name = _(u"PHP config")
        verbose_name_plural = _(u"PHP configs")

class PHPExtension(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=75, unique=True, verbose_name=_(u"Extension module"))
    enabled = models.BooleanField(default=False)
    
    def __unicode__(self):
        return u"%s" % (self.name,)

    class Meta:
        ordering = ["name"]
        verbose_name = _(u"PHP extension")
        verbose_name_plural = _(u"PHP extensions")

class ServerConfig(models.Model):
    id = models.AutoField(primary_key=True)
    active = models.BooleanField(unique=True, default=True)
    default_php_config = models.ForeignKey(PHPConfig)
