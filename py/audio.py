import numpy as np, pygame
import wave


def set_channel_lr(channel: pygame.mixer.Channel, L: float, R: float, gain: float):
    channel.set_volume(max(0.0, min(1.0, L*gain)), max(0.0, min(1.0, R*gain)))

class SoundSourceBase:
    def next(self, n_frames: int, sr: int) -> np.ndarray:
        raise NotImplementedError
    @property
    def finished(self) -> bool:
        return False

class NoiseSource(SoundSourceBase):
    def __init__(self, gain=0.2, seed=None):
        self.gain = gain
        self.rng = np.random.default_rng(seed)
    def next(self, n_frames, sr):
        return (self.gain * self.rng.standard_normal(n_frames)).astype(np.float32)
    
class DualOscSource(SoundSourceBase):
    def __init__(self, f_hz=220.0, detune_cents=5.0, gain=0.2):
        self.f = f_hz
        self.detune = 2 ** (detune_cents / 1200.0)
        self.gain = gain
        self.ph1 = self.ph2 = 0.0
    def next(self, n_frames, sr):
        t = np.arange(n_frames, dtype=np.float32) / sr
        ph1 = (self.ph1 + 2*np.pi*self.f*t) % (2*np.pi)
        ph2 = (self.ph2 + 2*np.pi*(self.f*self.detune)*t) % (2*np.pi)
        sig = 0.5*np.sin(ph1) + 0.5*np.sin(ph2)
        self.ph1 = float(ph1[-1] + 2*np.pi*self.f/sr) % (2*np.pi)
        self.ph2 = float(ph2[-1] + 2*np.pi*(self.f*self.detune)/sr) % (2*np.pi)
        return (self.gain * sig).astype(np.float32)

def load_wav_mono(path: str):
    with wave.open(str(path), 'rb') as wf:
        sr = wf.getframerate()
        nchan = wf.getnchannels()
        sampwidth = wf.getsampwidth()
        nframes = wf.getnframes()
        raw = wf.readframes(nframes)
    dtype = {1: np.int8, 2: np.int16, 4: np.int32}[sampwidth]
    data = np.frombuffer(raw, dtype=dtype).astype(np.float32)
    if nchan > 1:
        data = data.reshape(-1, nchan).mean(axis=1)
    if dtype == np.int8:
        data /= 127.0
    elif dtype == np.int16:
        data /= 32767.0
    elif dtype == np.int32:
        data /= 2147483647.0
    return data, sr

class WavPlayerSource(SoundSourceBase):
    def __init__(self, path, loop=True, gain=0.8):
        self.data, self.src_sr = load_wav_mono(path)
        self.loop = loop
        self.gain = gain
        self.pos = 0.0
        self._finished = False
    @property
    def finished(self): return self._finished
    def next(self, n_frames, sr):
        if self._finished: return np.zeros(n_frames, np.float32)
        step = self.src_sr / sr
        idx = self.pos + step * np.arange(n_frames, dtype=np.float32)
        i0 = np.floor(idx).astype(np.int32)
        i1 = (i0 + 1) % len(self.data)
        frac = (idx - i0).astype(np.float32)
        y = (1 - frac) * self.data[i0] + frac * self.data[i1]
        self.pos += step * n_frames
        if not self.loop and self.pos >= len(self.data):
            self._finished = True
        return (self.gain * y).astype(np.float32)
    
class WavSampler:
    # def __init__(self, data, src_sr, loop=False, pitch=1.0):
    def __init__(self, path, loop=False, pitch=1.0):
        self.data, self.src_sr = load_wav_mono(path)
        # self.data = np.asarray(data, dtype=np.float32)
        # self.src_sr = float(src_sr)
        self.N = int(self.data.shape[0])
        self.loop = loop
        self.pitch = float(pitch)
        self.pos = 0.0
        self.rate_cache_sr = None
        self.rate = None
        self.finished = False
        self.debug = {'last_i0_max': 0, 'last_pos': 0.0, 'ended': False}

    def _ensure_rate(self, out_sr):
        if (self.rate_cache_sr != out_sr):
            self.rate = self.pitch * (self.src_sr / float(out_sr))
            self.rate_cache_sr = out_sr

    def next(self, frames, out_sr):
        if self.finished:
            return np.zeros(frames, dtype=np.float32)

        self._ensure_rate(out_sr)
        
        steps = self.rate * np.arange(frames, dtype=np.float32)
        pos = self.pos + steps  # float

        i0 = np.floor(pos).astype(np.int64)
        frac = pos - i0

        # debug
        self.debug['last_i0_max'] = int(i0.max())
        self.debug['last_pos'] = float(self.pos)        

        if self.loop:
            i0m = np.mod(i0, self.N)
            i1m = np.mod(i0 + 1, self.N)
            y = (1.0 - frac) * self.data[i0m] + frac * self.data[i1m]
            self.pos = (self.pos + self.rate * frames) % self.N
            return y.astype(np.float32, copy=False)
        else:
            # One-shot: calculate only this with pair (i0 < N-1)
            y = np.zeros(frames, dtype=np.float32)
            valid = i0 < (self.N - 1)
            if np.any(valid):
                i0v = i0[valid]
                fv = frac[valid]
                y[valid] = (1.0 - fv) * self.data[i0v] + fv * self.data[i0v + 1]
            
            will_end = (self.pos + self.rate * frames) >= (self.N - 1)
            if will_end:
                M = min(128, frames)  # 128 samples
                y[-M:] *= np.linspace(1.0, 0.0, M, dtype=np.float32)
            self.pos += self.rate * frames
            if self.pos >= (self.N - 1):
                self.pos = float(self.N - 1)
                self.finished = True
                # debug
                if self.finished and not self.debug['ended']:
                    self.debug['ended'] = True
            return y
