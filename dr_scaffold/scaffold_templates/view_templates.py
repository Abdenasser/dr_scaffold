"""
templates for views
"""

VIEWSET = """class %(model)sViewSet(viewsets.ModelViewSet):
    queryset = %(model)s.objects.all()
    serializer_class = %(model)sSerializer
    

"""

MODEL_IMPORT = """from %(app)s.models import %(model)s
"""

SERIALIZER_IMPORT = """from %(app)s.serializers import %(model)sSerializer
"""

SETUP = """from rest_framework import viewsets

"""
