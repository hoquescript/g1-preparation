#!/usr/bin/env python3
"""OCR the captured pages into a CSV of question number, question and answer (macOS Vision)."""
import argparse
import csv
import glob
import os
import re
import tempfile

import Quartz
import Vision
from PIL import Image, ImageDraw, ImageFont

from capture import load_pixels

# Vertical band (fractions of the window, top = 0) holding the question and answer text:
# below the "N/203" counter, above the prev/next arrows and ad banner.
CONTENT_TOP, CONTENT_BOTTOM = 0.20, 0.82
COUNTER_RE = re.compile(r"^(\d+)\s*/\s*(\d+)$")
# Bits of a blank's underline that OCR reads as punctuation next to the ____ marker.
BLANK_RE = re.compile(r"[\s.,\-—_]*____[\s.,\-—_]*")
PREFIX = "Answer is "
PREFIX_FONT = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"


def recognize(path):
    """Return [(text, (x, y, w, h))] with boxes as fractions of the image, y measured from the top."""
    url = Quartz.CFURLCreateFromFileSystemRepresentation(None, path.encode(), len(path.encode()), False)
    request = Vision.VNRecognizeTextRequest.alloc().init()
    request.setRecognitionLevel_(Vision.VNRequestTextRecognitionLevelAccurate)
    request.setUsesLanguageCorrection_(True)
    handler = Vision.VNImageRequestHandler.alloc().initWithURL_options_(url, None)
    handler.performRequests_error_([request], None)
    lines = []
    for obs in request.results():
        b = obs.boundingBox()
        top = 1 - b.origin.y - b.size.height
        lines.append((obs.topCandidates_(1)[0].string(), (b.origin.x, top, b.size.width, b.size.height)))
    return sorted(lines, key=lambda line: line[1][1])


def has_underline(pixels, x0, x1, top, height):
    """True if the gap between two words holds a drawn underline (a fill-in blank), not just spacing."""
    w, h, data = pixels
    dark = 0
    for y in range(int(top * h), int((top + height * 1.4) * h)):
        for x in range(int(x0 * w) + 2, int(x1 * w) - 2):
            i = (y * w + x) * 4
            if data[i] < 120 and data[i + 1] < 120 and data[i + 2] < 120:
                dark += 1
    return dark > 20


def merge_rows(pieces, pixels):
    """Join pieces on the same visual line left to right; an underlined gap is a fill-in blank, written as ____."""
    rows = []
    for text, box in sorted(pieces, key=lambda p: p[1][1]):
        if rows and abs(rows[-1][0][1][1] - box[1]) < 0.01:
            rows[-1].append((text, box))
        else:
            rows.append([(text, box)])
    merged = []
    for row in rows:
        row.sort(key=lambda p: p[1][0])
        text, (x, y, w, h) = row[0]
        for t, (bx, by, bw, bh) in row[1:]:
            text += " ____ " if has_underline(pixels, x + w, bx, y, h) else " "
            text += t
            w, h = bx + bw - x, max(h, bh)
        if x > 0.1 and has_underline(pixels, 0.03, x, y, h):
            text = "____ " + text
        if x + w < 0.9 and has_underline(pixels, x + w, 0.97, y, h):
            text += " ____"
        merged.append((text, (x, y, w, h)))
    return merged


def is_green(pixels, box):
    """True if the text inside box is drawn in the app's green answer colour."""
    w, h, data = pixels
    bx, by, bw, bh = box
    green = dark = 0
    for y in range(int(by * h), int((by + bh) * h)):
        for x in range(int(bx * w), int((bx + bw) * w), 2):
            i = (y * w + x) * 4
            r, g, b = data[i], data[i + 1], data[i + 2]
            if g > r + 40 and g > b + 40:
                green += 1
            elif r < 120 and g < 120 and b < 120:
                dark += 1
    return green > dark


def read_short_answer(path):
    """Vision skips lone characters like "0", so OCR the green text with a known prefix in front of it."""
    im = Image.open(path).convert("RGB")
    w, h = im.size
    px = im.load()
    green = [
        (x, y)
        for y in range(int(h * CONTENT_TOP), int(h * CONTENT_BOTTOM))
        for x in range(w)
        if px[x, y][1] > px[x, y][0] + 40 and px[x, y][1] > px[x, y][2] + 40
    ]
    if not green:
        return ""
    xs, ys = [p[0] for p in green], [p[1] for p in green]
    glyphs = im.crop((min(xs) - 6, min(ys) - 6, max(xs) + 6, max(ys) + 6))
    font = ImageFont.truetype(PREFIX_FONT, glyphs.height - 6)
    prefix_w = int(ImageDraw.Draw(im).textlength(PREFIX, font=font))
    canvas = Image.new("RGB", (prefix_w + glyphs.width + 60, glyphs.height + 60), px[30, h // 2])
    ImageDraw.Draw(canvas).text((30, 30), PREFIX, fill=(60, 160, 60), font=font)
    canvas.paste(glyphs, (30 + prefix_w, 30))
    canvas = canvas.resize((canvas.width * 2, canvas.height * 2))
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        canvas.save(tmp.name)
    try:
        text = " ".join(t for t, _ in recognize(tmp.name))
    finally:
        os.remove(tmp.name)
    return text.removeprefix(PREFIX.strip()).strip()


def parse_page(path):
    pixels = load_pixels(path)
    number, question, answer = None, [], []
    for text, box in merge_rows(recognize(path), pixels):
        if number is None and (m := COUNTER_RE.match(text.replace(" ", ""))):
            number = int(m.group(1))
        elif CONTENT_TOP <= box[1] <= CONTENT_BOTTOM:
            (answer if is_green(pixels, box) else question).append(text)
    answer = " ".join(answer) or read_short_answer(path)
    question = BLANK_RE.sub(" ____ ", " ".join(question)).strip()
    return number, question, answer


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--src", default="screenshots", help="directory of page_*.png files")
    p.add_argument("--out", default="questions.csv", help="CSV file to write")
    args = p.parse_args()

    files = sorted(glob.glob(f"{args.src}/page_*.png"))
    with open(args.out, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["number", "question", "answer", "file"])
        for path in files:
            number, question, answer = parse_page(path)
            writer.writerow([number, question, answer, path])
            flag = "" if number and question and answer else "  <-- check"
            print(f"{number}: {question[:60]} | {answer[:40]}{flag}")
    print(f"Wrote {len(files)} rows to {args.out}")


if __name__ == "__main__":
    main()
