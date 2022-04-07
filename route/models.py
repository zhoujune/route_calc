from email.policy import default
from django.db import models
from django.utils.translation import ugettext_lazy as _
import datetime


# Create your models here.

class Route(models.Model):
    code = models.CharField(_("route code"), max_length=50, default="")
    time_generated = models.DateField(_("time generated"), default=datetime.date.today)
    geo_codes = models.TextField(_("Geo code list"), default="")
    addrs = models.TextField(_("addr list"), default="")

    total_dist = models.DecimalField(_("total distance"),max_digits=10,decimal_places=2,default=0)
    image_url = models.CharField(_("image url"), max_length=200, default="")
    total_time = models.CharField(_("route time"), max_length=50, default="")

