import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.test import APIClient

from participants.models import Participant

from .factories import ParticipantFactory

fake = Faker()


@pytest.mark.django_db
class TestParticipantsEndpoint:
    def setup_method(self):
        self.client = APIClient()
        self.common_user = User.objects.create_user(
            username='nonadmin',
            email='nonadmin@example.com',
            password='password',
        )

        self.participant = ParticipantFactory()

    def test_list_participants_unauthenticated(self):
        url = reverse('participant-list')
        response = self.client.get(url)
        data = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert (
            len(data) == 1
        )   # Assumes there's one register (self.participant)

    def test_list_participants_authenticated(self):
        url = reverse('participant-list')
        self.client.force_authenticate(self.common_user)
        response = self.client.get(url)
        data = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert (
            len(data) == 1
        )   # Assumes there's one register (self.participant)

    def test_retrieve_participant_by_id_unauthenticated(self):
        url = reverse('participant-detail', kwargs={'pk': self.participant.pk})
        response = self.client.get(url)
        data = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert data['id'] == self.participant.pk
        assert data['first_name'] == self.participant.first_name
        assert data['last_name'] == self.participant.last_name
        assert data['participation'] == self.participant.participation

    def test_retrieve_participant_by_id_authenticated(self):
        url = reverse('participant-detail', kwargs={'pk': self.participant.pk})
        self.client.force_authenticate(self.common_user)
        response = self.client.get(url)
        data = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert data['id'] == self.participant.pk
        assert data['first_name'] == self.participant.first_name
        assert data['last_name'] == self.participant.last_name
        assert data['participation'] == self.participant.participation

    def test_create_participant_unauthenticated(self):
        url = reverse('participant-list')
        response = self.client.post(
            url,
            {
                'first_name': fake.first_name(),
                'last_name': fake.last_name(),
                'participation': fake.random_int(min=1, max=100),
            },
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_participant_authenticated(self):
        url = reverse('participant-list')
        self.client.force_authenticate(self.common_user)
        response = self.client.post(
            url,
            {
                'first_name': fake.first_name(),
                'last_name': fake.last_name(),
                'participation': fake.random_int(min=1, max=100),
            },
        )
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_participant_authenticated_with_invalid_data(self):
        url = reverse('participant-list')
        self.client.force_authenticate(self.common_user)
        response = self.client.post(
            url,
            {
                'first_name': 'Fir#st',
                'last_name': 'L@st',
                'participation': -50,
            },
        )

        response_data = response.json()

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            response_data['first_name'][0]
            == 'First name should only contain alphabetic characters and hyphens'
        )
        assert (
            response_data['last_name'][0]
            == 'Last name should only contain alphabetic characters and hyphens'
        )
        assert (
            response_data['participation'][0]
            == 'Ensure this value is greater than or equal to 0.'
        )

    def test_edit_participant_unauthenticated(self):
        url = reverse('participant-detail', kwargs={'pk': self.participant.pk})
        new_data = {
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'participation': fake.random_int(min=1, max=100),
        }
        response = self.client.put(url, new_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_edit_participant_authenticated(self):
        url = reverse('participant-detail', kwargs={'pk': self.participant.pk})
        self.client.force_authenticate(self.common_user)
        new_data = {
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'participation': fake.random_int(min=1, max=100),
        }
        response = self.client.put(url, new_data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['first_name'] == new_data['first_name']
        assert response.data['last_name'] == new_data['last_name']
        assert response.data['participation'] == new_data['participation']

    def test_edit_participant_authenticated_with_invalid_data(self):
        url = reverse('participant-detail', kwargs={'pk': self.participant.pk})
        self.client.force_authenticate(self.common_user)
        new_data = {
            'first_name': 'Fir#st',
            'last_name': 'L@st',
            'participation': -50,
        }
        response = self.client.put(url, new_data)

        response_data = response.json()

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            response_data['first_name'][0]
            == 'First name should only contain alphabetic characters and hyphens'
        )
        assert (
            response_data['last_name'][0]
            == 'Last name should only contain alphabetic characters and hyphens'
        )
        assert (
            response_data['participation'][0]
            == 'Ensure this value is greater than or equal to 0.'
        )

    def test_delete_participant_unauthenticated(self):
        url = reverse('participant-detail', kwargs={'pk': self.participant.pk})
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_participant_authenticated(self):
        url = reverse('participant-detail', kwargs={'pk': self.participant.pk})
        self.client.force_authenticate(self.common_user)
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Participant.objects.filter(pk=self.participant.pk).exists()
