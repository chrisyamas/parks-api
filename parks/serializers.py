from rest_framework import serializers
from .models import Park


class ParkSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id", "visitor", "name", "location", "description", "created_at")
        model = Park