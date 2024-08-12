from rest_framework import viewsets
from .models import AudioNote
from .serializers import AudioNoteSerializer
from rest_framework.permissions import IsAuthenticated

class AudioNoteViewSet(viewsets.ModelViewSet):
    queryset = AudioNote.objects.all()
    serializer_class = AudioNoteSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return AudioNote.objects.filter(chunk__user=self.request.user)
