import numpy as np
import soundfile as sf
import os
import math

sr = 44100
sfx_dir = r"E:\AI_Videos\Youtube\youtube_project\assets\sfx"
music_dir = r"E:\AI_Videos\Youtube\youtube_project\assets\music"
os.makedirs(sfx_dir, exist_ok=True)
os.makedirs(music_dir, exist_ok=True)

# 1. SFX: Sub-bass boom (1.5s)
t = np.linspace(0, 1.5, int(sr * 1.5), False)
freq = 55 * np.exp(-t * 2.5) # pitch drop from 55Hz to ~5Hz
env = np.exp(-t * 3.0)
boom = 0.8 * np.sin(2 * np.pi * freq * t) * env
# Add subtle sub-rumble
boom += 0.3 * np.sin(2 * np.pi * 35 * t) * env
sf.write(os.path.join(sfx_dir, "sfx_sub_boom.wav"), np.column_stack([boom, boom]), sr)

# 2. SFX: Camera Shutter Click (0.3s)
t = np.linspace(0, 0.3, int(sr * 0.3), False)
click1 = np.random.normal(0, 0.4, len(t)) * np.exp(-t * 40.0)
click2 = np.random.normal(0, 0.5, len(t)) * np.exp(-np.maximum(0, t - 0.08) * 50.0)
shutter = click1 + click2
sf.write(os.path.join(sfx_dir, "sfx_shutter_click.wav"), np.column_stack([shutter, shutter]), sr)

# 3. SFX: Paper/Tape Friction (0.5s)
t = np.linspace(0, 0.5, int(sr * 0.5), False)
noise = np.random.normal(0, 0.3, len(t))
paper = noise * np.sin(np.pi * t / 0.5) * np.exp(-t * 3.0)
sf.write(os.path.join(sfx_dir, "sfx_paper_slide.wav"), np.column_stack([paper, paper]), sr)

# 4. SFX: Forensic Scanner Chirp (0.4s)
t = np.linspace(0, 0.4, int(sr * 0.4), False)
chirp_freq = np.linspace(800, 2400, len(t))
chirp = 0.4 * np.sin(2 * np.pi * chirp_freq * t) * (1 - t/0.4)
sf.write(os.path.join(sfx_dir, "sfx_scanner_chirp.wav"), np.column_stack([chirp, chirp]), sr)

# 5. SFX: Knife Slice / Metallic Whoosh (0.6s)
t = np.linspace(0, 0.6, int(sr * 0.6), False)
metallic = 0.4 * np.sin(2 * np.pi * 3200 * t) * np.exp(-t * 8.0)
whoosh = 0.5 * np.random.normal(0, 0.2, len(t)) * np.sin(np.pi * t / 0.6)
slice_sfx = metallic + whoosh
sf.write(os.path.join(sfx_dir, "sfx_knife_slice.wav"), np.column_stack([slice_sfx, slice_sfx]), sr)

# 6. SFX: Cash Chime (1.2s)
t = np.linspace(0, 1.2, int(sr * 1.2), False)
bell1 = 0.4 * np.sin(2 * np.pi * 1760 * t) * np.exp(-t * 3.0) # A6
bell2 = 0.4 * np.sin(2 * np.pi * 2637 * t) * np.exp(-t * 3.5) # E7
chime = bell1 + bell2
sf.write(os.path.join(sfx_dir, "sfx_cash_chime.wav"), np.column_stack([chime, chime]), sr)

print("Generated all 6 core sound effects.")

# 7. GENERATE COMPLETE 5-MINUTE DOCUMENTARY MUSIC BED (305 seconds)
total_duration = 305.0 # ~5 minutes
total_samples = int(sr * total_duration)
t_full = np.linspace(0, total_duration, total_samples, False)

# BPM = 110 -> 1 beat = 60/110 = 0.5455s
beat_len = 60.0 / 110.0
beats_total = int(total_duration / beat_len)

music_left = np.zeros(total_samples)
music_right = np.zeros(total_samples)

# A. Clockwork Ticking Percussion on every 1/8 note (every 0.2727s)
tick_interval = beat_len / 2.0
num_ticks = int(total_duration / tick_interval)
tick_t = np.linspace(0, 0.05, int(sr * 0.05), False)
tick_sound = np.random.normal(0, 0.15, len(tick_t)) * np.exp(-tick_t * 80.0)

for i in range(num_ticks):
    pos = int(i * tick_interval * sr)
    if pos + len(tick_sound) < total_samples:
        vol = 0.25 if (i % 2 == 0) else 0.15
        # Slight panning oscillation
        pan = 0.5 + 0.1 * math.sin(i * 0.2)
        music_left[pos:pos+len(tick_sound)] += tick_sound * vol * (1.0 - pan)
        music_right[pos:pos+len(tick_sound)] += tick_sound * vol * pan

# B. Sub-Bass Pulse (55Hz / 110Hz) on beats 1 and 3 of every 4-beat bar
bar_len = beat_len * 4.0
num_bars = int(total_duration / bar_len)

# Minor Chord progression frequencies:
# Am (A1=55, C2=65.4, E2=82.4)
# F (F1=43.65, A1=55, C2=65.4)
# Dm (D1=36.7, F1=43.65, A1=55)
# E7 (E1=41.2, G#1=51.9, B1=61.7)
bass_freqs = [55.0, 43.65, 36.7, 41.2]

pulse_t = np.linspace(0, 0.8, int(sr * 0.8), False)
for b in range(num_bars):
    root = bass_freqs[b % len(bass_freqs)]
    pulse_wave = 0.35 * np.sin(2 * np.pi * root * pulse_t) * np.exp(-pulse_t * 1.5)
    pulse_wave += 0.15 * np.sin(2 * np.pi * root * 2 * pulse_t) * np.exp(-pulse_t * 2.0)
    
    # Hit on beat 0
    pos0 = int(b * bar_len * sr)
    if pos0 + len(pulse_wave) < total_samples:
        music_left[pos0:pos0+len(pulse_wave)] += pulse_wave * 0.8
        music_right[pos0:pos0+len(pulse_wave)] += pulse_wave * 0.8
        
    # Hit on beat 2
    pos2 = int((b * bar_len + beat_len * 2.0) * sr)
    if pos2 + len(pulse_wave) < total_samples:
        music_left[pos2:pos2+len(pulse_wave)] += pulse_wave * 0.6
        music_right[pos2:pos2+len(pulse_wave)] += pulse_wave * 0.6

# C. Atmospheric Ambient Synth Pad (Slow moving chords with stereo chorus)
chord_notes = [
    [220.0, 261.63, 329.63], # Am
    [174.61, 220.0, 261.63], # F
    [146.83, 174.61, 220.0], # Dm
    [164.81, 207.65, 246.94]  # E
]

for b in range(num_bars):
    notes = chord_notes[b % len(chord_notes)]
    bar_start_idx = int(b * bar_len * sr)
    bar_samples = int(bar_len * sr)
    if bar_start_idx + bar_samples > total_samples:
        bar_samples = total_samples - bar_start_idx
    
    t_bar = np.linspace(0, bar_samples / sr, bar_samples, False)
    # Smooth attack and release envelope
    env_bar = np.sin(np.pi * t_bar / (bar_samples / sr))
    
    pad_l = np.zeros(bar_samples)
    pad_r = np.zeros(bar_samples)
    for n_idx, freq in enumerate(notes):
        phase_l = n_idx * 0.5
        phase_r = n_idx * 0.5 + 0.3
        pad_l += 0.08 * np.sin(2 * np.pi * freq * t_bar + phase_l)
        pad_r += 0.08 * np.sin(2 * np.pi * (freq * 1.002) * t_bar + phase_r)
        
    music_left[bar_start_idx:bar_start_idx+bar_samples] += pad_l * env_bar
    music_right[bar_start_idx:bar_start_idx+bar_samples] += pad_r * env_bar

# Normalize and write music track
max_val = max(np.max(np.abs(music_left)), np.max(np.abs(music_right)))
if max_val > 0:
    music_left = (music_left / max_val) * 0.65
    music_right = (music_right / max_val) * 0.65

music_stereo = np.column_stack([music_left, music_right])
sf.write(os.path.join(music_dir, "soundtrack_bed.wav"), music_stereo, sr)
print(f"Generated soundtrack_bed.wav ({total_duration}s, 44.1kHz Stereo).")
