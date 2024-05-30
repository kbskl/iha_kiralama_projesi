from rest_framework import serializers

from iha.models import IHA


class IHAOwnerField(
    serializers.RelatedField):  # API dönüşünde owner field'ı username dönüyordu bunu ad ve soyad olarak değiştirmek için özel serializer field'ı yazıldı
    def to_representation(self, value):
        return f"{value.first_name} {value.last_name}"


class IHASerializer(serializers.ModelSerializer):
    owner = IHAOwnerField(read_only=True)

    class Meta:
        model = IHA
        fields = ['uuid', 'brand', 'model', 'communication_range', 'weight', 'length', 'category', 'owner']
