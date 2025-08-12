import pygame
from model import Map2D, SoundSource, Listener, Obstacle

def init_window(size_px=800):
    pygame.display.set_caption("Sound map")
    return pygame.display.set_mode((size_px,size_px))

def draw(scene: Map2D, sources: list[SoundSource], listener: Listener, screen, size_px):
    screen.fill((20,20,24))
    s = size_px / scene.size
    # obstacles
    for ob in scene.obstacles:
        pygame.draw.line(screen, (180,70,70),
                         (ob.a[0]*s, ob.a[1]*s), (ob.b[0]*s, ob.b[1]*s), 3)
    # sources
    for src in sources:
        pygame.draw.circle(screen, (70,170,255), (int(src.pos[0]*s), int(src.pos[1]*s)), 6)
    # listener
    pygame.draw.circle(screen, (80,255,120), (int(listener.pos[0]*s), int(listener.pos[1]*s)), 7)
    pygame.display.flip()
