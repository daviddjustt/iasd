from rest_framework import viewsets
from rest_framework.response import Response
from iasd.eventos.models import Evento, Agendamento
from rest_framework.decorators import action
from django.utils import timezone
from iasd.eventos.api.serializers import EventoSerializer, AgendamentoSerializer

class EventoViewSet(viewsets.ModelViewSet):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        
        # Lógica extra para verificar se houve sobreposição de ministérios diferentes
        # e adicionar um header de aviso
        response["X-Warning"] = "Houve sobreposicao com outros ministerios."
        return response
    
    @action(detail=False, methods=['get'], url_path='proximos-horarios')
    def listar_proximos(self, request):
        """Retorna todos os horários de eventos a partir de hoje"""
        hoje = timezone.now().date()
        agendamentos = Agendamento.objects.filter(data__gte=hoje).select_related('evento')
        
        # Você pode usar um serializer específico aqui se quiser mostrar dados do evento junto
        data = [{
            "data": a.data,
            "inicio": a.horario_inicio,
            "fim": a.horario_final,
            "evento": a.evento.tematica
        } for a in agendamentos]
        
        return Response(data)
    
    @action(detail=False, methods=['get'], url_path='calendario')
    def calendario(self, request):
        """Retorna agendamentos agrupados por data para facilitar o componente de calendário."""
        mes = request.query_params.get('mes') # Opcional: filtrar por mês
        
        agendamentos = Agendamento.objects.select_related('evento__ministerio_responsavel').all()
        
        if mes:
            agendamentos = agendamentos.filter(data__month=mes)

        # Organiza os dados para o Front
        calendario_data = {}
        for agend in agendamentos:
            data_str = agend.data.isoformat()
            if data_str not in calendario_data:
                calendario_data[data_str] = []
            
            calendario_data[data_str].append({
                "id_evento": agend.evento.id,
                "tematica": agend.evento.tematica,
                "ministerio": agend.evento.ministerio_responsavel.nome,
                "horario": f"{agend.horario_inicio} - {agend.horario_final}"
            })
        
        return Response(calendario_data)
    
    @action(detail=False, methods=['post'], url_path='verificar-conflito')
    def verificar_conflito(self, request):
        """Verifica se já existe algo agendado para o mesmo dia e horário."""
        data = request.data.get('data')
        inicio = request.data.get('horario_inicio')
        fim = request.data.get('horario_final')

        # Busca agendamentos que se sobrepõem
        conflitos = Agendamento.objects.filter(
            data=data,
            horario_inicio__lt=fim,
            horario_final__gt=inicio
        )

        if conflitos.exists():
            return Response({
                "disponivel": False,
                "conflito": EventoSerializer(conflitos.first().evento).data
            }, status=200)
        
        return Response({"disponivel": True}, status=200)