from rest_framework import generics, permissions
from onlyevents_drf_api.permissions import IsOwnerOrReadOnly
from .models import Going
from .serializers import GoingSerializer


class GoingList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = GoingSerializer
    queryset = Going.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class GoingDetail(generics.RetrieveDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = GoingSerializer
    queryset = Going.objects.all()