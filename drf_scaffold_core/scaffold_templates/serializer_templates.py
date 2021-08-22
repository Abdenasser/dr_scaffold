SERIALIZER = """class %(model)sSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = %(model)s
        fields = '__all__'
        
"""

MODEL_IMPORT = """from %(app)s.models import %(model)s
"""

SERIALIZER_SETUP = """from rest_framework import serializers
"""

SETUP="""from rest_framework import serializers

"""