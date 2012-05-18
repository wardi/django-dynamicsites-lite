import os

from filebrowser.conf import FileBrowserSettings, fb_settings
from filebrowser.settings import DIRECTORY
from dynamicsiteslite.utils import make_tls_property

FB_DIR = FileBrowserSettings.DIRECTORY = make_tls_property(DIRECTORY)

class DynamicFileBrowserMiddleware(object):
    """
    Add the dynamicsites directory to the uploads directory setting

    e.g. 'uploads/' becomes 'uploads/some_host_example_com/'

    if this directory doesn't exist then create it.
    """
    def process_request(self, request):
        FB_DIR.value = DIRECTORY + request.dynamicsites_folder_name + '/'

        abs_path = os.path.join(fb_settings.MEDIA_ROOT, fb_settings.DIRECTORY)
        if not os.path.isdir(abs_path):
            os.mkdir(abs_path)

