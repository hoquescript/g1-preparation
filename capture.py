#!/usr/bin/env python3
"""Screenshot each page of an app shown in iPhone Mirroring, clicking "next" between pages."""
import argparse
import os
import subprocess
import sys
import time

import Quartz

# Position of the "next" arrow as a fraction of the window size
# (measured from a 708x1562 window capture: arrow at ~615,1356).
NEXT_X = 615 / 708
NEXT_Y = 1356 / 1562
# Half-size of the box searched for the blue arrow, as a fraction of the window.
ARROW_BOX = 30 / 708


def find_window(app_name):
    windows = Quartz.CGWindowListCopyWindowInfo(
        Quartz.kCGWindowListOptionOnScreenOnly | Quartz.kCGWindowListExcludeDesktopElements,
        Quartz.kCGNullWindowID,
    )
    candidates = [
        w for w in windows
        if w.get("kCGWindowOwnerName") == app_name and w.get("kCGWindowLayer") == 0
    ]
    if not candidates:
        names = sorted({w.get("kCGWindowOwnerName", "") for w in windows})
        sys.exit(f"No window found for '{app_name}'. Visible apps: {', '.join(names)}")
    # Largest window is the phone screen.
    win = max(candidates, key=lambda w: w["kCGWindowBounds"]["Width"] * w["kCGWindowBounds"]["Height"])
    b = win["kCGWindowBounds"]
    return win["kCGWindowNumber"], (b["X"], b["Y"], b["Width"], b["Height"])


def screenshot(window_id, path):
    subprocess.run(["screencapture", "-x", "-o", "-l", str(window_id), path], check=True)


def load_pixels(path):
    """Return (width, height, RGBA bytes) of a PNG, top row first."""
    url = Quartz.CFURLCreateFromFileSystemRepresentation(None, path.encode(), len(path.encode()), False)
    img = Quartz.CGImageSourceCreateImageAtIndex(Quartz.CGImageSourceCreateWithURL(url, None), 0, None)
    w, h = Quartz.CGImageGetWidth(img), Quartz.CGImageGetHeight(img)
    ctx = Quartz.CGBitmapContextCreate(
        None, w, h, 8, w * 4, Quartz.CGColorSpaceCreateDeviceRGB(), Quartz.kCGImageAlphaPremultipliedLast
    )
    Quartz.CGContextDrawImage(ctx, ((0, 0), (w, h)), img)
    return w, h, bytes(Quartz.CGBitmapContextGetData(ctx).as_buffer(w * h * 4))


def page_counter(path):
    """Pixels of the "N/203" counter strip, for detecting page changes."""
    w, h, data = load_pixels(path)
    return data[int(h * 0.16) * w * 4 : int(h * 0.20) * w * 4]


def page_changed(before, after):
    """True if the counter strip differs by more than re-render noise."""
    return sum(1 for a, b in zip(before, after) if abs(a - b) > 80) > 100


# Spots (fractions of the window) that are always plain page background on a question page.
BACKGROUND_SPOTS = [(0.035, 0.16), (0.035, 0.35), (0.035, 0.55), (0.035, 0.75), (0.5, 0.84), (0.2, 0.18)]
BACKGROUND_RGB = (241, 246, 251)


def has_next_arrow(path):
    """True if this is a normal question page (light background + blue "next" arrow), not an ad."""
    w, h, data = load_pixels(path)
    for fx, fy in BACKGROUND_SPOTS:
        i = (int(h * fy) * w + int(w * fx)) * 4
        if any(abs(data[i + c] - BACKGROUND_RGB[c]) > 12 for c in range(3)):
            return False
    cx, cy, r = int(w * NEXT_X), int(h * NEXT_Y), int(w * ARROW_BOX)
    blue = 0
    for y in range(cy - r, cy + r):
        for x in range(cx - r, cx + r):
            i = (y * w + x) * 4
            if data[i + 2] > 200 and data[i] < 100:
                blue += 1
    return blue > 50


def wait_for_page(window_id, path):
    """Screenshot; if an ad is covering the page, alert and wait until it's closed."""
    screenshot(window_id, path)
    if has_next_arrow(path):
        return
    print("  Ad detected - close it on the phone; continuing automatically once it's gone...")
    subprocess.Popen(["afplay", "/System/Library/Sounds/Glass.aiff"])
    while not has_next_arrow(path):
        time.sleep(1)
        screenshot(window_id, path)
    time.sleep(0.5)
    screenshot(window_id, path)


def click(x, y):
    # iPhone Mirroring ignores bare instant clicks: move first, set click state, hold briefly.
    point = Quartz.CGPointMake(x, y)
    source = Quartz.CGEventSourceCreate(Quartz.kCGEventSourceStateHIDSystemState)
    for event_type, pause in (
        (Quartz.kCGEventMouseMoved, 0.2),
        (Quartz.kCGEventLeftMouseDown, 0.15),
        (Quartz.kCGEventLeftMouseUp, 0),
    ):
        event = Quartz.CGEventCreateMouseEvent(source, event_type, point, Quartz.kCGMouseButtonLeft)
        Quartz.CGEventSetIntegerValueField(event, Quartz.kCGMouseEventClickState, 1)
        Quartz.CGEventPost(Quartz.kCGHIDEventTap, event)
        time.sleep(pause)


def activate(app_name):
    subprocess.run(["osascript", "-e", f'tell application "{app_name}" to activate'], check=False)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--app", default="iPhone Mirroring", help="owner name of the mirror window")
    p.add_argument("--count", type=int, default=203, help="number of pages to capture")
    p.add_argument("--start", type=int, default=1, help="number of the first file (for resuming)")
    p.add_argument("--delay", type=float, default=1.0, help="seconds to wait after clicking next")
    p.add_argument("--out", default="screenshots", help="output directory")
    p.add_argument("--dry-run", action="store_true", help="take one screenshot, print the click point, don't click")
    args = p.parse_args()

    os.makedirs(args.out, exist_ok=True)
    window_id, (wx, wy, ww, wh) = find_window(args.app)
    nx, ny = wx + ww * NEXT_X, wy + wh * NEXT_Y
    print(f"Window {window_id}: x={wx} y={wy} w={ww} h={wh}; next button at ({nx:.0f}, {ny:.0f})")

    if args.dry_run:
        path = os.path.join(args.out, "dry_run.png")
        screenshot(window_id, path)
        print(f"Saved {path}; next arrow visible: {has_next_arrow(path)}")
        return

    activate(args.app)
    for i in range(3, 0, -1):
        print(f"Starting in {i}...", end="\r", flush=True)
        time.sleep(1)

    end = args.start + args.count - 1
    try:
        for n in range(args.start, end + 1):
            # Re-read bounds each page in case the window was moved.
            window_id, (wx, wy, ww, wh) = find_window(args.app)
            path = os.path.join(args.out, f"page_{n:03d}.png")
            if n < end:
                wait_for_page(window_id, path)
            else:
                screenshot(window_id, path)  # last page may have no active next arrow
            print(f"[{n}/{end}] {path}")
            if n < end:
                before = page_counter(path)
                check = os.path.join(args.out, "_check.png")
                for attempt in range(3):
                    activate(args.app)
                    click(wx + ww * NEXT_X, wy + wh * NEXT_Y)
                    time.sleep(args.delay)
                    screenshot(window_id, check)
                    if page_changed(before, page_counter(check)):
                        break
                    print("  Page didn't change, clicking again...")
                else:
                    sys.exit(f"Next click isn't working. Fix it and resume with --start {n + 1}")
    except KeyboardInterrupt:
        print(f"\nStopped. Resume with --start {n}")
    finally:
        if os.path.exists(os.path.join(args.out, "_check.png")):
            os.remove(os.path.join(args.out, "_check.png"))


if __name__ == "__main__":
    main()
