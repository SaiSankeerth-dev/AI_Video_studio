import librosa
import numpy as np

# Load first 120 seconds of audio to analyze opening hook pacing
audio_path = r"E:\AI_Videos\Youtube\youtube_project\reference\reference_video.mp4"
y, sr = librosa.load(audio_path, sr=22050, duration=120)

rms = librosa.feature.rms(y=y)[0]
tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
tempo_val = float(tempo[0]) if hasattr(tempo, '__len__') else float(tempo)

print(f"Sample Rate: {sr}")
print(f"Estimated Music/Background Tempo: {tempo_val:.1f} BPM")
print(f"Mean RMS Loudness: {np.mean(rms):.4f}")
print(f"Peak RMS Loudness: {np.max(rms):.4f}")
print(f"Dynamic Range Ratio (Peak/Mean): {np.max(rms)/np.mean(rms):.2f}")

