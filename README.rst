dynamicsites
============

By UYSRC <http://www.uysrc.com/>

Host multiple sites from a single django project 

Expands the standard django.contrib.sites package to allow for:

 * Sites identified dynamically from the request via middleware
 * No need for multiple virtual hosts at the webserver level
 * 301 Redirects to canonical hostnames
 * Allows for a site to support multiple subdomains
 * Allows for a site to be an independent subdomain of another site
 * A site may have its own urls.py and templates
 * A single site may accept requests from multiple hostnames
 * Allows for environment hostname mappings to use non-production hostnames (for use in dev, staging, test, etc. environments)

Configuration
-------------

 1. Before you install dynamicsites, make sure you have configured at least 1 site in the admin panel, because once dynamicsites is installed, it will try to lookup a site from request.get_host(), and, if none exists, will always throw 404

 2. Add the app to INSTALLED_APPS ::

        INSTALLED_APPS = (
            ...
            'dynamicsites',
        )

 3. Add the middleware to MIDDLEWARE_CLASSES ::
    
        MIDDLEWARE_CLASSES = (
            ...
            'dynamicsites.middleware.DynamicSitesMiddleware'
        )

 4. Add the context processor to TEMPLATE_CONTEXT_PROCESSORS ::

        TEMPLATE_CONTEXT_PROCESSORS = (
            ...
            'dynamicsites.context_processors.current_site',
        )

 5. Configure dynamicsites by adding SITES_DIR, DEFAULT_HOST, and HOSTNAME_REDIRECTS to settings.py ::

        SITES_DIR = os.path.join(os.path.dirname(__file__), 'sites')
        DEFAULT_HOST = 'www.your-default-site.com'
        HOSTNAME_REDIRECTS = {
        #    'redirect-src-1.com':         'www.redirect-dest-1.com',
            ...
        }

 6. If your local environment (eg. test, dev, staging) uses different hostnames than production, set the ENV_HOSTNAMES map as well ::

        ENV_HOSTNAMES = {
            'my-site.dev':    'www.your-default-site.com',
            ...
        }

 7. make ``sites`` dir (from the SITES_DIR setting above) and put a ``__init__.py`` file inside

 8. make a site dir for each site you're hosting (eg. ``mkdir sites/{{mysyte}}``) <-- you'll put ``{{mysyte}}`` in the admin screen when you go to configure mysyte there.  Make sure to put an ``__init__.py`` file in each site dir as well.

 9. run ``syncdb``.  If your django_site table fails to modify, you will need to modify the table via sql::

        alter table django_site add column folder_name varchar(255);
        alter table django_site add column subdomains varchar(255);
        
 10. go to the admin panel for sites.  You should see two fields added now, one for the site folder name (#8 above) and another for which subdomains you wish to support

Configuration
-------------

Using dynamicsites you can host multiple sites within a single domain.  This may be the most common setup.  This will allow different url mappings by subdomain.  To do this you'll need to create a site object for the different subdomain sites.

Within the list of subdomains for a site, the first subdomain listed will be the default subdomain.  If you want the default subdomain to be blank, put '' (single quote empty string) as the first subdomain in the subdomain list in the admin panel for sites.

Debugging
---------

In the current codebase, if you have the django debug toolba unstalled and enable redirect tracking, ie. 

::

    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': True,
    }

django-dynamicsites will intercept redirects, which is very helpful when dialing in your site config.

There's also a view included with the codebase which is useful for checking which site dynamicsites thinks you're seeing.  Just add an entry to your urls.py file::

    from dynamicsites.views import site_info

    urlpatterns += patterns('',
        url(r'^site-info$', site_info),)

Notes
-----

* you need to run syncdb after dynamicsites is installed (to be sure the fields folder_name and subdomains is added to the standard Site model)
* in sites folder, each folder must have a __init__.py file.

More Info
---------

More info can be found here:  http://blog.uysrc.com/2011/03/23/serving-multiple-sites-with-django/
