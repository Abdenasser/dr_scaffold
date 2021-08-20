from os import path, system
from core.scaffold_templates import model_templates

class Generator(object):

    def __init__(self, appdir, model_name, fields):
      self.appdir = appdir
      self.MAIN_DIR = './'
      self.app_name = appdir
      if len(appdir.split('/'))>= 2:
        self.MAIN_DIR = appdir.split("/", maxsplit=1)[0]
        self.app_name = appdir.split("/", maxsplit=1)[1]
      self.model_name = model_name
      self.fields = fields
      self.foreign_model_imports = list()
      self.models_file = '%s/models.py' % (appdir)

    def generate(self):
      self.generate_app()
      self.generate_model()
      print("Model %s have been created at %s%s with the following field: \n %s"% (self.model_name, self.MAIN_DIR, self.app_name, self.fields))

    def generate_app(self):
      if not path.exists('%s' % (self.appdir)):
        system('python manage.py startapp %s' % self.app_name)
        system('mv %s %s' % (self.app_name, self.appdir))
        print("Generating app through startapp")
      else:
        print("App does already exist at %s" % (self.appdir))

    def generate_model(self):
      models_file = open(self.models_file, 'r')
      if self.model_exist(models_file, self.model_name):
        return 
      fields_templates = self.get_fields_templates(self.fields)
      model_template = model_templates.MODEL % (self.model_name, ''.join(field for field in fields_templates))
      imports_template = ''.join(import_line for import_line in self.foreign_model_imports)
      self.rewrite_models_file(imports_template,model_template)

    def rewrite_models_file(self, imports, model):
      with open(self.models_file, 'r+') as models_file:
        file_content = ''.join(line for line in models_file.readlines())
        new_content = imports+file_content+model+"\n"
        models_file.seek(0)
        models_file.write(new_content)
      return print("-------|| FINISHED ||-------")

    def get_fields_templates(self, fields):
      actual_fields = list()
      for field in fields:
        new_field = self.select_field_template(field)
        if new_field:
          actual_fields.append(new_field)
      return actual_fields

    def model_exist(self, models_file, model): 
      for line in models_file.readlines():
        if 'class %s' % model in line:
          print('Model already exists at %s/models.py' % (self.appdir))
          return True
      return False

    def select_field_template(self, field):
      field_name = field.split(':')[0]
      field_type = field.split(':')[1].lower()
      if field_type == 'foreignkey':
        self.set_foreign_field(field)
      return self.get_field_template(field_type,field_name) 

    def set_foreign_field(self, field):
      self.foreign_model = field.split(':')[2]
      field_name = field.split(':')[0]
      field_type = field.split(':')[1].lower()
      #foreign_model_import = self.get_import_template(self.foreign_model)
      if self.is_imported(self.models_file, self.foreign_model):
        return self.get_field_template(field_type, field_name)
      # No need to add imports of models of the same app
      #self.foreign_model_imports.append(foreign_model_import)
      return self.get_field_template(field_type, field_name)
      
    def get_field_template(self, field_type, field_name):
      if field_type == 'foreignkey':
        return model_templates.FIELD_TYPES[field_type] % {'name': field_name, 'foreign': self.foreign_model}
      return model_templates.FIELD_TYPES[field_type] % {'name': field_name}  
    
    def get_import_template(self, model):
      return model_templates.MODEL_IMPORT % {'app': self.appdir.replace("/", "."), 'model': model}

    def is_imported(self, path, model):
      file = open(path, 'r')
      for line in file.readlines():
        if 'import %s' % model in line:
          return True
      return False