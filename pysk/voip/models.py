# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class SipAccount(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32, unique=True)
    user = models.ForeignKey(User, blank=True, null=True)

    def __unicode__(self):
        return u"%s" % (self.name,)

    class Meta:
        verbose_name = "SIP Account"
        verbose_name_plural = "SIP Accounts"
        ordering = ["name"]

class Destination(models.Model):
    id = models.IntegerField(primary_key=True)
    name_de = models.CharField(max_length=64)
    name_en = models.CharField(max_length=64)

    def __unicode__(self):
        return u"%s" % (self.name_de,)

    class Meta:
        verbose_name = "Destination"
        verbose_name_plural = "Destinations"
        ordering = ["id"]

class CDR(models.Model):
    id = models.AutoField(primary_key=True)
    fid = models.CharField(max_length=64, unique=True)
    sip_account = models.ForeignKey(SipAccount)
    quellrufnr = models.CharField(max_length=32)
    zielrufnr = models.CharField(max_length=32)
    beginn = models.DateTimeField()
    dauer = models.IntegerField()
    dest = models.ForeignKey(Destination)
    vk = models.DecimalField(max_digits=10, decimal_places=4)
    ek = models.DecimalField(max_digits=10, decimal_places=4)

    def __unicode__(self):
        return u"%s: %s (%s -> %s), %s Sekunden, VK: %s, EK: %s" % (self.beginn, self.sip_account, self.quellrufnr, self.zielrufnr, self.dauer, self.vk, self.ek)

    class Meta:
        verbose_name = "CDR"
        verbose_name_plural = "CDRs"
        ordering = ["beginn"]
