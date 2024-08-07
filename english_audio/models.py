from django.db import models

# Create your models here.


class AudioFile(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to="uploads/")
    uploaded_at = models.DateTimeField(auto_now_add=True)


class AudioChunk(models.Model):
    audio_file = models.ForeignKey(
        AudioFile, on_delete=models.CASCADE, related_name="chunks"
    )
    chunk_file = models.FileField(upload_to="chunks/")
    start_time = models.FloatField()
    end_time = models.FloatField()
