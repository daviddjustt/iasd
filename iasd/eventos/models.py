import uuid
from django.db import models
from iasd.ministerios.models import Ministerio

class Evento(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ministerio_responsavel = models.ForeignKey(
        Ministerio, 
        on_delete=models.CASCADE, 
        related_name='eventos'
    )
    endereco = models.CharField(max_length=255)
    tematica = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.tematica} - {self.ministerio_responsavel.nome}"

class Agendamento(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    evento = models.ForeignKey( # Mudamos de OneToOne para ForeignKey
        Evento, 
        on_delete=models.CASCADE, 
        related_name='agendamentos' # No plural agora
    )
    data = models.DateField()
    horario_inicio = models.TimeField()
    horario_final = models.TimeField()

    class Meta:
        ordering = ['data', 'horario_inicio']
