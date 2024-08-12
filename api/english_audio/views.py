from django.http import JsonResponse
import requests
from django.views.decorators.csrf import csrf_exempt
from admin_backend import settings
from .models import AudioChunk, AudioFile, AudioTranscript
from .utils import split_audio_file

from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404


@csrf_exempt
def upload_audio(request):
    if request.method == "POST":
        if "file" in request.FILES:
            audio_file = request.FILES.get("file")
            # saved = default_storage.save(audio_file.name, audio_file)
            if audio_file:
                audio = AudioFile.objects.create(title=audio_file.name, file=audio_file, user=request.user)
                chunks = split_audio_file(audio, user=request.user)
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
        else:
            return JsonResponse({"error": "No file found"}, status=400)
    return JsonResponse({"error": "Invalid request"}, status=400)


def get_audio_files(request):
    audio_files = AudioFile.objects.filter(user=request.user).order_by("-uploaded_at")
    data = []
    for audio in audio_files:
        chunks = audio.chunks.all().order_by("start_time")
        if chunks:
            data.append(
                {
                    "id": audio.id,
                    "title": audio.title,
                    "chunks": [
                        {
                            "id": chunk.id,
                            "media": chunk.chunk_file.url,
                            "start": chunk.start_time,
                            "end": chunk.end_time,
                        }
                        for chunk in chunks
                    ],
                }
            )
    return JsonResponse(data, safe=False)


def get_chunk(request, chunk_id):
    chunk = AudioChunk.objects.get(id=chunk_id)
    return JsonResponse(
        {
            "id": chunk.id,
            "media": chunk.chunk_file.url,
            "transcript": chunk.transcript.text if hasattr(chunk, 'transcript') else None,
            "note_id": chunk.note.id if hasattr(chunk, 'note') else None,
            "note_content": chunk.note.text if hasattr(chunk, 'note') else None,
            "start": chunk.start_time,
            "end": chunk.end_time,
        }
    )


@csrf_exempt
def audio_transcript(request, chunk_id):
    url = "https://api.siliconflow.cn/v1/audio/transcriptions"
    chunk: AudioChunk = AudioChunk.objects.get(id=chunk_id)
    try:
        chunk.transcript
        return JsonResponse({"text": chunk.transcript.text})
    except AudioTranscript.DoesNotExist:
        pass
    file_path = chunk.chunk_file.path
    files = {
        "file": (
            chunk.chunk_file.name,
            open(
                file_path,
                "rb",
            ),
            "audio/mp3",
        )
    }
    payload = {"model": "iic/SenseVoiceSmall"}
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {settings.SILICIONFLOW_API_KEY}",
    }

    response = requests.post(url, data=payload, files=files, headers=headers)

    if response.status_code == 200:
        response_json = response.json()
        text = response_json["text"]
        AudioTranscript.objects.create(chunk=chunk, text=text, user=request.user)
        return JsonResponse(response_json)
    else:
        return JsonResponse(response.text, status=response.status_code, safe=False)


@require_http_methods(["DELETE"])
@csrf_exempt
def delete_transcript(request, chunk_id):
    chunk: AudioChunk = get_object_or_404(AudioChunk, id=chunk_id)

    try:
        transcript = chunk.transcript
        transcript.delete()
        return JsonResponse({"message": "Transcript deleted successfully"}, status=200)
    except AudioTranscript.DoesNotExist:
        return JsonResponse({"error": "Transcript not found"}, status=404)


