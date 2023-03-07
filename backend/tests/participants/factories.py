import factory
from faker import Faker

from participants.models import Participant


fake = Faker()


class ParticipantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Participant

    first_name = fake.first_name()
    last_name = fake.last_name()
    participation = fake.random_int(min=1, max=100)
