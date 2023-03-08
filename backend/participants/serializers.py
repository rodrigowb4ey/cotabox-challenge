from django.core.exceptions import ValidationError
from rest_framework import serializers

from participants.models import Participant


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = '__all__'

    def validate_first_name(self, value):
        if not value:
            raise ValidationError('This field is required')
        
        if not all(char.isalpha() or char == '-' for char in value) or value != value.strip():
            raise ValidationError(
                'First name should only contain alphabetic characters and hyphens'
            )
        
        if value.strip() != value:
            raise ValidationError(
                'First name cannot have leading or trailing spaces'
            )

        return value

    def validate_last_name(self, value):
        if not value:
            raise ValidationError('This field is required')
        
        if not all(char.isalpha() or char == '-' for char in value) or value != value.strip():
            raise ValidationError(
                'Last name should only contain alphabetic characters and hyphens'
            )
        
        if value.strip() != value:
            raise ValidationError(
                'Last name cannot have leading or trailing spaces'
            )
        
        return value
    
    def validate_participation(self, value):
        if value <= 0:
            raise ValidationError(
                'Ensure this value is greater than or equal to 1'
            )
        return value
