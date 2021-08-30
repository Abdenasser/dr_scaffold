"""
templates for views
"""

VIEWSET = """class %(model)sViewSet(viewsets.ModelViewSet):
    queryset = %(model)s.objects.all()
    serializer_class = %(model)sSerializer


"""


FULL_VIEWSET = """class %(model)sViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
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

    def create(self, request, *args, **kwargs):
        serializer = %(model)sSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = %(model)sSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = %(model)sSerializer(instance=instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = %(model)sSerializer(instance=instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request=request, *args, **kwargs)


"""

MODEL_IMPORT = """from %(app)s.models import %(model)s
"""

SERIALIZER_IMPORT = """from %(app)s.serializers import %(model)sSerializer
"""

SETUP = """from rest_framework import viewsets

"""

FULL_SETUP = """from rest_framework import mixins, permissions
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

"""
