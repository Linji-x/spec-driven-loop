from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
FONT_CANDIDATES = [
    Path("C:/Windows/Fonts/segoeuib.ttf"),
    Path("C:/Windows/Fonts/arialbd.ttf"),
]


def font(size: int):
    for candidate in FONT_CANDIDATES:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


def gradient(size, start, end):
    image = Image.new("RGB", size, start)
    pixels = image.load()
    width, height = size
    for y in range(height):
        for x in range(width):
            t = (x / max(width - 1, 1) + y / max(height - 1, 1)) / 2
            pixels[x, y] = tuple(int(a + (b - a) * t) for a, b in zip(start, end))
    return image


def draw_icon(size: int) -> Image.Image:
    image = Image.new("RGBA", (size, size), (17, 21, 43, 255))
    draw = ImageDraw.Draw(image)
    radius = size // 4
    draw.rounded_rectangle((0, 0, size - 1, size - 1), radius=radius, fill=(17, 21, 43, 255))
    left, right = int(size * .23), int(size * .77)
    line_width = max(5, int(size * .09))
    for y, short in ((.28, False), (.5, True), (.72, False)):
        x2 = int(size * (.58 if short else .77))
        draw.line((left, int(size * y), x2, int(size * y)), fill=(109, 94, 248, 255), width=line_width)
    cx, cy, cr = int(size * .71), int(size * .5), int(size * .15)
    draw.ellipse((cx-cr, cy-cr, cx+cr, cy+cr), fill=(17, 21, 43, 255), outline=(255, 255, 255, 255), width=max(3, int(size * .055)))
    draw.line((cx-int(cr*.35), cy, cx-int(cr*.05), cy+int(cr*.3)), fill=(49, 216, 181, 255), width=max(3, int(size*.04)))
    draw.line((cx-int(cr*.05), cy+int(cr*.3), cx+int(cr*.48), cy-int(cr*.35)), fill=(49, 216, 181, 255), width=max(3, int(size*.04)))
    return image


def render_icon():
    target = ROOT / "spec-driven-loop" / "assets" / "icon-512.png"
    target.parent.mkdir(parents=True, exist_ok=True)
    draw_icon(512).save(target)


def render_social():
    width, height = 1280, 640
    image = gradient((width, height), (17, 21, 43), (36, 28, 70)).convert("RGBA")
    draw = ImageDraw.Draw(image, "RGBA")
    draw.ellipse((950, -270, 1500, 280), fill=(109, 94, 248, 32))
    draw.ellipse((-260, 410, 290, 960), fill=(49, 216, 181, 22))
    image.alpha_composite(draw_icon(132), (74, 68))
    draw.text((230, 76), "Spec-Driven Loop", font=font(58), fill=(255, 255, 255, 255))
    draw.text((77, 234), "Freeze the specification.", font=font(48), fill=(255, 255, 255, 255))
    draw.text((77, 297), "Coordinate the agents.", font=font(48), fill=(202, 197, 255, 255))
    draw.text((77, 360), "Judge the evidence.", font=font(48), fill=(159, 241, 221, 255))
    stages = ["Inspect", "Grill", "Freeze", "Agents", "Judge", "Loop"]
    x, y = 78, 484
    for index, stage in enumerate(stages):
        box_w = 164
        fill = (35, 42, 76, 240) if index < 4 else (24, 59, 61, 240)
        border = (129, 119, 255, 255) if index < 4 else (49, 216, 181, 255)
        draw.rounded_rectangle((x, y, x + box_w, y + 66), radius=16, fill=fill, outline=border, width=2)
        bbox = draw.textbbox((0, 0), stage, font=font(24))
        draw.text((x + (box_w - (bbox[2]-bbox[0]))/2, y + 18), stage, font=font(24), fill=(255, 255, 255, 255))
        if index < len(stages) - 1:
            draw.text((x + box_w + 10, y + 15), "→", font=font(24), fill=(129, 119, 255, 255))
        x += 198
    target = ROOT / "docs" / "assets" / "social-preview.png"
    target.parent.mkdir(parents=True, exist_ok=True)
    image.save(target, optimize=True)


if __name__ == "__main__":
    render_icon()
    render_social()
