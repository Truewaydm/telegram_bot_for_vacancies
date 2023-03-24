from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('cities', CityViewSet, basename='cities')
router.register('language', LanguageViewSet, basename='language')
urlpatterns = router.urls