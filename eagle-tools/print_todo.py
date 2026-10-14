#!/usr/bin/env python3
"""Make a compact, print-friendly PDF of the Eagle To-Do List.

Input: the saved result of a Claude Docs `read` of the to-do list body (either the
plain JSON reply or the [{type,text}] list the tool output file holds).
Output: a letter-size PDF with short notes, small type and tight tables.

    python3 eagle-tools/print_todo.py <doc-read-result-file> <out.pdf>
"""
import html
import json
import re
import sys
import xml.etree.ElementTree as ET

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (KeepTogether, Paragraph, SimpleDocTemplate, Spacer,
                                Table, TableStyle)

NOTE_MAX = 140          # characters kept from each "what they need" note
EMAIL_RE = re.compile(r"\S+@\S+")
PHONE_RE = re.compile(r"\(?\d{3}\)?[-. ]?\d{3}-\d{4}")


def load_xml(path):
    raw = open(path).read()
    data = json.loads(raw)
    if isinstance(data, list):                       # tool-output wrapper
        data = json.loads(next(d["text"] for d in data if d["text"].lstrip().startswith("{")))
    return data["data"]["xml"]


def text_of(el):
    return re.sub(r"\s+", " ", "".join(el.itertext())).strip()


def short_note(s, keep_all=False):
    """Trim filler, then cap at NOTE_MAX on a word boundary (start of the note kept)."""
    s = s.strip()
    s = re.sub(r"^\(by text (\d+/\d+)\)\s*", r"Text \1: ", s)
    s = re.sub(r"\bWeb request \d+/\d+\.\s*", "", s)
    s = re.sub(r"\s*No reply (yet|found)\.", "", s)
    if keep_all or len(s) <= NOTE_MAX:
        return s
    return s[:NOTE_MAX].rsplit(" ", 1)[0].rstrip(",;:") + "…"


def short_contact(s):
    phones = PHONE_RE.findall(s)
    if phones:
        return ", ".join(dict.fromkeys(phones))
    m = EMAIL_RE.search(s)
    return m.group(0) if m else s


def parse(xml):
    root = ET.fromstring(xml)
    title, prepared, sections = "", "", []
    cur = None
    for el in root:
        if el.tag == "paragraph":
            t = text_of(el)
            lvl = el.get("heading")
            if lvl == "1":
                title = t
            elif lvl == "2":
                cur = {"name": t, "blocks": []}
                sections.append(cur)
            elif t.startswith("Prepared"):
                prepared = t
            elif cur is not None and t:
                cur["blocks"].append(("note", t))
        elif el.tag == "table" and cur is not None:
            rows = []
            for row in el.findall("row"):
                rows.append([text_of(c) for c in row.findall("cell")])
            cur["blocks"].append(("table", rows))
        elif el.tag == "list" and cur is not None:
            cur["blocks"].append(("list", [text_of(li) for li in el.findall("listItem")]))
    return title, prepared, sections


def build(xml, out):
    title, prepared, sections = parse(xml)
    base = ParagraphStyle("b", fontName="Helvetica", fontSize=7.5, leading=9)
    bold = ParagraphStyle("bb", parent=base, fontName="Helvetica-Bold")
    h1 = ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=13, leading=15)
    h2 = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=9.5, leading=11,
                        spaceBefore=6, spaceAfter=2)
    small = ParagraphStyle("s", parent=base, textColor=colors.HexColor("#555555"))
    P = lambda t, st=base: Paragraph(html.escape(t), st)

    story = [P(title, h1), P(prepared, small), Spacer(1, 4)]
    width = letter[0] - 0.8 * inch
    grid = TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#999999")),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8e8e8")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 2), ("RIGHTPADDING", (0, 0), (-1, -1), 2),
        ("TOPPADDING", (0, 0), (-1, -1), 1), ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
    ])

    for sec in sections:
        name = sec["name"]
        if name.startswith("7."):
            continue                                  # the done-log stays in the doc
        tables = [b for b in sec["blocks"] if b[0] == "table"]
        count = sum(max(len(t[1]) - 1, 0) for t in tables)
        story.append(P(f"{name}  ({count})", h2))
        for kind, val in sec["blocks"]:
            if kind == "note":
                if not name.startswith(("1.", "4.")):   # skip long intro lines
                    story.append(P(short_note(val), small))
                continue
            if kind != "table" or len(val) < 2:
                continue
            head, body = val[0], val[1:]
            ncol = len(head)
            if name.startswith("5."):                 # web quotes: compact 3-across list
                items = [f"[  ] {r[2]} — {r[3]} — {r[4]} — {r[5]}" for r in body if len(r) >= 6]
                cols = 2
                rows = [items[i:i + cols] + [""] * (cols - len(items[i:i + cols]))
                        for i in range(0, len(items), cols)]
                t = Table([[P(c) for c in r] for r in rows], colWidths=[width / cols] * cols)
                t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                                       ("LEFTPADDING", (0, 0), (-1, -1), 1),
                                       ("TOPPADDING", (0, 0), (-1, -1), 0),
                                       ("BOTTOMPADDING", (0, 0), (-1, -1), 1)]))
                story.append(t)
                continue
            data = [[P("" if i == 0 else h, bold) for i, h in enumerate(head)]]
            for r in body:
                r = (r + [""] * ncol)[:ncol]
                cells = []
                for i, c in enumerate(r):
                    if i == 0:
                        c = "[x]" if "x" in c.lower() else "[  ]"
                    elif ncol == 5 and i == 3:
                        c = short_contact(c)
                    elif i == ncol - 1:
                        c = short_note(c, keep_all="," in r[1] or r[1].startswith("Quotes"))
                    cells.append(P(c))
                data.append(cells)
            if ncol == 5:
                cw = [0.28, 1.3, 1.55, 1.2]
                cw.append(width / inch - sum(cw))
            elif ncol == 3:
                cw = [0.28, 1.6, width / inch - 1.88]
            else:
                cw = [width / inch / ncol] * ncol
            t = Table(data, colWidths=[c * inch for c in cw], repeatRows=1)
            t.setStyle(grid)
            story.append(t)
            story.append(Spacer(1, 3))

    def footer(canvas, doc):
        canvas.setFont("Helvetica", 6.5)
        canvas.setFillColor(colors.HexColor("#777777"))
        canvas.drawString(0.4 * inch, 0.3 * inch,
                          "Eagle To-Do List  ·  notes shortened for printing; full notes and "
                          "the 'Already done' log are in the online list")
        canvas.drawRightString(letter[0] - 0.4 * inch, 0.3 * inch, f"Page {doc.page}")

    SimpleDocTemplate(out, pagesize=letter, leftMargin=0.4 * inch, rightMargin=0.4 * inch,
                      topMargin=0.4 * inch, bottomMargin=0.5 * inch,
                      title="Eagle To-Do List").build(story, onFirstPage=footer,
                                                     onLaterPages=footer)


if __name__ == "__main__":
    build(load_xml(sys.argv[1]), sys.argv[2])
