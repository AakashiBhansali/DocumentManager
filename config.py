import os
import urllib
DEBUG =  True
SECRET_KEY = os.urandom(24)
MONGO_USERNAME = urllib.parse.quote('lazypanda')
MONGO_PASSWORD = urllib.parse.quote('lazy')
MONGO_URI = 'mongodb://{0}:{1}@ds231199.mlab.com:31199/caavo'.format(MONGO_USERNAME,MONGO_PASSWORD)
MONGO_DB = 'caavo'