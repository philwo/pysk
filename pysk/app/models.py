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
