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
TEXTFIELD = """
    %(name)s = models.TextField(null=True, blank=True)"""
INTEGERFIELD = """
    %(name)s = models.IntegerField(null=True, default=0)"""
DECIMALFIELD = """
    %(name)s = models.DecimalField(null=True, default=0.0)"""
DATETIMEFIELD = """
    %(name)s = models.DateTimeField(null=True)"""
FOREIGNKEY = """
    %(name)s = models.ForeignKey(%(foreign)s, on_delete=models.CASCADE, null=True)"""

FIELD_TYPES = {
    'charfield': CHARFIELD,
    'textfield': TEXTFIELD,
    'integerfield':INTEGERFIELD,
    'decimalfield':DECIMALFIELD,
    'datetimefield':DATETIMEFIELD,
    'foreignkey':FOREIGNKEY,
}