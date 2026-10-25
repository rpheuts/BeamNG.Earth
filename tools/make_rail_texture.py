"""Generate seamless PBR railway track texture t_rail_track_b.png.

Geometry layout on a 2.8m wide by 2.4m long ribbon:
- 512x512 RGBA
- Width 2.8m -> 512 px (~182.9 px/m)
- Length 2.4m -> 512 px (~213.3 px/m)
- Standard gauge: 1.435m -> 262 px spacing (rails at x=125 and x=387)
- 4 timber ties (sleepers) per repeat -> 0.6m spacing (128 px period)
- Transparent alpha between ties so the ballast easement shows through
"""
import os
import numpy as np
from PIL import Image, ImageDraw


def generate_rail_texture(size=512):
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)

    # 1. Generate 4 timber ties (sleepers)
    tie_h = 46                     # px height (~21.5 cm)
    tie_x0 = 18                    # left end of tie
    tie_x1 = size - 18             # right end of tie (~2.6 m long)
    tie_centers = [32, 160, 288, 416]

    for cy in tie_centers:
        y0 = cy - tie_h // 2
        y1 = cy + tie_h // 2
        # Base tie wood
        draw.rectangle([tie_x0, y0, tie_x1, y1], fill=(46, 41, 37, 255))
        # Top bevel / highlight
        draw.line([tie_x0 + 1, y0, tie_x1 - 1, y0], fill=(62, 56, 50, 255))
        # Bottom bevel / shadow
        draw.line([tie_x0 + 1, y1, tie_x1 - 1, y1], fill=(30, 26, 23, 255))
        # Left/right end shadows
        draw.line([tie_x0, y0 + 1, tie_x0, y1 - 1], fill=(35, 31, 28, 255))
        draw.line([tie_x1, y0 + 1, tie_x1, y1 - 1], fill=(35, 31, 28, 255))

        # Subtle wood grain variations
        np.random.seed(cy)
        for gy in range(y0 + 2, y1 - 1, 3):
            variation = int(np.random.randint(-6, 8))
            r = min(255, max(0, 46 + variation))
            g = min(255, max(0, 41 + variation))
            b = min(255, max(0, 37 + variation))
            draw.line([tie_x0 + 2, gy, tie_x1 - 2, gy], fill=(r, g, b, 255))

    # 2. Steel tie plates & fastener clips under rails
    rail_xs = [125, 387]
    plate_hw = 16                  # half-width across track
    plate_hh = 20                  # half-height along track

    for cy in tie_centers:
        for rx in rail_xs:
            px0, px1 = rx - plate_hw, rx + plate_hw
            py0, py1 = cy - plate_hh, cy + plate_hh
            # Base plate
            draw.rectangle([px0, py0, px1, py1], fill=(60, 58, 56, 255))
            draw.rectangle([px0, py0, px1, py1], outline=(40, 38, 36, 255))
            # 4 spike / bolt heads
            for sx in (px0 + 3, px1 - 3):
                for sy in (py0 + 3, py1 - 3):
                    draw.rectangle([sx - 1, sy - 1, sx + 1, sy + 1], fill=(95, 92, 88, 255))

    # 3. Continuous steel rails (vertical lines from y=0 to size-1)
    for rx in rail_xs:
        # Rail foot / flange (dark rusted/weathered steel, width 15 px)
        draw.line([(rx - 7, 0), (rx - 7, size)], fill=(55, 52, 49, 255), width=1)
        draw.line([(rx + 7, 0), (rx + 7, size)], fill=(55, 52, 49, 255), width=1)
        draw.rectangle([rx - 6, 0, rx + 6, size], fill=(75, 71, 68, 255))

        # Rail head sides (width 9 px)
        draw.rectangle([rx - 4, 0, rx + 4, size], fill=(135, 140, 148, 255))
        draw.rectangle([rx - 3, 0, rx + 3, size], fill=(185, 192, 202, 255))

        # Polished running crown (polished bright steel from train wheels, width 5 px)
        draw.rectangle([rx - 2, 0, rx + 2, size], fill=(225, 230, 238, 255))
        # Central specular highlight
        draw.line([(rx, 0), (rx, size)], fill=(250, 252, 255, 255), width=1)

    return im


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target = os.path.join(root, "mod", "beamng_earth", "levels", "beamng_earth",
                          "art", "shapes", "beamngEarth", "t_rail_track_b.png")
    os.makedirs(os.path.dirname(target), exist_ok=True)
    im = generate_rail_texture(512)
    im.save(target, "PNG")
    print(f"Saved rail track texture to {target} ({im.size}, mode={im.mode})")


if __name__ == "__main__":
    main()
