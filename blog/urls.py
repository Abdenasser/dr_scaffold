from blog.views import ArticleViewSet
from blog.views import StatusViewSet
from rest_framework import routers
from django.urls import include, path

router = routers.DefaultRouter()

router.register(r'statuses', StatusViewSet)

router.register(r'articlees', ArticleViewSet)
urlpatterns = [
    path("", include(router.urls)),
]
