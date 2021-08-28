"""
Tests for Generator
"""
import os
import io
import sys
import tempfile
from unittest import TestCase, mock
from django.conf import settings
from dr_scaffold.generators import Generator, pluralize
from dr_scaffold.scaffold_templates import serializer_templates, model_templates


class TestGenerator(TestCase):
    """
    Tests for Generator
    """
    tmpfilepath = os.path.join(tempfile.gettempdir(), "tmp-testfile")
    tmpdirpath = tempfile.mkdtemp()
    # tmpdirpath = 'generated_tests_folder'
    if not os.path.exists(tmpdirpath):
        os.mkdir(tmpdirpath)
    core_folder = tmpdirpath+'/'+ settings.CORE_FOLDER
    api_folder = tmpdirpath+'/'+ settings.API_FOLDER
    generator = Generator("blog", "Article", ("title:charfield", "body:textfield"))

    def setUp(self):
        """
        Tests
        """
        if not os.path.exists(self.core_folder):
            os.mkdir(self.core_folder)
            os.mkdir(self.core_folder+'blog')
        if not os.path.exists(self.api_folder):
            os.mkdir(self.api_folder)
            os.mkdir(self.api_folder+'blog')
        for file_name in [f'{self.core_folder}blog/models.py',
                f'{self.api_folder}blog/serializers.py',
                f'{self.core_folder}blog/admin.py',
                f'{self.api_folder}blog/urls.py',
                f'{self.api_folder}blog/views.py']:
            with open(file_name, 'x', encoding='utf8') as file:
                file.close()

    def tearDown(self):
        """
        Tests
        """
        for file_name in [f'{self.core_folder}blog/models.py',
                f'{self.api_folder}blog/serializers.py',
                f'{self.core_folder}blog/admin.py',
                f'{self.api_folder}blog/urls.py',
                f'{self.api_folder}blog/views.py']:
            os.remove(file_name)

    @classmethod
    def test_pluralize(cls):
        """
        Tests
        """
        assert pluralize("article") == 'articles'
        assert pluralize("category") == 'categories'
        assert pluralize("post") == 'posts'

    def test_init(self):
        """
        Tests
        """
        generator_obj = self.generator
        assert generator_obj.app_name == "blog"
        assert generator_obj.model_name == "Article"

    def test_add_setup_imports(self):
        """
        Tests
        """
        generator_obj = self.generator
        generator_obj.core_folder = self.core_folder
        file_paths = (f'{self.core_folder}blog/models.py',)
        matching_imports = (serializer_templates.SETUP,)
        generator_obj.add_setup_imports(file_paths, matching_imports)
        with open(file_paths[0], 'r+', encoding='utf8') as file:
            body = ''.join(line for line in file.readlines())
        assert body == serializer_templates.SETUP

    def test_setup_files(self):
        """
        Tests
        """
        generator_obj = Generator("blog",
            "Article",
            ("title:charfield", "body:textfield"))
        generator_obj.core_dir = self.core_folder
        generator_obj.api_dir = self.api_folder
        generator_obj.setup_files()
        core_files = list(os.listdir(self.core_folder+'blog/'))
        api_files= list(os.listdir(self.api_folder+'blog/'))
        with open(self.core_folder+'blog/models.py', 'r+', encoding='utf8') as file:
            body = ''.join(line for line in file.readlines())
        assert len(core_files+api_files) == 6 #taking in count migrations folder
        assert ("from django.db import models" in body) is True

    @mock.patch('dr_scaffold.generators.file_api.is_present_in_file')
    def test_get_fields_string(self, mock_is_in_file):
        """
        Tests
        """
        generator_obj = self.generator
        fields_string = generator_obj.get_fields_string(generator_obj.fields)
        body_template = (model_templates.TEXTFIELD % dict(name="body"))
        title_template = model_templates.CHARFIELD % dict(name ="title")
        string = title_template + body_template
        assert fields_string == string
        #test relation field type
        generator_obj2 = Generator("blog",
            "Article",
            ("author:foreignkey:Author",))
        generator_obj2.get_fields_string(generator_obj2.fields)
        mock_is_in_file.assert_called_once()

    def test_get_fields_string_relation_model_not_created_yet(self):
        """
        Tests
        """
        generator_obj2 = Generator("blog",
            "Article",
            ("author:foreignkey:Author",))
        generator_obj2.core_dir = self.core_folder
        generator_obj2.api_dir = self.api_folder
        captured_output = io.StringIO()
        sys.stdout = captured_output
        generator_obj2.get_fields_string(generator_obj2.fields)
        sys.stdout = sys.__stdout__
        assert "⚠️ bare in mind that Author" in captured_output.getvalue()

    def test_get_model_string(self):
        """
        Tests
        """
        generator_obj = self.generator
        fields_string = generator_obj.get_fields_string(fields = generator_obj.fields)
        model_string = generator_obj.get_model_string()
        string = model_templates.MODEL % ("Article", fields_string, "Articles")
        assert model_string == string

    def test_run(self):
        """
        Tests
        """
        generator_obj = Generator("blog",
            "Article",
            ("title:charfield", "body:textfield"))
        generator_obj.core_dir = self.core_folder
        generator_obj.api_dir = self.api_folder
        result = generator_obj.run()
        assert result == print("🎉 Your RESTful Article api resource is ready 🎉")
        # test case where something is wront
        generator_obj2 = Generator("blog", "Author", ("title:charfiel",))
        generator_obj2.core_dir = self.core_folder
        generator_obj2.api_dir = self.api_folder
        result = generator_obj2.run()
        assert result == print("🤔 Oops something is wrong: charfiel")

    @mock.patch('dr_scaffold.generators.Generator.generate_app')
    def test_generate_api(self,mock_generate_app):
        """
        Tests
        """
        generator_obj = Generator("blog",
            "Article",
            ("title:charfield", "body:textfield"))
        generator_obj.core_dir = self.core_folder
        generator_obj.api_dir = self.api_folder
        generator_obj.generate_api()
        mock_generate_app.assert_called_once()

    def test_generate_models(self):
        """
        Tests
        """
        generator_obj = Generator("blog",
            "Article",
            ("title:charfield", "body:textfield"))
        generator_obj.core_dir = self.core_folder
        generator_obj.api_dir = self.api_folder
        generator_obj.generate_models()
        with open(f"{self.core_folder}blog/models.py", 'r+', encoding='utf8') as file:
            body = ''.join(line for line in file.readlines())
        assert ('Article' in body) is True
        assert ('Articles' in body) is True
        assert ('title' in body) is True
        assert ('body' in body) is True
        # test when model already generated
        generator_obj = Generator("blog",
            "Article",
            ("title:charfield", "body:textfield"))
        generator_obj.core_dir = self.core_folder
        generator_obj.api_dir = self.api_folder
        generator_obj.generate_models()
        assert body.count('class Article') == 1
        assert body.count('class Meta:') == 1

    def test_get_admin_parts(self):
        """
        Tests
        """
        generator_obj = Generator("blog", "Article", ("title:charfield",))
        generator_obj.core_dir = self.core_folder
        generator_obj.api_dir = self.api_folder
        head, body = generator_obj.get_admin_parts()
        assert ("import Article" in head) is True
        assert ("@admin.register(Article)" in body) is True

    def test_register_models_to_admin(self):
        """
        Tests
        """
        generator_obj = Generator("blog", "Article", ("title:charfield",))
        generator_obj.core_dir = self.core_folder
        generator_obj.api_dir = self.api_folder
        generator_obj.register_models_to_admin()
        with open(f"{self.core_folder}blog/admin.py", 'r+', encoding='utf8') as file:
            body = ''.join(line for line in file.readlines())
        assert ("import Article" in body) is True
        assert ("@admin.register(Article)" in body) is True
        # test when model already registered
        generator_obj = Generator("blog", "Article", ("title:charfield",))
        generator_obj.core_dir = self.core_folder
        generator_obj.api_dir = self.api_folder
        generator_obj.register_models_to_admin()
        with open(f"{self.core_folder}blog/admin.py", 'r+', encoding='utf8') as file:
            body = ''.join(line for line in file.readlines())
        assert body.count('models import Article') == 1
        assert body.count('@admin.register(Article)') == 1

    def test_get_viewset_parts(self):
        """
        Tests
        """
        generator_obj = Generator("blog", "Article", ("title:charfield",))
        generator_obj.core_dir = self.core_folder
        generator_obj.api_dir = self.api_folder
        head, body = generator_obj.get_viewset_parts()
        assert ("import Article" in head) is True
        assert ("class ArticleViewSet" in body) is True

    def test_generate_views(self):
        """
        Tests
        """
        generator_obj = Generator("blog", "Article", ("title:charfield",))
        generator_obj.core_dir = self.core_folder
        generator_obj.api_dir = self.api_folder
        generator_obj.generate_views()
        with open(f"{self.api_folder}blog/views.py", 'r+', encoding='utf8') as file:
            body = ''.join(line for line in file.readlines())
        assert ('import Article' in body) is True
        assert ('ArticleViewSet' in body) is True
        assert ('ArticleSerializer' in body) is True
        # test if view already exists
        generator_obj = Generator("blog", "Article", ("title:charfield",))
        generator_obj.core_dir = self.core_folder
        generator_obj.api_dir = self.api_folder
        generator_obj.generate_views()
        with open(f"{self.api_folder}blog/views.py", 'r+', encoding='utf8') as file:
            body = ''.join(line for line in file.readlines())
        assert body.count('models import Article') == 1
        assert body.count('ArticleViewSet') == 1
        assert body.count('import ArticleSerializer') == 1
        assert body.count('serializer_class = ArticleSerializer') == 1

    def test_get_serializer_parts(self):
        """
        Tests
        """
        generator_obj = Generator("blog", "Article", ("title:charfield",))
        generator_obj.core_dir = self.core_folder
        generator_obj.api_dir = self.api_folder
        head, body = generator_obj.get_serializer_parts()
        assert ("import Article" in head) is True
        assert ("class ArticleSerializer" in body) is True

    def test_generate_serializer(self):
        """
        Tests
        """
        generator_obj = Generator("blog", "Article", ("title:charfield",))
        generator_obj.core_dir = self.core_folder
        generator_obj.api_dir = self.api_folder
        generator_obj.generate_serializers()
        with open(f"{self.api_folder}blog/serializers.py", 'r+', encoding='utf8') as file:
            body = ''.join(line for line in file.readlines())
        assert ('import Article' in body) is True
        assert ('ArticleSerializer' in body) is True
        #test if serializer already exists
        generator_obj = Generator("blog", "Article", ("title:charfield",))
        generator_obj.core_dir = self.core_folder
        generator_obj.api_dir = self.api_folder
        generator_obj.generate_serializers()
        with open(f"{self.api_folder}blog/serializers.py", 'r+', encoding='utf8') as file:
            body = ''.join(line for line in file.readlines())
        assert body.count('import Article') == 1
        assert body.count('ArticleSerializer') == 1

    def test_get_url_parts(self):
        """
        Tests
        """
        generator_obj = Generator("blog", "Article", ("title:charfield",))
        generator_obj.core_dir = self.core_folder
        generator_obj.api_dir = self.api_folder
        head, body = generator_obj.get_url_parts()
        assert ("import ArticleViewSet" in head) is True
        assert (", ArticleViewSet)" in body) is True

    @mock.patch('dr_scaffold.file_api.replace_file_chunk')
    def test_generate_urls(self, mock_replace_chunk):
        """
        Tests
        """
        generator_obj = Generator("blog", "Article", ("title:charfield",))
        generator_obj.core_dir = self.core_folder
        generator_obj.api_dir = self.api_folder
        generator_obj.generate_urls()
        with open(f"{self.api_folder}blog/urls.py", 'r+', encoding='utf8') as file:
            body = ''.join(line for line in file.readlines())
        assert ('import ArticleViewSet' in body) is True
        assert (', ArticleViewSet)' in body) is True
        #test : if url have been added we won't add it again
        generator_obj = Generator("blog", "Article", ("title:charfield",))
        generator_obj.core_dir = self.core_folder
        generator_obj.api_dir = self.api_folder
        generator_obj.generate_urls()
        with open(f"{self.api_folder}blog/urls.py", 'r+', encoding='utf8') as file:
            body = ''.join(line for line in file.readlines())
        assert body.count('import ArticleViewSet') == 1
        assert body.count(', ArticleViewSet)') == 1
        #test : if when creating another resource we replace the url_patterns
        generator_obj = Generator("blog", "Author", ("name:charfield",))
        generator_obj.core_dir = self.core_folder
        generator_obj.api_dir = self.api_folder
        generator_obj.generate_urls()
        mock_replace_chunk.assert_called()

    @mock.patch('dr_scaffold.generators.Generator.generate_api')
    def test_generate_api_called(self, mock_generate_api):
        """
        Tests
        """
        generator_obj = Generator("blog", "Article", ("title:charfield",))
        generator_obj.core_dir = self.core_folder
        generator_obj.api_dir = self.api_folder
        generator_obj.generate_api()
        mock_generate_api.assert_called()

    @mock.patch('dr_scaffold.generators.Generator.run')
    def test_run_called(self, mock_run):
        """
        Tests
        """
        generator_obj = Generator("blog", "Article", ("title:charfield",))
        generator_obj.core_dir = self.core_folder
        generator_obj.api_dir = self.api_folder
        generator_obj.run()
        mock_run.assert_called()

    @mock.patch('dr_scaffold.generators.Generator.setup_files')
    def test_generate_app(self, mock_setup_files):
        """
        Tests
        """
        generator_obj = Generator("blog2", "Article", ("title:charfield",))
        generator_obj.core_dir = self.core_folder
        generator_obj.api_dir = self.api_folder
        generator_obj.generate_app()
        mock_setup_files.assert_called()

    @mock.patch('dr_scaffold.generators.Generator.setup_files')
    def test_generate_app_appdir_exist(self, mock_setup_files):
        """
        Tests
        """
        generator_obj = Generator("blog", "Author", ("name:charfield",))
        generator_obj.core_dir = self.core_folder
        generator_obj.api_dir = self.api_folder
        generator_obj.generate_app()
        mock_setup_files.assert_not_called()
