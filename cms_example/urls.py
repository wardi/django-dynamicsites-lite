from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

# make filebrowser item appear in admin index:
admin.site.index_template = 'admin/index_filebrowser.html'
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/filebrowser/', include('filebrowser.urls')),
    url(r'^admin/', include(admin.site.urls)),

)

# THIS MUST BE LAST
# catch-all URL to use CMS pages
urlpatterns += patterns('',
    (r'^', include('pages.urls')),
)
