#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/catalog/catalog/")

#from catalog import app as application
from application import app
application = app
#application.secret_key = 'Add your secret key'
