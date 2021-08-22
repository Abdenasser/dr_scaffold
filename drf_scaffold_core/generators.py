import inflect
from os import path, system
from drf_scaffold_core.scaffold_templates import model_templates, admin_templates, view_templates, serializer_templates, url_templates
from drf_scaffold_core import file_api

def pluralize(str):
    p = inflect.engine()
    return p.plural(str)

def wipe_files(file_paths):
    for f in file_paths:
        file_api.wipe_file_content(f)

def create_files(file_paths):
    for f in file_paths:
        file_api.create_file(f)

class Generator(object):

    def __init__(self, appdir, model_name, fields):
      self.appdir = appdir
      self.MAIN_DIR = './'
      self.app_name = appdir
      if len(appdir.split('/'))>= 2:
        self.MAIN_DIR = appdir.split("/")[0]
        self.app_name = appdir.split("/")[1]
      self.model_name = model_name
      self.fields = fields

    def generate(self):
      self.generate_app()
      self.generate_models()
      self.register_models_to_admin()
      self.generate_serializers()
      self.generate_views()
      self.generate_urls()

    def add_setup_imports(self, file_paths, imports):
      for i, f in enumerate(file_paths):
        file_api.set_file_content(f, imports[i])

    def setup_files(self):
      extra_files = (f"{self.appdir}/serializers.py", f"{self.appdir}/urls.py" )
      original_files = (f"{self.appdir}/models.py", f"{self.appdir}/admin.py", f"{self.appdir}/views.py")
      all_files = extra_files + original_files
      setup_imports = (serializer_templates.SETUP, url_templates.SETUP, model_templates.SETUP, admin_templates.SETUP, view_templates.SETUP)
      create_files(extra_files)
      wipe_files(all_files)
      self.add_setup_imports(all_files, setup_imports)

    def generate_app(self):
      if not path.exists('%s' % (self.appdir)):
        system(f'python manage.py startapp {self.app_name}')
        system(f'mv {self.app_name} {self.appdir}')
        self.setup_files()
      else:
        print(f"App does already exist at {self.appdir}")

    """ 
    MODELS GENERATION METHODS 
        1 - get_fields_string : match fields from cli with their templates and return a string of them joined
        2 - get_model_string : yield the fields string in the Model template and returns a new Model string
        3 - generate_models: check if the model does already exists in the models.py file if not it append it
    """
    def get_fields_string(self, fields):
      actual_fields = list()
      for field in fields:
        field_name = field.split(':')[0]
        field_type = field.split(':')[1].lower()
        field_dict = dict(name= field_name, foreign = field.split(':')[2] if (field_type == 'foreignkey') else '')
        field_template = model_templates.FIELD_TYPES[field_type] % field_dict
        actual_fields.append(field_template)
      fields_string = ''.join(f for f in actual_fields)    
      return fields_string

    def get_model_string(self):
      fields_string = self.get_fields_string(self.fields)
      params = (self.model_name, fields_string, pluralize(self.model_name).capitalize())
      return model_templates.MODEL % params

    def generate_models(self):
      file = f"{self.appdir}/models.py"
      chunk = f'class {self.model_name}'
      if file_api.is_present_in_file(file, chunk):
        return 
      model_string = self.get_model_string()
      file_api.append_file_content(file, model_string)

    """ 
    MODELS REGISTRATION TO ADMIN 
        1 - get_admin_parts : returns the register template and imports of the Model class
        2 - register_models_to_admin : check if the model already registered in admin.py if not 
        it wraps the admin file content between the Model imports and register template 
    """
    def get_admin_parts(self):
      app_path = self.appdir.replace("/", ".")
      model_register_template = admin_templates.REGISTER % {'model': self.model_name}
      model_import_template = admin_templates.MODEL_IMPORT % {'app': app_path, 'model': self.model_name}
      return (model_import_template, model_register_template)

    def register_models_to_admin(self):
      file = f"{self.appdir}/admin.py"
      chunk = f'@admin.register({self.model_name})'
      if file_api.is_present_in_file(file, chunk):
        return 
      head, body = self.get_admin_parts()
      file_api.wrap_file_content(file, head, body)

    """ 
    VIEWS GENERATION 
        1 - get_viewset_parts : returns the viewset template and model + serializers imports of the Model class
        2 - generate_views : check if the viewset already exists in views.py if not 
        it wraps the file content between the imports and the viewset template 
    """
    def get_viewset_parts(self):
      app_path = self.appdir.replace("/", ".")
      viewset_template = view_templates.VIEWSET % {'model': self.model_name}
      model_import_template = view_templates.MODEL_IMPORT % {'app': app_path, 'model': self.model_name}
      serializer_import_template= view_templates.SERIALIZER_IMPORT % {'app': app_path, 'model': self.model_name}
      imports = model_import_template + serializer_import_template
      return (imports, viewset_template)

    def generate_views(self):
      file = f"{self.appdir}/views.py"
      chunk = f'class {self.model_name}ViewSet'
      if file_api.is_present_in_file(file, chunk):
        return 
      head, body = self.get_viewset_parts()  
      file_api.wrap_file_content(file, head, body)
    
    """ 
    SERIALIZER GENERATION 
        1 - get_serializer_parts : returns the serializer template and imports of the Model class
        2 - generate_serializers : check if the viewset already exists in serializers.py if not 
        it wraps the file content between the imports and the serializer template 
    """
    def get_serializer_parts(self):
      app_path = self.appdir.replace("/", ".")
      serializer_template = serializer_templates.SERIALIZER % {'model': self.model_name}
      imports = serializer_templates.MODEL_IMPORT % {'app': app_path, 'model': self.model_name}
      return(imports, serializer_template)

    def generate_serializers(self):
      serializer_file = f"{self.appdir}/serializers.py"
      serializer_head = f'class {self.model_name}Serializer'
      if file_api.is_present_in_file(serializer_file, serializer_head):
        return 
      head, body = self.get_serializer_parts()  
      file_api.wrap_file_content(serializer_file, head, body)
    
    """ 
    URLS GENERATION 
        1 - get_url_parts : returns the url template and model imports of the Model class
        2 - generate_urls : check if the url already exists in urls.py if not 
        it wraps the file content between the imports and the url template, before wrapping 
        it checks if the file has URL_PATTERS it take it off and append it to the url template 
    """
    def get_url_parts(self):
      app_path = self.appdir.replace("/", ".")  
      plural_path = pluralize(self.model_name.lower()).capitalize()
      url_template = url_templates.URL % {'model': self.model_name, 'path': plural_path}
      imports = url_templates.MODEL_IMPORT % {'app': app_path, 'model': self.model_name}
      return(imports, url_template)

    def generate_urls(self):
      file = f"{self.appdir}/urls.py"
      chunk = f'{self.model_name}ViewSet)'
      if file_api.is_present_in_file(file, chunk):
        return 
      head, body = self.get_url_parts() 
      if file_api.is_present_in_file(file, url_templates.URL_PATTERNS):
        file_api.replace_file_chunk(file,url_templates.URL_PATTERNS, "")
      body = body + url_templates.URL_PATTERNS
      file_api.wrap_file_content(file, head, body)