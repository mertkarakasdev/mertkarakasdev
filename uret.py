# -*- coding: utf-8 -*-
"""Profil README'si için SVG varlıklarını üretir. Düzenleyip tekrar çalıştır: python3 uret.py"""
import re, pathlib, html

QR_KAYNAK = "/private/tmp/claude-501/-Users-tallconn-Desktop-Blog/1b976717-2646-4796-b49b-a26af27ab6d0/scratchpad/qr.svg"

AD        = "TUĞRUL MERT KARAKAŞ"
ALT       = "FULL STACK · DESIGN · BRANDING · SEO"
SLOGAN    = "From idea to deployment."
DISIPLIN  = "FULL STACK DEVELOPMENT · GRAPHIC DESIGN · BRAND IDENTITY · SEO"
SATIRLAR  = [
    ("Frontend", "React · Next.js · Vue.js · JavaScript · HTML · CSS"),
    ("Backend",  "Node.js · Python · REST API"),
    ("DevOps",   "Vercel · Docker · Git · GitHub"),
    ("Design",   "Figma · Photoshop · Illustrator"),
    ("Growth",   "Google Ads · Google Business · SEO"),
]
DUGMELER = [
    ("website",  "MERTKARAKASDEV.GITHUB.IO", 250),
    ("linkedin", "LINKEDIN",                 150),
    ("email",    "EMAIL",                    120),
]

FONT = "'Helvetica Neue', Helvetica, Arial, sans-serif"

TEMA = {
    "dark":  dict(zemin="#0d1117", ad="#f0f6fc", ikincil="#8b949e", silik="#6e7681",
                  dugme="#161b22", kenar="#21262d", qr="#f0f6fc"),
    "light": dict(zemin="#ffffff", ad="#1f2328", ikincil="#656d76", silik="#8c959f",
                  dugme="#f6f8fa", kenar="#d0d7de", qr="#1f2328"),
}

IKON = {
    "website":  '<circle cx="8" cy="8" r="7"/><ellipse cx="8" cy="8" rx="3.2" ry="7"/>'
                '<line x1="1" y1="8" x2="15" y2="8"/>',
    "linkedin": '<rect x="1" y="1" width="14" height="14" rx="2"/><line x1="4.5" y1="7" x2="4.5" y2="12"/>'
                '<circle cx="4.5" cy="4.3" r="0.6"/><path d="M8 12V8.6a1.9 1.9 0 0 1 3.8 0V12"/>',
    "email":    '<rect x="1" y="2.5" width="14" height="11" rx="2"/><path d="M1.6 4l6.4 4.6L14.4 4"/>',
}

def svg(ic, w, h, zemin=None):
    arka = f'<rect width="{w}" height="{h}" fill="{zemin}"/>' if zemin else ""
    return (f'<svg fill="none" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'xmlns="http://www.w3.org/2000/svg">\n  {arka}\n{ic}\n</svg>\n')

def metin(x, y, s, boyut, renk, agirlik=400, aralik=0):
    return (f'  <text x="{x}" y="{y}" font-family="{FONT}" font-size="{boyut}" '
            f'font-weight="{agirlik}" letter-spacing="{aralik}" fill="{renk}">{html.escape(s)}</text>')

qr_d = re.search(r'<path style="fill:rgb\(0, 0, 0\)" d="([^"]+)"', pathlib.Path(QR_KAYNAK).read_text()).group(1)

for ad_tema, t in TEMA.items():
    # --- header ---
    qr = (f'  <svg x="664" y="52" width="96" height="96" viewBox="0 0 200 200">\n'
          f'    <path d="{qr_d}" fill="{t["qr"]}"/>\n  </svg>')
    pathlib.Path(f"header-{ad_tema}.svg").write_text(svg(
        metin(56, 98, AD, 26, t["ad"], 500, 7) + "\n" +
        metin(58, 128, ALT, 10.5, t["ikincil"], 400, 4.5) + "\n" + qr,
        800, 200, t["zemin"]))

    # --- disiplinler ---
    pathlib.Path(f"disciplines-{ad_tema}.svg").write_text(svg(
        metin(0, 26, SLOGAN, 18, t["ikincil"]) + "\n" +
        metin(0, 56, DISIPLIN, 10, t["silik"], 400, 2.2),
        640, 72))

    # --- tech ---
    satir = []
    for i, (etiket, deger) in enumerate(SATIRLAR):
        y = 18 + i * 24
        satir.append(metin(0, y, etiket, 13, t["ikincil"], 500))
        satir.append(metin(72, y, deger.replace(" · ", "  ·  "), 13, t["silik"], 300, 0.6))
    pathlib.Path(f"tech-{ad_tema}.svg").write_text(svg("\n".join(satir), 650, 18 + len(SATIRLAR) * 24))

    # --- iletişim düğmeleri ---
    for anahtar, yazi, w in DUGMELER:
        ic = (f'  <rect x="0" y="0" width="{w}" height="40" rx="6" fill="{t["dugme"]}" '
              f'stroke="{t["kenar"]}"/>\n'
              f'  <g transform="translate(14, 12)" fill="none" stroke="{t["ikincil"]}" '
              f'stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round">{IKON[anahtar]}</g>\n'
              + metin(42, 25, yazi, 10.5, t["ikincil"], 500, 1.2))
        pathlib.Path(f"contact-{anahtar}-{ad_tema}.svg").write_text(svg(ic, w, 40))

print("uretildi:", len(list(pathlib.Path('.').glob('*.svg'))), "svg")
