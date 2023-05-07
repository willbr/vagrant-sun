import pyxel
import math

shear_limit = 1
shear_step = 0.1
shear = shear_limit
auto = True

pyxel.init(320, 144, title="gameboy", fps=15)
pyxel.camera(-80, 0)

pyxel.image(0).load(0, 0, "images/background3.png")

def update():
    global auto
    global shear

    if pyxel.btn(pyxel.KEY_LEFT):
        shear -= shear_step

    if pyxel.btn(pyxel.KEY_RIGHT):
        shear += shear_step

    if pyxel.btnp(pyxel.KEY_SPACE):
        auto = not auto

    if auto:
        pass

    if auto:
        shear -= shear_step

    if shear < -shear_limit:
        shear = shear_limit
    elif shear > shear_limit:
        shear = -shear_limit


def draw():
    pyxel.cls(0)

    if False:
        pyxel.line(-16,0, -16,140, 2)
        pyxel.line(+16,0, +16,140, 2)
        pyxel.line(+32,0, +32,140, 2)

    floor()

    pyxel.line(0,0, 0, 144, 2)
    pyxel.line(160,0, 160, 144, 2)

    if True:
        pyxel.rect(-80, 0, 80, 144, 3)
        pyxel.rect(160, 0, 80, 144, 3)

    #pyxel.rect(80, 80, 2, 2, 5)

    pyxel.text(4,4, f"{shear:+2.2f}", 2)

def floor():
    src_y = 0
    y = 80
    x = (16 * shear) - 32


    for i in range(32):
        pyxel.blt(x, y, 0, 0, src_y, 224, 1)
        y += 1
        pyxel.blt(x, y, 0, 0, src_y, 224, 1)
        y += 1

        if y % 2 == 0:
            x += shear

        src_y += 1

pyxel.run(update, draw)

