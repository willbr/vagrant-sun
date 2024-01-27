import pyxel
import math
import os

shear_limit = 10
shear_step = 1
shear = 0
auto = True

ax, ay = 140, 90
ax_step = 32

pyxel.init(256, 144, title="gameboy", fps=15, display_scale=4)
pyxel.camera(-48, 0)

background_path =  "images/background3.png"

old_stamp = os.stat(background_path).st_mtime

def load_background():
    pyxel.image(0).load(0, 0, background_path)

    pyxel.image(0).blt(128, 0, 0, 0, 0, -128, 32)

    #blt(x, y, img, u, v, w, h, [colkey])

load_background()
pyxel.image(0).load(0, 32, "images/actors.png")

def update():
    global auto
    global shear
    global ax
    global ax_step
    global old_stamp

    stamp = os.stat(background_path).st_mtime
    if stamp != old_stamp:
        try:
            load_background()
            old_stamp = stamp
        except:
            pass

    if pyxel.btnp(pyxel.KEY_UP):
        ax_step += 1
    if pyxel.btnp(pyxel.KEY_DOWN):
        ax_step -= 1

    if pyxel.btnp(pyxel.KEY_LEFT):
        pass

    if pyxel.btnp(pyxel.KEY_RIGHT):
        pass

    if pyxel.btnp(pyxel.KEY_SPACE):
        auto = not auto

    if auto:
        shear -= shear_step

    if shear <= -shear_limit:
        shear = 0
    elif shear >= shear_limit:
        shear = 0

    if auto:
        ax -= ax_step >> 3
        if ax < -40:
            ax = 160


def draw():
    pyxel.cls(0)

    if False:
        pyxel.line(-16,0, -16,140, 2)
        pyxel.line(+16,0, +16,140, 2)
        pyxel.line(+32,0, +32,140, 2)

    floor(y=80, stop=32, step=1)
    floor(y=40, stop=-32, step=-1)
    actors()

    if False:
        pyxel.line(0,0, 0, 144, 2)
        pyxel.line(80,0, 80, 144, 2)
        pyxel.line(160,0, 160, 144, 2)

    if True:
        pyxel.rect(-48, 0, 48, 144, 3)
        pyxel.rect(160, 0, 48, 144, 3)

    #pyxel.rect(48, 48, 2, 2, 5)

    pyxel.text(-40,4, f"{shear:+2d}", 2)
    pyxel.text(-40,8, f"{ax_step:+2d}", 2)

def floor(y, stop, step):
    src_y = 0
    x = (16 * shear/10) - 48


    for i in range(0, stop, step):
        pyxel.blt(x, y, 0, 0, src_y, 256, 1)
        y += step
        pyxel.blt(x, y, 0, 0, src_y, 256, 1)
        y += step

        if y % 2 == 0:
            x += shear/10

        src_y += 1

def actors():
    pyxel.blt(ax, ay,
              0,
              0, 32,
              17, 32)

    """
    pyxel.blt(100, 40,
              0,
              24, 32,
              17, 32)

    pyxel.blt(130, 90,
              0,
              50, 32,
              17, 32)
              """

pyxel.run(update, draw)

