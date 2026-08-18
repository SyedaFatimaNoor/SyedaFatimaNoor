"""Photo to dithered dot runs: crop, skin mask, luminance adapt, threshold."""

from PIL import Image, ImageChops, ImageFilter, ImageOps

from .build import CROP, GRID_H, GRID_W, LUM_THRESHOLD


def load_rgb(path):
    return Image.open(path).convert("RGB")


def crop_to_grid(img):
    w, h = img.size
    x0, y0, x1, y1 = CROP
    box = (int(w * x0), int(h * y0), int(w * x1), int(h * y1))
    cropped = img.crop(box)
    return ImageOps.fit(cropped, (GRID_W, GRID_H), Image.LANCZOS)


def mean_luminance(img):
    gray = ImageOps.grayscale(img)
    data = list(gray.getdata())
    return sum(data) / len(data)


def _largest_blob(mask):
    w, h = mask.size
    raw = list(mask.getdata())
    seen = [False] * (w * h)
    best = []

    def fill(sx, sy):
        stack = [(sx, sy)]
        comp = []
        while stack:
            x, y = stack.pop()
            i = y * w + x
            if x < 0 or y < 0 or x >= w or y >= h or seen[i] or raw[i] == 0:
                continue
            seen[i] = True
            comp.append((x, y))
            stack.extend(((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)))
        return comp

    for y in range(h):
        for x in range(w):
            i = y * w + x
            if raw[i] and not seen[i]:
                comp = fill(x, y)
                if len(comp) > len(best):
                    best = comp
    out = Image.new("L", (w, h), 0)
    for x, y in best:
        out.putpixel((x, y), 255)
    return out


def subject_mask(img, thr_scale=1.0):
    hsv = img.convert("HSV")
    h, s, v = hsv.split()
    hue_ok = h.point(lambda p: 255 if p < 32 else 0)
    sat_ok = s.point(lambda p: 255 if 20 < p < 225 else 0)
    val_ok = v.point(lambda p: 255 if p > int(46 * thr_scale) else 0)
    mask = ImageChops.multiply(hue_ok, ImageChops.multiply(sat_ok, val_ok))
    mask = mask.filter(ImageFilter.MedianFilter(5))
    mask = _largest_blob(mask)
    return mask.filter(ImageFilter.GaussianBlur(1))


def _threshold(data, w, h, thresh, dark):
    table = list(data)
    for y in range(h):
        for x in range(w):
            i = y * w + x
            old = table[i]
            new = 255.0 if (old >= thresh if dark else old <= thresh) else 0.0
            err = old - new
            table[i] = new
            if x + 1 < w:
                table[y * w + x + 1] += err * 7 / 16
            if y + 1 < h:
                if x > 0:
                    table[(y + 1) * w + x - 1] += err * 3 / 16
                table[(y + 1) * w + x] += err * 5 / 16
                if x + 1 < w:
                    table[(y + 1) * w + x + 1] += err * 1 / 16
    return table


def dot_runs(img, dark, thr_scale=1.0, mask=None):
    img = crop_to_grid(img)
    gray = ImageOps.grayscale(img)
    w, h = gray.size
    data = [float(p) for p in gray.getdata()]
    subj = mask if mask is not None else subject_mask(img, thr_scale)
    subj_data = list(subj.getdata())

    mask_mean = 128.0
    subj_lum = [data[i] for i in range(len(data)) if subj_data[i] > 90]
    if subj_lum:
        mask_mean = sum(subj_lum) / len(subj_lum)

    mean = mean_luminance(gray)
    if dark:
        polarity = "paint"
    else:
        polarity = "ink" if mean >= LUM_THRESHOLD else "paint"
    thresh = mask_mean * (0.94 if polarity == "paint" else 1.04)

    table = _threshold(data, w, h, thresh, polarity == "paint")
    for i in range(len(table)):
        if table[i] < 128:
            continue
        lit = data[i] >= 200
        inside = subj_data[i] > 90
        if not (inside or lit):
            table[i] = 0.0

    runs = []
    for y in range(h):
        row = []
        x = 0
        while x < w:
            if table[y * w + x] >= 128:
                x1 = x
                while x + 1 < w and table[y * w + x + 1] >= 128:
                    x += 1
                row.append((x1, x))
            x += 1
        if row:
            runs.append((y, row))
    return runs
