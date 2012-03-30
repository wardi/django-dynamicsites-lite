from django.conf import settings
from django.core.cache import cache
from django.contrib.sites.models import Site
from django.http import HttpResponsePermanentRedirect, Http404
from django.shortcuts import render_to_response
from django.utils.cache import patch_vary_headers
from django.utils.http import urlquote
from utils import make_tls_property

import logging
import os

SITE_ID = settings.__dict__['_wrapped'].__class__.SITE_ID = make_tls_property()
TEMPLATE_DIRS = settings.__dict__['_wrapped'].__class__.TEMPLATE_DIRS = make_tls_property(settings.TEMPLATE_DIRS)

class DynamicSitesError(Exception):
    pass

class DynamicSitesMiddleware(object):
    """
    Sets settings.SITE_ID based on request's domain.
    Also handles hostname redirects, and ensures the 
    proper subdomain is requested for the site
    """
    def process_request(self, request):
        self.logger = logging.getLogger(__name__)
        self.HOSTNAME_REDIRECTS = getattr(settings, "HOSTNAME_REDIRECTS", None)
        self.ENV_HOSTNAMES = getattr(settings, "ENV_HOSTNAMES", None)
        self.request = request
        self.site = None
        self.domain, self.port = self.get_domain_and_port()
        self.domain_requested = self.domain
        self.domain_unsplit = self.domain
        self.subdomain = None
        self.env_domain_requested = None
        self._old_TEMPLATE_DIRS = getattr(settings, "TEMPLATE_DIRS", None)

        # main loop - lookup the site by domain/subdomain, plucking 
        # subdomains off the request hostname until a site or
        # redirect is found
        res = self.lookup()
        while res is False:
            try:
                self.domain_unsplit = self.domain
                self.subdomain, self.domain = self.domain.split('.', 1)
            except ValueError:
                try:
                    self.logger.debug(
                        'no match found redirecting to default_host=%s',
                        settings.DEFAULT_HOST)
                    return self.redirect(settings.DEFAULT_HOST)
                except AttributeError:
                    raise Http404
            res = self.lookup()

        # At this point res can be either None, meaning we have a site,
        # or an HttpResponsePermanentRedirect obj

        if self.site:
            # we have a site
            self.logger.debug('Using site id=%s domain=%s',
                self.site.id,
                self.site.domain)

            # make sure the domain requested is the subdomain/domain 
            # (ie. domain_unsplit) we used to locate the site
            if self.domain_requested is not self.domain_unsplit:
                # if not redirect to the subdomain/domain 
                # (ie. domain_unsplit) we used to locate the site
                self.logger.debug('%s does not match %s.  Redirecting to %s',
                    self.domain_requested,
                    self.domain_unsplit,
                    self.domain_unsplit)                    
                return self.redirect(self.domain_unsplit)
            # keep copies of these for other apps/middleware to use
            self.request.domain_unsplit = self.domain_unsplit
            self.request.domain = self.domain
            self.request.subdomain = (self.subdomain) and self.subdomain or ''
            self.request.port = self.port

            folder_name = site_folder_name(self.site)
            if folder_name:
                # set from where urlconf will be loaded if it exists
                try:
                    urlconf_pkg = '%s.%s.urls' % (
                        settings.SITES_PACKAGE, folder_name)
                    __import__(urlconf_pkg)
                    self.logger.debug('using %s for urlconf', urlconf_pkg)
                    self.request.urlconf = urlconf_pkg
                except ImportError:
                    # urlconf doesn't exist... skip it
                    self.logger.debug(
                        'cannot find %s.%s.urls for urlconf... skipping',
                        settings.SITES_PACKAGE, folder_name)
                    pass
                # add site templates dir to TEMPLATE_DIRS
                self.logger.debug(
                    'adding %s to TEMPLATE_DIRS', 
                    os.path.join(settings.SITES_DIR, folder_name, 'templates'))
                TEMPLATE_DIRS.value = (os.path.join(settings.SITES_DIR,
                    folder_name, 'templates'),) + TEMPLATE_DIRS.value

        return res


    def process_response(self, request, response):
        """
        Notify the caching system to cache output based on HTTP_HOST as well as request
        """
        if getattr(request, "urlconf", None):
            patch_vary_headers(response, ('Host',))
        # reset TEMPLATE_DIRS because we unconditionally add to it when
        # processing the request
        try:
            if self._old_TEMPLATE_DIRS is not None:
                settings.TEMPLATE_DIRS = self._old_TEMPLATE_DIRS
        except AttributeError:
            pass
        return response


    def get_domain_and_port(self):
        """
        Django's request.get_host() returns the requested host and possibly the
        port number.  Return a tuple of domain, port number.  
        Domain will be lowercased
        """
        host = self.request.get_host()
        if ':' in host:
            domain, port = host.split(':')
            return (domain.lower(), port)
        else:
            return (host.lower(), 
                self.request.META.get('SERVER_PORT'))


    def lookup(self):
        """
        The meat of this middleware.
        
        Returns None and sets settings.SITE_ID if able to find a Site
        object by domain and its subdomain is valid.
        
        Returns an HttpResponsePermanentRedirect to the Site's default
        subdomain if a site is found but the requested subdomain 
        is not supported, or if domain_unsplit is defined in 
        settings.HOSTNAME_REDIRECTS

        Otherwise, returns False.
        """

        self.logger.debug('ENV_HOSTNAMES lookup subdomain=%s domain=%s domain_unsplit=%s',
            self.subdomain, self.domain, self.domain_unsplit)
        # check to see if this hostname is actually a env hostname
        if self.ENV_HOSTNAMES and self.domain in self.ENV_HOSTNAMES:
            self.logger.debug('Got a ENV_HOSTNAME %s:%s',
                self.domain, self.ENV_HOSTNAMES[self.domain])
            # reset subdomain, domain, and domain_unsplit
            self.domain = self.ENV_HOSTNAMES[self.domain]
            if self.subdomain:
                self.domain_unsplit = '%s.%s' % (self.subdomain, self.domain)
            else:
                self.domain_unsplit = self.domain

            self.env_domain_requested = self.domain_requested
            self.domain_requested = self.domain_unsplit

        # check to see if this hostname redirects
        if self.HOSTNAME_REDIRECTS and self.domain_unsplit in self.HOSTNAME_REDIRECTS:
            self.logger.debug('Found HOSTNAME_REDIRECT %s=>%s',
               self.domain_unsplit, self.HOSTNAME_REDIRECTS[self.domain_unsplit])
            return self.redirect(self.HOSTNAME_REDIRECTS[self.domain_unsplit])

        # check cache
        cache_key = 'site_id:%s' % self.domain_unsplit
        site_id = cache.get(cache_key)
        if site_id:
            self.logger.debug('Found site_id=%s from cache.get(\'%s\')',
                site_id,
                cache_key)
            try:
                self.site = all_sites().get(id=site_id)
                SITE_ID.value = site_id
            except Site.DoesNotExist:
                # This might happen if the Site object was deleted from the
                # database after it was cached.  Remove from cache and act
                # as if the cache lookup failed.
                cache.delete(cache_key)
            else:
                return None

        # check database
        try:
            self.logger.debug(
                'Checking database for domain=%s', 
                self.domain)
            self.site = all_sites().get(domain=self.domain)
        except Site.DoesNotExist:
            return False
        if not self.site:
            return False

        SITE_ID.value = self.site.pk
        cache.set(cache_key, SITE_ID.value, 5*60)
        return None

    def _redirect(self, new_host, subdomain=None):
        """experimental: 
        wrapper around _redirect_real to throw up
        any django debug toolbar redirect notices.
        Note todo: this is not properly respecting
        the django debug toolbar's IP address restriction"""
        response = self._redirect_real(new_host, subdomain)
        dtc = getattr(settings, "DEBUG_TOOLBAR_CONFIG", None)
        try:
            if dtc.get('INTERCEPT_REDIRECTS', False):
                if isinstance(response, HttpResponsePermanentRedirect):
                    redirect_to = response.get('Location', None)
                    if redirect_to:
                        cookies = response.cookies
                        response = render_to_response(
                            'debug_toolbar/redirect.html',
                            {'redirect_to': redirect_to}
                        )
                        response.cookies = cookies
        except AttributeError:
            pass
        return response

    def _redirect_real(self, new_host, subdomain=None):
        """
        Tries its best to preserve request protocol, port, path, 
        and query args.  Only works with HTTP GET
        """
        if subdomain and subdomain is not "''":
            new_host = subdomain + "." + new_host
        if (new_host, self.port) == self.get_domain_and_port():
            raise DynamicSitesError("Redirect loop detected. The domain"
                " specified in settings.DEFAULT_HOST: '%s' may not exist"
                " in the Sites table." % settings.DEFAULT_HOST)

        return HttpResponsePermanentRedirect('%s://%s%s%s%s' % (
            self.request.is_secure() and 'https' or 'http',
            new_host,
            (int(self.port) not in (80, 443)) and ':%s' % self.port or '',
            urlquote(self.request.path),
            (self.request.method == 'GET' 
                and len(self.request.GET) > 0) 
                    and '?%s' % self.request.GET.urlencode() or ''
        ))

    def redirect(self, new_host, subdomain=None):
        """
        wraps around self._redirect to modify new_host, subdomain
        if the new_host has a matching ENV_HOSTNAME
        """
        if self.env_domain_requested:
            self.logger.debug('Remapping %s to ENV_HOSTNAME %s',
                new_host,
                self.env_domain_requested)
            # does a env_hostname exist for the target redirect?
            target_domain = '%s%s' % ((subdomain and subdomain is not "''") and '%s.' % subdomain or '', new_host)
            target_env_hostname = self.find_env_hostname(target_domain)
            target_subdomain=None
            while not target_env_hostname and target_domain:
                try:
                    target_subdomain, target_domain = target_domain.split('.',1)
                except ValueError:
                    break
                target_env_hostname = self.find_env_hostname(target_domain)
            if target_env_hostname:
                self.logger.debug(
                    'Redirecting to target env_hostname=%s, subdomain=%s', 
                    target_env_hostname, 
                    target_subdomain)
                return self._redirect(target_env_hostname,
                                     subdomain=target_subdomain)
            # unable to find env_hostname for target redirect... 
            # fall through to redirect to target redirect
            self.logger.debug(
                'No ENV_HOSTNAME map found for %s', 
                new_host)
        return self._redirect(new_host, subdomain)

    def find_env_hostname(self, target_domain):
        for k, v in self.ENV_HOSTNAMES.iteritems():
            if v == target_domain:
                return k


def site_folder_name(site):
    """
    Just a simple implementation to start.
    """
    return site.domain.replace('.', '_')

def all_sites():
    """
    Apply optional SITES_FILTER setting to Site.objects
    """
    return Site.objects.filter(**getattr(settings, 'SITES_FILTER', {}))
