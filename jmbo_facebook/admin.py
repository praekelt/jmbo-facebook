from django.contrib import admin

from jmbo.admin import ModelBaseAdmin

from jmbo_facebook import models


class PageAdmin(ModelBaseAdmin):
    list_display = ModelBaseAdmin.list_display + ('facebook_id', 'access_token')


admin.site.register(models.Page, PageAdmin)
