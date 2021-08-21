from blog.models import Article
from blog.models import Status
from django.contrib import admin

# Register your models here.
@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    exclude = ()
    

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    exclude = ()
    

