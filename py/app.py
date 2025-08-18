import pygame
from model import Map2D, SoundSource, Listener, Obstacle
from acoustics import dist, gain_distance, obstacle_attenuation, pan_lr, smooth, smooth_channels
from audio import init_audio, start_sources, set_channel_lr
from render import init_window, draw

import time

amplitude_state = {} # id(src) -> {'l':0.0, 'r':0.0}

def main():
    size = 600

    # pre-config
    scene = Map2D(size=size, obstacles=[
        Obstacle((150, 100), (450, 100), absorb=0.35),
        Obstacle((300, 100), (300, 500), absorb=0.55),
        Obstacle((200, 300), (580, 300), absorb=0.9),
        Obstacle((50, 200), (320, 450), absorb=0.25)
    ])
    sources = [
        SoundSource(pos=(120, 120), freq=220.0),
        SoundSource(pos=(500, 260), freq=330.0),
        SoundSource(pos=(400, 520), freq=440.0),

        SoundSource(pos=(220, 130), freq=480.0),
        SoundSource(pos=(130, 550), freq=100.0)
    ]
    listener = Listener(pos=(300, 300))

    pygame.init()

    # font = pygame.font.SysFont("consolas", 16)
    last_t = time.perf_counter()
    screen = init_window(size_px=800)
    init_audio()
    channels = start_sources(sources)

    clock = pygame.time.Clock()
    running = True
    while running:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT: running = False
            if ev.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
                mx,my = ev.pos
                listener.pos = (mx*size/800, my*size/800)

        now = time.perf_counter()
        dt = now - last_t
        last_t = now
        tau = 0.08  # 20 ms
        alpha = 1.0 - pow(2.718281828, -dt / tau)

        # audio update
        for (src, ch) in channels:
            r = dist(src.pos, listener.pos)
            gd = gain_distance(r, src.r0, src.rmax)
            obs = obstacle_attenuation(src.pos, listener.pos, scene.obstacles)
            g = src.base_gain * gd * obs
            L, R = pan_lr(src.pos, listener.pos, R=scene.size/2)

            # target_L = L * g
            # target_R = R * g
            target_LR = (L * g, R * g)

            s = amplitude_state.setdefault(id(src), {'l': 0.0, 'r': 0.0})
            # s['l'] = smooth(s['l'], target_L, alpha)
            # s['r'] = smooth(s['r'], target_R, alpha)
            s = smooth_channels(s, target_LR, alpha=alpha)

            # set_channel_lr(ch, L, R, g)
            set_channel_lr(ch, s['l'], s['r'], gain=1.0)

        draw(scene, sources, listener, screen, size_px=800)
        
        pygame.display.flip()
        clock.tick(60)


    pygame.quit()

if __name__ == "__main__":
    main()
