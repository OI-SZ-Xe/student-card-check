# -*- coding: utf-8 -*-
import math, random, struct, wave, os

RATE = 22050
OUT = r"F:\请出示学生证\audio"
os.makedirs(OUT, exist_ok=True)

def write(name, samples):
    data = bytearray()
    for s in samples:
        v = int(max(-1.0, min(1.0, s)) * 32000)
        data += struct.pack("<h", v)
    path = os.path.join(OUT, name + ".wav")
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(bytes(data))
    print("wrote", path, len(samples))

def env(i, n, attack=0.005, decay=3.0):
    t = i / RATE
    a = min(1.0, t / max(attack, 1e-4))
    return a * math.exp(-decay * t)

def click():
    n = int(RATE * 0.05)
    out = []
    for i in range(n):
        e = env(i, n, 0.001, 90.0)
        out.append(random.uniform(-1, 1) * e * 0.5)
    return out

def type_click():
    n = int(RATE * 0.025)
    return [random.uniform(-1, 1) * env(i, n, 0.0005, 160.0) * 0.35 for i in range(n)]

def stamp():
    n = int(RATE * 0.42)
    out = []
    for i in range(n):
        t = i / RATE
        freq = 130.0 * math.exp(-t * 6.0) + 55.0
        body = math.sin(2 * math.pi * freq * t)
        noise = random.uniform(-1, 1) * math.exp(-t * 55.0) * 0.8
        out.append((body * 0.55 + noise * 0.35) * env(i, n, 0.002, 11.0))
    return out

def paper():
    n = int(RATE * 0.5)
    out = []
    prev = 0.0
    for i in range(n):
        t = i / RATE
        white = random.uniform(-1, 1)
        prev = prev * 0.82 + white * 0.18
        amp = math.sin(math.pi * min(1.0, t / 0.5)) ** 2
        out.append(prev * amp * 0.55)
    return out

def error():
    n = int(RATE * 0.4)
    out = []
    for i in range(n):
        t = i / RATE
        freq = 240.0 * math.exp(-t * 2.5) + 90.0
        sq = 1.0 if math.sin(2 * math.pi * freq * t) > 0 else -1.0
        out.append(sq * 0.18 * env(i, n, 0.005, 6.0))
    return out

def chime():
    n = int(RATE * 0.9)
    out = []
    for i in range(n):
        t = i / RATE
        s = math.sin(2 * math.pi * 784 * t) * 0.22 + math.sin(2 * math.pi * 1176 * t) * 0.12
        out.append(s * env(i, n, 0.01, 2.6))
    return out

write("click", click())
write("type", type_click())
write("stamp", stamp())
write("paper", paper())
write("error", error())
write("chime", chime())
