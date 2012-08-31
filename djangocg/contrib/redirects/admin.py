
from djangocg.contrib import admin
from djangocg.contrib.redirects.models import Redirect

class RedirectAdmin(admin.ModelAdmin):
    list_display = ('old_path', 'new_path')
    list_filter = ('site',)
    search_fields = ('old_path', 'new_path')
    radio_fields = {'site': admin.VERTICAL}

admin.site.register(Redirect, RedirectAdmin)