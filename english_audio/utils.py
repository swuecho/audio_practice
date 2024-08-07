# audio_app/utils.py
from pydub import AudioSegment
from .models import AudioChunk
import os
from pathlib import Path


def split_audio_file(audio_file, chunk_length=5 * 60 * 1000):
    audio = AudioSegment.from_file(audio_file.file.path)
    chunks = []
    for i, chunk in enumerate(audio[::chunk_length]):
        start_time = i * chunk_length / 1000
        end_time = (i + 1) * chunk_length / 1000
        chunk_filename = f"chunk_{i+1}.mp3"
        chunk_dir = (
            Path(audio_file.file.path).parent.parent
            / "media"
            / Path(audio_file.file.path).stem
        )
        print(chunk_dir)
        if not chunk_dir.exists():
            chunk_dir.mkdir(parents=True, exist_ok=True)
        chunk_path = str(chunk_dir / chunk_filename)
        chunk.export(chunk_path, format="mp3")
        audio_chunk = AudioChunk.objects.create(
            audio_file=audio_file,
            chunk_file=chunk_path,
            start_time=start_time,
            end_time=end_time,
        )
        chunks.append(audio_chunk)
    return chunks
