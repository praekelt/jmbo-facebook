import datetime
from urllib2 import URLError

from django.db import models
from django.core.cache import cache

from jmbo.models import ModelBase


class FacebookPage(ModelBase):
    facebook_id = models.CharField(max_length=64, editable=False, unique=True)
    access_token = models.CharField(max_length=255, editable=False)
