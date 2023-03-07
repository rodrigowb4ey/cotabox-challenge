import pytest
from django.db.utils import IntegrityError

from participants.models import Participant


@pytest.fixture
def participant():
    return Participant.objects.create(
        first_name='John', last_name='Doe', participation=50
    )


@pytest.mark.django_db
class TestParticipantModel:
    def test_participant_str_representation(self, participant):
        assert str(participant) == 'John Doe'

    def test_valid_data_creates_participant_instance(self):
        participant = Participant.objects.create(
            first_name='First', last_name='Last', participation=50
        )

        assert len(Participant.objects.all()) == 1

    def test_participant_participation_non_negative(self):
        with pytest.raises(IntegrityError):
            Participant.objects.create(
                first_name='Jane', last_name='Doe', participation=-50
            )
