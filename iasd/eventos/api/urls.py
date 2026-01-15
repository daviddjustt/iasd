from django.urls import path, include
from rest_framework.routers import DefaultRouter
from iasd.eventos.api.views import EventoViewSet

# 1. Instancie o router
router = DefaultRouter()

# 2. Registre seus ViewSets
# O 'basename' é importante, especialmente para Proxy Models
router.register("eventos", EventoViewSet)

# 3. Defina o urlpatterns
app_name = "eventos_api" # Nome opcional para namespace

urlpatterns = [
    path('', include(router.urls)),
]