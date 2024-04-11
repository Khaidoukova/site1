# -*- coding: utf-8 -*-

import os,sys

# #путь к проекту
# sys.path.append('/home/a/allagro/site1/config')
# #путь к фреймворку
# sys.path.append('/home/a/allagro/site1')
# #путь к виртуальному окружению
# sys.path.append('/home/a/allagro/.djangovenv/lib/python3.8/site-packages/')
# #исключить системную директорию
# sys.path.remove('/usr/lib/python3.8/site-packages')
os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings"

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()