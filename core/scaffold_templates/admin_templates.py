REGISTER = """@admin.register(%s)\
class %sAdmin(admin.ModelAdmin):
    exclude = ()
    
"""
MODEL_IMPORT = """from %(app)s.models import %(model)s
"""