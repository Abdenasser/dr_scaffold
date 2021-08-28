"""
templates for urls
"""

URL = """router.register(r'%(path)s', %(model)sViewSet)

"""

VIEWSET_IMPORT = """from %(app)s.views import %(model)sViewSet
"""

URL_PATTERNS = """urlpatterns = [
    path("", include(router.urls)),
]"""

SETUP = """from rest_framework import routers
from django.urls import include, path

router = routers.DefaultRouter()

"""
