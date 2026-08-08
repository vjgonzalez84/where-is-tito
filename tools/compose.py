#!/usr/bin/env python3
"""Recorta a Tito y a Lola por umbral y los compone sobre la lamina.

El umbral se aplica a resolucion completa y la figura se reduce despues, para
que el resampleo antialiasee el borde duro que deja el corte. Las posiciones se
expresan en porcentaje del lienzo, igual que las hitboxes del JSON de nivel:
x/y son la esquina superior izquierda.
"""
import argparse
import pathlib

from PIL import Image

AVATARS = pathlib.Path("/home/sanjocara/projects/where-is-tito/assets/avatars")
LOLA_PLINTH_TOP = 916  # fila donde arranca el pedestal de piedra


def cutout(path, cut_below=None):
    """Umbral a blanco -> alfa, y recorte a la caja de tinta."""
    im = Image.open(path).convert("RGBA")
    if cut_below:
        im = im.crop((0, 0, im.width, cut_below))
    px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, _ = px[x, y]
            if r > 240 and g > 240 and b > 240:
                px[x, y] = (r, g, b, 0)
    return im.crop(im.getbbox())


def place(plate, fig, x, y, h):
    """Pega fig con su alto en % del lienzo; el ancho sale del aspecto real."""
    W, H = plate.size
    ph = round(h / 100 * H)
    pw = round(fig.width * ph / fig.height)
    plate.alpha_composite(fig.resize((pw, ph), Image.LANCZOS),
                          (round(x / 100 * W), round(y / 100 * H)))
    return pw / W * 100  # ancho efectivo en %, para la hitbox


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("plate")
    ap.add_argument("out")
    ap.add_argument("--tito", nargs=3, type=float, metavar=("X", "Y", "H"),
                    default=[18.5, 83.0, 13.0])
    ap.add_argument("--lola", nargs=3, type=float, metavar=("X", "Y", "H"),
                    default=[82.0, 57.0, 14.0])
    ap.add_argument("--boxes", action="store_true", help="dibujar las hitboxes")
    args = ap.parse_args()

    tito = cutout(AVATARS / "tito_perdido.jpg")
    lola = cutout(AVATARS / "lola.jpg", cut_below=LOLA_PLINTH_TOP)
    tito.save("tito.png")
    lola.save("lola.png")
    print(f"tito recortado {tito.size}  lola recortada {lola.size}")

    plate = Image.open(args.plate).convert("RGBA")
    wt = place(plate, tito, *args.tito)
    wl = place(plate, lola, *args.lola)
    for name, (x, y, h), w in [("tito", args.tito, wt), ("lola", args.lola, wl)]:
        print(f'  {name}: "x": {x}, "y": {y}, "width": {w:.1f}, "height": {h}')

    if args.boxes:
        from PIL import ImageDraw
        d = ImageDraw.Draw(plate)
        W, H = plate.size
        for (x, y, h), w, col in [(args.tito, wt, (200, 40, 40, 255)),
                                  (args.lola, wl, (30, 110, 200, 255))]:
            d.rectangle([x / 100 * W, y / 100 * H,
                         (x + w) / 100 * W, (y + h) / 100 * H],
                        outline=col, width=4)

    plate.convert("RGB").save(args.out, quality=92)
    print("->", args.out)


if __name__ == "__main__":
    main()
