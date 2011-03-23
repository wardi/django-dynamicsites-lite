from django.conf import settings
import os

SITES_DIR = os.path.join(os.path.dirname(__file__), 'sites')

DEFAULT_HOST = 'www.corp-umbrella-site.com'
HOSTNAME_REDIRECTS = {
    'aboutfood.com':              'www.about-food.com',
    'about-food.net':             'www.about-food.com',
    'meats.about-food.com':       'meat.about-food.com',
    'fruits.about-food.com':      'fruit.about-food.com',
    'vegetable.about-food.com':   'vegetables.about-food.com',
    'diary.about-food.com':       'dairy.about-food.com',
    'restaurant.about-food.com':  'restaurants.about-food.com',
    'dining.about-food.com':      'restaurants.about-food.com',
    'carnes.sobre-comida.com.br': 'carne.sobre-comida.com.br',
    'frutas.sobre-comida.com.br': 'fruta.sobre-comida.com.br',
    'legume.sobre-comida.com.br': 'legumes.sobre-comida.com.br',
    'leites.sobre-comida.com.br': 'leite.sobre-comida.com.br',
    'about-games.com':            'about.gam.es'
}

DEV_HOSTNAMES = {
    'cus.dev':    'corp-umbrella-site.com',
    'af.dev':     'about-food.com',
    'res.af.dev': 'restaurants.about-food.com',
    'sc.dev':     'sobre-comida.com.br',
    'ag.dev':     'about.gam.es'
}

class TestSettings(object):
    """
    Temporarily modifies django.conf.settings to use test settings
    """
    SITES_DIR = None
    DEFAULT_HOST = None
    HOSTNAME_REDIRECTS = None
    DEV_HOSTNAMES = None

    def __init__(self):
        """
        Modifies django's settings for this test environment
        """
        self._copy_in()
        self._set_test_settings()

    def _copy_in(self):
        try:
            self.SITES_DIR = settings.SITES_DIR
        except AttributeError:
            pass
        try:
            self.DEFAULT_HOST = settings.DEFAULT_HOST
        except AttributeError:
            pass
        try:
            self.HOSTNAME_REDIRECTS = settings.HOSTNAME_REDIRECTS
        except AttributeError:
            pass
        try:
            self.DEV_HOSTNAMES = settings.DEV_HOSTNAMES
        except AttributeError:
            pass

    def _set_test_settings(self):
        settings.SITES_DIR          = SITES_DIR
        settings.DEFAULT_HOST       = DEFAULT_HOST
        settings.HOSTNAME_REDIRECTS = HOSTNAME_REDIRECTS
        settings.DEV_HOSTNAMES      = DEV_HOSTNAMES

    def revert(self):
        """
        reverts django.conf.settings back to what they were
        """
        if self.SITES_DIR:
            settings.SITES_DIR = self.SITES_DIR
        else:
            delattr(settings, 'SITES_DIR')

        if self.DEFAULT_HOST:
            settings.DEFAULT_HOST = self.DEFAULT_HOST
        else:
            delattr(settings, 'DEFAULT_HOST')

        if self.HOSTNAME_REDIRECTS:
            settings.HOSTNAME_REDIRECTS = self.HOSTNAME_REDIRECTS
        else:
            delattr(settings, 'HOSTNAME_REDIRECTS')

        if self.DEV_HOSTNAMES:
            settings.DEV_HOSTNAMES = self.DEV_HOSTNAMES
        else:
            delattr(settings, 'DEV_HOSTNAMES')