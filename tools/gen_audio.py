# -*- coding: utf-8 -*-
import os, math, random, wave, struct
import numpy as np

OUT = r"F:\请出示学生证\audio"
os.makedirs(OUT, exist_ok=True)
SR = 22050

def write(name, data):
    data = np.clip(data, -1.0, 1.0)
    pcm = (data * 32767).astype("<i2")
    with wave.open(os.path.join(OUT, name), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    print(name, len(data) / SR, "s")

def env(n, a=0.02, d=0.4):
    t = np.linspace(0, 1, n, endpoint=False)
    return np.minimum(1.0, t / a) * np.exp(-t / d)

def tone(freq, dur, amp=0.2, kind="sine", detune=0.0):
    n = int(SR * dur)
    t = np.arange(n) / SR
    w = np.sin(2 * np.pi * (freq + detune) * t)
    if kind == "tri":
        w = 2 * np.abs(2 * ((t * freq) % 1) - 1) - 1
    return w * env(n) * amp

# --- day BGM: slow minor pad, 32s
dur = 32.0
n = int(SR * dur)
buf = np.zeros(n)
chords = [(110.0, 130.81, 164.81), (87.31, 110.0, 130.81), (130.81, 164.81, 196.0), (98.0, 123.47, 146.83)]
step = dur / len(chords)
for i, ch in enumerate(chords):
    start = int(i * step * SR)
    seg_len = int(step * SR * 1.02)
    t = np.arange(seg_len) / SR
    seg = np.zeros(seg_len)
    for f in ch:
        seg += np.sin(2 * np.pi * f * t) * 0.10
        seg += np.sin(2 * np.pi * (f * 1.005) * t) * 0.05
    fade = np.minimum(1.0, t / 1.2) * np.minimum(1.0, (seg_len / SR - t) / 1.2)
    end = min(n, start + seg_len)
    buf[start:end] += seg[:end - start] * fade[:end - start]
rng = np.random.default_rng(3)
for _ in range(14):
    pos = rng.integers(0, n - SR * 3)
    f = float(rng.choice([440.0, 523.25, 659.25, 392.0]))
    note = tone(f, 2.4, 0.05)
    buf[pos:pos + len(note)] += note
hiss = rng.normal(0, 0.0035, n)
buf = buf * 0.6 + hiss
write("bgm_day.wav", buf)

# --- tense BGM: pulse + dissonance, 24s
dur = 24.0
n = int(SR * dur)
buf = np.zeros(n)
beat = 0.42
t_pos = 0.0
i = 0
while t_pos < dur:
    start = int(t_pos * SR)
    f = 55.0 if i % 4 else 65.41
    pulse = tone(f, 0.22, 0.22, "tri")
    end = min(n, start + len(pulse))
    buf[start:end] += pulse[:end - start]
    t_pos += beat
    i += 1
t = np.arange(n) / SR
buf += np.sin(2 * np.pi * 220.0 * t) * 0.02
buf += np.sin(2 * np.pi * 233.08 * t) * 0.02
buf += np.sin(2 * np.pi * 55.0 * t) * 0.06
write("bgm_tense.wav", buf * 0.8)

# --- ambience: room tone
dur = 20.0
n = int(SR * dur)
rng = np.random.default_rng(11)
brown = np.cumsum(rng.normal(0, 0.02, n))
brown = brown - np.convolve(brown, np.ones(400) / 400, mode="same")
t = np.arange(n) / SR
hum = np.sin(2 * np.pi * 50.0 * t) * 0.02 + np.sin(2 * np.pi * 100.0 * t) * 0.01
buf = brown * 0.3 + hum
for k in range(10):
    start = int((k * 2.0 + 0.4) * SR)
    tick = tone(1800.0, 0.05, 0.02)
    end = min(n, start + len(tick))
    buf[start:end] += tick[:end - start]
write("amb_room.wav", buf)

# --- rain
dur = 15.0
n = int(SR * dur)
rng = np.random.default_rng(7)
noise = rng.normal(0, 0.06, n)
kernel = np.ones(30) / 30
rain = np.convolve(noise, kernel, mode="same")
write("amb_rain.wav", rain * 0.8)
