from django.contrib.sites.admin import SiteAdmin

SiteAdmin.list_display += ('subdomains',)