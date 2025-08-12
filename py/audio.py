import numpy as np, pygame
from model import SoundSource

def init_audio(sample_rate=44100, buffer=512):
    pygame.mixer.pre_init(frequency=sample_rate, size=-16, channels=2, buffer=buffer)
    pygame.mixer.init()

def make_tone(freq: float, seconds=1.0, sr=44100):
    t = np.linspace(0, seconds, int(sr*seconds), endpoint=False)
    wave = (0.5*np.sin(2*np.pi*freq*t)).astype(np.float32)
    stereo = np.stack([wave, wave], axis=1)
    return pygame.sndarray.make_sound((stereo*32767).astype(np.int16))

def start_sources(sources: list[SoundSource]):
    channels = []
    for s in sources:
        snd = make_tone(s.freq, seconds=1.0)  # krótka pętla
        ch = snd.play(loops=-1)
        channels.append((s, ch))
    return channels

def set_channel_lr(channel: pygame.mixer.Channel, L: float, R: float, gain: float):
    channel.set_volume(max(0.0, min(1.0, L*gain)), max(0.0, min(1.0, R*gain)))
