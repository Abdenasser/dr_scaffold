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

SETUP = """from rest_framework import mixins, permissions, viewsets
from rest_framework.response import Response

"""


CLRUD_MIXINS = {
    "C": """    mixins.CreateModelMixin,\n""",
    "R": """    mixins.ListModelMixin,\n    mixins.RetrieveModelMixin,\n""",
    "U": """    mixins.UpdateModelMixin,\n""",
    "D": """    mixins.DestroyModelMixin,\n""",
}

CLRUD_ACTIONS = {
    "C": """    def create(self, request, *args, **kwargs):
        serializer = %(model)sSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)\n\n""",
    "R": """    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = %(model)sSerializer(queryset, many=True)
        return Response(serializer.data)\n\n    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = %(model)sSerializer(instance=instance)
        return Response(serializer.data)\n\n""",
    "U": """    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = %(model)sSerializer(instance=instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)\n\n""",
    "D": """    def destroy(self, request, *args, **kwargs):
        return super().destroy(request=request, *args, **kwargs)\n\n""",
}

CLRUD_VIEWSET = """class %(model)sViewSet(
%(mixins)s\tviewsets.GenericViewSet
):
    queryset = %(model)s.objects.all()
    serializer_class = %(model)sSerializer
    #permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        #user = self.request.user
        queryset = %(model)s.objects.all()
        #insert specific queryset logic here
        return queryset

    def get_object(self):
        #insert specific get_object logic here
        return super().get_object()

%(actions)s
"""
