"""Adds play buttons and clickable video links to portfolio.pdf.

PDFs can't play video reliably outside Acrobat, so each motion piece gets a
play badge plus a link to its MP4 on joozoo.work (assets/video/).
Run once on a fresh portfolio.pdf: `python3 add_video_links.py`.
"""
import io

from pypdf import PdfReader, PdfWriter
from pypdf.annotations import Link
from reportlab.lib.colors import Color
from reportlab.pdfgen import canvas

PDF = "portfolio.pdf"
SITE = "https://joozoo.work/assets/video/"

# page number (1-based) → [(x0, y0, x1, y1) in points from the top-left, video file, draw badge?]
LINKS = {
    28: [((557, 187, 1023, 558), "vertical-holiday-card-2022.mp4", False)],  # mockup already shows ▶
    32: [((197, 215, 377, 520), "harris-lines-city-panel-1.mp4", True),
         ((457, 215, 636, 520), "harris-lines-city-panel-2.mp4", True),
         ((716, 215, 895, 520), "harris-lines-city-panel-3.mp4", True)],
}


def badge_overlay(w, h, boxes):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=(w, h))
    for (x0, y0, x1, y1), _, draw in boxes:
        if not draw:
            continue
        cx, cy, r = (x0 + x1) / 2, h - (y0 + y1) / 2, 22
        c.setFillColor(Color(1, 1, 1, alpha=0.88))
        c.circle(cx, cy, r, stroke=0, fill=1)
        c.setFillColor(Color(0.1, 0.1, 0.1))
        p = c.beginPath()
        p.moveTo(cx - 6, cy - 9)
        p.lineTo(cx - 6, cy + 9)
        p.lineTo(cx + 10, cy)
        p.close()
        c.drawPath(p, stroke=0, fill=1)
    c.showPage()
    c.save()
    buf.seek(0)
    return PdfReader(buf).pages[0]


def main():
    reader = PdfReader(PDF)
    writer = PdfWriter(clone_from=reader)
    for num, boxes in LINKS.items():
        page = writer.pages[num - 1]
        w, h = float(page.mediabox.width), float(page.mediabox.height)
        page.merge_page(badge_overlay(w, h, boxes))
        for (x0, y0, x1, y1), video, _ in boxes:
            link = Link(rect=(x0, h - y1, x1, h - y0), url=SITE + video, border=[0, 0, 0])
            writer.add_annotation(page_number=num - 1, annotation=link)
    with open(PDF, "wb") as f:
        writer.write(f)
    print("linked", sum(len(v) for v in LINKS.values()), "videos")


if __name__ == "__main__":
    main()
