import pyxel


pyxel.init(160, 144, title="gameboy", fps=60)

pyxel.image(0).load(0, 0, "images/background2.png")
pyxel.image(0).load(0, 32, "images/actors.png")

def update():
    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()


def draw():
    pyxel.cls(0)
    #pyxel.rect(10, 10, 20, 20, c)
    background()
    floor()
    ceiling()
    actors()

def background():
    dst_y = 32
    for i in range(64):
        pyxel.blt(-32, dst_y, 0, 0, 3, 224, 1)
        dst_y += 1

def floor():
    dst_y = 80
    src_y = 0
    for i in range(64):
        pyxel.blt(-32, dst_y, 0, 0, src_y, 224, 1)
        dst_y += 1
        if i % 2 == 0:
            src_y += 1

def ceiling():
    dst_y = 32
    src_y = 0
    for i in range(64):
        pyxel.blt(-32, dst_y, 0, 0, src_y, 224, 1)
        dst_y -= 1
        if i % 2 == 0:
            src_y += 1

def actors():
    pyxel.blt(20, 90,
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

