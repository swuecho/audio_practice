# audio_app/utils.py
from pydub import AudioSegment
from .models import AudioChunk
from pathlib import Path


def split_audio_file(audio_file, user, chunk_length=2 * 60 * 1000):
    """5 min is too long"""
    audio_file_path = audio_file.file.path
    audio = AudioSegment.from_file(audio_file_path)
    chunks = []
    for i, chunk in enumerate(audio[::chunk_length]):
        start_time = i * chunk_length / 1000
        end_time = (i + 1) * chunk_length / 1000
        chunk_filename = f"chunk_{i+1}.mp3"
        chunk_dir = (
            Path(audio_file_path).parent.parent / "chunks" / Path(audio_file_path).stem
        )
        if not chunk_dir.exists():
            chunk_dir.mkdir(parents=True, exist_ok=True)
        chunk_path = str(chunk_dir / chunk_filename)
        chunk.export(chunk_path, format="mp3")
        audio_chunk = AudioChunk.objects.create(
            audio_file=audio_file,
            chunk_file=f"chunks/{chunk_dir.name}/{chunk_filename}",
            start_time=start_time,
            end_time=end_time,
            user=user,
        )
        chunks.append(audio_chunk)
    return chunks
