"""
apps.py template
"""

TEMPLATE = """from django.apps import AppConfig

class %sConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = '%s'

"""
