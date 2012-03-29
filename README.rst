dynamicsiteslite
================

Original dynamicsites By UYSRC <http://www.uysrc.com/>

Host multiple sites from a single django project 

Expands the standard django.contrib.sites package to allow for:

 * Sites identified dynamically from the request via middleware
 * No need for multiple virtual hosts at the webserver level
 * 301 Redirects to canonical hostnames
 * A site may have its own urls.py and templates
 * Allows for environment hostname mappings to use non-production hostnames (for use in dev, staging, test, etc. environments)

Configuration
-------------

 1. Before you install dynamicsites, make sure you have configured at least 1 site in the admin panel, because once dynamicsites is installed, it will try to lookup a site from request.get_host(), and, if none exists, will always throw 404

 2. Add the app to INSTALLED_APPS ::

        INSTALLED_APPS = (
            ...
            'dynamicsiteslite',
        )

 3. Add the middleware to MIDDLEWARE_CLASSES ::
    
        MIDDLEWARE_CLASSES = (
            ...
            'dynamicsiteslite.middleware.DynamicSitesMiddleware'
        )

 4. Add the context processor to TEMPLATE_CONTEXT_PROCESSORS ::

        TEMPLATE_CONTEXT_PROCESSORS = (
            ...
            'dynamicsiteslite.context_processors.current_site',
        )

 5. Configure dynamicsites by adding SITES_DIR, SITES_PACKAGE, DEFAULT_HOST, and HOSTNAME_REDIRECTS to settings.py ::

        SITES_DIR = os.path.join(os.path.dirname(__file__), 'sites')
        SITES_PACKAGE = 'sites'
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

 8. make a site dir for each site you're hosting (eg. ``mkdir sites/www_mysitesdomain_com``) <-- put underscores instead of dots in the domain name, these need to be imported as python packages.  Make sure to put an ``__init__.py`` file in each site dir as well.

 9. add a SITES_FILTER setting if you want to restrict the sites served by this project.  SITES_FILTER is a dict used as follows when dynamicsiteslite looks up sites in the database::

        Site.objects.filter(**SITES_FILTER)

Debugging
---------

In the current codebase, if you have the django debug toolba unstalled and enable redirect tracking, ie. 

::

    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': True,
    }

django-dynamicsites will intercept redirects, which is very helpful when dialing in your site config.

There's also a view included with the codebase which is useful for checking which site dynamicsites thinks you're seeing.  Just add an entry to your urls.py file::

    from dynamicsiteslite.views import site_info

    urlpatterns += patterns('',
        url(r'^site-info$', site_info),)

Notes
-----

* in sites folder, each folder must have a __init__.py file.

More Info
---------

More info can be found here:  http://blog.uysrc.com/2011/03/23/serving-multiple-sites-with-django/
