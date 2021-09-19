# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-arguments
# pylint: disable=too-many-ancestors
"""
Generator module where the real work happens
"""
from os import makedirs, path
from typing import Tuple

import inflect
import isort
from django.conf import settings

from dr_scaffold import file_api, print_off
from dr_scaffold.scaffold_templates import (
    admin_templates,
    app_template,
    factory_templates,
    factory_tests_templates,
    model_templates,
    serializer_templates,
    url_templates,
    view_templates,
)


def pluralize(string):
    """
    pluralizes a string word using a python library, needed for verbose model names and url paths
    """
    pluralizer = inflect.engine()
    return pluralizer.plural(string)


class BaseGenerator:
    """
    Base generator that any other generator class should inherit from
    """

    app_name: str
    model_name: str
    fields: Tuple[str]
    core_dir: str
    api_dir: str
    root_dir: str
    mixins: Tuple[str]
    tests: bool

    def __init__(self, app_name, model_name, fields, mixins, tests):
        self.init_paths_from_settings()
        self.app_name = app_name
        self.model_name = model_name
        self.fields = fields
        self.mixins = mixins
        self.tests = tests
        self.root_dir = "."

    @property
    def core_app_path(self):
        """
        Shortcut for core_dir + app_name
        """
        return self.core_dir + self.app_name

    @property
    def api_app_path(self):
        """
        Shortcut for api_dir + app_name
        """
        return self.api_dir + self.app_name

    @property
    def tests_path(self):
        """
        Shortcut for tests path
        """
        return self.root_dir + "/tests"

    def init_paths_from_settings(self):
        """
        Get folder paths from settings if they exist and add forward slash if forgotten
        """
        self.core_dir = getattr(settings, "CORE_FOLDER", "")
        self.api_dir = getattr(settings, "API_FOLDER", "")
        slashed = self.core_dir.endswith("/") and self.api_dir.endswith("/")
        if len(self.api_dir) > 0 and len(self.core_dir) > 0 and not slashed:
            raise ValueError("🤔 Oops CORE_FOLDER & API_FOLDER should end with a '/'")


class AppGenerator(BaseGenerator):
    """
    APP GENERATION
    1 - first we generate a django app through django's startapp command
    2 - we move the generated app directory to the apps directory if one is
     specified in our CLI command
    3 - we setup the files with the basic imports needed for each component
    4 - if application folder does already exist we return
    """

    def get_file_imports(self):
        """
        Returns all import statements
        """
        imports = [
            serializer_templates.SETUP,
            url_templates.SETUP,
            model_templates.SETUP,
            admin_templates.SETUP,
            view_templates.SETUP,
            app_template.TEMPLATE
            % (
                self.app_name.capitalize(),
                self.core_app_path.replace("/", "."),
            ),
        ]
        if self.tests:
            imports = [factory_templates.SETUP, factory_tests_templates.SETUP] + imports
        return imports

    def get_files(self):
        """
        Files to be generated
        """
        files = [
            f"{self.api_app_path}/serializers.py",
            f"{self.api_app_path}/urls.py",
            f"{self.core_app_path}/models.py",
            f"{self.core_app_path}/admin.py",
            f"{self.api_app_path}/views.py",
            f"{self.core_app_path}/apps.py",
        ]
        if self.tests:
            files = [
                f"{self.tests_path}/core/{self.app_name}/factories.py",
                f"{self.tests_path}/core/{self.app_name}/test_factories.py",
            ] + files
        return files

    def setup_folders(self):
        """
        creates folders if they not exist
        """
        migrations_path = f"{self.core_app_path}/migrations/"
        makedirs(self.api_app_path, exist_ok=True)
        makedirs(self.core_app_path, exist_ok=True)
        makedirs(migrations_path, exist_ok=True)
        if self.tests:
            factories_path = f"{self.tests_path}/core/{self.app_name}/"
            makedirs(factories_path, exist_ok=True)

    def add_setup_imports(self):
        """
        adds the bare minimum imports needed for each file
        """
        for i, file_path in enumerate(self.get_files()):
            file_api.set_file_content(file_path, self.get_file_imports()[i])

    def setup_files(self):
        """
        creates files if not exist, and adds appropriate imports
        """
        files = self.get_files()
        file_api.create_files(files)
        if not path.exists(f"{self.core_app_path}/migrations/__init__.py"):
            file_api.create_file(f"{self.core_app_path}/migrations/__init__.py")
        file_api.wipe_files(files)

    def is_already_generated(self):
        """
        Check if the core app path and the api app path exists already
        """
        return path.exists(self.core_app_path) or path.exists(self.api_app_path)

    def generate_app(self):
        """
        Generates files related to the app
        """
        if not self.is_already_generated():
            self.setup_folders()
            self.setup_files()
            self.add_setup_imports()


class ModelGenerator(BaseGenerator):
    """
    MODELS GENERATION METHODS
    1 - get_fields_string : match fields from cli with their templates and return a
     string of them joined
    2 - get_model_string : yield the fields string in the Model template and returns
     a new Model string
    3 - generate_models: check if the model does already exists in the models.py
     file if not it append it
    """

    def get_fields_string(self):
        """
        get appropriate fields templates based on the field type and return them joined in a string
        """
        actual_fields = []
        relation_types = ("foreignkey", "manytomany", "onetoone")
        file = f"{self.core_app_path}/models.py"
        for field in self.fields:
            field_name = field.split(":")[0]
            field_type = field.split(":")[1].lower()
            field_dict = dict(
                name=field_name,
                related=field.split(":")[2] if (field_type in relation_types) else "",
            )
            if field_type in relation_types:
                # tells developer if related model doesn't exist in file
                chunk = f'class {field_dict["related"]}(models.Model)'
                if not file_api.is_present_in_file(file, chunk):
                    print(
                        "⚠️ \033[93mbare in mind\033[0m that "
                        f"{field_dict['related']} model doesn't exist yet!"
                    )
            field_template = model_templates.FIELD_TYPES[field_type] % field_dict
            actual_fields.append(field_template)
        return "".join(actual_fields)

    def get_model_string(self):
        """
        returns a Model class string with fields and Meta class
        """
        fields_string = self.get_fields_string()
        fields_for_str = " ".join("{self.%s}" % f.split(":")[0] for f in self.fields)
        params = (
            self.model_name,
            fields_string,
            fields_for_str,
            pluralize(self.model_name.lower()).capitalize(),
        )
        return model_templates.MODEL % params

    def generate_models(self):
        """
        Generates models
        """
        file = f"{self.core_app_path}/models.py"
        chunk = f"class {self.model_name}"
        if file_api.is_present_in_file(file, chunk):
            return
        model_string = self.get_model_string()
        file_api.append_file_content(file, model_string)


class AdminGenerator(BaseGenerator):
    """
    MODELS REGISTRATION TO ADMIN
    1 - get_admin_parts : returns the register template and imports of the Model
     class
    2 - register_models_to_admin : check if the model already registered in admin.py
     if not it wraps the admin file content between the Model imports and register
     template
    """

    def get_admin_parts(self):
        """
        returns admin Model register template and import
        """
        app_dir = self.core_app_path
        app_path = app_dir.replace("/", ".")
        model_register_template = admin_templates.REGISTER % {"model": self.model_name}
        model_import_template = admin_templates.MODEL_IMPORT % {
            "app": app_path,
            "model": self.model_name,
        }
        return model_import_template, model_register_template

    def generate_admin(self):
        """
        Generate admin classes
        """
        file = f"{self.core_app_path}/admin.py"
        chunk = f"@admin.register({self.model_name})"
        if file_api.is_present_in_file(file, chunk):
            return
        head, body = self.get_admin_parts()
        file_api.wrap_file_content(file, head, body)


class SerializerGenerator(BaseGenerator):
    """
    SERIALIZER GENERATION
    1 - get_serializer_parts : returns the serializer template and imports of the Model class
    2 - generate_serializers : check if the viewset already exists in serializers.py if not
    it wraps the file content between the imports and the serializer template
    """

    def get_serializer_parts(self):
        """
        returns serializer class template and model import
        """
        app_dir = self.core_app_path
        app_path = app_dir.replace("/", ".")
        serializer_template = serializer_templates.SERIALIZER % {
            "model": self.model_name
        }
        imports = serializer_templates.MODEL_IMPORT % {
            "app": app_path,
            "model": self.model_name,
        }
        return imports, serializer_template

    def generate_serializers(self):
        """Generates serializers classes"""
        serializer_file = f"{self.api_app_path}/serializers.py"
        serializer_head = f"class {self.model_name}Serializer"
        if file_api.is_present_in_file(serializer_file, serializer_head):
            return
        head, body = self.get_serializer_parts()
        file_api.wrap_file_content(serializer_file, head, body)


class ViewGenerator(BaseGenerator):
    """
    VIEWS GENERATION
    1 - get_viewset_parts : returns the viewset template and model + serializers
    imports of the Model class
    2 - generate_views : check if the viewset already exists in views.py if not
    it wraps the file content between the imports and the viewset template
    """

    def get_mixins_template(self):
        """
        returns viewset template matching the mixins based on developer command
        """
        mixins_list = {key: view_templates.CLRUD_MIXINS[key] for key in self.mixins}
        mixins_string = "".join(
            str(mixins_list[x] % {"model": self.model_name}) for x in mixins_list
        )
        actions_list = {key: view_templates.CLRUD_ACTIONS[key] for key in self.mixins}
        actions_string = "".join(
            str(actions_list[x] % {"model": self.model_name}) for x in mixins_list
        )
        return view_templates.CLRUD_VIEWSET % {
            "model": self.model_name,
            "mixins": mixins_string,
            "actions": actions_string,
        }

    def get_viewset_parts(self):
        """
        returns viewsets templates and imports
        """
        core_app_path = self.core_app_path.replace("/", ".")
        api_app_path = self.api_app_path.replace("/", ".")
        viewset_template = view_templates.VIEWSET % {"model": self.model_name}
        if self.mixins:
            viewset_template = self.get_mixins_template()

        model_import_template = view_templates.MODEL_IMPORT % {
            "app": core_app_path,
            "model": self.model_name,
        }
        serializer_import_template = view_templates.SERIALIZER_IMPORT % {
            "app": api_app_path,
            "model": self.model_name,
        }
        imports = model_import_template + serializer_import_template
        return imports, viewset_template

    def generate_views(self):
        """
        Generates views classes
        """
        file = f"{self.api_app_path}/views.py"
        chunk = f"class {self.model_name}ViewSet"
        if file_api.is_present_in_file(file, chunk):
            return
        head, body = self.get_viewset_parts()
        file_api.wrap_file_content(file, head, body)


class FactoryGenerator(BaseGenerator):
    """
    FACTORY GENERATION
    1 - get_factory_parts : returns the factory template and imports of the Model class
    2 - generate_factories : check if the factory already exists in factories.py if not
    it wraps the file content between the imports and the factory template
    """

    def get_factory_parts(self):
        """
        returns serializer class template and model import
        """
        app_dir = self.core_app_path
        app_path = app_dir.replace("/", ".")
        factory_template = factory_templates.FACTORY % {"model": self.model_name}
        imports = factory_templates.MODEL_IMPORT % {
            "app": app_path,
            "model": self.model_name,
        }
        return imports, factory_template

    def generate_factories(self):
        """Generates serializers classes"""
        if not self.tests:
            return
        factory_file = f"{self.tests_path}/core/{self.app_name}/factories.py"
        factory_head = f"class {self.model_name}Factory"
        if file_api.is_present_in_file(factory_file, factory_head):
            return
        head, body = self.get_factory_parts()
        file_api.wrap_file_content(factory_file, head, body)


class FactoryTestGenerator(BaseGenerator):
    """
    FACTORY GENERATION
    1 - get_factory_parts : returns the factory template and imports of the Model class
    2 - generate_factories : check if the factory already exists in factories.py if not
    it wraps the file content between the imports and the factory template
    """

    def get_factory_test_parts(self):
        """
        returns serializer class template and model import
        """
        factory_test_template = factory_tests_templates.FACTORY_TEST % {
            "model_lower": self.model_name.lower(),
            "model": self.model_name,
        }
        imports = factory_tests_templates.MODEL_IMPORT % {
            "model": self.model_name,
        }
        return imports, factory_test_template

    def generate_factories_tests(self):
        """Generates serializers classes"""
        if not self.tests:
            return
        factory_test_file = f"{self.tests_path}/core/{self.app_name}/test_factories.py"
        factory_test_head = f"def test_{self.model_name.lower()}_factory():"
        if file_api.is_present_in_file(factory_test_file, factory_test_head):
            return
        head, body = self.get_factory_test_parts()
        file_api.wrap_file_content(factory_test_file, head, body)


class URLGenerator(BaseGenerator):
    """
    URLS GENERATION
    1 - get_url_parts : returns the url template and model imports of the Model class
    2 - generate_urls : check if the url already exists in urls.py if not
    it wraps the file content between the imports and the url template, before wrapping
    it checks if the file has URL_PATTERS it take it off and append it to the url template
    """

    def get_url_parts(self):
        """
        returns the url template and imports of the Model class
        """
        api_app_dir = self.api_app_path
        api_app_path = api_app_dir.replace("/", ".")
        plural_path = pluralize(self.model_name.lower())
        url_template = url_templates.URL % {
            "model": self.model_name,
            "path": plural_path,
        }
        imports = url_templates.VIEWSET_IMPORT % {
            "app": api_app_path,
            "model": self.model_name,
        }
        return imports, url_template

    def generate_urls(self):
        """
        Generates urls
        """
        file = f"{self.api_app_path}/urls.py"
        chunk = f"{self.model_name}ViewSet)"
        if file_api.is_present_in_file(file, chunk):
            return
        head, body = self.get_url_parts()
        if file_api.is_present_in_file(file, url_templates.URL_PATTERNS):
            file_api.replace_file_chunk(file, url_templates.URL_PATTERNS, "")
        body = body + url_templates.URL_PATTERNS
        file_api.wrap_file_content(file, head, body)


class Generator(
    AppGenerator,
    ModelGenerator,
    AdminGenerator,
    SerializerGenerator,
    ViewGenerator,
    FactoryGenerator,
    FactoryTestGenerator,
    URLGenerator,
):
    """
    A wrapper for CLI command arguments and the REST api different files generation methods
    """

    def __init__(self, app_name, model_name, fields, mixins, tests):
        super().__init__(
            app_name=app_name,
            model_name=model_name,
            fields=fields,
            mixins=mixins,
            tests=tests,
        )

    def run(self):
        """
        runs generate api and throws an exception if something went wrong
        """
        try:
            self.generate()
        except Exception as error:
            return print(f"🤔 \033[93mOops\033[0m something is wrong: {error}")
        return print(
            "🎉 \033[92mSuccess:\033[0m your RESTful "
            f"\033[1m{self.model_name}\033[0m api resource is ready."
        )

    def sort_imports(self):
        """
        Sort file imports using isort
        """
        print("🦄 \033[95mSorting file imports ...\033[0m")
        for file in self.get_files()[:-1]:
            with print_off.HiddenPrints():
                isort.file(file)

    def generate(self):
        """
        Calls the appropriate generator classes in the correct order
        """
        self.generate_app()
        self.generate_models()
        self.generate_admin()
        self.generate_serializers()
        self.generate_views()
        self.generate_factories()
        self.generate_factories_tests()
        self.generate_urls()
        self.sort_imports()
