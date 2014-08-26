Example
=======

To run this example run following commands:

    pip install -r requirements.txt
    pip install ..
    python manage.py syncdb
    python manage.py loaddata fixtures/initial_data.json
    python manage.py runserver

Add following to your `/etc/hosts` file (`C:\Windows\System32\Drivers\etc\hosts` on Windows):

    127.0.0.1 host1.example.com host2.example.com host3.example.com

Open http://127.0.0.1:8000 in your browser.
