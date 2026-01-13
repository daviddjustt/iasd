from rest_framework import serializers
from django.contrib.auth import get_user_model

# Referencias do código 
from iasd.users.models import Membro, Visitante, User

User = get_user_model()

class UserBaseSerializer(serializers.ModelSerializer):
    """
    Serializer base para lidar com campos comuns e segurança da senha.
    """
    class Meta:
        model = User
        fields = [
            'id', 'email', 'name', 'password', 'role',
            'telefone', 'cep', 'rua', 'numero', 'bairro', 
            'cidade', 'complemento', 'redes_sociais',
            'membro_responsavel'
        ]
        # A senha deve ser write_only (não aparece no GET)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Interceptamos a criação para garantir que a senha seja criptografada
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        # Atualização segura de senha, caso seja enviada
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class MembroSerializer(UserBaseSerializer):
    """
    Serializer específico para Membros.
    Força o role para MEMBRO automaticamente na validação.
    """
    class Meta(UserBaseSerializer.Meta):
        model = Membro
        # Podemos remover campos que membro não usa, se houver
        
    def create(self, validated_data):
        # Garante que, ao criar por essa rota, seja sempre MEMBRO
        validated_data['role'] = User.Roles.MEMBRO
        return super().create(validated_data)


class VisitanteSerializer(UserBaseSerializer):
    """
    Serializer específico para Visitantes.
    """
    # Campo calculado para exibir o nome do membro responsável de forma amigável
    nome_responsavel = serializers.CharField(source='membro_responsavel.name', read_only=True)

    class Meta(UserBaseSerializer.Meta):
        model = Visitante
        # Adiciona o campo extra na lista de campos
        fields = UserBaseSerializer.Meta.fields + ['nome_responsavel']

    def create(self, validated_data):
        # Garante que, ao criar por essa rota, seja sempre VISITANTE
        validated_data['role'] = User.Roles.VISITANTE
        return super().create(validated_data)
