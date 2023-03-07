from django.core.exceptions import ValidationError
from rest_framework import serializers

from participants.models import Participant


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = '__all__'

    def validate_first_name(self, value):
        if not all(char.isalpha() or char == '-' for char in value):
            raise ValidationError("First name should only contain alphabetic characters and hyphens")
        return value

    def validate_last_name(self, value):
        if not all(char.isalpha() or char == '-' for char in value):
            raise ValidationError("Last name should only contain alphabetic characters and hyphens")
        return value
