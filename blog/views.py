from blog.models import Article
from blog.serializers import ArticleSerializer
from blog.models import Status
from blog.serializers import StatusSerializer
from rest_framework import viewsets
from django.shortcuts import render

# Create your views here.

class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

