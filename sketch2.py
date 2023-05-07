import pyxel
import math

shear_limit = 1
shear_step = 0.1
shear = 0
auto = True

ax, ay = 140, 90

pyxel.init(256, 144, title="gameboy", fps=15, display_scale=2)
pyxel.camera(-48, 0)

pyxel.image(0).load(0, 0, "images/background3.png")
pyxel.image(0).load(0, 32, "images/actors.png")

def update():
    global auto
    global shear
    global ax

    if pyxel.btnp(pyxel.KEY_LEFT):
        shear -= shear_step

    if pyxel.btnp(pyxel.KEY_RIGHT):
        shear += shear_step

    if pyxel.btnp(pyxel.KEY_SPACE):
        auto = not auto

    if auto:
        shear -= shear_step

    if shear < -shear_limit:
        shear = shear_limit
    elif shear > shear_limit:
        shear = -shear_limit

    ax -= 3.2
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

    pyxel.text(-40,4, f"{shear:+2.2f}", 2)

def floor(y, stop, step):
    src_y = 0
    x = (16 * shear) - 48


    for i in range(0, stop, step):
        pyxel.blt(x, y, 0, 0, src_y, 256, 1)
        y += step
        pyxel.blt(x, y, 0, 0, src_y, 256, 1)
        y += step

        if y % 2 == 0:
            x += shear

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

