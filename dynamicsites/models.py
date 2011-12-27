from django.contrib.sites.models import Site
from fields import SubdomainListField, FolderNameField

"""
Monkey-patch the Site object to include a list of subdomains

Future ideas include:

* Site-enabled checkbox
* Site-groups
* Account subdomains (ala basecamp)
"""

# not sure which is better...
# Site.add_to_class('subdomains', SubdomainListField(blank=True))
FolderNameField(blank=True).contribute_to_class(Site,'folder_name')
SubdomainListField(blank=True).contribute_to_class(Site,'subdomains')

@property
def has_subdomains(self):
    return len(self.subdomains)

@property
def default_subdomain(self):
    """
    Return the first subdomain in self.subdomains or '' if no subdomains defined
    """
    if len(self.subdomains):
        if self.subdomains[0]=="''":
            return ''
        return self.subdomains[0]
    return ''

Site.has_subdomains = has_subdomains
Site.default_subdomain = default_subdomain


