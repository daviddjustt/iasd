from rest_framework import serializers
from iasd.eventos.models import Evento, Agendamento

class AgendamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agendamento
        fields = ['id', 'data', 'horario_inicio', 'horario_final']

class EventoSerializer(serializers.ModelSerializer):
    # Permite enviar uma lista de agendamentos no momento da criação
    agendamentos = AgendamentoSerializer(many=True)

    class Meta:
        model = Evento
        fields = ['id', 'ministerio_responsavel', 'endereco', 'tematica', 'agendamentos']

    def validate(self, data):
        ministerio_atual = data['ministerio_responsavel']
        novos_horarios = data['agendamentos']

        for horario in novos_horarios:
            data_ev = horario['data']
            inicio = horario['horario_inicio']
            fim = horario['horario_final']

            # Busca qualquer agendamento que se sobreponha no mesmo horário e dia
            conflitos = Agendamento.objects.filter(
                data=data_ev,
                horario_inicio__lt=fim,   # Começa antes do novo terminar
                horario_final__gt=inicio   # Termina depois do novo começar
            )

            if conflitos.exists():
                # 1. Verificar se algum conflito é do MESMO ministério
                mesmo_ministerio = conflitos.filter(evento__ministerio_responsavel=ministerio_atual)
                
                if mesmo_ministerio.exists():
                    raise serializers.ValidationError(
                        f"Erro: O ministério {ministerio_atual.nome} já possui um evento "
                        f"neste horário ({data_ev} às {inicio})."
                    )

                # 2. Se chegou aqui, há conflito mas é de MINISTÉRIOS DIFERENTES
                # No Django, para enviar um "aviso" mas ainda salvar, o ideal é que 
                # o Front-end use o endpoint de 'verificar-conflito' antes de postar.
                # Se for um POST forçado, vamos permitir o save, mas poderíamos logar isso.
        
        return data

    def create(self, validated_data):
        agendamentos_data = validated_data.pop('agendamentos')
        evento = Evento.objects.create(**validated_data)
        for agend_info in agendamentos_data:
            Agendamento.objects.create(evento=evento, **agend_info)
        return evento