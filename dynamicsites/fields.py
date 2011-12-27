from django import forms
from django.db import models
from django.core.validators import URLValidator, ValidationError
from django.utils.encoding import smart_unicode
from widgets import SubdomainTextarea, FolderNameInput
import re

import logging

class SubdomainListFormField(forms.Field):

    def __init__(self, *args, **kwargs):
        kwargs['widget'] = SubdomainTextarea()
        self.logger = logging.getLogger(__name__)
        super(SubdomainListFormField, self).__init__(*args, **kwargs)

    """
    A form field to accept a string of subdomains, separated by commas
    If blank or an asterisk '*', allow all subdomains
    """
    def to_python(self, value):
        """
        return list of subdomains
        """
        if not value:
            return []

        # convert newlines to commas
        value = re.sub("\n|\r", ',', value)
       
        # clean incoming subdomains
        subdomains = []
        for subdomain in value.split(','):
            subdomain = subdomain.strip().lower()
            if subdomain and subdomain is not '*':
                subdomains.append(subdomain)
        return subdomains

    def validate(self, value):
        """
        Uses URLValidator to validate subdomains
        """
        # TODO Make a SubdomainValidator as a subclass of 
        # URLValidator and use it both in model and form fields (ala URLField)
        super(SubdomainListFormField, self).validate(value)

        u = URLValidator()
        for subdomain in value:
            self.logger.debug('validating %s', subdomain)
            if subdomain == "''":
                self.logger.debug('passing')
                pass
            else:
                test_host = 'http://%s.example.com/' % subdomain
                self.logger.debug('testing %s', test_host)
                u(test_host)

class SubdomainListField(models.TextField):
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        kwargs['help_text'] = "Comma separated list of subdomains this site supports.  Leave blank to support all subdomains"
        super(SubdomainListField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        value = super(SubdomainListField, self).to_python(value)
        if not value: return []
        if isinstance(value, list):
            return value
        return value.split(',')

    def formfield(self, **kwargs):
        defaults = {'form_class':SubdomainListFormField}
        defaults.update(kwargs)
        return super(SubdomainListField, self).formfield(**defaults)

    def get_db_prep_value(self, value, connection=None, prepared=False):
        if not value: return ""
        assert(isinstance(value, list) or isinstance(value, tuple))
        return u','.join([smart_unicode(s) for s in value])

    def value_to_string(self, obj):
        print 'value to string()'
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)
        

class FolderNameFormField(forms.CharField):
    """
    A form field to accept a foldername for this site
    """
    def __init__(self, *args, **kwargs):
        kwargs['widget'] = FolderNameInput()
        super(FolderNameFormField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        """
        return value stripped of leading/trailing whitespace, and lowercased
        """
        return value.strip().lower()
    
    def validate(self, value):
        """
        Validates the folder name is a valid Python package name
        Verifies if the folder name exists by trying to 
        do an import
        """
        super(FolderNameFormField, self).validate(value)
        
        if re.search(r"[^a-z0-9_]", value):
            raise ValidationError('The folder name must only contain letters, numbers, or underscores')
        try:
            __import__("sites.%s" % value)
        except ImportError:
            raise ValidationError('The folder sites/%s/ does not exist or is missing the __init__.py file' % value)

class FolderNameField(models.CharField):
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        kwargs['help_text'] = "Folder name for this site's files.  The name may only consist of lowercase characters, numbers (0-9), and/or underscores"
        kwargs['max_length'] = 64
        super(FolderNameField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'form_class':FolderNameFormField}
        defaults.update(kwargs)
        return super(FolderNameField, self).formfield(**defaults)
