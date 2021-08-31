"""
templates for admin
"""

REGISTER = """@admin.register(%(model)s)
class %(model)sAdmin(admin.ModelAdmin):
    exclude = ()

"""
MODEL_IMPORT = """from %(app)s.models import %(model)s
"""

SETUP = """from django.contrib import admin

"""
