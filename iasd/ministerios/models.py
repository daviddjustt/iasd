
from django.db import models
import uuid
from django.db import models
from iasd.users.models import Membro

class Ministerio(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=100)
    lider = models.ForeignKey(
        Membro, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='ministerios_liderados'
    )
    # Substitui a tabela 'Membros_associados' do seu diagrama
    membros = models.ManyToManyField(
        Membro, 
        related_name='ministerios',
        blank=True
    )

    def __str__(self):
        return self.nome