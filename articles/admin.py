from django.contrib import admin
from . import models

admin.site.register(models.Article_type)
admin.site.register(models.Article)
admin.site.register(models.Article_zan_log)
admin.site.register(models.Article_pinglun)
admin.site.register(models.Favorites)
