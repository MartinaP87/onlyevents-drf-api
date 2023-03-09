from rest_framework import generics, permissions, filters
from onlyevents_drf_api.permissions import IsOwnerOrReadOnly
from .models import Interested
from .serializers import InterestedSerializer
from django_filters.rest_framework import DjangoFilterBackend


class InterestedList(generics.ListCreateAPIView):
    """
    List interesteds or create an interested if logged in.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = InterestedSerializer
    queryset = Interested.objects.all()
    filter_backends = [
        DjangoFilterBackend
    ]
    filterset_fields = [
        'owner',
        'posted_event'
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class InterestedDetail(generics.RetrieveDestroyAPIView):
    """
    Retrieve an interested, or delete it by id if you own it.
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = InterestedSerializer
    queryset = Interested.objects.all()
