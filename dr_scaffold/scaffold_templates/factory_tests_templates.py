"""
templates for factories
"""

FACTORY_TEST = """@pytest.mark.django_db
def test_%(model_lower)s_factory():
    instance = %(model)sFactory()
    assert instance.id

"""

MODEL_IMPORT = """from factories import %(model)sFactory
"""

SETUP = """import pytest

"""
