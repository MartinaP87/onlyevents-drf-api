from rest_framework import generics, permissions
from onlyevents_drf_api.permissions import IsOwnerOrReadOnly
from .models import Interested
from .serializers import InterestedSerializer


class InterestedList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = InterestedSerializer
    queryset = Interested.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class InterestedDetail(generics.RetrieveDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = InterestedSerializer
    queryset = Interested.objects.all()
