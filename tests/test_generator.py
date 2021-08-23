import os
import pytest  
import tempfile  
from os import path, system
from dr_scaffold.generators import Generator
from dr_scaffold.scaffold_templates import serializer_templates, model_templates
from unittest import TestCase

class TestGenerator(TestCase):
    tmpfilepath = os.path.join(tempfile.gettempdir(), "tmp-testfile")
    tmpdirpath = tempfile.mkdtemp()
    generator = Generator("apps/blog", "Article", ("title:charfield", "body:textfield"))

    def setUp(self):
        with open(self.tmpfilepath, "x") as f:
            f.write("Delete me!")
        
    def tearDown(self):
        os.remove(self.tmpfilepath)

    def test_init(self):
        g = self.generator
        assert g.app_name == "blog"
        assert g.MAIN_DIR == "apps"
        assert g.model_name == "Article"

    def test_add_setup_imports(self):
        g = self.generator
        file_paths = (self.tmpfilepath,)
        matching_imports = (serializer_templates.SETUP,)
        g.add_setup_imports(file_paths, matching_imports)
        with open(self.tmpfilepath, 'r+') as file:
            body = ''.join(line for line in file.readlines())
        assert body == serializer_templates.SETUP

    def test_setup_files(self):
        g = Generator(f"{self.tmpdirpath}/blog", "Article", ("title:charfield", "body:textfield"))
        system(f'python manage.py startapp {g.app_name}')
        system(f'mv {g.app_name} {self.tmpdirpath}')
        #making the appdir the temp folder for test purpose
        g.appdir = self.tmpdirpath
        g.setup_files()
        files = [f for f in os.listdir(self.tmpdirpath)]        
        assert len(files) == 5
        assert files == ['models.py', 'serializers.py', 'admin.py', 'urls.py', 'views.py']

    def test_get_fields_string(self):
        g = self.generator
        fields_string = g.get_fields_string(g.fields)
        string = model_templates.CHARFIELD % dict(name ="title") + model_templates.TEXTFIELD % dict(name="body")
        assert fields_string == string

    def test_get_model_string(self):
        g = self.generator
        fields_string = g.get_fields_string(fields = g.fields)
        model_string = g.get_model_string()
        string = model_templates.MODEL % ("Article", fields_string, "Articles")
        assert model_string == string

    def test_generate_models(self):
        g = Generator(f"{self.tmpdirpath}/blog", "Article", ("title:charfield", "body:textfield"))
        system(f'python manage.py startapp {g.app_name}')
        system(f'mv {g.app_name} {self.tmpdirpath}')
        #making the appdir the temp folder for test purpose
        g.appdir = self.tmpdirpath
        g.setup_files()
        g.generate_models()      
        with open(f"{g.appdir}/models.py", 'r+') as file:
            body = ''.join(line for line in file.readlines())
        assert ('Article' in body) == True
        assert ('Articles' in body) == True
        assert ('title' in body) == True
        assert ('body' in body) == True
        