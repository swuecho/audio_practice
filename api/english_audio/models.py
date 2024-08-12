from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class AudioFile(models.Model):
    title = models.CharField(max_length=2550)
    file = models.FileField(upload_to="uploads/", max_length=2550)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="audio_files")


class AudioChunk(models.Model):
    audio_file = models.ForeignKey(
        AudioFile, on_delete=models.CASCADE, related_name="chunks"
    )
    chunk_file = models.FileField(max_length=2550)
    start_time = models.FloatField()
    end_time = models.FloatField()
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="audio_chunks"
    )


class AudioTranscript(models.Model):
    chunk = models.OneToOneField(
        AudioChunk, on_delete=models.CASCADE, related_name="transcript"
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="audio_transcripts")

    def __str__(self):
        return f"Transcript for {self.chunk}"


class AudioNote(models.Model):
    chunk = models.OneToOneField(
        AudioChunk, on_delete=models.CASCADE, related_name="note"
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="audio_notes")

    def __str__(self):
        return f"note for {self.chunk}"
