# -*- coding: utf-8 -*-
"""Parameterized Eagle proposal generator. Renders the pre-signed form and overlays fields.
Usage:
  make_proposal.py --name "Lauren Garant" --addr "44 Jasper St" --town "Saugus Ma" \
      --points 1 --pipe 3 --fan GX5A --price 1650.00 --date 6/10/2026 \
      --template "/path/Blank with signature.pdf" \
      --out "/path/Proposal.pdf" [--central] [--run "to the exterior"] [--interior]

  --interior  Fan in attic, pipe through roof. Omits suction-point count description.
"""
import argparse
import pypdfium2 as pdfium
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader

p = argparse.ArgumentParser()
p.add_argument("--name", required=True)
p.add_argument("--addr", required=True)
p.add_argument("--town", required=True)
p.add_argument("--points", type=int, default=1)
p.add_argument("--pipe", default="3")
p.add_argument("--fan", default="RP145")
p.add_argument("--price", required=True)
p.add_argument("--date", required=True)
p.add_argument("--template", required=True)      # path to "Blank with signature.pdf"
p.add_argument("--out", required=True)
p.add_argument("--central", action="store_true")
p.add_argument("--run", default="to the exterior")
p.add_argument("--interior", action="store_true")
args = p.parse_args()

im = pdfium.PdfDocument(args.template)[0].render(scale=3.0).to_pil().convert("RGB")
TMP = "/tmp/_eagle_base_signed.png"
im.save(TMP)
H = 792.0
def ry(t): return H - t
c = canvas.Canvas(args.out, pagesize=letter)
c.drawImage(ImageReader(TMP), 0, 0, width=612, height=792)
c.setFillColorRGB(0, 0, 0)
c.setFont("Helvetica", 10); c.drawString(476, ry(124), args.date)
c.setFont("Helvetica", 8); c.drawString(474, ry(100), args.addr)
c.setFont("Helvetica", 10)
c.drawString(60, ry(138), args.name)
c.drawString(60, ry(158), args.addr)
c.drawString(60, ry(177), args.town)
c.drawString(213, ry(138), "Same")
c.setFont("Helvetica", 9.5)
c.drawString(315, ry(244), str(args.points))
c.drawString(85, ry(255), args.pipe)
c.drawString(345, ry(255), args.run)
c.drawString(446, ry(266.5), "RadonAway")
if args.interior:
    c.drawString(245, ry(280), "in the attic")
    c.drawString(135, ry(291), "through the roof")
else:
    c.drawString(245, ry(280), "on the outside")
    c.drawString(135, ry(291), "above the roof edge")
c.drawString(165, ry(416), "1")
_words = ["Zero","One","Two","Three","Four","Five","Six","Seven","Eight","Nine","Ten"]
def _pt(n):
    w = _words[n] if n < len(_words) else str(n)
    return f"{w} ({n})"

if args.interior:
    l1 = "Zero (0) holes will be drilled in the foundation slab for this installation."
    l2 = "Exact fan and pipe location to be determined the day of installation."
    l3 = "System guaranteed below 4.0 pCi/L.  5-year manufacturer's warranty on fan."
elif args.points == 1:
    if args.central:
        l1 = "One (1) suction point located toward the center of the basement; pipe runs from the"
        l2 = "hole out to the exterior fan. Exact location to be determined the day of installation."
    else:
        l1 = "One (1) suction point; pipe runs from the hole to the exterior."
        l2 = "Exact location to be determined the day of installation."
    l3 = "System guaranteed below 4.0 pCi/L.  5-yr warranty on fan unit."
else:
    l1 = f"{_pt(args.points)} suction points; pipe runs from the holes, segmenting the basement slab, to the"
    l2 = "exterior. Exact locations to be determined the day of installation."
    l3 = "System guaranteed below 4.0 pCi/L.  5-yr warranty on fan unit."
c.drawString(95, ry(443), l1)
c.drawString(95, ry(455), l2)
c.drawString(95, ry(467), l3)
c.setFont("Helvetica-Bold", 11); c.drawString(515, ry(571), args.price)
c.save()
print("wrote", args.out)
