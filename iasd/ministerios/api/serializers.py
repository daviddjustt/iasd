from rest_framework import serializers
from iasd.ministerios.models import Ministerio

class MinisterioSerializer(serializers.ModelSerializer):
    nome_lider = serializers.ReadOnlyField(source='lider.name')

    class Meta:
        model = Ministerio
        fields = ['id', 'nome', 'lider', 'nome_lider', 'membros']