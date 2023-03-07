from rest_framework.routers import DefaultRouter
from participants.views import ParticipantViewSet

router = DefaultRouter()
router.register(r'participants', ParticipantViewSet)
