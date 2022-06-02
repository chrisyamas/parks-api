from rest_framework import generics
from .models import Park
from .serializers import ParkSerializer


class ParkList(generics.ListCreateAPIView):
    queryset = Park.objects.all()
    serializer_class = ParkSerializer


class ParkDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Park.objects.all()
    serializer_class = ParkSerializer


