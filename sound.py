# sound.py
import io
import math
import struct
import wave
import pygame


class SoundManager:
    def __init__(self):
        self.enabled = False
        self.sounds = {}
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=44100, size=-16, channels=1)
            self.sounds["shift"] = self._generate_sweep(320, 740, 0.14, volume=0.25)
            self.sounds["key"] = self._generate_sweep(520, 1040, 0.18, volume=0.3)
            self.sounds["fail"] = self._generate_sweep(260, 90, 0.25, volume=0.35)
            self.sounds["win"] = self._generate_sweep(440, 1320, 0.35, volume=0.3)
            self.enabled = True
        except pygame.error:
            self.enabled = False

    def _generate_sweep(self, start_freq, end_freq, duration, volume=0.3, sample_rate=44100):
        num_samples = int(sample_rate * duration)
        buf = io.BytesIO()

        with wave.open(buf, "wb") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)

            frames = bytearray()
            for i in range(num_samples):
                t = i / num_samples
                freq = start_freq + (end_freq - start_freq) * t
                # Blago opadanje jačine zvuka pri kraju (envelope)
                env = 1.0 - t
                val = math.sin(2.0 * math.pi * freq * (i / sample_rate))
                sample = int(val * volume * env * 32767)
                frames.extend(struct.pack("<h", sample))

            wav_file.writeframes(frames)

        buf.seek(0)
        return pygame.mixer.Sound(buf)

    def play(self, name):
        if self.enabled and name in self.sounds:
            self.sounds[name].play()