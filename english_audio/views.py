from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import AudioFile, AudioChunk

from .utils import split_audio_file


@csrf_exempt
def upload_audio(request):
    if request.method == "POST":
        audio_file = request.FILES.get("file")
        if audio_file:
            audio = AudioFile.objects.create(title=audio_file.name, file=audio_file)
            chunks = split_audio_file(audio)
            return JsonResponse(
                {
                    "id": audio.id,
                    "title": audio.title,
                    "chunks": [
                        {
                            "id": chunk.id,
                            "start": chunk.start_time,
                            "end": chunk.end_time,
                        }
                        for chunk in chunks
                    ],
                }
            )
    return JsonResponse({"error": "Invalid request"}, status=400)


def get_audio_files(request):
    audio_files = AudioFile.objects.all().order_by("-uploaded_at")
    data = []
    for audio in audio_files:
        chunks = audio.chunks.all().order_by("start_time")
        data.append(
            {
                "id": audio.id,
                "title": audio.title,
                "chunks": [
                    {"id": chunk.id, "start": chunk.start_time, "end": chunk.end_time}
                    for chunk in chunks
                ],
            }
        )
    return JsonResponse(data, safe=False)
