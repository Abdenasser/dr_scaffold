from django.db import models

# Create your models here.
class Status(models.Model):    
    name = models.CharField(max_length=255, null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    

class Article(models.Model):    
    title = models.CharField(max_length=255, null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    

