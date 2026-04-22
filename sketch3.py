import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import os

WIDTH = 256
HEIGHT = 144
SCALE = 2
CAMERA_X = -48
CAMERA_Y = 0
FPS = 15
FRAME_MS = int(1000 / FPS)

BACKGROUND_PATH = "images/background3.png"
ACTORS_PATH = "images/actors.png"

COL_BLACK = (0, 0, 0, 255)
COL_PURPLE = (0x7E, 0x20, 0x72, 255)
COL_TEAL = (0x19, 0x95, 0x9C, 255)

shear_limit = 10
shear_step = 1
shear = 0
auto = True
ax, ay = 140, 90
ax_step = 32

bg_bank = None
actors_img = None
old_stamp = 0


def load_background():
    global bg_bank, old_stamp
    src = Image.open(BACKGROUND_PATH).convert("RGBA")
    bank = Image.new("RGBA", (256, 32), COL_BLACK)
    bank.paste(src, (0, 0))
    bank.paste(src.transpose(Image.FLIP_LEFT_RIGHT), (128, 0))
    bg_bank = bank
    old_stamp = os.stat(BACKGROUND_PATH).st_mtime


def load_actors():
    global actors_img
    actors_img = Image.open(ACTORS_PATH).convert("RGBA")


load_background()
load_actors()

root = tk.Tk()
root.title("gameboy")
canvas = tk.Canvas(
    root,
    width=WIDTH * SCALE,
    height=HEIGHT * SCALE,
    highlightthickness=0,
    bg="black",
)
canvas.pack()

keys_down = set()
keys_just_pressed = set()


def on_key_press(event):
    k = event.keysym
    if k not in keys_down:
        keys_just_pressed.add(k)
    keys_down.add(k)


def on_key_release(event):
    keys_down.discard(event.keysym)


root.bind("<KeyPress>", on_key_press)
root.bind("<KeyRelease>", on_key_release)


def world_to_screen(x, y):
    return int(x - CAMERA_X), int(y - CAMERA_Y)


def blit_slice(frame, wx, wy, src_y):
    sx, sy = world_to_screen(wx, wy)
    slice_img = bg_bank.crop((0, src_y, 256, src_y + 1))
    frame.alpha_composite(slice_img, (sx, sy))


def draw_floor(frame, y, stop, step):
    src_y = 0
    x = (16 * shear / 10) - 48

    for _ in range(0, stop, step):
        blit_slice(frame, x, y, src_y)
        y += step
        blit_slice(frame, x, y, src_y)
        y += step

        if y % 2 == 0:
            x += shear / 10

        src_y += 1


def draw_actor(frame):
    sprite = actors_img.crop((0, 0, 17, 30))
    sx, sy = world_to_screen(ax, ay)
    frame.alpha_composite(sprite, (sx, sy))


def draw_rect_world(draw, wx, wy, w, h, color):
    sx, sy = world_to_screen(wx, wy)
    draw.rectangle([sx, sy, sx + w - 1, sy + h - 1], fill=color)


_photo = None


def render():
    global _photo
    frame = Image.new("RGBA", (WIDTH, HEIGHT), COL_BLACK)

    draw_floor(frame, y=80, stop=32, step=1)
    draw_floor(frame, y=40, stop=-32, step=-1)
    draw_actor(frame)

    draw = ImageDraw.Draw(frame)
    draw_rect_world(draw, -48, 0, 48, 144, COL_TEAL)
    draw_rect_world(draw, 160, 0, 48, 144, COL_TEAL)

    scaled = frame.resize((WIDTH * SCALE, HEIGHT * SCALE), Image.NEAREST)
    _photo = ImageTk.PhotoImage(scaled)
    canvas.delete("all")
    canvas.create_image(0, 0, image=_photo, anchor="nw")

    sx, sy = world_to_screen(-40, 4)
    canvas.create_text(
        sx * SCALE,
        sy * SCALE,
        text=f"{shear:+2d}",
        fill="#7E2072",
        anchor="nw",
        font=("Courier", 8),
    )
    sx, sy = world_to_screen(-40, 12)
    canvas.create_text(
        sx * SCALE,
        sy * SCALE,
        text=f"{ax_step:+2d}",
        fill="#7E2072",
        anchor="nw",
        font=("Courier", 8),
    )


def update():
    global auto, shear, ax, ax_step, old_stamp

    try:
        stamp = os.stat(BACKGROUND_PATH).st_mtime
        if stamp != old_stamp:
            load_background()
    except OSError:
        pass

    if "Up" in keys_just_pressed:
        ax_step += 1
    if "Down" in keys_just_pressed:
        ax_step -= 1
    if "space" in keys_just_pressed:
        auto = not auto

    keys_just_pressed.clear()

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


def tick():
    update()
    render()
    root.after(FRAME_MS, tick)


tick()
root.mainloop()
