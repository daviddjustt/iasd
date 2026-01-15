from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone

from iasd.eventos.models import Agendamento
from iasd.eventos.api.serializers import AgendamentoSerializer
from iasd.ministerios.models import Ministerio
from .serializers import MinisterioSerializer

class MinisterioViewSet(viewsets.ModelViewSet):
    queryset = Ministerio.objects.all()
    serializer_class = MinisterioSerializer

    @action(detail=True, methods=['get'], url_path='resumo-atividades')
    def resumo_atividades(self, request, pk=None):
        """Retorna estatísticas rápidas e os próximos 3 eventos deste ministério."""
        ministerio = self.get_object()
        hoje = timezone.now().date()
        
        proximos = Agendamento.objects.filter(
            evento__ministerio_responsavel=ministerio,
            data__gte=hoje
        ).order_by('data')[:3]

        total_eventos = ministerio.eventos.count()
        
        return Response({
            "total_eventos_historico": total_eventos,
            "membros_count": ministerio.membros.count(),
            "proximas_atividades": AgendamentoSerializer(proximos, many=True).data
        })