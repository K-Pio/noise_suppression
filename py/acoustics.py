import math
from typing import List
from model import Vec2, Obstacle
from acoustics_c import intersects

def obstacle_attenuation(src: Vec2, lst: Vec2, obstacles: List[Obstacle]) -> float:
    att = 1.0
    for ob in obstacles:
        if intersects(float(src[0]), float(src[1]), 
                      float(lst[0]), float(lst[1]), 
                      float(ob.a[0]), float(ob.a[1]),
                      float(ob.b[0]), float(ob.b[1])):
            
            att *= (1.0 - ob.absorb)
    return att


# legacy:

"""def gain_distance(r: float, r0: float, rmax: float, gmin: float=0.02) -> float:
    if r > rmax: return 0.0
    return max(gmin, min(1.0, 1.0 / (1.0 + r / r0)**2))"""
"""def dist(a: Vec2, b: Vec2) -> float:
    return math.hypot(a[0]-b[0], a[1]-b[1])"""
"""def smooth(prev: float, target: float, alpha: float) -> float:
    return prev + alpha * (target - prev)"""
"""def smooth_channels(channels: dict, targets: tuple, alpha: float) -> dict:
    target_L, target_R = targets
    channels['l'] = smooth(channels['l'], target_L, alpha)
    channels['r'] = smooth(channels['r'], target_R, alpha)
    return channels"""
"""def pan_lr(src: Vec2, lst: Vec2, R: float) -> tuple[float,float]:
    dx = src[0] - lst[0]
    p = max(0.0, min(1.0, 0.5 + dx/(2*R)))
    L = math.cos(math.pi/2 * p)
    Rv = math.sin(math.pi/2 * p)
    return L, Rv"""
"""def obstacle_attenuation(src: Vec2, lst: Vec2, obstacles: List[Obstacle]) -> float:
    att = 1.0
    for ob in obstacles:
        if intersects(src, lst, ob.a, ob.b):
            att *= (1.0 - ob.absorb)
    return att"""
"""def intersects(a: Vec2, b: Vec2, c: Vec2, d: Vec2) -> bool:
    def orient(p, q, r):
        return (q[0]-p[0])*(r[1]-p[1]) - (q[1]-p[1])*(r[0]-p[0])
    o1 = orient(a,b,c); o2 = orient(a,b,d); o3 = orient(c,d,a); o4 = orient(c,d,b)
    if o1==0 and o2==0 and o3==0 and o4==0:
        return False
    return (o1*o2 <= 0) and (o3*o4 <= 0)"""