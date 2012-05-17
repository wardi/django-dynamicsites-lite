from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
)

# THIS MUST BE LAST
# catch-all URL to use CMS pages
urlpatterns += patterns('',
    (r'^', include('pages.urls')),
)
