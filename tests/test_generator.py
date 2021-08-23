import os
import pytest  
import tempfile  
from os import path
from dr_scaffold.generators import Generator
from dr_scaffold.scaffold_templates import serializer_templates, model_templates
from unittest import TestCase

class TestGenerator(TestCase):
    tmpfilepath = os.path.join(tempfile.gettempdir(), "tmp-testfile")
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
