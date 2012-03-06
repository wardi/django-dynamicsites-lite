from django.conf import settings
from django.test import TestCase
from django.contrib.sites.models import Site

from test.settings import TestSettings
from test.config import *

from middleware import DynamicSitesMiddleware

class MyTest(TestCase):
    def setUp(self):
        # modify django.conf.settings the way we need
        self.old_settings = TestSettings()
        # create all the sites in the test database
        for site in sites:
            site.save()

    def tearDown(self):
        # delete all the test sites from the test database
        for site in sites:
            s = Site.objects.get(domain=site.domain)
            s.delete()
        # reset settings back to what they were
        self.old_settings.revert()

    def test_my_patience(self):
        """
        make sure the sites we created in setup
        actually exist
        """
        for suit in sites:
            s = Site.objects.get(domain=suit.domain)

    def test_prod_host_redirects(self):
        # note these don't work because request.get_host() 
        # always returns "testserver" when using the testclient
        return
        for (src,dest) in prod_redirect_host_tests.iteritems():
            print 'testing %s ' % src
            # make a request for src
            response = self.client.get(src)
            self.assertEqual(response.status_code, 301)
            allgood = False
            badmsg = '%s did not redirect to %s as expected' % (src,dest)
            print 'RESPONSE'
            for a,b in response.items():
                print '%s=%s' % (a,b)
                if a == 'Location':
                    # verify redirect to dest
                    self.assertEqual(b, dest, badmsg)
                    allgood = True
                    break
            # if we got here then no 'Location' was found in
            # response.items() -- not expecting this to happen
            self.assertTrue(allgood, 'UNEXPECTED: %s' % badmsg)

    def test_dev_hostnames(self):
        pass

    def test_site_identification(self):
        # note these don't work because request.get_host() 
        # always returns "testserver" when using the testclient
        return        
        for (test_domain,expected_domain) in site_identification_tests.iteritems():
            # client needs to follow redirects now... (?)
            response = self.client.get(test_domain)
            self.assertEqual(response.domain, expected_domain)

    def test_hostname_parsing(self):
        mommyware = DynamicSitesMiddleware()
        for (test_input, (expected_hostname, expected_port)) in hostname_and_port_tests.iteritems():
            mommyware.request = MockRequest(test_input)
            (hostname,port) = mommyware.get_domain_and_port()
            self.assertEqual(hostname, expected_hostname)
            self.assertEqual(port, expected_port)

    def test_default_subdomains(self):
        for (domain,default_subdomain) in default_subdomain_tests.iteritems():
            s = Site.objects.get(domain=domain)
            self.assertEquals(default_subdomain, s.default_subdomain, 
                'Site domain=%s default_subdomain=%s, expected %s' % 
                    (s.domain, s.default_subdomain, default_subdomain))
