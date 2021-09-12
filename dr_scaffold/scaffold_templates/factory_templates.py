"""
templates for factories
"""

FACTORY = """class %(model)sFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = %(model)s

    def __new__(cls, *args, **kwargs):
        return super().__new__(*args, **kwargs)

"""

MODEL_IMPORT = """from %(app)s.models import %(model)s
"""

SETUP = """import factory

"""
