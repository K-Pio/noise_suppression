import pygame
from model import Map2D, SoundSource, Listener, Obstacle
from acoustics import dist, gain_distance, obstacle_attenuation, pan_lr
from audio import init_audio, start_sources, set_channel_lr
from render import init_window, draw

def main():
    size = 600
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

    font = pygame.font.SysFont("consolas", 16)
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

        # audio update
        for (src, ch) in channels:
            r = dist(src.pos, listener.pos)
            gd = gain_distance(r, src.r0, src.rmax)
            obs = obstacle_attenuation(src.pos, listener.pos, scene.obstacles)
            g = src.base_gain * gd * obs
            L, R = pan_lr(src.pos, listener.pos, R=scene.size/2)
            set_channel_lr(ch, L, R, g)

        draw(scene, sources, listener, screen, size_px=800)
        

        # debugging scheme
        # params for first source (src0):
        # src0 = sources[0]
        # r0 = dist(src0.pos, listener.pos)
        # gd0 = gain_distance(r0, src0.r0, src0.rmax)
        # obs0 = obstacle_attenuation(src0.pos, listener.pos, scene.obstacles)
        # g0 = src0.base_gain * gd0 * obs0
        # L0, R0 = pan_lr(src0.pos, listener.pos, R=scene.size/2)

        # overlay = [
        #     f"src0 r={r0:6.1f} gd={gd0:0.3f} obs={obs0:0.3f} g={g0:0.3f}",
        #     f"L={L0:0.3f} R={R0:0.3f}"
        # ]
        # y = 8
        # for line in overlay:
        #     surf = font.render(line, True, (230,230,230))
        #     screen.blit(surf, (8, y))
        #     y += 18
        
        pygame.display.flip()
        clock.tick(60)


    pygame.quit()

if __name__ == "__main__":
    main()
