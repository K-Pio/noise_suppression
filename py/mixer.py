import numpy as np
import sounddevice as sd
# from acoustics import dist, gain_distance, obstacle_attenuation, pan_lr
from acoustics_c import gain_distance, pan_lr, smooth_channels, dist
from acoustics import obstacle_attenuation
import math

def mix_and_play(sources, listener, scene, sr=44100, blocksize=512, tau_s=0.02, amplitude_state={}):
    """
    sources: listOf objects with: pos: (x,y), generator: object with next(frames, sr)->mono float32
    listener: objectwith pos: (x,y)
    scene: Map2D with obstacles
    tau_s: time constant smoothingu (sec)
    """
    def callback(outdata, frames, tinfo, status):
        block_dt = frames / sr
        alpha = 1.0 - math.exp(-block_dt / tau_s) # alpha per-blok depends from blocks length

        buf = np.zeros((frames, 2), dtype=np.float32)

        lx, ly = listener.pos

        for s in sources:
            gen = getattr(s, "generator", None)
            if gen is None or getattr(gen, "finished", False):
                continue

            # Acustic
            r = dist(s.pos, (lx, ly))
            gd = gain_distance(r, getattr(s, "r0", 50.0), getattr(s, "rmax", scene.size))
            obs = obstacle_attenuation(s.pos, (lx, ly), scene.obstacles)
            g_total = getattr(s, "base_gain", 1.0) * gd * obs

            # L, R = pan_lr(s.pos, (lx, ly), R=scene.size/2)
            L, R = pan_lr(s.pos[0], lx, R=scene.size/2)
            

            target_LR = (L * g_total, R * g_total)

            st = amplitude_state.setdefault(id(s), {'l': 0.0, 'r': 0.0})
            st = smooth_channels(st, target_LR, alpha)

            # gen'n'mix
            mono = gen.next(frames, sr)  # shape (frames,)
            buf[:, 0] += mono * st['l']
            buf[:, 1] += mono * st['r']

        # headroom + clip
        outdata[:] = np.clip(buf, -1.0, 1.0)

    stream = sd.OutputStream(samplerate=sr,
                             blocksize=blocksize,
                             channels=2,
                             dtype='float32',
                             callback=callback)
    stream.start()
    return stream  # keep the handle to close on exit
