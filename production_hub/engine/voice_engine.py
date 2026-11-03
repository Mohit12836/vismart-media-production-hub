import asyncio
import os
import re
import subprocess
import edge_tts

def get_audio_duration(file_path: str) -> float:
    """Accurately extracts audio duration using ffmpeg."""
    cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", file_path]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30, check=True)
    seconds = float(result.stdout.strip())
    if seconds <= 0:
        raise ValueError("Audio has no measurable duration")
    return round(seconds, 2)

async def generate_speech(text: str, output_path: str, voice: str = "hi-IN-MadhurNeural", rate: str = "+10%", pitch: str = "+0Hz") -> float:
    """
    Generates 100% Free Neural Voiceover via Edge-TTS with full speed & pitch tone controls.
    Returns the exact duration in seconds.
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    communicator = edge_tts.Communicate(text, voice=voice, rate=rate, pitch=pitch)
    await communicator.save(output_path)
    dur = get_audio_duration(output_path)
    print(f"[VoiceEngine] Generated audio: {output_path} ({dur}s, voice: {voice}, rate: {rate}, pitch: {pitch})")
    return dur

def process_uploaded_audio(input_audio_path: str, dest_path: str) -> float:
    """
    Processes user-uploaded audio file, normalizes format to MP4-compatible mp3,
    and returns duration.
    """
    os.makedirs(os.path.dirname(os.path.abspath(dest_path)), exist_ok=True)
    cmd = [
        "ffmpeg", "-y", "-i", input_audio_path,
        "-acodec", "libmp3lame", "-ar", "44100", "-ac", "2", "-b:a", "192k",
        dest_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return get_audio_duration(dest_path)

if __name__ == "__main__":
    asyncio.run(generate_speech("नमस्ते, यह वॉयस इंजन टेस्ट है।", "test_speech.mp3"))
