from rest_framework import routers
from logic.api.viewsets.file import FileViewSet
from logic.api.viewsets.base64 import Base64ViewSet

router = routers.DefaultRouter()

router.register(r'file', FileViewSet, basename='File')
router.register(r'base64', Base64ViewSet, basename='Base64')

urlpatterns = router.urls
