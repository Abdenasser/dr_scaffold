"""
templates for models
"""

MODEL = """class %s(models.Model):\
    %s
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "%s"


"""

MODEL_IMPORT = """from %(app)s.models import %(model)s
"""

CHARFIELD = """
    %(name)s = models.CharField(max_length=255, null=True, blank=True)"""

BIGINTEGERFIELD = """
    %(name)s = models.BigIntegerField()"""

BINARYFIELD = """
    %(name)s = models.BinaryField()"""

BOOLEANFIELD = """
    %(name)s = models.BooleanField()"""

DATEFIELD = """
    %(name)s = models.DateField()"""

FLOATFIELD = """
    %(name)s = models.FloatField()"""

GENERICIPADDRESSFIELD = """
    %(name)s = models.GenericIPAddressField()"""

NULLBOOLEANFIELD = """
    %(name)s = forms.NullBooleanField()"""

POSITIVEINTEGERFIELD = """
    %(name)s = models.PositiveIntegerField()"""

POSITIVESMALLINTEGERFIELD = """
    %(name)s = models.PositiveSmallIntegerField()"""

EMAILFIELD = """
    %(name)s = models.EmailField(max_length=254)"""

SLUGFIELD = """
    %(name)s = models.SlugField(max_length=200)"""

TIMEFIELD = """
    %(name)s = models.TimeField()"""

URLFIELD = """
    %(name)s = models.URLField(max_length=200)"""

SMALLINTEGERFIELD = """
    %(name)s = models.SmallIntegerField()"""

TEXTFIELD = """
    %(name)s = models.TextField(null=True, blank=True)"""

INTEGERFIELD = """
    %(name)s = models.IntegerField(null=True, default=0)"""

DECIMALFIELD = """
    %(name)s = models.DecimalField(max_digits=5, decimal_places=2, null=True, default=0.0)"""

DATETIMEFIELD = """
    %(name)s = models.DateTimeField(null=True)"""

FOREIGNKEY = """
    %(name)s = models.ForeignKey(%(related)s, on_delete=models.CASCADE, null=True)"""

MANYTOMANY = """
    %(name)s = models.ManyToManyField(%(related)s)"""

ONETOONE = """
    %(name)s = models.OneToOneField(%(related)s, on_delete = models.CASCADE, primary_key = True)"""

FIELD_TYPES = {
    "charfield": CHARFIELD,
    "textfield": TEXTFIELD,
    "integerfield": INTEGERFIELD,
    "decimalfield": DECIMALFIELD,
    "datetimefield": DATETIMEFIELD,
    "foreignkey": FOREIGNKEY,
    "bigintegerfield": BIGINTEGERFIELD,
    "binaryfield": BINARYFIELD,
    "booleanfield": BOOLEANFIELD,
    "datefield": DATEFIELD,
    "floatfield": FLOATFIELD,
    "genericipaddressfield": GENERICIPADDRESSFIELD,
    "nullbooleanfield": NULLBOOLEANFIELD,
    "positiveintegerfield": POSITIVEINTEGERFIELD,
    "positivesmallintegerfield": POSITIVESMALLINTEGERFIELD,
    "emailfield": EMAILFIELD,
    "slugfield": SLUGFIELD,
    "timefield": TIMEFIELD,
    "urlfield": URLFIELD,
    "smallintegerfield": SMALLINTEGERFIELD,
    "manytomany": MANYTOMANY,
    "onetoone": ONETOONE,
}

SETUP = """from django.db import models

"""
