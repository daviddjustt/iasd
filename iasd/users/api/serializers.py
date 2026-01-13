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
    Não possui membro_responsavel pois ele É o responsável.
    """
    class Meta(UserBaseSerializer.Meta):
        model = Membro
        # Campos herdados automaticamente da Base
        
    def create(self, validated_data):
        validated_data['role'] = User.Roles.MEMBRO
        return super().create(validated_data)


class VisitanteSerializer(UserBaseSerializer):
    """
    Serializer para Visitantes. 
    Inclui explicitamente o membro responsável.
    """
    nome_responsavel = serializers.CharField(source='membro_responsavel.name', read_only=True)

    class Meta(UserBaseSerializer.Meta):
        model = Visitante
        # Adicionamos os campos de relacionamento que só existem para Visitantes
        fields = UserBaseSerializer.Meta.fields + ['membro_responsavel', 'nome_responsavel']

    def create(self, validated_data):
        validated_data['role'] = User.Roles.VISITANTE
        return super().create(validated_data)