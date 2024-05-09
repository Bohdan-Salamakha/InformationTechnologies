from rest_framework import serializers


class ExceptionTypeSerializer(serializers.Serializer):
    EXCEPTION_CHOICES = (
        (1, 'CustomException1'),
        (2, 'CustomException2'),
        (3, 'CustomException3'),
        (4, 'CustomException4'),
        (5, 'CustomException5'),
    )

    exception_type = serializers.ChoiceField(choices=EXCEPTION_CHOICES)


class ExceptionResponseSerializer(serializers.Serializer):
    error = serializers.CharField()
