from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, MembroViewSet, VisitanteViewSet

# 1. Instancie o router
router = DefaultRouter()

# 2. Registre seus ViewSets
# O 'basename' é importante, especialmente para Proxy Models
router.register(r'todos', UserViewSet, basename='user')
router.register(r'membros', MembroViewSet, basename='membro')
router.register(r'visitantes', VisitanteViewSet, basename='visitante')

# 3. Defina o urlpatterns
app_name = "users_api" # Nome opcional para namespace

urlpatterns = [
    path('', include(router.urls)),
]