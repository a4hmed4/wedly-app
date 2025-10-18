from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.username', read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'sender', 'sender_name', 'event_type', 'message', 'is_read', 'created_at']
        read_only_fields = ['id', 'sender_name', 'created_at']
