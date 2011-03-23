from django.contrib.sites.models import Site

"""
dev_redirect_tests
------------------
maps a test request.HTTP_HOST to the expected (redirect, site.hostname)
"""
dev_redirect_tests = {
    'cus.dev':                        ('www.cus.dev','corp-umbrella-site.com'),
    'gfarbage':                       ('www.cus.dev','corp-umbrella-site.com'),
    'pignose.gfarbage.com':           ('pignose.cus.dev','corp-umbrella-site.com'),
    'dining.af.dev':                  ('res.af.dev','about-food.com'),
    'sc.dev':                         ('www.sc.dev','sobre-comida.com.br'),
    'sc.dev/marshmallows':            ('www.sc.dev/marshmallows','sobre-comida.com.br'),
    'www.ag.dev/conqueronious':       ('ag.dev/conqueronious','about.game.es'),
}

"""
prod_redirect_tests
------------------
maps a test request.HTTP_HOST to the expected redirect
"""
prod_redirect_host_tests = {
    'http://gfarbage/':                       'http://www.corp-umbrella-site.com/',
    'http://gfarbage/farm-animals':           'http://www.corp-umbrella-site.com/farm-animals',
    'http://pignose.gfarbage.com/':           'http://www.corp-umbrella-site.com/',
    'http://about-food.net/':                 'http://www.about-food.com/',
    'http://aboutfood.com/':                  'http://www.about-food.com/',
    'http://fruits.about-food.com/':          'http://fruit.about-food.com/',
    'http://fruits.about-food.net/':          'http://fruit.about-food.com/',
    'http://www.about-games.com/':            'http://about.gam.es/',
    'http://www.about-games.com/toast':       'http://about.gam.es/toast',
    'http://fruits.about-food.net/mapple':    'http://fruit.about-food.com/mapple',
    'http://diary.aboutfood.com/whole-milk':  'http://dairy.about-food.com/whole-milk',
}

"""
test sites
----------
"""
sites = [
    Site(domain='about-food.com',
         name='Site About Food',
         folder_name='about_food_com',
         subdomains=['www','fruit','meat','vegetables','dairy']),

    Site(domain='about.gam.es',
         name='About Games Site',
         folder_name='about_games'),

    Site(domain='corp-umbrella-site.com',
         name='Corporate Umbrella Site',
         folder_name='corp_site',
         subdomains=['www']),

    Site(domain='restaurants.about-food.com',
         name='About Food Subdomain Site',
         folder_name='about_food_restaurants'),

    Site(domain='sobre-comida.com.br',
         name='About Food Brazil Site',
         folder_name='sobre_comida_br',
         subdomains=['www', 'fruta', 'carne', 'legumes', 'leite'])
]

default_subdomain_tests = {
    'sobre-comida.com.br':'www',
    'restaurants.about-food.com':'',
    'corp-umbrella-site.com':'www',
    'about.gam.es':'',
    'about-food.com':'www',
}

site_identification_tests = {
    'http://gfarbage.sobre-comida.com.br/':'sobre-comida.com.br',
    'http://www.sobre-comida.com.br/':'sobre-comida.com.br',
    'http://peelandeat.about.game.es/':'about.game.es',
    'http://game.es/':'about.game.es',
    'http://about-food.com/':'about-food.com',
    'http://www.about-food.com/':'about-food.com',
    'http://restaurants.about-food.com/':'restaurants.about-food.com',
    'http://gfeebleminded.about-food.net/':'about-food.com',
    'http://gfeebleminded.restaurants.about-food.com/':'about-food.com',
    'http://www.aboutfood.com/':'about-food.com',
    'http://dining.aboutfood.com/':'restaurants.about-food.com',
    'http://gfeebleminded.aboutfood.com/':'about-food.com',
    'http://gfeebleminded.dining.aboutfood.com/':'about-food.com',
}

class MockRequest(object):
    def __init__(self, host):
        self.host = host

    def get_host(self):
        return self.host
        
    META = {'SERVER_PORT':'80'}

hostname_and_port_tests = {
    'AbOUt-FOOd.cOm:9394': ('about-food.com','9394'),
    'a.B.c.D.e.F.G:64693': ('a.b.c.d.e.f.g','64693'),
    'aboutfood.com': ('aboutfood.com','80'),
}