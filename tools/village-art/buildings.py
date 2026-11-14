"""Valbrume buildings, all modelled in world units centred on (0,0) footprint, ground z=0."""
import sys, json, time
import numpy as np
from engine import Vol, save2x
from gi import render, trim
S_B = 1.4
import engine; engine.VS_DEFAULT[0] = 1 / S_B
from kit3d import *

B = {}
def bld(name):
    def deco(f): B[name] = f; return f
    return deco

@bld('tavern')
def tavern():
    v = Vol(-52, 52, -48, 50, 0, 150)
    x0, x1, y0, y1 = -34, 34, -28, 28
    v.box(x0, x1, y0, y1, 0, 14, STONE)                       # stone ground floor plinth
    v.box(x0 + 1, x1 - 1, y0 + 1, y1 - 1, 14, 36, PLASTER)    # ground floor
    v.box(x0 - 3, x1 + 3, y0 - 3, y1 + 3, 36, 39, TIMBER)     # jetty beam
    v.box(x0 - 3, x1 + 3, y0 - 3, y1 + 3, 39, 62, PLASTER)    # jettied upper floor
    timber_frame(v, 'y', y1 - 1, x0 + 1, x1 - 1, 14, 36, spacing=13)
    timber_frame(v, 'x', x1 - 1, y0 + 1, y1 - 1, 14, 36, spacing=13)
    timber_frame(v, 'y', y1 + 3, x0 - 3, x1 + 3, 39, 62, spacing=10, braces=True)
    timber_frame(v, 'x', x1 + 3, y0 - 3, y1 + 3, 39, 62, spacing=10)
    v.roof(x0 - 9, x1 + 9, y0 - 10, y1 + 10, 58, 112, ROOF_R, axis='x', th=5, fill=PLASTER, curve=1.15)
    # gable dormer on the left face
    v.box(-8, 10, y1 + 2, y1 + 14, 60, 76, PLASTER)
    timber_frame(v, 'y', y1 + 14, -8, 10, 60, 76, spacing=9, braces=False)
    v.roof(-12, 14, y1 - 2, y1 + 18, 74, 92, ROOF_R, axis='y', th=4, fill=PLASTER)
    window(v, 'y', y1 + 14, -3, 5, 64, 72, shutters=None)
    # ridge cap
    v.box(x0 - 9, x1 + 9, -1.5, 1.5, 110, 114, ROOF_S)
    chimney(v, -20, -6, 80, 128, BRICK, 9)
    chimney(v, 24, 4, 90, 118, STONE_D, 7)
    # windows ground + upper (left face y=y1, right face x=x1)
    door(v, 'y', y1, -6, 6, 22, arch=True)
    for a in (-26, 16):
        window(v, 'y', y1 - 1, a, a + 9, 20, 30, shutters=CLOTH_G)
    for a in (-24, -6, 12):
        window(v, 'y', y1 + 3, a, a + 9, 44, 55, shutters=CLOTH_G)
    for a in (-14, 6):
        window(v, 'x', x1 - 1, a, a + 9, 20, 30)
        window(v, 'x', x1 + 3, a, a + 9, 44, 55, shutters=CLOTH_G)
    # hanging sign with mug emblem
    v.box(x1 + 3, x1 + 18, y1 - 2, y1, 52, 54, METAL)
    v.box(x1 + 8, x1 + 18, y1 - 1.4, y1 - 0.6, 38, 50, WOOD_L)
    v.box(x1 + 11, x1 + 15, y1 - 0.6, y1 + 0.4, 41, 47, GOLD)
    for xx in (x1 + 9, x1 + 17):
        v.box(xx - 0.5, xx + 0.5, y1 - 1.2, y1 - 0.8, 50, 52, METAL)
    lantern(v, -11, y1 + 3, 30); lantern(v, 11, y1 + 3, 30)
    for k, (bx, by) in enumerate(((x1 + 6, y1 - 10), (x1 + 6, y1 - 3), (x1 + 13, y1 + 4))):
        barrel(v, bx, by)
    crate(v, -30, y1 + 4, 8); crate(v, -29, y1 + 4, 6, z=8)
    # bench + table
    v.box(16, 30, y1 + 6, y1 + 9, 4, 5.5, WOOD_L); v.box(17, 18.5, y1 + 6, y1 + 9, 0, 4, TIMBER); v.box(27.5, 29, y1 + 6, y1 + 9, 0, 4, TIMBER)
    return v


def gable_frame(v, face, c, a0, a1, z0, ztop, mat=TIMBER):
    m = (a0 + a1) / 2; hw = (a1 - a0) / 2
    for k in np.arange(-hw, hw, 0.5):
        zt = z0 + (ztop - z0) * (1 - abs(k) / hw)
        if abs(k) < 1 or abs(abs(k) - hw * 0.5) < 0.8:
            fbox(v, face, c, m + k, m + k + 0.5, z0, zt, -0.5, 1, mat)
    fbox(v, face, c, a0, a1, z0 + (ztop - z0) * 0.45, z0 + (ztop - z0) * 0.45 + 1.6, -0.5, 1, mat)

def spire(v, cx, cy, r, z0, z1, mat, finial=GOLD, p=1.7):
    v.cone(cx, cy, r, z0, z1, mat, p=p)
    v.cyl(cx, cy, 0.9, z1 - 2, z1 + 8, finial)
    v.ell(cx, cy, z1 + 4, 2, 2, 2, finial)

@bld('townhall')
def townhall():
    v = Vol(-80, 80, -66, 70, 0, 210)
    x0, x1, y0, y1 = -58, 58, -40, 40
    v.box(x0, x1, y0, y1, 0, 18, STONE)
    v.box(x0 - 2, x1 + 2, y0 - 2, y1 + 2, 0, 4, STONE_D)
    v.box(x0 + 1, x1 - 1, y0 + 1, y1 - 1, 18, 44, PLASTER)
    v.box(x0 - 2, x1 + 2, y0 - 2, y1 + 2, 44, 47, TIMBER)
    v.box(x0 - 2, x1 + 2, y0 - 2, y1 + 2, 47, 70, PLASTER)
    timber_frame(v, 'y', y1 - 1, x0 + 1, x1 - 1, 18, 44, spacing=14)
    timber_frame(v, 'x', x1 - 1, y0 + 1, y1 - 1, 18, 44, spacing=14)
    timber_frame(v, 'y', y1 + 2, x0 - 2, x1 + 2, 47, 70, spacing=11)
    timber_frame(v, 'x', x1 + 2, y0 - 2, y1 + 2, 47, 70, spacing=11)
    # corner stone quoins
    for (cx, cy) in ((x1, y1), (x0, y1), (x1, y0)):
        for zz in range(0, 70, 8):
            v.box(cx - 3, cx + 3, cy - 3, cy + 3, zz, zz + 5, STONE)
    v.roof(x0 - 10, x1 + 10, y0 - 10, y1 + 10, 66, 126, ROOF_B, axis='x', hip=0.9, th=5, fill=PLASTER, curve=1.25)
    v.box(-23, 23, -1.5, 1.5, 123, 128, GOLD)
    for xx in (-23, 23):
        v.ell(xx, 0, 130, 2.5, 2.5, 3.5, GOLD)
    # belfry / clock tower rising from the front of the roof
    bx0, bx1, by0, by1 = -14, 14, 18, 46
    v.box(bx0, bx1, by0, by1, 0, 112, STONE)
    v.box(bx0 - 2, bx1 + 2, by0 - 2, by1 + 2, 110, 116, STONE_D)
    v.box(bx0, bx1, by0, by1, 116, 146, PLASTER)
    timber_frame(v, 'y', by1, bx0, bx1, 116, 146, spacing=7, braces=False)
    timber_frame(v, 'x', bx1, by0, by1, 116, 146, spacing=7, braces=False)
    for face, c in (('y', by1), ('x', bx1)):
        fbox(v, face, c, -6 if face == 'y' else 26, 6 if face == 'y' else 38, 124, 140, -4, 1, 0)
        fbox(v, face, c, -6 if face == 'y' else 26, 6 if face == 'y' else 38, 124, 140, -4, -3, COAL)
    v.box(-2, 2, 30, 34, 120, 137, GOLD)  # bell
    v.roof(bx0 - 6, bx1 + 6, by0 - 6, by1 + 6, 144, 200, ROOF_B, axis='x', hip=1.0, th=4, curve=1.6, fill=PLASTER)
    v.cyl(0, 32, 1, 196, 208, GOLD); v.ell(0, 32, 203, 2.2, 2.2, 2.2, GOLD)
    # clock on the belfry shaft
    v.put((-8, 8, by1, by1 + 2, 84, 100), lambda X, Y, Z: ((X) ** 2 + (Z - 92) ** 2 <= 64) & (Y < by1 + 1.5), GOLD)
    v.put((-8, 8, by1, by1 + 2.5, 84, 100), lambda X, Y, Z: ((X) ** 2 + (Z - 92) ** 2 <= 36) & (Y < by1 + 2), CREAM)
    v.box(-0.5, 0.5, by1 + 1.8, by1 + 2.6, 92, 97, COAL); v.box(0, 4, by1 + 1.8, by1 + 2.6, 91.5, 92.5, COAL)
    door(v, 'y', by1, -8, 8, 34, arch=True)
    window(v, 'y', by1, -5, 5, 56, 70, arch=True)
    window(v, 'x', bx1, 27, 37, 56, 70, arch=True)
    # main facade windows
    for a in (-50, -34, 22, 40):
        window(v, 'y', y1 - 1, a, a + 9, 24, 36, shutters=CLOTH_B)
        window(v, 'y', y1 + 2, a, a + 9, 52, 63, shutters=CLOTH_B)
    for a in (-30, -12, 6, 22):
        window(v, 'x', x1 - 1, a, a + 9, 24, 36, shutters=CLOTH_B)
        window(v, 'x', x1 + 2, a, a + 9, 52, 63, shutters=CLOTH_B)
    # dormers on the roof
    for a in (-40, 30):
        v.box(a - 7, a + 7, y1 - 6, y1 + 6, 70, 86, PLASTER)
        v.roof(a - 10, a + 10, y1 - 10, y1 + 10, 84, 98, ROOF_B, axis='y', th=3, fill=PLASTER)
        window(v, 'y', y1 + 6, a - 3, a + 3, 74, 82, cross=False)
    banner(v, 'y', y1 + 2, -24, 66, 22, 8, CLOTH_B, GOLD, GOLD)
    banner(v, 'y', y1 + 2, 30 - 2, 66, 22, 8, CLOTH_B, GOLD, GOLD) if False else None
    banner(v, 'x', x1 + 2, -2, 66, 22, 8, CLOTH_B, GOLD, GOLD)
    # front steps + lanterns
    for k in range(3):
        v.box(-12 - 3 * (2 - k), 12 + 3 * (2 - k), by1, by1 + 9 - 3 * k, 2 * k, 2 * k + 2, STONE_D)
    lantern(v, -18, by1 + 2, 30); lantern(v, 18, by1 + 2, 30)
    chimney(v, -42, -20, 90, 120, BRICK, 8)
    return v

@bld('magetower')
def magetower():
    v = Vol(-46, 46, -46, 46, 0, 262)
    v.cyl(0, 0, 25, 0, 10, STONE_D)
    v.put((-24, 24, -24, 24, 10, 130), lambda X, Y, Z: X ** 2 + Y ** 2 <= (22 - (Z - 10) * 0.035) ** 2, PAL_ID('tower_st'))
    for ang in (0.4, 1.25, 2.1, 3.0, 3.9, 4.8, 5.6):
        bx, by = 22 * np.cos(ang), 22 * np.sin(ang)
        v.put((bx - 6, bx + 6, by - 6, by + 6, 0, 60), lambda X, Y, Z, bx=bx, by=by: ((X - bx) ** 2 + (Y - by) ** 2 <= 16) & (Z < 60 - 2.2 * np.sqrt((X - bx * 1.25) ** 2 + (Y - by * 1.25) ** 2) * 2.4) , STONE_D)
    # corbelled balcony
    v.cone(0, 0, 21, 112, 130, STONE_D, r1=30, p=1.0) if False else None
    v.put((-31, 31, -31, 31, 112, 132), lambda X, Y, Z: X ** 2 + Y ** 2 <= (19 + (Z - 112) * 0.6) ** 2, STONE_D)
    v.cyl(0, 0, 31, 132, 136, STONE)
    for k in range(20):
        a = k / 20 * 2 * np.pi
        v.cyl(30 * np.cos(a), 30 * np.sin(a), 1.4, 136, 143, STONE)
    v.cyl(0, 0, 31.5, 143, 145.5, STONE, rin=28)
    # upper chamber
    v.cyl(0, 0, 18, 136, 176, PAL_ID('tower_st'))
    for k in range(6):
        a = k / 6 * 2 * np.pi + 0.3
        v.cyl(18 * np.cos(a), 18 * np.sin(a), 2.2, 136, 176, STONE_D)
    v.cyl(0, 0, 20, 174, 179, GOLD)
    # flared curved spire
    v.put((-32, 32, -32, 32, 176, 250), lambda X, Y, Z: (X ** 2 + Y ** 2 <= (2 + 28 * (1 - np.clip((Z - 176) / 74, 0, 1)) ** 2.1) ** 2), PAL_ID('tower_roof'))
    v.cyl(0, 0, 1, 246, 256, GOLD); v.ell(0, 0, 252, 2.5, 2.5, 2.5, GOLD)
    # floating crystal (detached voxels)
    v.put((-5, 5, -5, 5, 236, 262), lambda X, Y, Z: (np.abs(X) + np.abs(Y)) * 1.0 <= 4.2 * (1 - np.abs(Z - 252) / 9) , 0) if False else None
    # windows (arched, magic glow) on the visible faces
    def rwin(ang, z, h, hw, R):
        def m(X, Y, Z, d0, d1, ext=0):
            an = np.arctan2(Y, X); dr = np.hypot(X, Y)
            da = np.abs(((an - ang + np.pi) % (2 * np.pi)) - np.pi) * R
            top = z + h + np.sqrt(np.clip((hw + ext) ** 2 - da ** 2, 0, None))
            return (da <= hw + ext) & (Z >= z - ext) & (Z < top + ext) & (dr >= d0) & (dr <= d1)
        bb = (-R - 6, R + 6, -R - 6, R + 6, z - 3, z + h + hw + 3)
        v.put(bb, lambda X, Y, Z: m(X, Y, Z, R - 1.5, R + 1.6, 1.3), GOLD)
        v.put(bb, lambda X, Y, Z: m(X, Y, Z, R - 3, R + 2), 0)
        v.put(bb, lambda X, Y, Z: m(X, Y, Z, R - 4, R - 2.2), MAGIC)
        v.put(bb, lambda X, Y, Z: m(X, Y, Z, R - 2.5, R - 0.5) & (np.abs(Z - (z + h * 0.55)) < 0.6), GOLD)
    for ang, z in ((0.3, 34), (1.3, 34), (0.8, 68), (1.55, 96), (0.45, 98)):
        rwin(ang, z, 9, 3.2, 22 - (z - 10) * 0.035)
    for ang in (0.35, 0.95, 1.55):
        rwin(ang, 148, 12, 3.2, 18)
    for zz in (62, 92):
        v.cyl(0, 0, 22.6 - (zz - 10) * 0.035, zz, zz + 2.5, STONE_D)
    for ang in (0.2, 1.4):
        cx, cy = 31 * np.cos(ang), 31 * np.sin(ang)
        for zz in np.arange(110, 134, 0.5):
            w = 4.5 if zz > 114 else (zz - 110) * 1.1
            v.put((cx - 6, cx + 6, cy - 6, cy + 6, zz, zz + 0.5), lambda X, Y, Z, cx=cx, cy=cy, w=w, ang=ang: (np.abs(-(X - cx) * np.sin(ang) + (Y - cy) * np.cos(ang)) <= w) & (np.abs((X - cx) * np.cos(ang) + (Y - cy) * np.sin(ang)) < 0.8), PAL[31] and 31)
    # rune band glowing at the base
    v.put((-26, 26, -26, 26, 14, 18), lambda X, Y, Z: (X ** 2 + Y ** 2 <= 22.8 ** 2) & (X ** 2 + Y ** 2 > 20.5 ** 2) & (np.sin(np.arctan2(Y, X) * 22) > 0.2), MAGIC)
    # door
    a = 0.8; cx, cy = 23 * np.cos(a), 23 * np.sin(a)
    v.put((cx - 9, cx + 9, cy - 9, cy + 9, 0, 30), lambda X, Y, Z: ((X - cx) ** 2 + (Y - cy) ** 2 <= 8.5 ** 2) & (Z < 18 + np.sqrt(np.clip(36 - ((X - cx) * 0.7 - (Y - cy) * 0.7) ** 2, 0, None))), 0)
    v.put((cx - 9, cx + 9, cy - 9, cy + 9, 0, 30), lambda X, Y, Z: ((X - cx) ** 2 + (Y - cy) ** 2 <= 8.5 ** 2) & (X ** 2 + Y ** 2 <= 19 ** 2) & (Z < 18 + np.sqrt(np.clip(36 - ((X - cx) * 0.7 - (Y - cy) * 0.7) ** 2, 0, None))), PLANK)
    v.cyl(cx + 4, cy + 4, 4, 0, 1.5, STONE)
    # banners on the balcony
    return v

def PAL_ID(k):
    return {'tower_st': 48, 'tower_roof': 49, 'temple_dome': 50}[k]

PAL[48] = Mat('#8c8aa6', t_stone, params={'c': (0, 0), 'r': 22, 'ch': 6, 'bl': 9, 'moss': 40, 'mossh': 24}, hs=24)
PAL[49] = Mat('#6b3fb0', t_shingle, params={'c': (0, 0), 'r': 24, 'round': True, 'rh': 3.2, 'w': 4.5}, hs=26, light=1.35)
PAL[50] = Mat('#e0a32a', t_shingle, params={'c': (0, 0), 'r': 20, 'round': True, 'rh': 3.0, 'w': 4}, hs=20, light=1.38)

@bld('forge')
def forge():
    v = Vol(-56, 56, -50, 52, 0, 150)
    x0, x1, y0, y1 = -36, 20, -30, 26
    v.box(x0, x1, y0, y1, 0, 40, STONE_D)
    v.roof(x0 - 7, x1 + 7, y0 - 8, y1 + 8, 36, 82, ROOF_S, axis='x', th=4, fill=STONE_D)
    gable_frame(v, 'x', x1, y0, y1, 40, 78)
    # open lean-to smithy on the right
    lx0, lx1 = x1, x1 + 26
    v.box(lx0, lx1, y0 + 4, y1, 0, 2, STONE)
    for (px, py) in ((lx1 - 2, y1 - 4), (lx1 - 2, y0 + 6)):
        v.box(px - 2, px + 2, py - 2, py + 2, 0, 34, TIMBER)
    v.put((lx0 - 2, lx1 + 6, y0, y1 - 2, 30, 50), lambda X, Y, Z: (Z <= 48 - (X - lx0) * 0.55) & (Z > 44 - (X - lx0) * 0.55), ROOF_S)
    barrel(v, lx0 + 8, y0 + 10); barrel(v, lx0 + 8, y0 + 18); crate(v, lx0 + 14, y0 + 8, 8)
    # furnace protruding from the left face with a glowing arched mouth
    fx0, fx1, fy1 = -2, 16, y1 + 12
    v.box(fx0, fx1, y1, fy1, 0, 28, BRICK)
    v.box(fx0 - 1, fx1 + 1, y1, fy1 + 1, 26, 30, STONE_D)
    v.put((fx0 + 3, fx1 - 3, fy1 - 4, fy1 + 1, 2, 20), lambda X, Y, Z: (Z < 12 + np.sqrt(np.clip(25 - (X - 7) ** 2, 0, None))) & (np.abs(X - 7) <= 5), 0)
    v.put((fx0 + 3, fx1 - 3, fy1 - 6, fy1 - 3, 2, 20), lambda X, Y, Z: (Z < 12 + np.sqrt(np.clip(25 - (X - 7) ** 2, 0, None))) & (np.abs(X - 7) <= 5), FIRE)
    v.put((fx0 + 1, fx1 - 1, fy1 - 1, fy1 + 1.5, 0, 22), lambda X, Y, Z: (np.abs(np.hypot(X - 7, np.maximum(Z - 12, 0)) - 6.5) < 1.3) & (Z > 1), STONE)
    v.box(fx0 + 4, fx1 - 4, fy1, fy1 + 3, 0, 3, COAL)
    chimney(v, 7, y1 + 4, 28, 104, BRICK, 10)
    v.box(4, 10, y1 + 1, y1 + 7, 101, 103, FIRE)
    # anvil out front
    ax_, ay_ = x1 + 10, y1 + 6
    v.box(ax_, ax_ + 4, ay_, ay_ + 4, 0, 7, STONE_D)
    v.box(ax_ - 2, ax_ + 7, ay_ - 0.5, ay_ + 4.5, 7, 11, METAL)
    v.box(ax_ + 7, ax_ + 10, ay_ + 1, ay_ + 3, 8.5, 10.5, METAL)
    # tool rack on the wall
    for k in range(4):
        xx = -30 + k * 4
        v.box(xx, xx + 1, y1, y1 + 1.2, 12, 26, WOOD_L)
        v.box(xx - 1, xx + 2, y1, y1 + 1.6, 24 - (k % 2) * 3, 27, METAL)
    # water trough + quench barrel
    barrel(v, lx1 + 4, y1 - 4)
    v.box(lx0 + 2, lx0 + 14, y1 + 2, y1 + 8, 0, 6, PLANK); v.box(lx0 + 3, lx0 + 13, y1 + 3, y1 + 7, 4, 5.5, WATER)
    # door + windows on the stone house
    door(v, 'y', y1, -20, -8, 24, arch=True)
    window(v, 'x', x1, -26, -18, 18, 28)
    # gear sign
    gy = y1 + 1
    v.put((-34, -24, gy, gy + 2, 26, 40), lambda X, Y, Z: (((X + 29) ** 2 + (Z - 33) ** 2) <= (4.6 + 1.3 * (np.sin(np.arctan2(Z - 33, X + 29) * 8) > 0)) ** 2) & (((X + 29) ** 2 + (Z - 33) ** 2) > 2.0 ** 2), GOLD)
    v.box(-30, -28, gy - 1, gy, 38, 46, METAL)
    # log pile + wheel
    for k in range(3):
        v.put((x0 - 10, x0, y1 - 20, y1, 0, 12), lambda X, Y, Z, k=k: ((Z - 3 - k * 3.5) ** 2 + ((Y - (y1 - 16 + (k % 2) * 3.5)) % 7 - 3.5) ** 2 <= 9.5) & (X >= x0 - 9) & (X < x0 - 1) & (Y < y1 - 2 - k * 2), BARK)
    for zz in range(4):
        pass
    lantern(v, -2, y1 + 2, 30)
    return v

@bld('barracks')
def barracks():
    v = Vol(-74, 74, -52, 56, 0, 190)
    x0, x1, y0, y1 = -58, 34, -30, 30
    v.box(x0, x1, y0, y1, 0, 46, STONE)
    v.box(x0 - 2, x1 + 2, y0 - 2, y1 + 2, 44, 49, STONE_D)
    # crenellations
    for a in np.arange(x0 - 2, x1 + 2, 7):
        v.box(a, a + 4, y1 - 2, y1 + 2, 49, 55, STONE_D)
        v.box(a, a + 4, y0 - 2, y0 + 2, 49, 55, STONE_D)
    for a in np.arange(y0 - 2, y1 + 2, 7):
        v.box(x1 - 2, x1 + 2, a, a + 4, 49, 55, STONE_D)
        v.box(x0 - 2, x0 + 2, a, a + 4, 49, 55, STONE_D)
    v.roof(x0 + 2, x1 - 2, y0 + 2, y1 - 2, 46, 78, ROOF_R, axis='x', th=4, fill=STONE)
    # corner keep
    kx, ky = x1, y1 - 6
    v.box(kx - 14, kx + 14, ky - 14, ky + 14, 0, 98, STONE)
    v.box(kx - 16, kx + 16, ky - 16, ky + 16, 96, 102, STONE_D)
    for a in np.arange(-16, 16, 6):
        v.box(kx + a, kx + a + 3.5, ky + 13, ky + 16, 102, 108, STONE_D)
        v.box(kx + 13, kx + 16, ky + a, ky + a + 3.5, 102, 108, STONE_D)
    v.roof(kx - 12, kx + 12, ky - 12, ky + 12, 102, 156, ROOF_R, axis='x', hip=1.0, th=4, curve=1.5, fill=STONE)
    v.cyl(kx, ky, 1, 152, 160, GOLD)
    flag(v, kx, ky, 156, 24, CLOTH_R, 18)
    for zz in (30, 64):
        window(v, 'y', ky + 14, kx - 3, kx + 3, zz, zz + 12, cross=False, sill=False)
        window(v, 'x', kx + 14, ky - 3, ky + 3, zz, zz + 12, cross=False, sill=False)
    # gate
    door(v, 'y', y1, -26, -6, 30, arch=True, leaf=PLANK)
    for a in (-48, 4, 18):
        window(v, 'y', y1, a, a + 4, 22, 34, cross=False, sill=False)
    banner(v, 'y', y1, -38, 44, 26, 9, CLOTH_R, GOLD, GOLD)
    banner(v, 'y', y1, 8, 44, 26, 9, CLOTH_R, GOLD, GOLD) if False else None
    # weapon rack + training dummy
    rx = -58
    v.box(rx, rx + 22, y1 + 8, y1 + 10, 0, 3, TIMBER); v.box(rx, rx + 22, y1 + 8, y1 + 10, 14, 16, TIMBER)
    for k in range(5):
        xx = rx + 2 + k * 4.5
        v.box(xx, xx + 1, y1 + 8.5, y1 + 9.5, 0, 26, WOOD_L)
        v.cone(xx + 0.5, y1 + 9, 1.6, 26, 31, METAL)
    dx, dy = 2, y1 + 18
    v.cyl(dx, dy, 1.2, 0, 28, TIMBER)
    v.box(dx - 8, dx + 8, dy - 1, dy + 1, 20, 22, TIMBER)
    v.ell(dx, dy, 22, 5, 4, 7, HAY); v.ell(dx, dy, 32, 3.5, 3.5, 3.5, HAY)
    v.ell(dx, dy + 0.5, 21, 5.3, 4.3, 3, CLOTH_R)
    return v

@bld('temple')
def temple():
    v = Vol(-64, 64, -60, 72, 0, 210)
    x0, x1, y0, y1 = -40, 40, -40, 34
    for k in range(3):
        v.box(x0 - 8 + 2 * k, x1 + 8 - 2 * k, y0 - 8 + 2 * k, y1 + 26 - 2 * k, 2 * k, 2 * k + 2, MARBLE)
    v.box(x0, x1, y0, y1, 6, 56, MARBLE)
    v.box(x0 - 3, x1 + 3, y0 - 3, y1 + 3, 54, 60, GOLD)
    v.box(x0 - 2, x1 + 2, y0 - 2, y1 + 2, 60, 64, MARBLE)
    # portico with columns on the left (+y) face
    for a in np.linspace(x0 + 4, x1 - 4, 5):
        v.cyl(a, y1 + 16, 3.4, 6, 54, MARBLE)
        v.box(a - 4.5, a + 4.5, y1 + 11.5, y1 + 20.5, 50, 54, MARBLE)
        v.cyl(a, y1 + 16, 4.4, 6, 9, MARBLE)
    v.box(x0 - 3, x1 + 3, y1, y1 + 22, 54, 60, GOLD)
    v.box(x0 - 2, x1 + 2, y1, y1 + 21, 60, 64, MARBLE)
    v.roof(x0 - 4, x1 + 4, y0 - 4, y1 + 22, 64, 92, PAL_ID('temple_dome'), axis='y', th=4, fill=MARBLE)
    # pediment sun disk
    v.put((-9, 9, y1 + 21, y1 + 24, 66, 86), lambda X, Y, Z: (X ** 2 + (Z - 74) ** 2 <= 42) & (Y < y1 + 23), HOLY)
    # drum + dome
    v.cyl(0, -6, 22, 80, 110, MARBLE)
    for k in range(10):
        a = k / 10 * 2 * np.pi
        v.cyl(22 * np.cos(a), -6 + 22 * np.sin(a), 2.4, 80, 110, GOLD)
    v.cyl(0, -6, 24, 108, 112, GOLD)
    v.put((-24, 24, -30, 18, 112, 170), lambda X, Y, Z: (X ** 2 + (Y + 6) ** 2) / 23.0 ** 2 + ((Z - 112) / 44.0) ** 2 <= 1, PAL_ID('temple_dome'))
    v.cyl(0, -6, 4, 152, 166, GOLD); v.cone(0, -6, 3, 166, 186, GOLD, p=1.5)
    v.ell(0, -6, 192, 4.2, 4.2, 4.2, HOLY)
    for ang in (0.6, 1.4):
        cx, cy = 22 * np.cos(ang), -6 + 22 * np.sin(ang)
        v.put((cx - 4, cx + 4, cy - 4, cy + 4, 86, 104), lambda X, Y, Z, cx=cx, cy=cy: ((X - cx) ** 2 + (Y - cy) ** 2 <= 9) & (Z < 102), HOLY)
    # holy windows on the cella
    for a in (-4,):
        window(v, 'x', x1, -26, -18, 18, 38, frame=GOLD, glass=HOLY, arch=True, cross=False, sill=False)
        window(v, 'x', x1, -2, 6, 18, 38, frame=GOLD, glass=HOLY, arch=True, cross=False, sill=False)
        window(v, 'x', x1, 20, 28, 18, 38, frame=GOLD, glass=HOLY, arch=True, cross=False, sill=False)
    door(v, 'y', y1, -8, 8, 30, frame=GOLD, leaf=PLANK, arch=True)
    # braziers
    for bx in (x0 - 4, x1 + 4):
        v.cyl(bx, y1 + 30, 1.5, 0, 14, METAL); v.cone(bx, y1 + 30, 4.5, 14, 18, GOLD, r1=4.5) if False else v.cyl(bx, y1 + 30, 4, 14, 18, GOLD)
        v.cone(bx, y1 + 30, 3.4, 18, 26, FIRE, p=1.3)
    return v

@bld('barn')
def barn():
    v = Vol(-56, 60, -44, 48, 0, 140)
    x0, x1, y0, y1 = -40, 40, -26, 26
    v.box(x0, x1, y0, y1, 0, 4, STONE)
    v.box(x0 + 1, x1 - 1, y0 + 1, y1 - 1, 4, 40, PAL_ID('barn_pl'))
    # gambrel roof (convex profile) along y so the gable faces right
    v.roof(x0 - 6, x1 + 6, y0 - 5, y1 + 5, 38, 96, ROOF_S, axis='y', th=5, curve=0.6, fill=PAL_ID('barn_pl'))
    for zz in (40,):
        pass
    gable_frame(v, 'y', y1 - 1, x0, x1, 40, 92, mat=CREAM) if False else None
    # big X doors on the left face and the hayloft
    for (a0, a1) in ((-14, 14),):
        fbox(v, 'y', y1 - 1, a0, a1, 4, 34, -2, 1.2, CREAM)
        fbox(v, 'y', y1 - 1, a0 + 2, a1 - 2, 6, 32, -3, 1.4, 0)
        fbox(v, 'y', y1 - 1, a0 + 2, a1 - 2, 6, 32, -3, -1, PAL_ID('barn_pl'))
        for s in np.linspace(0, 1, 60):
            for sg in (0, 1):
                xx = a0 + 2 + (a1 - a0 - 4) * (s if sg else 1 - s); zz = 6 + 26 * s
                fbox(v, 'y', y1 - 1, xx - 1, xx + 1, zz - 1, zz + 1, -1.5, 0.6, CREAM)
        fbox(v, 'y', y1 - 1, -0.6, 0.6, 6, 32, -1.5, 0.6, CREAM)
    for face, c, a0, a1 in (('y', y1 - 1, -38, -26), ('y', y1 - 1, 26, 38), ('x', x1 - 1, -12, 0)):
        window(v, face, c, a0 + 3, a1 - 3, 16, 26, frame=CREAM, cross=True)
    # hayloft on the right gable
    fbox(v, 'x', x1 + 1, -9, 9, 50, 70, -1, 1, CREAM); fbox(v, 'x', x1 + 1, -7, 7, 52, 68, -4, 2, 0)
    v.ell(x1 - 3, 0, 52, 3, 7, 4, HAY)
    v.box(x1 - 2, x1 + 12, -1, 1, 74, 76, TIMBER)
    v.box(x1 + 10, x1 + 11, -0.5, 0.5, 60, 74, ROPE)
    # hay bales + cart wheel
    for (hx_, hy_, hz) in ((x1 + 6, y1 + 6, 0), (x1 + 14, y1 + 2, 0), (x1 + 9, y1 + 3, 8)):
        v.box(hx_, hx_ + 9, hy_, hy_ + 7, hz, hz + 8, HAY)
        v.box(hx_ + 2, hx_ + 3, hy_ - 0.3, hy_ + 7.3, hz, hz + 8.3, ROPE)
    v.put((x0 - 4, x0 + 10, y1 + 2, y1 + 4, 0, 16), lambda X, Y, Z: (np.abs(np.hypot(X - x0 - 3, Z - 7.5) - 6.5) < 1.1) | ((np.hypot(X - x0 - 3, Z - 7.5) < 6.5) & ((np.abs(X - x0 - 3) < 0.6) | (np.abs(Z - 7.5) < 0.6))), PLANK)
    return v

PAL[51] = Mat('#a33a2a', t_plank, params={'w': 4}, hs=26)
_old = PAL_ID
def PAL_ID(k):
    return {'tower_st': 48, 'tower_roof': 49, 'temple_dome': 50, 'barn_pl': 51}[k]

def stall(cloth):
    v = Vol(-30, 30, -24, 26, 0, 70)
    x0, x1, y0, y1 = -20, 20, -12, 12
    for (px, py) in ((x0, y0), (x1 - 2, y0), (x0, y1 - 2), (x1 - 2, y1 - 2)):
        v.box(px, px + 2, py, py + 2, 0, 40 if py < 0 else 30, TIMBER)
    v.box(x0, x1, y0, y1 + 2, 12, 14, WOOD_L)
    v.box(x0, x1, y1, y1 + 2, 0, 12, PLANK)
    # awning sloping toward the viewer (+y) with scalloped edge
    v.put((x0 - 3, x1 + 3, y0 - 4, y1 + 2, 30, 48),
          lambda X, Y, Z: (np.abs(Z - (37 + (Y - y0) * 0.32)) < 1.0) & (Y < y1 - 4 - (np.sin((X - x0) * 0.8) > 0) * 1.5), cloth)
    for px in (x0, x1 - 2):
        v.box(px, px + 2, y1 - 6, y1 - 4, 0, 44, TIMBER)
    # produce
    for k, (mat, cx) in enumerate(((APPLE, -14), (PUMPKIN, -3), (CABBAGE, 9))):
        crate(v, cx - 4.5, y1 - 10, 9, PLANK, z=14)
        for j in range(7):
            ox, oy = (j % 3) * 2.6 - 2.6, (j // 3) * 2.6 - 2.6
            v.ell(cx + ox + 0.4, y1 - 5.5 + oy, 23.5 + (j % 2) * 0.6, 1.8, 1.8, 1.6, mat)
    crate(v, x1 + 2, y1 - 6, 8, PLANK); v.ell(x1 + 6, y1 - 2, 9, 3.5, 3.5, 2, APPLE)
    barrel(v, x0 - 5, y1 + 2, 3.2, 8)
    return v

@bld('stall-red')
def stall_r(): return stall(RED_AWN)
@bld('stall-blue')
def stall_b(): return stall(BLU_AWN)
@bld('stall-green')
def stall_g(): return stall(GRN_AWN)

@bld('well')
def well():
    v = Vol(-22, 22, -22, 22, 0, 70)
    PAL[52] = Mat('#9a8f86', t_stone, params={'c': (0, 0), 'r': 12, 'ch': 4.5, 'bl': 6, 'moss': 40, 'mossh': 10})
    v.cyl(0, 0, 13, 0, 13, 52, rin=9)
    v.cyl(0, 0, 14, 12, 15, STONE_D, rin=9)
    v.cyl(0, 0, 9, 0, 9, WATER)
    for py in (-12, 12):
        v.box(-1.5, 1.5, py - 1.5, py + 1.5, 13, 40, TIMBER)
    v.cyl(0, 0, 0, 0, 0, 0) if False else None
    v.box(-1, 1, -14, 14, 30, 32.5, WOOD_L)
    v.box(-1, 1, 14, 18, 28, 29.5, METAL)
    v.box(-2.5, 2.5, -1.5, 1.5, 20, 25, PLANK); v.box(-0.3, 0.3, -0.3, 0.3, 25, 30, ROPE)
    v.roof(-12, 12, -18, 18, 36, 52, ROOF_R, axis='y', th=3.5)
    v.box(-12, 12, -0.8, 0.8, 50, 53, TIMBER) if False else None
    return v

@bld('noticeboard')
def noticeboard():
    v = Vol(-22, 22, -10, 12, 0, 56)
    for px in (-15, 13):
        v.box(px, px + 2.5, -1, 1.5, 0, 42, TIMBER)
    v.box(-16, 16, -0.5, 1.5, 14, 36, PLANK)
    v.box(-17, 17, -0.6, 2.2, 13, 14.5, TIMBER); v.box(-17, 17, -0.6, 2.2, 35.5, 37, TIMBER)
    papers = [(-13, 18, 8, 9, PAPER), (-3, 24, 7, 9, CREAM), (6, 17, 7, 8, PAPER), (-12, 28, 6, 6, CREAM), (5, 26, 8, 7, PAPER)]
    for (a, z, w, h, m) in papers:
        v.box(a, a + w, 1.5, 2.1, z, z + h, m)
        v.box(a + w / 2 - 0.5, a + w / 2 + 0.5, 2.0, 2.5, z + h - 1.5, z + h - 0.5, CLOTH_R)
    v.roof(-19, 19, -5, 7, 38, 48, ROOF_R, axis='x', th=2.5)
    return v

@bld('campfire')
def campfire():
    v = Vol(-14, 14, -14, 14, 0, 26)
    for k in range(9):
        a = k / 9 * 2 * np.pi
        v.ell(9 * np.cos(a), 9 * np.sin(a), 1.2, 2.8, 2.6, 2.2, STONE_D)
    for a in (0.3, 1.9, 3.5, 5.0):
        c, s = np.cos(a), np.sin(a)
        v.capsule((6 * c, 6 * s, 1.2), (-1 * c, -1 * s, 4.5), 1.4, BARK)
    v.cyl(0, 0, 3.5, 1, 3, COAL)
    v.put((-6, 6, -6, 6, 2, 22), lambda X, Y, Z: (X ** 2 + Y ** 2) <= (4.6 * (1 - (Z - 2) / 18) ** 1.2 + 0.9 * np.sin(Z * 0.9 + np.arctan2(Y, X) * 3)) ** 2, FIRE)
    return v

def canopy(v, cx, cy, cz, r, mat, seed=1, n=9):
    rng = np.random.default_rng(seed)
    blobs = [(cx, cy, cz, r * 0.8)]
    for k in range(n):
        a = rng.uniform(0, 2 * np.pi); e = rng.uniform(-0.6, 0.8)
        d = r * rng.uniform(0.45, 0.7)
        blobs.append((cx + d * np.cos(a) * np.cos(e), cy + d * np.sin(a) * np.cos(e), cz + d * np.sin(e) * 0.8, r * rng.uniform(0.42, 0.58)))
    for (bx, by, bz, br) in blobs:
        v.put((bx - br - 2, bx + br + 2, by - br - 2, by + br + 2, bz - br - 2, bz + br + 2),
              lambda X, Y, Z, bx=bx, by=by, bz=bz, br=br: (X - bx) ** 2 + (Y - by) ** 2 + ((Z - bz) * 1.1) ** 2 <= (br + 1.4 * (hash3(np.floor(X / 2).astype(np.int64), np.floor(Y / 2).astype(np.int64), np.floor(Z / 2).astype(np.int64), 5) - 0.5) * 2) ** 2, mat)

@bld('tree-oak')
def oak():
    v = Vol(-34, 34, -34, 34, 0, 96)
    v.put((-6, 6, -6, 6, 0, 50), lambda X, Y, Z: X ** 2 + Y ** 2 <= (2.6 + 3.2 * np.clip(1 - Z / 9, 0, 1) ** 2) ** 2, BARK)
    v.capsule((0, 0, 30), (10, -4, 46), 1.8, BARK); v.capsule((0, 0, 32), (-9, 6, 44), 1.8, BARK)
    canopy(v, 0, 0, 52, 27, LEAF, seed=3, n=12)
    return v

@bld('tree-pine')
def pine():
    v = Vol(-22, 22, -22, 22, 0, 110)
    v.cyl(0, 0, 2.4, 0, 30, BARK)
    for k, (z0, r) in enumerate(((16, 19), (36, 16), (54, 12.5), (70, 9))):
        v.put((-r - 2, r + 2, -r - 2, r + 2, z0, z0 + 30),
              lambda X, Y, Z, z0=z0, r=r: np.hypot(X, Y) <= (r * (1 - (Z - z0) / 30) + 1.4 * np.sin(np.arctan2(Y, X) * 9) * (1 - (Z - z0) / 30)), LEAF_D)
    return v

@bld('bush')
def bush():
    v = Vol(-18, 18, -18, 18, 0, 26)
    canopy(v, 0, 0, 8, 11, LEAF_F, seed=7, n=7)
    return v

@bld('tree-autumn')
def autumn():
    v = Vol(-26, 26, -26, 26, 0, 80)
    v.put((-6, 6, -6, 6, 0, 40), lambda X, Y, Z: X ** 2 + Y ** 2 <= (2.2 + 2.6 * np.clip(1 - Z / 8, 0, 1) ** 2) ** 2, BARK)
    canopy(v, 0, 0, 50, 19, LEAF_A, seed=11, n=9)
    return v

@bld('rocks')
def rocks():
    v = Vol(-18, 18, -16, 16, 0, 18)
    for (x, y, rx, ry, rz) in ((-4, -2, 9, 7, 9), (6, 4, 6, 5, 6), (-9, 7, 4, 4, 4), (9, -6, 3.5, 3, 3)):
        v.put((x - rx - 2, x + rx + 2, y - ry - 2, y + ry + 2, 0, rz + 2),
              lambda X, Y, Z, x=x, y=y, rx=rx, ry=ry, rz=rz: ((X - x) / rx) ** 2 + ((Y - y) / ry) ** 2 + (Z / rz) ** 2 <= 1 - 0.25 * (hash3(np.floor(X / 3).astype(np.int64), np.floor(Y / 3).astype(np.int64), np.floor(Z / 3).astype(np.int64), 9)), STONE_D)
    v.put((-16, 16, -14, 14, 0, 10), lambda X, Y, Z: (Z > 6) & (hash3(np.floor(X / 2).astype(np.int64), np.floor(Y / 2).astype(np.int64), np.zeros_like(X, dtype=np.int64), 3) > 0.7) & (v.m[0:1, 0:1, 0:1].size > 0) & False, MOSS)
    return v

def fence(axis):
    v = Vol(-20, 20, -20, 20, 0, 18)
    for k in (-15, 0, 15):
        if axis == 'x': v.box(k - 1.2, k + 1.2, -1.2, 1.2, 0, 15, TIMBER); v.cone(k, 0, 1.3, 15, 17, TIMBER)
        else: v.box(-1.2, 1.2, k - 1.2, k + 1.2, 0, 15, TIMBER); v.cone(0, k, 1.3, 15, 17, TIMBER)
    for zz in (5, 11):
        if axis == 'x': v.box(-16, 16, -0.6, 0.6, zz, zz + 2, WOOD_L)
        else: v.box(-0.6, 0.6, -16, 16, zz, zz + 2, WOOD_L)
    return v

@bld('fence-x')
def fx(): return fence('x')
@bld('fence-y')
def fy(): return fence('y')

# ------------------------------------------------------------------ the Shire (this fork)
def disc_y(v, cx, cz, r, y0, y1, mat, rin=None):
    """A disc standing in a wall plane y (facing +y), centre (cx, cz): round doors and windows."""
    def f(X, Y, Z):
        d = (X - cx) ** 2 + (Z - cz) ** 2
        m = (d <= r * r) & (Y >= y0) & (Y < y1) & (Z >= 0)
        if rin: m &= d > rin * rin
        return m
    v.put((cx - r, cx + r, y0, y1, max(0, cz - r), cz + r), f, mat)

def round_window(v, x, z, face, r=6.5):
    disc_y(v, x, z, r, face - 1, face + 1.4, TIMBER)
    disc_y(v, x, z, r - 1.5, face - 2, face + 1.6, GLASS)
    v.box(x - 0.4, x + 0.4, face + 1.4, face + 2, z - 5, z + 5, TIMBER)
    v.box(x - r + 1.5, x + r - 1.5, face + 1.4, face + 2, z - 0.4, z + 0.4, TIMBER)
    for k, c in enumerate((CLOTH_R, CLOTH_Y, CLOTH_R, CLOTH_Y)):   # a window box of flowers
        v.ell(x - 4.5 + k * 3, face + 4, z - 6.4, 1.5, 1.5, 1.5, c)
    v.box(x - 6.5, x + 6.5, face + 1.5, face + 5, z - 9.5, z - 7, PLANK)

@bld('smial')
def smial():
    """A grand hobbit smial (the Mathom-house): a long turf hill cut flat in front, a stone face with the round
    green door and four round windows, two chimneys, a path and a garden fence."""
    v = Vol(-70, 70, -60, 52, 0, 90)
    FACE = 6
    v.ell(0, -6, -10, 66, 54, 62, MOSS)        # the turf
    v.ell(0, -6, -10, 64.5, 52.5, 60.5, LEAF_D)  # a darker rim where it is cut
    v.ell(0, -6, -10, 62, 50, 58, STONE)       # the stone under it: shows on the cut face
    v.box(-70, 70, FACE, 52, 0, 90, 0)         # cut the front flat
    disc_y(v, 0, 16, 20, FACE - 1, FACE + 1.5, STONE_D)
    disc_y(v, 0, 16, 16, FACE - 2, FACE + 2, DOOR_G)
    for a in (-10, -5, 0, 5, 10):
        v.box(a - 0.3, a + 0.3, FACE + 1.6, FACE + 2.2, 1, 31, TIMBER)
    v.ell(0, FACE + 3, 16, 2, 2, 2, GOLD)      # the brass knob, in the middle
    v.box(-5, 5, FACE - 1, FACE + 2.5, 36, 40, MARBLE)  # keystone
    for x in (-46, -26, 26, 46):
        round_window(v, x, 22 if abs(x) < 30 else 17, FACE, r=7.5 if abs(x) < 30 else 6.5)
    v.box(-15.5, -14.5, FACE + 12, FACE + 13, 0, 16, TIMBER)   # the sign
    v.box(-22, -8, FACE + 12.6, FACE + 13.6, 9, 17, WOOD_L); v.box(-20, -10, FACE + 13.6, FACE + 14, 11, 15, GOLD)
    chimney(v, 28, -14, 30, 70, BRICK, 7)
    chimney(v, -34, -24, 24, 62, BRICK, 6)
    v.ell(-12, -30, 46, 10, 9, 8, LEAF); v.ell(-2, -36, 44, 7, 7, 6, LEAF_F); v.ell(44, -20, 30, 8, 7, 6, LEAF)
    for k in range(5):
        v.box(-6 + (k % 2) * 2, 6 + (k % 2) * 2, FACE + 5 + k * 6.5, FACE + 10 + k * 6.5, 0, 0.8, STONE)
    rng = np.random.default_rng(5)
    for x in np.arange(-58, 60, 4.2):
        if abs(x) < 23: continue
        v.ell(x + rng.uniform(-1, 1), FACE + 2.8, 1.3, 1.5, 1.5, 1.7, [CLOTH_R, CLOTH_Y, CLOTH_W, LEAF, CLOTH_P][int(rng.integers(5))])
    for x in range(-64, 65, 10):
        if abs(x) < 11: continue
        v.box(x - 0.8, x + 0.8, FACE + 34, FACE + 35.6, 0, 8, TIMBER)
    for zz in (3, 6):
        v.box(-64, -11, FACE + 34.3, FACE + 35.3, zz, zz + 1.2, WOOD_L); v.box(11, 64, FACE + 34.3, FACE + 35.3, zz, zz + 1.2, WOOD_L)
    return v

# ---- this fork: Middle-earth buildings (Elf-tower, Dwarf-forge, Rohan longhall, Elvish house)


def lancet(v, ang, z, h, hw, R, glow=ELF_GLOW, frame=METAL):
    """A tall pointed (lancet) window cut into a round wall at angle ang."""
    def m(X, Y, Z, d0, d1, ext=0):
        an = np.arctan2(Y, X); dr = np.hypot(X, Y)
        da = np.abs(((an - ang + np.pi) % (2 * np.pi)) - np.pi) * R
        top = z + h + (hw + ext - da) * 1.8
        return (da <= hw + ext) & (Z >= z - ext) & (Z < top) & (dr >= d0) & (dr <= d1)
    bb = (-R - 6, R + 6, -R - 6, R + 6, z - 3, z + h + hw * 2 + 4)
    v.put(bb, lambda X, Y, Z: m(X, Y, Z, R - 1.2, R + 1.4, 1.2), frame)
    v.put(bb, lambda X, Y, Z: m(X, Y, Z, R - 3, R + 2), 0)
    v.put(bb, lambda X, Y, Z: m(X, Y, Z, R - 4, R - 2.2), glow)

@bld('elftower')
def elftower():
    """A white Elf-tower like those on the Tower Hills: a slender shaft, an open lantern with a seeing-stone, a silver spire."""
    v = Vol(-46, 46, -46, 46, 0, 232)
    v.cyl(0, 0, 27, 0, 3, STONE)
    v.cyl(0, 0, 23, 3, 7, MARBLE)
    r = lambda z: 17 - (z - 7) * 0.022
    v.put((-18, 18, -18, 18, 7, 168), lambda X, Y, Z: X ** 2 + Y ** 2 <= r(Z) ** 2, MARBLE)
    for zz in (56, 108):
        v.cyl(0, 0, r(zz) + 1.3, zz, zz + 2, METAL)
    # a leaf-carved string course under the lantern
    v.put((-22, 22, -22, 22, 156, 168), lambda X, Y, Z: X ** 2 + Y ** 2 <= (r(156) + (Z - 156) * 0.45) ** 2, MARBLE)
    for ang, z in ((0.25, 28), (1.35, 28), (0.8, 70), (0.3, 120), (1.3, 120)):
        lancet(v, ang, z, 12, 2.8, r(z))
    # the open lantern: a floor, eight slender columns, the seeing-stone glowing inside
    v.cyl(0, 0, 21, 168, 171, MARBLE)
    for k in range(8):
        a = k / 8 * 2 * np.pi + 0.2
        v.cyl(17 * np.cos(a), 17 * np.sin(a), 1.6, 171, 191, MARBLE)
    v.cyl(0, 0, 4, 171, 177, METAL)
    v.ell(0, 0, 181, 5.5, 5.5, 5.5, ELF_GLOW)
    v.cyl(0, 0, 20.5, 191, 193.5, METAL)
    # a tall, slightly concave silver spire with a star on its needle
    v.put((-22, 22, -22, 22, 193.5, 227), lambda X, Y, Z: X ** 2 + Y ** 2 <= (0.8 + 19 * (1 - np.clip((Z - 193.5) / 33.5, 0, 1)) ** 2.4) ** 2, ELF_ROOF)
    v.cyl(0, 0, 0.8, 224, 232, METAL)
    for dx, dy, dz in ((0, 0, 3), (3, 0, 0), (-3, 0, 0), (0, 3, 0), (0, -3, 0)):
        v.ell(dx * 0.6, dy * 0.6, 229 + dz * 0.5, 1.4 if (dx or dy) else 1.6, 1.4, 1.4, ELF_GLOW)
    # a pointed white door with a silver frame
    a = 0.8; R0 = r(10)
    def door(X, Y, Z, d0, d1, ext=0):
        an = np.arctan2(Y, X); dr = np.hypot(X, Y)
        da = np.abs(((an - a + np.pi) % (2 * np.pi)) - np.pi) * R0
        return (da <= 6 + ext) & (Z >= 7) & (Z < 24 + (6 + ext - da) * 1.6) & (dr >= d0) & (dr <= d1)
    bb = (-26, 26, -26, 26, 7, 40)
    v.put(bb, lambda X, Y, Z: door(X, Y, Z, R0 - 1, R0 + 1.6, 1.4), METAL)
    v.put(bb, lambda X, Y, Z: door(X, Y, Z, R0 - 3, R0 + 2), 0)
    v.put(bb, lambda X, Y, Z: door(X, Y, Z, R0 - 3.6, R0 - 2.4), WOOD_L)
    # ivy and white flowers climbing the foot, on the visible side
    rng = np.random.default_rng(7)
    for an0 in (0.05, 0.4, 1.25, 1.6):
        an = an0; top = rng.uniform(40, 70)
        for zz in np.arange(7, top, 2.2):
            an += rng.uniform(-0.05, 0.05)
            rr = r(zz) + 0.8
            v.ell(rr * np.cos(an), rr * np.sin(an), zz, 1.6, 1.6, 1.4, LEAF_D if rng.random() < 0.7 else LEAF)
            if rng.random() < 0.18: v.ell((rr + 1.2) * np.cos(an + 0.06), (rr + 1.2) * np.sin(an + 0.06), zz, 0.9, 0.9, 0.9, CLOTH_W)
    return v

@bld('dwarfforge')
def dwarfforge():
    """A Dwarvish forge: a stone gate carved into a crag, the forge glowing in its mouth, a mine cart on rails."""
    v = Vol(-56, 60, -50, 58, 0, 150)
    FACE = 22
    # the crag: a few rough lumps, cut flat where the gate is carved
    def crag(X, Y, Z):
        # a lumpy, faceted crag: an ellipsoid whose radius wobbles with direction, with ledges
        dx, dy, dz = (X + 6) / 52, (Y + 14) / 40, Z / 84
        rr = np.sqrt(dx * dx + dy * dy + dz * dz)
        th = np.arctan2(dy, dx); ph = np.arctan2(dz, np.hypot(dx, dy))
        wob = 1 + 0.10 * np.sin(th * 5 + 1.3) * np.cos(ph * 3) + 0.06 * np.sin(th * 11 + ph * 7) + 0.05 * np.round(np.sin(ph * 9) * 2) / 2
        return rr <= wob
    v.put((-56, 56, -50, 52, 0, 100), crag, ROCK)
    v.put((24, 56, -40, 6, 0, 60), lambda X, Y, Z: ((X - 34) / 22) ** 2 + ((Y + 18) / 22) ** 2 + (Z / 52) ** 2 <= 1 + 0.12 * np.sin(np.arctan2(Y + 18, X - 34) * 6), ROCK)
    for (bx, by) in ((-44, 20), (-38, 28), (48, 18)):
        v.ell(bx, by, 2, 5, 4, 4, ROCK)
    v.box(-56, 56, FACE, 52, 0, 150, 0)
    # the carved facade: a tall sunken panel, two great pillars with capitals, a heavy stepped lintel
    v.box(-28, 42, FACE - 4, FACE, 0, 70, 0)
    v.box(-28, 42, FACE - 6, FACE - 4, 0, 70, STONE_D)
    for px in (-26, 31):
        v.box(px, px + 9, FACE - 4, FACE + 4, 0, 56, STONE)
        for zz in range(8, 56, 12):
            v.box(px - 0.4, px + 9.4, FACE + 3.6, FACE + 4.4, zz, zz + 1, STONE_D)
        v.box(px - 2, px + 11, FACE - 4, FACE + 5.5, 56, 61, STONE)
    v.box(-30, 44, FACE - 4, FACE + 5.5, 61, 70, STONE)
    v.box(-22, 36, FACE - 4, FACE + 5.5, 70, 75, STONE)
    for k in range(9):                                          # an angular rune band on the lintel
        xx = -25 + k * 7.5
        v.box(xx, xx + 2, FACE + 5.5, FACE + 6.2, 63, 68, GOLD)
        v.box(xx + 2, xx + 4.5, FACE + 5.5, FACE + 6.2, 66 - (k % 2) * 3, 68 - (k % 2) * 3, GOLD)
    # the doorway: tall and squared, with stepped shoulders, the forge fire deep inside
    def gate(X, Y, Z, w):
        return (np.abs(X - 7) <= w) & (Z < 44 + np.clip(w - np.abs(X - 7), 0, 7) * 1.3)
    v.put((-12, 26, FACE - 34, FACE + 2, 0, 58), lambda X, Y, Z: gate(X, Y, Z, 15), 0)
    v.put((-12, 26, FACE - 34, FACE - 26, 0, 58), lambda X, Y, Z: gate(X, Y, Z, 15), COAL)
    v.put((-8, 22, FACE - 28, FACE - 18, 0, 34), lambda X, Y, Z: (np.abs(X - 7) <= 12) & (Z < 20 + np.sqrt(np.clip(110 - (X - 7) ** 2, 0, None))), FIRE)
    v.box(-6, 20, FACE - 18, FACE - 10, 0, 6, BRICK); v.box(0, 14, FACE - 16, FACE - 12, 6, 9, FIRE)
    v.box(-8, 22, FACE - 10, FACE + 1, 0, 0.6, FIRE)          # firelight spilling over the floor
    # three broad steps up to the gate
    for k in range(3):
        v.box(-14 - k * 2, 28 + k * 2, FACE + k * 4, FACE + 4 + k * 4, 0, 4.5 - k * 1.5, STONE)
    # two dwarf statues on plinths, leaning on their axes
    def statue(x):
        y = FACE + 9
        v.box(x - 6, x + 6, y - 6, y + 6, 0, 7, STONE_D)                              # plinth
        v.box(x - 7, x + 7, y - 7, y + 7, 6, 8, STONE_D)
        v.put((x - 7, x + 7, y - 7, y + 7, 8, 30), lambda X, Y, Z: ((X - x) ** 2 + (Y - y) ** 2) <= (5.8 - (Z - 8) * 0.06) ** 2, STONE)   # stout body
        v.ell(x, y, 32, 5.6, 5.6, 3.5, STONE)                                       # shoulders
        v.ell(x, y, 37, 3.6, 3.6, 3.8, STONE)                                       # head
        v.cone(x, y, 4.2, 38, 46, STONE_D, p=1.0, r1=0.3)                            # pointed helm
        v.put((x - 5, x + 6, y, y + 7, 18, 37), lambda X, Y, Z: ((Y - y) > 2.5) & (np.abs(X - x) <= 1 + (Z - 18) * 0.16) & ((Y - y) < 3 + 3.6 - (37 - Z) * 0.05), STONE)  # long forked beard
        v.box(x + 6, x + 7.6, y + 4, y + 5.6, 8, 44, METAL)                         # axe haft, upright
        v.put((x + 5, x + 13, y + 3.6, y + 6, 36, 46), lambda X, Y, Z: (X > x + 7) & ((X - x - 7) <= 5 - np.abs(Z - 41) * 0.7), METAL)  # axe blade
    statue(-40); statue(50)
    # braziers by the steps
    for bx in (-20, 34):
        v.cyl(bx, FACE + 16, 1.2, 0, 10, METAL); v.cyl(bx, FACE + 16, 3.2, 10, 13, METAL)
        v.ell(bx, FACE + 16, 14, 2.6, 2.6, 3, FIRE)
    # chimney cut up through the crag, smoke where the old one was
    chimney(v, 7, -2, 70, 104, STONE, 9)
    v.box(4, 10, -5, 1, 101, 103, FIRE)
    # anvil and quench trough on a flagstone yard
    v.box(-30, 50, FACE + 12, FACE + 30, 0, 1, STONE)
    ax_, ay_ = 40, FACE + 22
    v.box(ax_, ax_ + 4, ay_, ay_ + 4, 1, 8, ROCK)
    v.box(ax_ - 2, ax_ + 7, ay_ - 0.5, ay_ + 4.5, 8, 12, METAL)
    v.box(ax_ + 7, ax_ + 10, ay_ + 1, ay_ + 3, 9.5, 11.5, METAL)
    v.box(-34, -20, FACE + 20, FACE + 26, 1, 7, STONE_D); v.box(-33, -21, FACE + 21, FACE + 25, 5, 6.5, WATER)
    # a mine cart of ore on rails, out of a small side adit
    v.put((36, 56, -12, 10, 0, 24), lambda X, Y, Z: (np.abs(Y + 1) <= 8) & (Z < 14 + np.sqrt(np.clip(64 - (Y + 1) ** 2, 0, None))), 0)
    for ry in (-5, 3):
        v.box(30, 56, ry, ry + 1.2, 0, 1.6, METAL)
    for rx in range(31, 56, 5):
        v.box(rx, rx + 2, -7, 6, 0, 0.8, TIMBER)
    v.box(40, 52, -5, 4, 3, 10, PLANK); v.box(40, 52, -5.5, 4.5, 9, 10.5, METAL)
    for wx in (42, 50):
        for wy in (-6, 4):
            v.ell(wx, wy, 2.6, 2.2, 1.0, 2.2, METAL)
    for k in range(6):
        v.ell(42 + (k % 3) * 4, -2 + (k // 3) * 4, 11, 2.2, 2.2, 1.8, COAL if k % 2 else GOLD)
    return v

@bld('longhall')
def longhall():
    """A Rohan longhall: a timber hall on a stone terrace, a steep thatched roof, crossed horse-head gables, green banners."""
    v = Vol(-74, 74, -52, 56, 0, 190)
    x0, x1, y0, y1 = -64, 38, -24, 24
    # stone terrace with steps up to the gable door
    v.box(x0 - 8, x1 + 12, y0 - 8, y1 + 8, 0, 8, STONE)
    v.box(x0 - 9, x1 + 13, y0 - 9, y1 + 9, 7, 9, STONE_D)
    for k in range(3):
        v.box(x1 + 13 + k * 4, x1 + 17 + k * 4, -14 + k * 2, 14 - k * 2, 0, 8 - (k + 1) * 2.6, STONE)
    # timber walls: dark planks with posts
    v.box(x0, x1, y0, y1, 9, 40, PLANK)
    for a in np.arange(x0, x1 + 1, 11.5):
        v.box(a - 1.5, a + 1.5, y1 - 0.5, y1 + 2, 9, 42, TIMBER); v.box(a - 1.5, a + 1.5, y0 - 2, y0 + 0.5, 9, 42, TIMBER)
    for a in np.arange(y0, y1 + 1, 12):
        v.box(x1 - 0.5, x1 + 2, a - 1.5, a + 1.5, 9, 42, TIMBER)
    v.box(x0, x1, y1, y1 + 1.5, 38, 41, TIMBER)
    # small high windows along the side
    for a in np.arange(x0 + 6, x1 - 6, 11.5):
        window(v, 'y', y1, a, a + 4, 26, 34, cross=False, sill=False)
    # the great thatched roof, ridge along the hall, low eaves
    v.roof(x0 - 6, x1 + 6, y0 - 8, y1 + 8, 40, 92, THATCH, axis='x', th=5, fill=PLANK, curve=1.0)
    RW = (y1 - y0) / 2 + 8
    def shell(X, Y, Z):
        h = 40 + 52 * np.clip(1 - np.abs(Y) / RW, 0, 1)
        return (X >= x0 - 6) & (X < x1 + 6) & (np.abs(Y) < RW) & (Z >= 40) & (Z <= h) & (Z > h - 5)
    v.put((x0 - 6, x1 + 6, -RW, RW, 40, 93), lambda X, Y, Z: shell(X, Y, Z) & (((Z - 40) % 11) < 1.6), THATCH_D)
    rng = np.random.default_rng(11)
    for _ in range(5):                                            # a few ragged patches of moss
        mx, my = rng.uniform(x0, x1), rng.uniform(6, RW - 6) * rng.choice([-1, 1])
        for _ in range(7):
            px, py = mx + rng.uniform(-6, 6), my + rng.uniform(-3, 3); pz = 40 + 52 * (1 - abs(py) / RW)
            r = rng.uniform(1.5, 3.0)
            v.put((px - 4, px + 4, py - 4, py + 4, pz - 4, pz + 4), lambda X, Y, Z, px=px, py=py, pz=pz, r=r: shell(X, Y, Z) & ((X - px) ** 2 + (Y - py) ** 2 + (Z - pz) ** 2 <= r * r), MOSS_R)
    v.box(x0 - 6, x1 + 6, -2.5, 2.5, 88, 94, TIMBER)
    for a in np.arange(x0 - 4, x1 + 6, 9):
        v.box(a, a + 2, -3.5, 3.5, 90, 95.5, TIMBER)
    for zz in (60, 80):                                           # thatch ties
        hw = (y1 + 12 - (y0 - 12)) / 2; d = 1 - (zz - 34) / 62
        v.box(x0 - 6, x1 + 6, -hw * d - 0.6, -hw * d + 0.6, zz, zz + 1.5, ROPE) if False else None
    # the gable end: carved board, gold sun disc, crossed barge-boards ending in horse heads
    gx = x1 + 6
    hw = (y1 - y0) / 2 + 8
    def barge(sign):
        for t in np.arange(0, 1.1, 0.012):
            yy = sign * hw * (1 - t); zz = 40 + 52 * t
            v.box(gx - 1, gx + 2.5, yy - 1.6, yy + 1.6, zz - 1.4, zz + 1.4, TIMBER)
        # the carved horse head, past the crossing, looking outward
        HEAD = ["...X.X.......",
                "...XXXX......",
                "..XXXXXX.....",
                "..XXXXXXXX...",
                ".XXXXXXXXXXX.",
                ".XXXX..XXXXXX",
                "XXXX.....XXX.",
                "XXX..........",
                "XXX..........",
                "XXX.........."]
        t = 1.06; by = sign * hw * (1 - t); bz = 40 + 52 * t
        for r, row in enumerate(HEAD):
            for c, ch in enumerate(row):
                if ch != 'X': continue
                yy = by + sign * (c - 1) * 1.7; zz = bz + (len(HEAD) - r) * 1.7
                v.box(gx - 1.4, gx + 3.0, yy - 0.9, yy + 0.9, zz - 0.9, zz + 0.9, GOLD)
    barge(1); barge(-1)
    v.put((gx - 0.5, gx + 1.8, -8, 8, 56, 74), lambda X, Y, Z: (Y ** 2 + (Z - 64) ** 2 <= 30) & (Y ** 2 + (Z - 64) ** 2 > 7), GOLD)
    # a porch with carved posts before the gable door
    door(v, 'x', x1, -7, 7, 30, arch=False, leaf=PLANK_R if False else PLANK)
    for py in (-12, 12):
        v.box(x1 + 9, x1 + 12.5, py - 1.75, py + 1.75, 9, 44, TIMBER)
        for zz in (16, 26, 36):
            v.box(x1 + 8.6, x1 + 12.9, py - 2.1, py + 2.1, zz, zz + 1.4, GOLD)
    v.roof(x1, x1 + 15, -17, 17, 42, 54, THATCH, axis='x', th=3)
    # green and white banners on the long wall
    for a in (-50, -16, 16):
        banner(v, 'y', y1 + 2, a, 40, 24, 8, CLOTH_G, CLOTH_W, CLOTH_W)
    # hitching rail and a hay pile, a water trough
    hx, hy = -56, y1 + 5
    v.box(hx, hx + 30, hy, hy + 1.6, 19, 21, TIMBER)
    for px in (hx, hx + 14, hx + 28):
        v.box(px, px + 2, hy - 0.2, hy + 1.8, 9, 21, TIMBER)
    v.box(-6, 10, y1 + 18, y1 + 24, 0, 6, PLANK); v.box(-5, 9, y1 + 19, y1 + 23, 4, 5.5, WATER)
    v.cone(28, y1 + 20, 7, 0, 16, HAY, p=0.6)
    flag(v, x0 - 2, y0 + 4, 40, 70, CLOTH_G, 18)
    return v

def arcade(v, y, xa, xb, z0, z1, step=12, depth=11):
    """A gallery of slender columns under pointed arches, set into the y-facing wall."""
    v.box(xa, xb, y - depth, y + 0.5, z0, z1, 0)
    v.box(xa, xb, y - depth - 1, y - depth, z0, z1, ELF_STONE)
    for x in np.arange(xa, xb + 0.1, step):
        v.box(x - 0.9, x + 0.9, y - 2, y, z0, z1, MARBLE)
        v.box(x - 1.6, x + 1.6, y - 2.6, y + 0.4, z1 - 3, z1 - 1, GOLD)
    for x in np.arange(xa, xb - step + 0.1, step):
        cx = x + step / 2
        v.put((x, x + step, y - 2.6, y, z1 - step, z1), lambda X, Y, Z, cx=cx: (Z > z1 - step * 0.9 + (step / 2 - np.abs(X - cx)) * 1.5), MARBLE)
    v.box(xa - 1.5, xb + 1.5, y - 3, y + 1, z1, z1 + 3, MARBLE)

@bld('elfhouse')
def elfhouse():
    """An Elvish house in the manner of Rivendell: pale stone, pointed arcades, a slim tower, sage roofs, autumn trees."""
    v = Vol(-80, 80, -66, 70, 0, 210)
    # terraces
    v.box(-64, 62, -46, 46, 0, 6, ELF_STONE)
    v.box(-65, 63, -47, 47, 5, 7, MARBLE)
    for k in range(3):
        v.box(-16 - k * 3, 16 + k * 3, 46 + k * 4, 50 + k * 4, 0, 6 - (k + 1) * 2, MARBLE)
    # the main hall, with an arcade along the front
    x0, x1, y0, y1 = -54, 26, -30, 30
    v.box(x0, x1, y0, y1, 7, 50, ELF_STONE)
    arcade(v, y1, x0 + 4, x1 - 4, 7, 40)
    v.box(x0 - 2, x1 + 2, y0 - 2, y1 + 2, 50, 53, MARBLE); v.box(x0 - 2.4, x1 + 2.4, y0 - 2.4, y1 + 2.4, 46, 47.2, GOLD)
    v.roof(x0 - 8, x1 + 8, y0 - 8, y1 + 8, 52, 92, ELF_SLATE, axis='x', hip=0.7, th=4, fill=ELF_STONE, curve=1.6)
    def crest(axis, a0, a1, c, ztop):
        mid, half = (a0 + a1) / 2, (a1 - a0) / 2
        def f(X, Y, Z):
            A, B = (X, Y) if axis == 'x' else (Y, X)
            t = np.clip(np.abs(A - mid) / half, 0, 1)
            return (A >= a0) & (A <= a1) & (np.abs(B - c) <= 0.9) & (Z >= ztop - 1) & (Z <= ztop + 1.5 + 12 * t ** 4)
        bb = (a0, a1, c - 1, c + 1, ztop - 1, ztop + 14) if axis == 'x' else (c - 1, c + 1, a0, a1, ztop - 1, ztop + 14)
        v.put(bb, f, GOLD)
    crest('x', -36, 8, 0, 91)
    for xx in ():
        v.put((xx - 3, xx + 3, -3, 3, 88, 102), lambda X, Y, Z, xx=xx: ((X - xx) / 2.4) ** 2 + (Y / 1.2) ** 2 <= (np.sin(np.clip((Z - 88) / 14, 0, 1) * np.pi)) ** 2, GOLD)
    # the east wing: taller, with a balcony and tall windows
    wx0, wx1, wy0, wy1 = 26, 56, -22, 22
    v.box(wx0, wx1, wy0, wy1, 7, 74, ELF_STONE)
    v.box(wx0 - 1, wx1 + 1, wy0 - 1, wy1 + 1, 74, 77, MARBLE); v.box(wx0 - 1.4, wx1 + 1.4, wy0 - 1.4, wy1 + 1.4, 70, 71.2, GOLD)
    for a in (-14, -3, 8):
        window(v, 'x', wx1, a, a + 6, 14, 34, frame=GOLD, arch=True, cross=False, sill=False)
        window(v, 'x', wx1, a, a + 6, 46, 64, frame=GOLD, arch=True, cross=False, sill=False)
    v.box(wx1, wx1 + 8, wy0 + 2, wy1 - 2, 40, 42, MARBLE)            # balcony
    for a in np.arange(wy0 + 3, wy1 - 2, 3):
        v.box(wx1 + 6.5, wx1 + 8, a, a + 1, 42, 47, MARBLE)
    v.box(wx1 + 6.5, wx1 + 8, wy0 + 2, wy1 - 2, 47, 48.5, MARBLE)
    window(v, 'y', wy1, wx0 + 8, wx0 + 16, 46, 64, frame=GOLD, arch=True, cross=False, sill=False)
    v.roof(wx0 - 6, wx1 + 6, wy0 - 6, wy1 + 6, 76, 118, ELF_SLATE, axis='y', hip=0.8, th=4, fill=ELF_STONE, curve=1.7)
    crest('y', -8, 8, (wx0 + wx1) / 2, 117)
    # a slim round tower behind, echoing the Elf-tower
    tx, ty = -38, -22
    v.cyl(tx, ty, 10, 7, 108, ELF_STONE)
    v.cyl(tx, ty, 11.5, 106, 110, MARBLE)
    for zz in (62, 88):
        window(v, 'y', ty + 10, tx - 2, tx + 2, zz, zz + 10, frame=GOLD, arch=True, cross=False, sill=False)
    v.put((tx - 14, tx + 14, ty - 14, ty + 14, 110, 152), lambda X, Y, Z: (X - tx) ** 2 + (Y - ty) ** 2 <= (0.6 + 13 * (1 - np.clip((Z - 110) / 42, 0, 1)) ** 2.2) ** 2, ELF_SLATE)
    v.cyl(tx, ty, 0.7, 148, 156, GOLD)
    # a pool with a little fall of water from the terrace
    v.put((-64, 46, 58, 68, 0, 2), lambda X, Y, Z: np.abs(Y - 63 - 2 * np.sin(X * 0.08)) <= 4 * np.clip(np.minimum(X + 64, 46 - X) / 14, 0.25, 1), WATER)
    v.put((-64, 46, 56, 70, 0, 2.5), lambda X, Y, Z: (np.abs(np.abs(Y - 63 - 2 * np.sin(X * 0.08)) - 1 - 4 * np.clip(np.minimum(X + 64, 46 - X) / 14, 0.25, 1)) <= 1) & (Z < 2.5), MARBLE)
    def bridge(X, Y, Z):
        arch = 2.5 + 6 * np.sqrt(np.clip(1 - ((Y - 63) / 9) ** 2, 0, 1))
        return (np.abs(X) <= 7) & (Z <= arch) & (Z > arch - 2.2)
    v.put((-8, 8, 52, 74, 0, 10), bridge, MARBLE)
    v.put((-8, 8, 52, 74, 0, 14), lambda X, Y, Z: (np.abs(np.abs(X) - 6.5) <= 0.6) & (Z > 2.5 + 6 * np.sqrt(np.clip(1 - ((Y - 63) / 9) ** 2, 0, 1))) & (Z < 4.5 + 6 * np.sqrt(np.clip(1 - ((Y - 63) / 9) ** 2, 0, 1))), GOLD)
    # slender silver-barked trees in golden autumn leaf
    rng = np.random.default_rng(3)
    for (tx2, ty2, s) in ((-72, 26, 1.0), (62, 40, 0.85), (-70, -44, 1.1)):
        v.cyl(tx2, ty2, 1.2 * s, 0, 62 * s, MARBLE)
        for k in range(14):
            ox, oy, oz = rng.uniform(-7, 7) * s, rng.uniform(-7, 7) * s, rng.uniform(34, 72) * s
            r = rng.uniform(2.6, 4.6) * s
            v.ell(tx2 + ox, ty2 + oy, oz, r, r, r * 0.9, HAY if k % 2 else LEAF_A)
    # slim lamp posts with soft white light by the steps
    for lx in (-22, 22):
        v.cyl(lx, 50, 0.8, 0, 20, METAL)
        v.ell(lx, 50, 21.5, 2, 2, 2.4, HOLY)
        v.cone(lx, 50, 2.6, 23, 27, METAL, p=1.0, r1=0.2)
    return v


def build(name):
    t = time.time()
    s = {'magetower': 1.3}.get(name, S_B)
    engine.VS_DEFAULT[0] = 1 / s
    v = B[name]()
    r = trim(render(v, PAL, S=s))
    print(name, 'rendered', r['color'].shape, 'anchor', r['anchor'], f'{time.time() - t:.1f}s', flush=True)
    return r

if __name__ == '__main__':
    import os
    OUT = os.environ.get('OUT', 'assets')
    os.makedirs(OUT, exist_ok=True)
    meta = {}
    if os.path.exists(OUT + '/meta.json'): meta = json.load(open(OUT + '/meta.json'))
    for name in (sys.argv[1:] or list(B)):
        r = build(name)
        from PIL import Image
        save2x(r['color'], f'{OUT}/b-{name}.png')
        save2x(r['shadow'], f'{OUT}/b-{name}-shadow.png')
        save2x(r['emis'], f'{OUT}/b-{name}-night.png')
        save2x(r['nightlit'], f'{OUT}/b-{name}-nightlit.png')
        save2x(r['cast'], f'{OUT}/b-{name}-cast.png')
        meta['b-' + name] = {'w': int(r['color'].shape[1]), 'h': int(r['color'].shape[0]), 'ax': int(r['anchor'][0]), 'ay': int(r['anchor'][1])}
        json.dump(meta, open(OUT + '/meta.json', 'w'), indent=1)
