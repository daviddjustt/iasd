from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
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
    queryset = Visitante.objects.all()
    serializer_class = VisitanteSerializer

    # LISTAR: Todos os visitantes vinculados a um membro específico
    # GET /api/v1/visitantes/por_membro/?membro_id=ID
    @action(detail=False, methods=['get'], url_path='por-membro')
    def por_membro(self, request):
        membro_id = request.query_params.get('membro_id')
        if not membro_id:
            return Response({"error": "O campo membro_id é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Filtra os visitantes onde o membro_responsavel é o ID passado
        visitantes = self.queryset.filter(membro_responsavel_id=membro_id)
        serializer = self.get_serializer(visitantes, many=True)
        return Response(serializer.data)

    # VINCULAR / ATUALIZAR EM MASSA (Opcional)
    # POST /api/v1/visitantes/vincular-membro/
    @action(detail=False, methods=['post'], url_path='vincular-membro')
    def vincular_membro(self, request):
        """
        Recebe um ID de membro e uma lista de IDs de visitantes para vincular.
        """
        membro_id = request.data.get('membro_id')
        visitantes_ids = request.data.get('visitantes_ids', []) # Lista de IDs [1, 2, 3]

        if not membro_id or not visitantes_ids:
            return Response({"error": "membro_id e visitantes_ids são obrigatórios."}, status=status.HTTP_400_BAD_REQUEST)

        # Atualiza todos os visitantes da lista de uma vez
        updated_count = Visitante.objects.filter(id__in=visitantes_ids).update(membro_responsavel_id=membro_id)
        
        return Response({
            "message": f"Sucesso! {updated_count} visitantes vinculados ao membro {membro_id}."
        }, status=status.HTTP_200_OK)

