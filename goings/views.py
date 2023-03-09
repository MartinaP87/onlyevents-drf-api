from rest_framework import generics, permissions, filters
from onlyevents_drf_api.permissions import IsOwnerOrReadOnly
from .models import Going
from .serializers import GoingSerializer
from django_filters.rest_framework import DjangoFilterBackend


class GoingList(generics.ListCreateAPIView):
    """
    List goings or create a going if logged in.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = GoingSerializer
    queryset = Going.objects.all()
    filter_backends = [
        DjangoFilterBackend
    ]
    filterset_fields = [
        'owner',
        'posted_event'
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class GoingDetail(generics.RetrieveDestroyAPIView):
    """
    Retrieve a going, or delete it by id if you own it.
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = GoingSerializer
    queryset = Going.objects.all()
