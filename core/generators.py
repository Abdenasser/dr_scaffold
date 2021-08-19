from django.conf import settings
from os import path, system

class Generator(object):

    def __init__(self, appdir, model_name, fields):
        self.appdir = appdir
        self.MAIN_DIR = appdir.split("/", maxsplit=1)[0]
        self.app_name = appdir.split("/", maxsplit=1)[1]
        self.model_name = model_name
        self.fields = fields

    def generate(self):
        self.generate_app()
        self.generate_model()
        print("finished %s %s %s %s"% (self.MAIN_DIR, self.app_name, self.model_name, self.fields))

    def generate_app(self):
        if not path.exists('%s' % (self.appdir)):
            system('python manage.py startapp %s' % self.app_name)
            system('mv %s %s' % (self.app_name, self.appdir))
            print("Generated App")
        else:
            print("app already exist @ %s" % (self.appdir))

    def generate_model(self):
        print("Generated Model")     