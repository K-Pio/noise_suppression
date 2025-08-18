import pygame
from model import Map2D, SoundSource, Listener, Obstacle
from render import init_window, draw
from audio import NoiseSource,DualOscSource, WavSampler, load_wav_mono
from mixer import mix_and_play

import time

amplitude_state = {} # id(src) -> {'l':0.0, 'r':0.0}

def main():
    size = 600

    samplePath = "./resc/sample-9s.wav"
    data, sr = load_wav_mono(samplePath)

    # pre-config
    scene = Map2D(size=size, obstacles=[
        Obstacle((150, 100), (450, 100), absorb=0.35),
        Obstacle((300, 100), (300, 500), absorb=0.55),
        Obstacle((200, 300), (580, 300), absorb=0.9),
        Obstacle((50, 200), (320, 450), absorb=0.25)
    ])
    sources = [
        SoundSource(pos=(120, 120), generator=(NoiseSource(0.2, 2137))),
        SoundSource(pos=(500, 260), generator=(DualOscSource(220, gain=.7))),
        SoundSource(pos=(400, 520), generator=(WavSampler(
            path=samplePath, loop=True
        )))

        # SoundSource(pos=(120, 120), freq=220.0),
        # SoundSource(pos=(500, 260), freq=330.0),
        # SoundSource(pos=(400, 520), freq=440.0),
        # SoundSource(pos=(220, 130), freq=480.0),
        # SoundSource(pos=(130, 550), freq=100.0)
    ]
    listener = Listener(pos=(300, 300))

    pygame.init()

    # font = pygame.font.SysFont("consolas", 16)
    last_t = time.perf_counter()
    screen = init_window(size_px=800)

    stream = mix_and_play(sources, listener, scene, 
                          sr=44100, blocksize=512, tau_s=0.08, 
                          amplitude_state = amplitude_state)

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

        draw(scene, sources, listener, screen, size_px=800)
        
        pygame.display.flip()
        clock.tick(60)


    stream.stop()
    stream.close()
    pygame.quit()

if __name__ == "__main__":
    main()
