"""
Tests for Generator
"""
import io
import os
import shutil
import sys
import tempfile
from unittest import TestCase, mock

import pytest
from django.conf import settings

from dr_scaffold.generators import (
    Generator,
    AppGenerator,
    ModelGenerator,
    AdminGenerator,
    ViewGenerator,
    SerializerGenerator,
    URLGenerator,
    pluralize,
)
from dr_scaffold.scaffold_templates import (
    model_templates,
    serializer_templates,
)


class TestGenerator(TestCase):
    """
    Tests for Generator
    """

    test_settings = settings
    tmpdirpath = tempfile.mkdtemp()
    # tmpdirpath = "generated_tests_folder"
    core_folder = f"{tmpdirpath}/{test_settings.CORE_FOLDER}"
    api_folder = f"{tmpdirpath}/{test_settings.API_FOLDER}"

    def setUp(self):
        """
        Tests set up : get executed before each test
        """
        os.makedirs(self.tmpdirpath, exist_ok=True)
        os.makedirs(f"{self.core_folder}blog", exist_ok=True)
        os.makedirs(f"{self.api_folder}blog", exist_ok=True)
        for file_name in [
            f"{self.core_folder}blog/models.py",
            f"{self.api_folder}blog/serializers.py",
            f"{self.core_folder}blog/admin.py",
            f"{self.api_folder}blog/urls.py",
            f"{self.api_folder}blog/views.py",
        ]:
            with open(file_name, "x", encoding="utf8"):
                pass

    def tearDown(self):
        """
        Tests tear down : get executed after each test
        """
        for file_name in [
            f"{self.core_folder}blog/models.py",
            f"{self.api_folder}blog/serializers.py",
            f"{self.core_folder}blog/admin.py",
            f"{self.api_folder}blog/urls.py",
            f"{self.api_folder}blog/views.py",
        ]:
            os.remove(file_name)
        if os.path.exists(self.tmpdirpath):
            shutil.rmtree(self.tmpdirpath)

    @classmethod
    def test_pluralize(cls):
        """
        Test pluralization
        """
        assert pluralize("article") == "articles"
        assert pluralize("category") == "categories"
        assert pluralize("post") == "posts"

    @classmethod
    def test_init(cls):
        """
        Test arguments
        """
        generator_obj = Generator("blog", "Article", "", False)
        assert generator_obj.app_name == "blog"
        assert generator_obj.model_name == "Article"

    def test_add_setup_imports(self):
        """
        Tests imports
        """
        generator_obj = Generator(
            "blog", "Article", ("title:charfield", "body:textfield"), False
        )
        generator_obj.core_folder = self.core_folder
        files = (f"{self.core_folder}blog/models.py",)
        generator_obj.get_files = lambda: files
        generator_obj.get_file_imports = lambda: (serializer_templates.SETUP,)
        generator_obj.add_setup_imports()
        with open(files[0], "r+", encoding="utf8") as file:
            body = "".join(file.readlines())
        assert body == serializer_templates.SETUP

    def test_setup_files(self):
        """
        Tests files setup
        """
        generator_obj = AppGenerator(
            app_name="blog",
            model_name="Article",
            fields=("title:charfield", "body:textfield"),
            mixins=False,
        )
        generator_obj.core_dir = self.core_folder
        generator_obj.api_dir = self.api_folder
        with mock.patch.object(
            AppGenerator, "is_already_generated", return_value=False
        ):
            generator_obj.generate_app()
        core_files = list(os.listdir(f"{self.core_folder}blog/"))
        api_files = list(os.listdir(f"{self.api_folder}blog/"))
        with open(f"{self.core_folder}blog/models.py", "r+", encoding="utf8") as file:
            body = "".join(file.readlines())
        assert len(core_files + api_files) == 7  # taking in count migrations folder
        assert ("from django.db import models" in body) is True

    @classmethod
    @mock.patch("dr_scaffold.generators.file_api.is_present_in_file")
    def test_get_fields_string(cls, mock_is_in_file):
        """
        Tests
        """
        generator_obj = Generator(
            "blog", "Article", ("title:charfield", "body:textfield"), False
        )
        fields_string = generator_obj.get_fields_string()
        body_template = model_templates.TEXTFIELD % dict(name="body")
        title_template = model_templates.CHARFIELD % dict(name="title")
        string = title_template + body_template
        assert fields_string == string
        # test relation field type
        generator_obj2 = Generator(
            "blog", "Article", ("author:foreignkey:Author",), False
        )
        generator_obj2.get_fields_string()
        mock_is_in_file.assert_called_once()

    def test_get_fields_string_relation_model_not_created_yet(self):
        """
        Tests
        """
        generator_obj2 = Generator(
            "blog", "Article", ("author:foreignkey:Author",), False
        )
        generator_obj2.core_dir = self.core_folder
        generator_obj2.api_dir = self.api_folder
        captured_output = io.StringIO()
        sys.stdout = captured_output
        generator_obj2.get_fields_string()
        sys.stdout = sys.__stdout__
        assert "⚠️ bare in mind that Author" in captured_output.getvalue()

    @classmethod
    def test_get_model_string(cls):
        """
        Tests
        """
        generator_obj = Generator(
            "blog", "Article", ("title:charfield", "body:textfield"), False
        )
        fields_string = generator_obj.get_fields_string()
        model_string = generator_obj.get_model_string()
        string = model_templates.MODEL % ("Article", fields_string, "Articles")
        assert model_string == string

    def test_run(self):
        """
        Tests
        """
        generator_obj = Generator(
            "blog", "Article", ("title:charfield", "body:textfield"), False
        )
        generator_obj.core_dir = self.core_folder
        generator_obj.api_dir = self.api_folder
        result = generator_obj.run()
        assert result == print("🎉 Your RESTful Article api resource is ready 🎉")
        # test case where something is wrong
        generator_obj2 = Generator("blog", "Author", ("title:charfiel",), False)
        generator_obj2.core_dir = self.core_folder
        generator_obj2.api_dir = self.api_folder
        result = generator_obj2.run()
        assert result == print("🤔 Oops something is wrong: charfiel")

    @mock.patch("dr_scaffold.generators.Generator.generate_app")
    def test_generate_api(self, mock_generate_app):
        """
        Tests
        """
        generator_obj = Generator(
            "blog", "Article", ("title:charfield", "body:textfield"), False
        )
        generator_obj.core_dir = self.core_folder
        generator_obj.api_dir = self.api_folder
        generator_obj.generate()
        mock_generate_app.assert_called_once()

    def test_generate_models(self):
        """
        Tests
        """
        generator_obj = ModelGenerator(
            app_name="blog",
            model_name="Article",
            fields=("title:charfield", "body:textfield"),
            mixins=False,
        )
        generator_obj.core_dir = self.core_folder
        generator_obj.api_dir = self.api_folder
        generator_obj.generate_models()
        with open(f"{self.core_folder}blog/models.py", "r+", encoding="utf8") as file:
            body = "".join(line for line in file.readlines())
        assert ("Article" in body) is True
        assert ("Articles" in body) is True
        assert ("title" in body) is True
        assert ("body" in body) is True
        # test when model already generated
        generator_obj = ModelGenerator(
            app_name="blog",
            model_name="Article",
            fields=("title:charfield", "body:textfield"),
            mixins=False,
        )
        generator_obj.core_dir = self.core_folder
        generator_obj.api_dir = self.api_folder
        generator_obj.generate_models()
        assert body.count("class Article") == 1
        assert body.count("class Meta:") == 1

    def test_get_admin_parts(self):
        """
        Tests
        """
        generator_obj = Generator("blog", "Article", ("title:charfield",), ["C", "R"])
        generator_obj.core_dir = self.core_folder
        generator_obj.api_dir = self.api_folder
        head, body = generator_obj.get_admin_parts()
        assert ("import Article" in head) is True
        assert ("@admin.register(Article)" in body) is True

    def test_register_models_to_admin(self):
        """
        Tests
        """
        generator_obj = AdminGenerator(
            app_name="blog",
            model_name="Article",
            fields=("title:charfield",),
            mixins=False,
        )
        generator_obj.core_dir = self.core_folder
        generator_obj.api_dir = self.api_folder
        generator_obj.generate_admin()
        with open(f"{self.core_folder}blog/admin.py", "r+", encoding="utf8") as file:
            body = "".join(file.readlines())
        assert ("import Article" in body) is True
        assert ("@admin.register(Article)" in body) is True
        # test when model already registered
        generator_obj = AdminGenerator(
            app_name="blog",
            model_name="Article",
            fields=("title:charfield",),
            mixins=False,
        )
        generator_obj.core_dir = self.core_folder
        generator_obj.api_dir = self.api_folder
        generator_obj.generate_admin()
        with open(f"{self.core_folder}blog/admin.py", "r+", encoding="utf8") as file:
            body = "".join(file.readlines())
        assert body.count("models import Article") == 1
        assert body.count("@admin.register(Article)") == 1

    def test_get_viewset_parts(self):
        """
        Tests
        """
        generator_obj = Generator("blog", "Article", ("title:charfield",), False)
        generator_obj.core_dir = self.core_folder
        generator_obj.api_dir = self.api_folder
        head, body = generator_obj.get_viewset_parts()
        assert ("import Article" in head) is True
        assert ("class ArticleViewSet" in body) is True

    def test_generate_views(self):
        """
        Tests
        """
        generator_obj = ViewGenerator(
            app_name="blog",
            model_name="Article",
            fields=("title:charfield",),
            mixins=False,
        )
        generator_obj.core_dir = self.core_folder
        generator_obj.api_dir = self.api_folder
        generator_obj.generate_views()
        with open(f"{self.api_folder}blog/views.py", "r+", encoding="utf8") as file:
            body = "".join(file.readlines())
        assert ("import Article" in body) is True
        assert ("ArticleViewSet" in body) is True
        assert ("ArticleSerializer" in body) is True
        # test if view already exists
        generator_obj = ViewGenerator(
            app_name="blog",
            model_name="Article",
            fields=("title:charfield",),
            mixins=False,
        )
        generator_obj.core_dir = self.core_folder
        generator_obj.api_dir = self.api_folder
        generator_obj.generate_views()
        with open(f"{self.api_folder}blog/views.py", "r+", encoding="utf8") as file:
            body = "".join(file.readlines())
        assert body.count("models import Article") == 1
        assert body.count("ArticleViewSet") == 1
        assert body.count("import ArticleSerializer") == 1
        assert body.count("serializer_class = ArticleSerializer") == 1

    def test_generate_views_with_mixins(self):
        """
        Tests
        """
        generator_obj = ViewGenerator(
            app_name="blog",
            model_name="Article",
            fields=("title:charfield",),
            mixins=["C", "R"],
        )
        generator_obj.core_dir = self.core_folder
        generator_obj.api_dir = self.api_folder
        generator_obj.generate_views()
        with open(f"{self.api_folder}blog/views.py", "r+", encoding="utf8") as file:
            body = "".join(file.readlines())
        assert ("import Article" in body) is True
        assert ("ArticleViewSet" in body) is True
        assert ("def create" in body) is True
        assert ("def retrieve" in body) is True
        assert ("def update" in body) is not True

    def test_get_serializer_parts(self):
        """
        Tests
        """
        generator_obj = SerializerGenerator(
            app_name="blog",
            model_name="Article",
            fields=("title:charfield",),
            mixins=False,
        )
        generator_obj.core_dir = self.core_folder
        generator_obj.api_dir = self.api_folder
        head, body = generator_obj.get_serializer_parts()
        assert ("import Article" in head) is True
        assert ("class ArticleSerializer" in body) is True

    def test_generate_serializer(self):
        """
        Tests
        """
        generator_obj = SerializerGenerator(
            app_name="blog",
            model_name="Article",
            fields=("title:charfield",),
            mixins=False,
        )
        generator_obj.core_dir = self.core_folder
        generator_obj.api_dir = self.api_folder
        generator_obj.generate_serializers()
        with open(
            f"{self.api_folder}blog/serializers.py", "r+", encoding="utf8"
        ) as file:
            body = "".join(file.readlines())
        assert ("import Article" in body) is True
        assert ("ArticleSerializer" in body) is True
        # test if serializer already exists
        generator_obj = SerializerGenerator(
            app_name="blog",
            model_name="Article",
            fields=("title:charfield",),
            mixins=False,
        )
        generator_obj.core_dir = self.core_folder
        generator_obj.api_dir = self.api_folder
        generator_obj.generate_serializers()
        with open(
            f"{self.api_folder}blog/serializers.py", "r+", encoding="utf8"
        ) as file:
            body = "".join(file.readlines())
        assert body.count("import Article") == 1
        assert body.count("ArticleSerializer") == 1

    def test_get_url_parts(self):
        """
        Tests
        """
        generator_obj = URLGenerator(
            app_name="blog",
            model_name="Article",
            fields=("title:charfield",),
            mixins=False,
        )
        generator_obj.core_dir = self.core_folder
        generator_obj.api_dir = self.api_folder
        head, body = generator_obj.get_url_parts()
        assert ("import ArticleViewSet" in head) is True
        assert (", ArticleViewSet)" in body) is True

    @mock.patch("dr_scaffold.generators.file_api.replace_file_chunk")
    def test_generate_urls(self, mock_replace_chunk):
        """
        Tests
        """
        generator_obj = URLGenerator(
            app_name="blog",
            model_name="Article",
            fields=("title:charfield",),
            mixins=False,
        )
        generator_obj.core_dir = self.core_folder
        generator_obj.api_dir = self.api_folder
        generator_obj.generate_urls()
        with open(f"{self.api_folder}blog/urls.py", "r+", encoding="utf8") as file:
            body = "".join(file.readlines())
        assert ("import ArticleViewSet" in body) is True
        assert (", ArticleViewSet)" in body) is True
        # test : if url have been added we won't add it again
        generator_obj = URLGenerator(
            app_name="blog",
            model_name="Article",
            fields=("title:charfield",),
            mixins=False,
        )
        generator_obj.core_dir = self.core_folder
        generator_obj.api_dir = self.api_folder
        generator_obj.generate_urls()
        with open(f"{self.api_folder}blog/urls.py", "r+", encoding="utf8") as file:
            body = "".join(file.readlines())
        assert body.count("import ArticleViewSet") == 1
        assert body.count(", ArticleViewSet)") == 1
        # test : if when creating another resource we replace the url_patterns
        generator_obj = URLGenerator(
            app_name="blog",
            model_name="Author",
            fields=("name:charfield",),
            mixins=False,
        )
        generator_obj.core_dir = self.core_folder
        generator_obj.api_dir = self.api_folder
        generator_obj.generate_urls()
        mock_replace_chunk.assert_called()

    @mock.patch("dr_scaffold.generators.Generator.generate")
    def test_generate_called(self, mock_generate):
        """
        Tests
        """
        generator_obj = Generator("blog", "Article", ("title:charfield",), False)
        generator_obj.core_dir = self.core_folder
        generator_obj.api_dir = self.api_folder
        generator_obj.run()
        mock_generate.assert_called()

    def test_generate_app(self):
        """
        Tests
        """
        generator_obj = AppGenerator(
            app_name="blog2",
            model_name="Article",
            fields=("title:charfield",),
            mixins=False,
        )
        generator_obj.core_dir = self.core_folder
        generator_obj.api_dir = self.api_folder
        setup_files_backup = generator_obj.setup_files
        with mock.patch.object(
            AppGenerator, "is_already_generated", return_value=False
        ):
            with mock.patch(
                "dr_scaffold.generators.AppGenerator.setup_files"
            ) as mocked:
                mocked.side_effect = setup_files_backup
                generator_obj.generate_app()
                mocked.assert_called()

    @mock.patch("dr_scaffold.generators.Generator.setup_files")
    def test_generate_app_appdir_exist(self, mock_setup_files):
        """
        Tests
        """
        generator_obj = Generator("blog", "Author", ("name:charfield",), False)
        generator_obj.core_dir = self.core_folder
        generator_obj.api_dir = self.api_folder
        generator_obj.generate()
        mock_setup_files.assert_not_called()

    def test_get_folder_settings_not_set(self):
        """
        if no settings folder paths exists
        """
        delattr(self.test_settings, "CORE_FOLDER")
        delattr(self.test_settings, "API_FOLDER")
        generator = Generator("blog", "Author", ("name:charfield",), False)
        assert generator.core_dir == ""
        assert generator.api_dir == ""

    def test_get_folder_settings_without_forward_slash(self):
        """
        test add forward slash if forgotten
        """
        # overwriting settings for test
        setattr(self.test_settings, "CORE_FOLDER", "core")
        setattr(self.test_settings, "API_FOLDER", "api")
        with pytest.raises(ValueError, match=r".* should end with .*"):
            Generator("blog", "Author", ("name:charfield",), False)
        # settings to normal
        setattr(self.test_settings, "CORE_FOLDER", "my_app_core/")
        setattr(self.test_settings, "API_FOLDER", "my_app_api/")

    def test_get_folder_settings_with_forward_slash(self):
        """
        if settings are well set
        """
        setattr(self.test_settings, "CORE_FOLDER", "core/")
        setattr(self.test_settings, "API_FOLDER", "api/")
        generator_obj = Generator("blog", "Author", ("name:charfield",), False)
        assert generator_obj.core_dir == "core/"
        assert generator_obj.api_dir == "api/"
