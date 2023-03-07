import pytest
from rest_framework.exceptions import ValidationError

from participants.models import Participant
from participants.serializers import ParticipantSerializer


@pytest.mark.django_db
class TestParticipantSerializer:
    valid_participant_data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'participation': 50,
    }

    def test_valid_data_creates_serializer_instance(self):
        serializer = ParticipantSerializer(data=self.valid_participant_data)
        assert serializer.is_valid() is True
        participant = serializer.save()
        assert isinstance(participant, Participant)

    def test_invalid_first_name_with_numbers(self):
        self.valid_participant_data['first_name'] = 'John123'
        with pytest.raises(ValidationError):
            serializer = ParticipantSerializer(
                data=self.valid_participant_data
            )
            serializer.is_valid(raise_exception=True)

    def test_invalid_last_name_with_numbers(self):
        self.valid_participant_data['last_name'] = 'Doe123'
        with pytest.raises(ValidationError):
            serializer = ParticipantSerializer(
                data=self.valid_participant_data
            )
            serializer.is_valid(raise_exception=True)

    def test_invalid_first_name_with_special_characters(self):
        self.valid_participant_data['first_name'] = 'John.&$'
        with pytest.raises(ValidationError):
            serializer = ParticipantSerializer(
                data=self.valid_participant_data
            )
            serializer.is_valid(raise_exception=True)

    def test_invalid_last_name_with_special_characters(self):
        self.valid_participant_data['last_name'] = 'Doe#@!'
        with pytest.raises(ValidationError):
            serializer = ParticipantSerializer(
                data=self.valid_participant_data
            )
            serializer.is_valid(raise_exception=True)
