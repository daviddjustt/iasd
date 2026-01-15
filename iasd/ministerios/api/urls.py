from django.urls import path, include
from rest_framework.routers import DefaultRouter
from iasd.ministerios.api.views import MinisterioViewSet

# 1. Instancie o router
router = DefaultRouter()

# 2. Registre seus ViewSets
# O 'basename' é importante, especialmente para Proxy Models
router.register("ministerios", MinisterioViewSet)

# 3. Defina o urlpatterns
app_name = "ministerios_api" # Nome opcional para namespace

urlpatterns = [
    path('', include(router.urls)),
]