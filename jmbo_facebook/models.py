import datetime
import urllib2

from django.db import models
from django.core.cache import cache
from django.utils import simplejson

from jmbo.models import ModelBase


class Update(ModelBase):
    """Purely a wrapper that allows us to use jmbo-foundry's listings for 
    updates."""
    def __init__(self, update):
        # Copy attributes over
        attrs = ('message', 'created_time', 'updated_time')
        for attr in attrs:            
            setattr(self, attr, update.get(attr))

    @property
    def as_leaf_class(self):
        return self

    def save(self):
        raise NotImplemented


class Page(ModelBase):
    facebook_id = models.CharField(max_length=64, editable=False, unique=True)
    access_token = models.CharField(max_length=255, editable=False)

    def fetch(self, force=False):
        cache_key = 'jmbo_facebook_page_%s' % self.slug
        cached = cache.get(cache_key, None)
        if cached is not None:
            return cached

        updates = []
        url ='https://graph.facebook.com/%s/feed?access_token=%s' \
            % (self.facebook_id, self.access_token)
        try:
            response = urllib2.urlopen(url)
        except Exception, e:
            # Blindly catch exceptions
            pass
        else:
            json = simplejson.loads(response.read())
            for di in json['data']:
                if di['type'] != 'status': continue
                if not di.get('message'): continue
                di['created_time'] = datetime.datetime.strptime(
                    di['created_time'], '%Y-%m-%dT%H:%M:%S+0000'
                )
                di['updated_time'] = datetime.datetime.strptime(
                    di['updated_time'], '%Y-%m-%dT%H:%M:%S+0000'
                )
                updates.append(di)
             
        cache.set(cache_key, updates, 1200)
        return updates

    @property
    def updates(self):
        class MyList(list):
            """Slightly emulate QuerySet API so jmbo-foundry listings work"""

            @property
            def exists(self):
                return len(self) > 0

        result = []
        for update in self.fetch():
            result.append(Update(update))

        return MyList(result)
