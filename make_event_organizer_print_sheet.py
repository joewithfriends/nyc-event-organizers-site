from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from reportlab.graphics.barcode import qr
from reportlab.graphics.shapes import Drawing
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.graphics import renderPDF


SOURCE_IMAGE = Path(
    "/Users/joeahearn/Documents/Documents - Joe’s MacBook Air/Pools (x-Withfriends)/Events Withfriends/Event Organizer Community/WhatsApp Image 2026-04-22 at 21.14.14.jpeg"
)
OUTPUT_PDF = Path("nyc_event_organizers_2x4_duplex.pdf")
POSTER_CROP = Path("nyc_event_organizers_poster_crop.png")
PREVIEW_FRONT = Path("nyc_event_organizers_front_preview.png")
PREVIEW_BACK = Path("nyc_event_organizers_back_preview.png")
QR_PREVIEW = Path("nyc_event_organizers_rsvp_qr.png")

RSVP_URL = "https://pools.events/t/nif8ozem/"

PAGE_W, PAGE_H = landscape(letter)
COLS = 4
ROWS = 2
CELL_W = PAGE_W / COLS
CELL_H = PAGE_H / ROWS
PAGE_SAFE_MARGIN = 0.25 * inch

CORAL = colors.Color(255 / 255, 106 / 255, 76 / 255)
INK = colors.HexColor("#191919")
LIGHT = colors.HexColor("#fff7f2")


def find_may_edition_poster_crop(source: Image.Image) -> Image.Image:
    """Detect the left-hand orange poster, which includes the May Edition text."""
    image = source.convert("RGB")
    width, height = image.size
    pixels = image.load()

    xs = []
    ys = []
    for y in range(height):
        for x in range(0, width // 2):
            r, g, b = pixels[x, y]
            if r > 220 and 60 <= g <= 130 and b < 110:
                xs.append(x)
                ys.append(y)

    if not xs:
        raise RuntimeError("Could not detect the orange poster area.")

    left, right = min(xs), max(xs)
    top, bottom = min(ys), max(ys)

    # Add a tiny inset to remove screenshot anti-aliased frame edges.
    inset = 2
    return image.crop((left + inset, top + inset, right + 1 - inset, bottom + 1 - inset))


def draw_centered_image(pdf: canvas.Canvas, img_path: Path, x: float, y: float, w: float, h: float) -> None:
    with Image.open(img_path) as img:
        iw, ih = img.size
    scale = min(w / iw, h / ih)
    draw_w = iw * scale
    draw_h = ih * scale
    pdf.drawImage(
        str(img_path),
        x + (w - draw_w) / 2,
        y + (h - draw_h) / 2,
        width=draw_w,
        height=draw_h,
        preserveAspectRatio=True,
        anchor="c",
    )


def draw_cut_guides(pdf: canvas.Canvas) -> None:
    return


def cell_safe_box(col: int, row: int) -> tuple[float, float, float, float]:
    """Return the printable-safe box for a cell, including outer page margins."""
    x = col * CELL_W
    y = PAGE_H - (row + 1) * CELL_H
    left_inset = PAGE_SAFE_MARGIN if col == 0 else 0
    right_inset = PAGE_SAFE_MARGIN if col == COLS - 1 else 0
    bottom_inset = PAGE_SAFE_MARGIN if row == ROWS - 1 else 0
    top_inset = PAGE_SAFE_MARGIN if row == 0 else 0
    return (
        x + left_inset,
        y + bottom_inset,
        CELL_W - left_inset - right_inset,
        CELL_H - top_inset - bottom_inset,
    )


def uniform_poster_box(col: int, row: int) -> tuple[float, float, float, float]:
    """Return an equal-size poster box that fits all cells and avoids page edges."""
    cell_x = col * CELL_W
    cell_y = PAGE_H - (row + 1) * CELL_H
    uniform_w = CELL_W - PAGE_SAFE_MARGIN
    uniform_h = CELL_H - PAGE_SAFE_MARGIN
    return (
        cell_x + (CELL_W - uniform_w) / 2,
        cell_y + (CELL_H - uniform_h) / 2,
        uniform_w,
        uniform_h,
    )


def draw_qr(pdf: canvas.Canvas, url: str, x: float, y: float, size: float) -> None:
    code = qr.QrCodeWidget(url)
    bounds = code.getBounds()
    qr_w = bounds[2] - bounds[0]
    qr_h = bounds[3] - bounds[1]
    drawing = Drawing(size, size, transform=[size / qr_w, 0, 0, size / qr_h, 0, 0])
    drawing.add(code)
    renderPDF.draw(drawing, pdf, x, y)


def make_qr_image(url: str, pixels: int = 600) -> Image.Image:
    code = qr.QrCodeWidget(url)
    matrix = code.qr
    matrix.make()
    modules = matrix.getModuleCount()
    quiet_zone = 4
    module_px = max(1, pixels // (modules + quiet_zone * 2))
    size = (modules + quiet_zone * 2) * module_px

    img = Image.new("RGB", (size, size), "white")
    draw = ImageDraw.Draw(img)
    for y in range(modules):
        for x in range(modules):
            if matrix.isDark(y, x):
                x0 = (x + quiet_zone) * module_px
                y0 = (y + quiet_zone) * module_px
                draw.rectangle([x0, y0, x0 + module_px - 1, y0 + module_px - 1], fill="black")
    return img


def draw_back_panel(pdf: canvas.Canvas, x: float, y: float, w: float, h: float) -> None:
    margin = 0.34 * inch
    inner_x = x + margin
    inner_y = y + margin
    inner_w = w - 2 * margin
    inner_h = h - 2 * margin

    pdf.setFillColor(colors.white)
    pdf.rect(x, y, w, h, stroke=0, fill=1)

    qr_size = min(inner_w * 0.72, inner_h * 0.58)
    qr_x = x + (w - qr_size) / 2
    qr_y = y + inner_h * 0.31

    pdf.setFillColor(CORAL)
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawCentredString(x + w / 2, y + inner_h * 0.86, "RSVP")

    draw_qr(pdf, RSVP_URL, qr_x, qr_y, qr_size)

    pdf.setFillColor(CORAL)
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawCentredString(x + w / 2, y + inner_h * 0.18, "NYC Event Organizers Meetup")


def make_pdf() -> None:
    source = Image.open(SOURCE_IMAGE)
    poster = find_may_edition_poster_crop(source)
    poster.save(POSTER_CROP)

    pdf = canvas.Canvas(str(OUTPUT_PDF), pagesize=(PAGE_W, PAGE_H))

    # Front: eight mini-posters.
    pdf.setFillColor(CORAL)
    pdf.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    pad = 0.05 * inch
    for row in range(ROWS):
        for col in range(COLS):
            x, y, w, h = uniform_poster_box(col, row)
            draw_centered_image(pdf, POSTER_CROP, x + pad, y + pad, w - 2 * pad, h - 2 * pad)
    pdf.showPage()

    # Back: matching RSVP QR panels.
    pdf.setFillColor(colors.white)
    pdf.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    for row in range(ROWS):
        for col in range(COLS):
            x = col * CELL_W
            y = PAGE_H - (row + 1) * CELL_H
            draw_back_panel(pdf, x, y, CELL_W, CELL_H)
    pdf.save()


def make_previews() -> None:
    # Lightweight raster previews so the file can be inspected without opening the PDF.
    scale = 2
    qr_img = make_qr_image(RSVP_URL, 600)
    qr_img.save(QR_PREVIEW)
    for output, is_back in ((PREVIEW_FRONT, False), (PREVIEW_BACK, True)):
        img = Image.new("RGB", (int(PAGE_W * scale), int(PAGE_H * scale)), "white" if is_back else "#ff6a4c")
        draw = ImageDraw.Draw(img)
        if is_back:
            for row in range(ROWS):
                for col in range(COLS):
                    x0 = int(col * CELL_W * scale)
                    y0 = int(row * CELL_H * scale)
                    x1 = int((col + 1) * CELL_W * scale)
                    y1 = int((row + 1) * CELL_H * scale)
                    draw.rectangle([x0, y0, x1, y1], fill="white")
                    draw.text((x0 + (x1 - x0) / 2, y0 + 52), "RSVP", fill="#ff624d", anchor="mm")
                    qr_px = int((x1 - x0) * 0.42)
                    resized_qr = qr_img.resize((qr_px, qr_px), Image.Resampling.NEAREST)
                    img.paste(resized_qr, (x0 + (x1 - x0 - qr_px) // 2, y0 + int((y1 - y0) * 0.30)))
                    draw.text((x0 + (x1 - x0) / 2, y0 + int((y1 - y0) * 0.75)), "NYC Event Organizers Meetup", fill="#ff624d", anchor="mm")
        else:
            poster = Image.open(POSTER_CROP).convert("RGB")
            for row in range(ROWS):
                for col in range(COLS):
                    x0 = int(col * CELL_W * scale)
                    y0 = int(row * CELL_H * scale)
                    cell_w = int(CELL_W * scale)
                    cell_h = int(CELL_H * scale)
                    box_w = int((CELL_W - PAGE_SAFE_MARGIN) * scale)
                    box_h = int((CELL_H - PAGE_SAFE_MARGIN) * scale)
                    pad_px = int(0.05 * inch * scale)
                    max_w = box_w - 2 * pad_px
                    max_h = box_h - 2 * pad_px
                    ratio = min(max_w / poster.width, max_h / poster.height)
                    resized = poster.resize((int(poster.width * ratio), int(poster.height * ratio)), Image.Resampling.LANCZOS)
                    box_x = x0 + (cell_w - box_w) // 2
                    box_y = y0 + (cell_h - box_h) // 2
                    img.paste(resized, (box_x + (box_w - resized.width) // 2, box_y + (box_h - resized.height) // 2))
        img.save(output)


if __name__ == "__main__":
    make_pdf()
    make_previews()
    print(f"Created {OUTPUT_PDF}")
    print(f"Created {POSTER_CROP}")
    print(f"Created {PREVIEW_FRONT}")
    print(f"Created {PREVIEW_BACK}")
    print(f"Created {QR_PREVIEW}")
