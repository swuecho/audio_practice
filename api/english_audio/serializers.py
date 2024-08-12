from rest_framework import serializers
from .models import AudioNote

class AudioNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioNote
        fields = ['id', 'chunk', 'text', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
