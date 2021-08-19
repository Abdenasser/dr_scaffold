from django.conf import settings

class Generator(object):

    def __init__(self, app_name, model_name, fields):
        self.app_name = app_name
        self.model_name = model_name
        self.fields = fields
        self.MAIN_DIR = './'

    def generate(self):
        self.generate_app()
        self.generate_model()
        print("finished %s %s %s"% (self.app_name, self.model_name, self.fields))

    def generate_app(self):
        print("Generated App")

    def generate_model(self):
        print("Generated Model")