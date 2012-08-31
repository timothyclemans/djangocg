from djangocg.conf.urls import patterns, include
from djangocg.contrib import admin
from djangocg.contrib.comments.admin import CommentsAdmin
from djangocg.contrib.comments.models import Comment

# Make a new AdminSite to avoid picking up the deliberately broken admin
# modules in other tests.
admin_site = admin.AdminSite()
admin_site.register(Comment, CommentsAdmin)

# To demonstrate proper functionality even when ``delete_selected`` is removed.
admin_site2 = admin.AdminSite()
admin_site2.disable_action('delete_selected')
admin_site2.register(Comment, CommentsAdmin)

urlpatterns = patterns('',
    (r'^admin/', include(admin_site.urls)),
    (r'^admin2/', include(admin_site2.urls)),
)
