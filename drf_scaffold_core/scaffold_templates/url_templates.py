URL = """router.register(r'%(path)s', %(model)sViewSet)
"""

MODEL_IMPORT = """from %(app)s.views import %(model)sViewSet
"""

URLS_SETUP = """from rest_framework import routers
from django.urls import include, path

router = routers.DefaultRouter()
"""

URL_PATTERNS = """urlpatterns = [
    path("", include(router.urls)),
]"""