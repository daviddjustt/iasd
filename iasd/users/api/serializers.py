from rest_framework import serializers
from django.contrib.auth import get_user_model

# Referencias do código 
from iasd.users.models import Membro, Visitante, User

User = get_user_model()

class UserBaseSerializer(serializers.ModelSerializer):
    """
    Serializer base com campos comuns a todos os usuários.
    """
    class Meta:
        model = User
        fields = [
            'id', 'email', 'name', 'password', 'role',
            'telefone', 'cep', 'rua', 'numero', 'bairro', 
            'cidade', 'complemento', 'redes_sociais',
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class MembroSerializer(UserBaseSerializer):
    """
    Serializer para Membros. 
    EXCLUI explicitamente o campo membro_responsavel.
    Não possui membro_responsavel pois ele É o responsável.
    """
    def validate(self, attrs):
        # Garante que, se por acaso o campo vier no request, ele seja descartado
        attrs.pop('membro_responsavel', None)
        return attrs
    class Meta(UserBaseSerializer.Meta):
        model = Membro
        # Aqui ele herda apenas os campos de UserBaseSerializer.Meta.fields
        # Campos herdados automaticamente da Base
        
    def create(self, validated_data):
        validated_data['role'] = User.Roles.MEMBRO
        return super().create(validated_data)

class VisitanteSerializer(UserBaseSerializer):
    """
    Serializer para Visitantes. 
    INCLUI o campo membro_responsavel e o nome amigável.
    """
    nome_responsavel = serializers.CharField(source='membro_responsavel.name', read_only=True)

    class Meta(UserBaseSerializer.Meta):
        model = Visitante
        # Concatenamos os campos base com os campos de relacionamento
        fields = UserBaseSerializer.Meta.fields + ['membro_responsavel', 'nome_responsavel']

class VinculacaoMembroSerializer(serializers.Serializer):
    """
    Serializer para validar a vinculação em massa de visitantes a um membro.
    """
    membro_uuid = serializers.UUIDField(
        help_text="UUID do membro que será o responsável."
    )
    visitantes_uuids = serializers.ListField(
        child=serializers.UUIDField(),
        min_length=1,
        help_text="Lista de UUIDs dos visitantes a serem vinculados."
    )

    def validate_membro_uuid(self, value):
        if not Membro.objects.filter(id=value).exists():
            raise serializers.ValidationError("Membro não encontrado com o UUID fornecido.")
        return value

    def validate_visitantes_uuids(self, value):
        # Verifica se todos os UUIDs enviados realmente pertencem a Visitantes
        existentes = Visitante.objects.filter(id__in=value).count()
        if existentes != len(value):
            raise serializers.ValidationError("Um ou mais UUIDs de visitantes são inválidos ou não existem.")
        return value
