VIEWSET = """class %(model)sViewSet(viewsets.ModelViewSet):
    queryset = %(model)s.objects.all()
    serializer_class = %(model)sSerializer
    
"""

MODEL_IMPORT = """from %(app)s.models import %(model)s
"""

SERIALIZER_IMPORT = """from %(app)s.serializers import %(model)sSerializer
"""

VIEWSET_SETUP = """from rest_framework import viewsets
"""

SETUP = """from rest_framework import viewsets

"""