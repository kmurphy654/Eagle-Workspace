# -*- coding: utf-8 -*-
"""Parameterized Eagle warranty + external-sheet generator (two separate files).
Usage:
  make_warranty.py --addr "44 Jasper St, Saugus, MA" \
      --template-warranty "/path/4 Warranty.pdf" \
      --template-external "/path/External Radon System Sheet.pdf" \
      --out-warranty "/path/Warranty.pdf" --out-external "/path/External.pdf"
"""
import argparse, io
from reportlab.pdfgen import canvas
from pypdf import PdfReader, PdfWriter

p = argparse.ArgumentParser()
p.add_argument("--addr", required=True)
p.add_argument("--template-warranty", required=True)   # path to "4 Warranty.pdf"
p.add_argument("--template-external", required=True)   # path to "External Radon System Sheet.pdf"
p.add_argument("--out-warranty", required=True)
p.add_argument("--out-external", required=True)
args = p.parse_args()

Wp, Hp = 611.04, 790.8
buf = io.BytesIO(); c = canvas.Canvas(buf, pagesize=(Wp, Hp))
c.setFont("Helvetica", 11)
c.drawString(140, Hp - 192, args.addr)
c.save(); buf.seek(0)
ov = PdfReader(buf).pages[0]
w = PdfWriter(); pg = PdfReader(args.template_warranty).pages[0]; pg.merge_page(ov); w.add_page(pg)
with open(args.out_warranty, "wb") as f: w.write(f)
print("wrote", args.out_warranty)
w2 = PdfWriter()
for page in PdfReader(args.template_external).pages: w2.add_page(page)
with open(args.out_external, "wb") as f: w2.write(f)
print("wrote", args.out_external)
