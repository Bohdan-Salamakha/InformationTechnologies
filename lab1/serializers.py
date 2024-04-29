from rest_framework import serializers

from .models import Document


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'
        extra_kwargs = {'user': {'read_only': True}}


class DocumentQuerySerializer(serializers.Serializer):
    is_signed = serializers.BooleanField(required=False, allow_null=True)
    start_date = serializers.DateTimeField(required=False, allow_null=True)
    end_date = serializers.DateTimeField(required=False, allow_null=True)
