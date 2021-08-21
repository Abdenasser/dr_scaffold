from os import path, system
from drf_scaffold_core.scaffold_templates import model_templates, admin_templates, view_templates, serializer_templates, url_templates

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
      self.admin_file = '%s/admin.py' % (appdir)
      self.views_file = '%s/views.py' % (appdir)
      self.serializers_file = '%s/serializers.py' % (appdir)
      self.urls_file = '%s/urls.py' % (appdir)

    def generate(self):
      self.generate_app()
      self.generate_models()
      self.register_models_to_admin()
      self.generate_serializers()
      self.generate_views()
      self.generate_urls()

    def generate_app(self):
      if not path.exists('%s' % (self.appdir)):
        system('python manage.py startapp %s' % self.app_name)
        system('mv %s %s' % (self.app_name, self.appdir))
        self.setup_views_file()
        self.setup_serializers_file()
        self.setup_urls_file()
      else:
        print("App does already exist at %s" % (self.appdir))

    def setup_views_file(self):
      view_setup = view_templates.VIEWSET_SETUP
      self.rewrite_component_file( self.views_file, view_setup, '')

    def setup_serializers_file(self):
      open(self.serializers_file, 'x')
      serializer_setup = serializer_templates.SERIALIZER_SETUP
      self.rewrite_component_file( self.serializers_file, serializer_setup, '')

    def setup_urls_file(self):
      open(self.urls_file, 'x')
      urls_setup = url_templates.URLS_SETUP
      self.rewrite_component_file( self.urls_file, urls_setup, '')

    def generate_models(self):
      models_file = open(self.models_file, 'r')
      if self.class_exist('models',models_file, self.model_name):
        return 
      fields_templates = self.get_fields_templates(self.fields)
      model_template = model_templates.MODEL % (self.model_name, ''.join(field for field in fields_templates))
      imports_template = ''.join(import_line for import_line in self.foreign_model_imports)
      self.rewrite_component_file(self.models_file, imports_template,model_template)
      return print("🚀 %s have been successfully updated"%self.models_file)

    def rewrite_component_file(self, file_path, head, body):
      with open(file_path, 'r+') as file:
        file_content = ''.join(line for line in file.readlines())
        new_content = head + file_content + body + "\n"
        file.seek(0)
        file.write(new_content)

    def get_fields_templates(self, fields):
      actual_fields = list()
      for field in fields:
        new_field = self.select_field_template(field)
        if new_field:
          actual_fields.append(new_field)
      return actual_fields

    def class_exist(self, component, file, model): 
      for line in file.readlines():
        if component == 'models':
          if 'class %s' % model in line:
            print('Model already exists at %s/models.py' % (self.appdir))
            return True
        elif component == 'admin':
          if '@admin.register(%s)' % model in line:
            print('Model already registered at %s/admin.py' % (self.appdir))
            return True
        elif component == 'view':
          if 'class %sViewSet' % model in line:
            print('ViewSet already exists at %s/views.py' % (self.appdir))
            return True   
        elif component == 'serializer':
          if 'class %sSerializer' % model in line:
            print('Serializer already exists at %s/serializers.py' % (self.appdir))
            return True
        elif component == 'url':
          if '%sViewSet)' % model in line:
            print('Url already exists at %s/urls.py' % (self.appdir))
            return True           
      return False

    def select_field_template(self, field):
      field_name = field.split(':')[0]
      field_type = field.split(':')[1].lower()
      return model_templates.FIELD_TYPES[field_type] % dict(name= field_name, foreign = field.split(':')[2] if (field_type == 'foreignkey') else '')

    def is_imported(self, path, model):
      file = open(path, 'r')
      for line in file.readlines():
        if 'import %s' % model in line:
          return True
      return False

    def register_models_to_admin(self):
      admin_file = open(self.admin_file, 'r')
      if self.class_exist('admin', admin_file, self.model_name):
        return 
      model_register_template = admin_templates.REGISTER % {'model': self.model_name}
      import_template = admin_templates.MODEL_IMPORT % {'app': self.appdir.replace("/", "."), 'model': self.model_name}
      self.rewrite_component_file(self.admin_file, import_template,model_register_template)
      return print("🚀 %s have been successfully updated"%self.admin_file)

    def generate_views(self):
      view_file = open(self.views_file, 'r')
      if self.class_exist('view', view_file, self.model_name):
        return 
      viewset_template = view_templates.VIEWSET % {'model': self.model_name}
      model_import_template = view_templates.MODEL_IMPORT % {'app': self.appdir.replace("/", "."), 'model': self.model_name}
      serializer_import_template= view_templates.SERIALIZER_IMPORT % {'app': self.appdir.replace("/", "."), 'model': self.model_name}
      imports = model_import_template+serializer_import_template
      self.rewrite_component_file(self.views_file, imports,viewset_template)
      return print("🚀 %s have been successfully updated"%self.views_file)

    def generate_serializers(self):
      serializer_file = open(self.serializers_file, 'r')
      if self.class_exist('serializer', serializer_file, self.model_name):
        return 
      serializer_template = serializer_templates.SERIALIZER % {'model': self.model_name}
      model_import_template = serializer_templates.MODEL_IMPORT % {'app': self.appdir.replace("/", "."), 'model': self.model_name}
      self.rewrite_component_file(self.serializers_file, model_import_template,serializer_template)
      return print("🚀 %s have been successfully updated"%self.serializers_file)

    def generate_urls(self):
      urls_file = open(self.urls_file, 'r')
      if self.class_exist('url', urls_file, self.model_name):
        return 
      url_template = url_templates.URL % {'model': self.model_name, 'path': self.model_name.lower()+'es'} + url_templates.URL_PATTERNS
      model_import_template = url_templates.MODEL_IMPORT % {'app': self.appdir.replace("/", "."), 'model': self.model_name}
      self.rewrite_component_file(self.urls_file, model_import_template,url_template)
      return print("🚀 %s have been successfully updated"%self.urls_file)