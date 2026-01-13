from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from iasd.users.models import Membro, Visitante, User
from .serializers import MembroSerializer, VisitanteSerializer, UserBaseSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    View para gerenciar TODOS os usuários (Admin/Staff).
    """
    queryset = User.objects.all()
    serializer_class = UserBaseSerializer
    permission_classes = [IsAuthenticated] # Ajuste conforme sua necessidade

class MembroViewSet(viewsets.ModelViewSet):
    """
    View para gerenciar apenas Membros.
    A QuerySet já filtra automaticamente pelo Proxy Model.
    """
    queryset = Membro.objects.all()
    serializer_class = MembroSerializer
    permission_classes = [IsAuthenticated]

class VisitanteViewSet(viewsets.ModelViewSet):
    """
    View para gerenciar apenas Visitantes.
    """
    queryset = Visitante.objects.all()
    serializer_class = VisitanteSerializer
    permission_classes = [IsAuthenticated]