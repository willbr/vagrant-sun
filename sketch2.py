import pyxel
import math

x_offset = 31
shear = 0

pyxel.init(320, 144, title="gameboy", fps=60)
pyxel.camera(-80, 0)

pyxel.image(0).load(0, 0, "images/background3.png")
pyxel.image(0).load(0, 32, "images/actors.png")

def update():
    global x_offset
    global shear

    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()

    if pyxel.btn(pyxel.KEY_LEFT):
        x_offset -= 1

    if pyxel.btn(pyxel.KEY_RIGHT):
        x_offset += 1

    #x_offset += 1
    x_offset %= 32
    shear = 0.05 * (x_offset - 16)


def draw():
    pyxel.cls(0)
    #background()
    floor()
    #ceiling()
    #actors()

    if False:
        pyxel.rect(-80, 0, 80, 144, 0)
        pyxel.rect(160, 0, 80, 144, 0)

    pyxel.line(0,0, 0, 144, 2)
    pyxel.line(160,0, 160, 144, 2)

    pyxel.text(4,4, f"{x_offset}\n{shear:+2.2f}", 2)

def background():
    dst_x = (x_offset % 32) - 32
    #dst_x = -32
    dst_y = 32
    for i in range(48):
        pyxel.blt(dst_x, dst_y, 0, 0, 3, 224, 1)
        dst_y += 1

def floor():
    global shear
    dst_y = 80
    src_y = 0
    for i in range(32):
        x = (shear * i) + x_offset - 32
        y = dst_y + i
        pyxel.blt(x, y, 0, 0, src_y, 224, 1)
        src_y += 1


def ceiling():
    dst_x = (x_offset % 32) - 32
    dst_x = -32
    dst_y = 32
    src_y = 0
    for i in range(64):
        pyxel.blt(dst_x, dst_y, 0, 0, src_y, 224, 1)
        dst_y -= 1
        if i % 2 == 0:
            src_y += 1

def actors():
    pyxel.blt(x_offset, 90,
              0,
              0, 32,
              17, 32)

    pyxel.blt(100, 40,
              0,
              24, 32,
              17, 32)

    pyxel.blt(130, 90,
              0,
              50, 32,
              17, 32)


pyxel.run(update, draw)

