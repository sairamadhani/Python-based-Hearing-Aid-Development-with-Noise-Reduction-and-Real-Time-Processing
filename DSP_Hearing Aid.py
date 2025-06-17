#KETERANGAN CODE KE-1
#CODE INI UNTUK KITA MEMBANDINGKAN VOLUME ANTARA 0-100 SECARA LANGSUNG DAN ADA FITUR GANTI VOLUME ATAU SELESAI

import pyaudio
import numpy as np
import noisereduce as nr
from scipy.io.wavfile import write
from pydub import AudioSegment
from pydub.effects import normalize
import matplotlib.pyplot as plt
import ctypes
import wave
import os

# Visualisasi Spektrogram
def plot_spectrogram(audio_data, rate, title="Spectrogram"):
    from scipy.signal import stft
    f, t, Zxx = stft(audio_data, fs=rate, nperseg=1024)
    plt.figure(figsize=(12, 6))
    plt.pcolormesh(t, f, 20 * np.log10(np.abs(Zxx) + 1e-8), shading='gouraud', cmap='inferno')
    plt.title(title, fontsize=16, weight='bold')
    plt.ylabel("Frequency (Hz)", fontsize=14)
    plt.xlabel("Time (s)", fontsize=14)
    plt.colorbar(label="Magnitude (dB)")
    plt.ylim(0, rate // 2)
    plt.grid(visible=True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

# Fungsi untuk memutar audio WAV
def play_audio(file_path):
    print(f"Memutar audio: {file_path}")
    wf = wave.open(file_path, 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    data = wf.readframes(1024)
    while data:
        stream.write(data)
        data = wf.readframes(1024)
    stream.stop_stream()
    stream.close()
    p.terminate()

# Fungsi kontrol volume sistem
def set_volume(volume: int):
    if 0 <= volume <= 100:
        level = int(volume * 65535 / 100)
        volume_level = level | (level << 16)
        ctypes.windll.winmm.waveOutSetVolume(0, volume_level)
        print(f"Volume sistem diatur ke {volume}%.")
    else:
        print("Error: Volume harus dalam rentang 0-100.")

# Fungsi untuk menyimpan file sementara
def save_audio_files(audio_data, rate, file_path):
    write(file_path, rate, audio_data)
    print(f"Audio disimpan ke '{file_path}'.")

# Fungsi untuk mengatur ulang volume tanpa rekaman ulang
def adjust_volume():
    new_volume = int(input("Masukkan volume baru (0-100): "))
    set_volume(new_volume)
    with open("volume_settings.txt", "w") as volume_file:
        volume_file.write(f"Volume: {new_volume}%\n")
    play_audio("output_audio.wav")

# Rekaman Audio
RATE = 44100
DURATION = 10
print("Mulai merekam...")
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=1024)

frames = []
for _ in range(0, int(RATE / 1024 * DURATION)):
    data = stream.read(1024)
    frames.append(data)
print("Rekaman selesai.")
stream.stop_stream()
stream.close()
p.terminate()

# Gabungkan frame menjadi numpy array
audio_data = np.frombuffer(b''.join(frames), dtype=np.int16)
save_audio_files(audio_data, RATE, "original_audio.wav")

# Visualisasi spektrogram asli
plot_spectrogram(audio_data, RATE, title="Original Audio Spectrogram")

# Noise Reduction
print("Mengurangi noise...")
reduced_noise_audio = nr.reduce_noise(
    y=audio_data,
    sr=RATE,
    freq_mask_smooth_hz=300,
    time_mask_smooth_ms=50
)
save_audio_files(reduced_noise_audio, RATE, "reduced_noise_audio.wav")

# Visualisasi spektrogram setelah noise reduction
plot_spectrogram(reduced_noise_audio, RATE, title="Reduced Noise Audio Spectrogram")

# Pemrosesan tambahan dengan Pydub
print("Memuat audio untuk pemrosesan lebih lanjut...")
audio = AudioSegment.from_wav("reduced_noise_audio.wav")
audio = audio + 10
normalized_audio = normalize(audio)
normalized_audio.export("output_audio.wav", format="wav")
print("Audio yang telah diperkuat dan dinormalisasi disimpan ke 'output_audio.wav'.")

# Meminta pengguna mengatur volume
adjust_volume()

# Menyediakan opsi untuk mengubah volume kembali
while True:
    option = input("Apakah Anda ingin mengubah volume lagi? (y/n): ").strip().lower()
    if option == 'y':
        adjust_volume()
    elif option == 'n':
        print("Proses selesai.")
        break
    else:
        print("Input tidak valid. Harap masukkan 'y' atau 'n'.")
    








# #KETERANGAN CODE KE-2
# #UTUK CODE INI MENYIMPAN WAV ATAU HASIL OUTPUT DARI VOLUME 25, 50, 75, 100 
import pyaudio
import numpy as np
import noisereduce as nr
from scipy.io.wavfile import write
from pydub import AudioSegment
from pydub.effects import normalize
import matplotlib.pyplot as plt
import ctypes
import wave
import os

# Visualisasi Spektrogram
def plot_spectrogram(audio_data, rate, title="Spectrogram"):
    from scipy.signal import stft
    f, t, Zxx = stft(audio_data, fs=rate, nperseg=1024)
    plt.figure(figsize=(12, 6))
    plt.pcolormesh(t, f, 20 * np.log10(np.abs(Zxx) + 1e-8), shading='gouraud', cmap='inferno')
    plt.title(title, fontsize=16, weight='bold')
    plt.ylabel("Frequency (Hz)", fontsize=14)
    plt.xlabel("Time (s)", fontsize=14)
    plt.colorbar(label="Magnitude (dB)")
    plt.ylim(0, rate // 2)
    plt.grid(visible=True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

# Fungsi untuk memutar audio WAV
def play_audio(file_path):
    print(f"Memutar audio: {file_path}")
    wf = wave.open(file_path, 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    data = wf.readframes(1024)
    while data:
        stream.write(data)
        data = wf.readframes(1024)
    stream.stop_stream()
    stream.close()
    p.terminate()

# Rekaman Audio
RATE = 44100
DURATION = 10
print("Mulai merekam...")
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=1024)

frames = []
for _ in range(0, int(RATE / 1024 * DURATION)):
    data = stream.read(1024)
    frames.append(data)
print("Rekaman selesai.")
stream.stop_stream()
stream.close()
p.terminate()

# Gabungkan frame menjadi numpy array
audio_data = np.frombuffer(b''.join(frames), dtype=np.int16)
write("original_audio.wav", RATE, audio_data)
print("Data audio asli disimpan ke 'original_audio.wav'.")

# Visualisasi spektrogram asli
plot_spectrogram(audio_data, RATE, title="Original Audio Spectrogram")

# Noise Reduction
print("Mengurangi noise...")
reduced_noise_audio = nr.reduce_noise(
    y=audio_data,
    sr=RATE,
    freq_mask_smooth_hz=300,
    time_mask_smooth_ms=50
)
write("reduced_noise_audio.wav", RATE, reduced_noise_audio)
print("Data audio setelah noise reduction disimpan ke 'reduced_noise_audio.wav'.")

# Visualisasi spektrogram setelah noise reduction
plot_spectrogram(reduced_noise_audio, RATE, title="Reduced Noise Audio Spectrogram")

# Pemrosesan tambahan dengan Pydub
audio = AudioSegment.from_wav("reduced_noise_audio.wav")

# Membuat file dengan berbagai level volume
volume_levels = [25, 50, 75, 100]
for level in volume_levels:
    adjusted_audio = audio + (level - 50)  # Sesuaikan berdasarkan level
    normalized_audio = normalize(adjusted_audio)
    file_name = f"output_audio_{level}.wav"
    normalized_audio.export(file_name, format="wav")
    print(f"Audio dengan volume {level}% disimpan ke '{file_name}'.")

print("Selesai memproses semua level volume.")