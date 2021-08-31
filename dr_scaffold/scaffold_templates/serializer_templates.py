"""
templates for serializers
"""

SERIALIZER = """class %(model)sSerializer(serializers.ModelSerializer):
    class Meta:
        model = %(model)s
        fields = '__all__'


"""

MODEL_IMPORT = """from %(app)s.models import %(model)s
"""

SETUP = """from rest_framework import serializers

"""
