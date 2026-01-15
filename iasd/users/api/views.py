from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from django.shortcuts import get_object_or_404

from iasd.users.models import Membro, Visitante, User
from .serializers import MembroSerializer, VisitanteSerializer, UserBaseSerializer, VinculacaoMembroSerializer

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
    lookup_field = 'id'  # No Django, o campo padrão costuma ser 'id' mesmo sendo UUID

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='membro_uuid',
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.QUERY,
                description='Insira o UUID do membro para ver seus visitantes vinculados.',
                required=True,
            ),
        ],
        responses={200: VisitanteSerializer(many=True)},
        description="Retorna a lista de visitantes relacionados a um membro específico (Membro, Pastor ou Admin)."
    )
    @action(detail=False, methods=['get'], url_path='vincular-membro')
    def listar_por_membro(self, request):
        membro_uuid = request.query_params.get('membro_uuid')

        if not membro_uuid:
            return Response(
                {"error": "O parâmetro membro_uuid é obrigatório."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validação: Garante que o UUID não pertence a um Visitante
        # .exclude(role='VISITANTE') garante que apenas MEMBRO, PASTOR ou ADMIN passem
        if not User.objects.filter(id=membro_uuid).exclude(role='VISITANTE').exists():
            return Response(
                {"error": "O UUID fornecido não pertence a um responsável válido ou usuário não encontrado."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        visitantes = Visitante.objects.filter(membro_responsavel__id=membro_uuid)
        serializer = self.get_serializer(visitantes, many=True)
        return Response(serializer.data)

    @extend_schema(
        request=VinculacaoMembroSerializer,
        responses={200: VinculacaoMembroSerializer},
        description="Vincula uma lista de visitantes a um membro responsável via UUID."
    )
    @action(detail=False, methods=['patch'], url_path='vincular-membro/atualizar')
    def vincular_membro(self, request):
        serializer = VinculacaoMembroSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        membro_uuid = serializer.validated_data['membro_uuid']
        visitantes_uuids = serializer.validated_data['visitantes_uuids']

        # Busca o membro (O serializer já validou a existência)
        membro = Membro.objects.get(id=membro_uuid)

        # Atualização em massa
        atualizados = Visitante.objects.filter(id__in=visitantes_uuids).update(membro_responsavel=membro)

        return Response({
            "mensagem": f"Sucesso! {atualizados} visitantes vinculados ao membro {membro.name}.",
            "membro_responsavel": {
                "id": membro.id,
                "nome": membro.name
            },
            "vinculados_count": atualizados
        }, status=status.HTTP_200_OK)