"""
templates for models
"""

MODEL = """class %s(models.Model):\
    %s
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"%s"

    class Meta:
        verbose_name_plural = "%s"

"""

MODEL_IMPORT = """from %(app)s.models import %(model)s
"""

CHARFIELD = """
    %(name)s = models.CharField(max_length=255, null=True, blank=True)"""

BIGINTEGERFIELD = """
    %(name)s = models.BigIntegerField(null=True, blank=True)"""

BINARYFIELD = """
    %(name)s = models.BinaryField(null=True, blank=True)"""

BOOLEANFIELD = """
    %(name)s = models.BooleanField(null=True, blank=True)"""

DATEFIELD = """
    %(name)s = models.DateField(null=True, blank=True)"""

FLOATFIELD = """
    %(name)s = models.FloatField(null=True, blank=True)"""

GENERICIPADDRESSFIELD = """
    %(name)s = models.GenericIPAddressField(null=True, blank=True)"""

NULLBOOLEANFIELD = """
    %(name)s = forms.NullBooleanField(null=True, blank=True)"""

POSITIVEINTEGERFIELD = """
    %(name)s = models.PositiveIntegerField(null=True, blank=True)"""

POSITIVESMALLINTEGERFIELD = """
    %(name)s = models.PositiveSmallIntegerField(null=True, blank=True)"""

EMAILFIELD = """
    %(name)s = models.EmailField(max_length=254, null=True, blank=True)"""

SLUGFIELD = """
    %(name)s = models.SlugField(max_length=200, null=True, blank=True)"""

TIMEFIELD = """
    %(name)s = models.TimeField(null=True, blank=True)"""

URLFIELD = """
    %(name)s = models.URLField(max_length=200, null=True, blank=True)"""

SMALLINTEGERFIELD = """
    %(name)s = models.SmallIntegerField(null=True, blank=True)"""

TEXTFIELD = """
    %(name)s = models.TextField(null=True, blank=True)"""

INTEGERFIELD = """
    %(name)s = models.IntegerField(null=True, default=0)"""

DECIMALFIELD = """
    %(name)s = models.DecimalField(max_digits=5, decimal_places=2, null=True, default=0.0)"""

DATETIMEFIELD = """
    %(name)s = models.DateTimeField(null=True, blank=True)"""

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
