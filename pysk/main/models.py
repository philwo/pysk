# -*- coding: utf-8 -*-

from __future__ import division
from decimal import Decimal, ROUND_HALF_UP

from datetime import *
import calendar
from dateutil.relativedelta import *
from dateutil.rrule import *

from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, unique=True)

    kundennr = models.IntegerField(blank=True, null=True)
    anrede = models.CharField(max_length=10,blank=True)
    titel = models.CharField(max_length=10,blank=True)
    firma = models.CharField(max_length=100,blank=True)
    strasse = models.CharField(max_length=40,blank=True)
    plz = models.CharField(max_length=10,blank=True)
    ort = models.CharField(max_length=20,blank=True)
    land = models.CharField(max_length=2,blank=True)
    telefon = models.CharField(max_length=20,blank=True)
    telefax = models.CharField(max_length=20,blank=True)

    desc = models.CharField(max_length=255, default="", blank=True)
    #unixuser = models.CharField(max_length=30, default="", blank=True)
    unixpw = models.CharField(max_length=255, default="", blank=True)
    statspw = models.CharField(max_length=255, default="", blank=True)

    def name(self):
        if self.firma != "":
            return self.firma
        else:
            return "%s, %s" % (self.user.last_name, self.user.first_name)
    name.admin_order_field = "user__last_name"

    def get_username(self):
        return self.user.username

    def is_active(self):
        return self.user.is_active

    def __unicode__(self):
        return u"%s: %s, %s-%s %s" % (self.user, self.name(), self.land, self.plz, self.ort)

    class Meta:
        ordering = ["user"]

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

