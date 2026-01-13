
from typing import ClassVar

import uuid

from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.db.models import EmailField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db import models

from django.core.validators import RegexValidator

from .managers import UserManager


# 1. Mixin para Endereço e Contato (Reutilizável e Organizado)
class AddressContactMixin(models.Model):
    telefone = models.CharField(
        max_length=16,
        validators=[
            RegexValidator(
                regex=r'^\(\d{2}\)\s\d\s\d{4}-\d{4}$',
                message="Telefone deve estar no formato (00) 0 0000-0000"
            )
        ],
        verbose_name='Telefone',
        help_text="Formato esperado: (00) 0 0000-0000",
        blank=True, null=True
    )
    cep = models.CharField(
        max_length=9,
        validators=[RegexValidator(regex=r'^\d{5}-?\d{3}$', message="CEP deve estar no formato XXXXX-XXX")],
        verbose_name="CEP",
        blank=True, null=True
    )
    rua = models.CharField(max_length=200, verbose_name="Logradouro", blank=True)
    numero = models.CharField(max_length=20, verbose_name="Número", blank=True)
    bairro = models.CharField(max_length=100, verbose_name="Bairro", blank=True)
    cidade = models.CharField(max_length=100, verbose_name="Cidade", blank=True)
    complemento = models.CharField(max_length=200, blank=True, null=True, verbose_name="Complemento")
    redes_sociais = models.CharField(max_length=200, verbose_name="Redes sociais", blank=True)

    class Meta:
        abstract = True

    @property
    def telefone_formatado(self):
        if not self.telefone:
            return ""
        t = self.telefone
        # Simples proteção contra index error se o telefone estiver mal formatado no banco
        if len(t) >= 11: 
             return f"({t[0:2]}) {t[2]} {t[3:7]}-{t[7:11]}"
        return t

# 2. Modelo de Usuário Unificado
class User(AbstractUser, AddressContactMixin):
    """
    Default custom user model for iasd.
    Armazena tanto Membros quanto Visitantes.
    """
    
    class Roles(models.TextChoices):
        ADMINISTRADOR = "ADMIN", _("Administrador")
        MEMBRO = "MEMBRO", _("Membro")
        VISITANTE = "VISITANTE", _("Visitante")
        EMPREGADO = "EMPREGADO", _("Empregado")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Campo 'name' para substituir first/last name se desejar
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  
    last_name = None  
    email = models.EmailField(_("email address"), unique=True)

    # Definição do Papel (Role)
    role = models.CharField(
        max_length=20, 
        choices=Roles.choices, 
        default=Roles.MEMBRO,
        verbose_name=_("Tipo de Usuário")
    )

    # Relacionamento: Visitante -> Membro
    # Um usuário (visitante) pode ter sido trazido por outro usuário (membro)
    membro_responsavel = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='visitantes_trazidos',
        verbose_name=_("Membro Responsável / Contato"),
        limit_choices_to={'role': Roles.MEMBRO} # Só permite selecionar quem é membro
    )
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_("Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."),
        null=True, # Permite que o banco aceite nulo
        blank=True, # Permite que formulários aceitem vazio
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects: ClassVar[UserManager] = UserManager()

    def get_absolute_url(self) -> str:
        return reverse("users:detail", kwargs={"pk": self.id})

    def is_membro(self):
        return self.role == self.Roles.MEMBRO

    def is_visitante(self):
        return self.role == self.Roles.VISITANTE


# 3. Modelos Proxy (Opcional, mas útil para organização)
# Eles permitem tratar Visitante e Membro como classes diferentes no código,
# mas salvam na mesma tabela 'User'.

class VisitanteManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role=User.Roles.VISITANTE)

class Visitante(User):
    objects = VisitanteManager()

    class Meta:
        proxy = True
        verbose_name = "Visitante"
        verbose_name_plural = "Visitantes"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = User.Roles.VISITANTE
        super().save(*args, **kwargs)


class MembroManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role=User.Roles.MEMBRO)

class Membro(User):
    objects = MembroManager()

    class Meta:
        proxy = True
        verbose_name = "Membro"
        verbose_name_plural = "Membros"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = User.Roles.MEMBRO
        super().save(*args, **kwargs)