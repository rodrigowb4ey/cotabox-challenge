from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from participants.models import Participant
from participants.serializers import ParticipantSerializer


class ParticipantViewSet(ModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = (
        SearchFilter,
        DjangoFilterBackend,
    )
    filterset_fields = ['first_name', 'last_name', 'participation']
    search_fields = [
        'first_name',
        'last_name'
    ]
