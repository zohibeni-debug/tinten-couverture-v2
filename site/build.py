# -*- coding: utf-8 -*-
"""Générateur du site Tinten Couverture.

Usage : python3 site/build.py
Produit le dossier public/ (pages HTML complètes, sitemap, robots, redirections).
"""
import hashlib
import html
import json
import math
import os
import re
import shutil
from datetime import date

import content as C

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
PUBLIC = os.path.join(ROOT, "public")
TODAY = date.today().isoformat()
PHOTOS = json.load(open(os.path.join(SITE, "photos.json"), encoding="utf-8"))
B = C.BUSINESS
URL = C.SITE_URL

# ---------------------------------------------------------------------------
# Outils
# ---------------------------------------------------------------------------

def esc(s):
    return html.escape(s, quote=True)


def fr(text):
    """Typographie française sur le texte (hors balises) : espaces insécables."""
    parts = re.split(r"(<[^>]+>)", text)
    out = []
    for p in parts:
        if p.startswith("<"):
            out.append(p)
            continue
        p = re.sub(r" ([?!;:])(?=\s|$|<)", "\u202f\\1", p)
        p = re.sub(r" ([?!;])", "\u202f\\1", p)
        p = p.replace("« ", "«\u00a0").replace(" »", "\u00a0»")
        p = re.sub(r"(\d) (km|m|cm|h|%|€|ans|semaines|jours)\b", "\\1\u00a0\\2", p)
        p = re.sub(r"(\d) (\d{3})\b", "\\1\u00a0\\2", p)
        out.append(p)
    return "".join(out)


def asset_version(path):
    with open(os.path.join(PUBLIC, path.lstrip("/")), "rb") as f:
        return hashlib.sha1(f.read()).hexdigest()[:10]


def img(slug, alt, sizes="100vw", cls="", eager=False):
    meta = PHOTOS[slug]
    widths = meta["sizes"]
    w = widths[-1]
    h = round(meta["h"] * w / meta["w"])
    srcset = ", ".join(f"/assets/img/{slug}-{x}.webp {x}w" for x in widths)
    src = f"/assets/img/{slug}-{widths[min(1, len(widths) - 1)]}.webp"
    attrs = [f'src="{src}"', f'srcset="{srcset}"', f'sizes="{sizes}"', f'width="{w}"', f'height="{h}"', f'alt="{esc(alt)}"']
    attrs.append('fetchpriority="high"' if eager else 'loading="lazy"')
    attrs.append('decoding="async"')
    if cls:
        attrs.append(f'class="{cls}"')
    return "<img " + " ".join(attrs) + ">"


def tel_link(cls="", label=None):
    label = label or B["phone"]
    c = f' class="{cls}"' if cls else ""
    return f'<a{c} href="tel:{B["phone_e164"]}">{esc(label)}</a>'


def jsonld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + "</script>"


ORG_ID = URL + "/#entreprise"
EARLY_JS = "document.documentElement.classList.add('js')"
EARLY_JS_HASH = "sha256-" + __import__("base64").b64encode(hashlib.sha256(EARLY_JS.encode()).digest()).decode()


def org_schema():
    return {
        "@context": "https://schema.org",
        "@type": "RoofingContractor",
        "@id": ORG_ID,
        "name": B["name"],
        "url": URL + "/",
        "logo": URL + "/assets/img/logo.png",
        "image": URL + "/assets/img/og-tinten-couverture.jpg",
        "telephone": B["phone_e164"],
        "email": B["email"],
        "foundingDate": str(B["since"]),
        "address": {
            "@type": "PostalAddress",
            "streetAddress": B["street"],
            "postalCode": B["postcode"],
            "addressLocality": B["city"],
            "addressRegion": "Pays de la Loire",
            "addressCountry": "FR",
        },
        "areaServed": [{"@type": "City", "name": c["name"]} for c in C.CITIES],
        "openingHoursSpecification": [
            {"@type": "OpeningHoursSpecification", "dayOfWeek": h["days"], "opens": h["opens"], "closes": h["closes"]}
            for h in B["hours_schema"]
        ],
        "sameAs": [B["facebook"]],
        "knowsAbout": ["Couverture en ardoise", "Couverture en tuiles", "Zinguerie", "Ravalement de façade", "Fenêtres de toit"],
    }


def breadcrumb_schema(items):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": name, "item": URL + path}
            for i, (name, path) in enumerate(items)
        ],
    }


def faq_schema(faq):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq
        ],
    }


# ---------------------------------------------------------------------------
# Gabarit commun
# ---------------------------------------------------------------------------

def header(current):
    items = []
    for s in C.SERVICES:
        here = ' aria-current="page"' if current == s["slug"] else ""
        items.append(f'<li><a href="/{s["slug"]}"{here}>{esc(s["nav"])}</a></li>')
    def nav_link(slug, label):
        here = ' aria-current="page"' if current == slug else ""
        return f'<li><a href="/{slug}"{here}>{label}</a></li>'
    return f"""
<a class="skip" href="#contenu">Aller au contenu</a>
<header class="site-header">
  <div class="wrap header-in">
    <a class="brand" href="/" aria-label="Tinten Couverture, accueil">
      <img src="/assets/img/logo-entete-64.png" srcset="/assets/img/logo-entete-64.png 249w, /assets/img/logo-entete-128.png 498w, /assets/img/logo-entete-192.png 747w" sizes="(min-width: 1040px) 218px, 187px" width="249" height="64" alt="Tinten Couverture, couvreur, zingueur et ravalement">
    </a>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="nav"><span class="burger" aria-hidden="true"></span>Menu</button>
    <nav class="nav" id="nav" aria-label="Navigation principale">
      <ul class="nav-list">
        <li class="has-sub">
          <details class="sub">
            <summary>Prestations</summary>
            <ul class="sub-list">{''.join(items)}</ul>
          </details>
        </li>
        {nav_link('zone-intervention', "Zone d'intervention")}
        {nav_link('realisations', 'Réalisations')}
        {nav_link('a-propos', 'À propos')}
      </ul>
      <div class="nav-cta">
        {tel_link('btn btn-ghost nav-tel')}
        <a class="btn btn-primary" href="/devis">Demander un devis</a>
      </div>
    </nav>
  </div>
</header>"""


def footer():
    services = "".join(f'<li><a href="/{s["slug"]}">{esc(s["nav"])}</a></li>' for s in C.SERVICES)
    cities = "".join(f'<li><a href="/{c["slug"]}">Couvreur à {esc(c["name"])}</a></li>' for c in C.CITIES)
    return f"""
<footer class="site-footer">
  <div class="wrap footer-grid">
    <div class="footer-id">
      <img src="/assets/img/logo-blanc-96.png" width="289" height="96" alt="Tinten Couverture" loading="lazy">
      <address>
        {esc(B['street'])}<br>{B['postcode']} {esc(B['city'])}<br>
        <a href="tel:{B['phone_e164']}">{B['phone']}</a><br>
        <a href="mailto:{B['email']}">{B['email']}</a>
      </address>
      <p>{fr(esc(B['hours_text']))}</p>
      <p><a href="{B['facebook']}" rel="noopener">Page Facebook</a></p>
    </div>
    <nav aria-label="Prestations"><h2>Prestations</h2><ul>{services}</ul></nav>
    <nav aria-label="Communes"><h2>Communes</h2><ul>{cities}<li><a href="/zone-intervention">Toute la zone d'intervention</a></li></ul></nav>
    <nav aria-label="Entreprise"><h2>Entreprise</h2><ul>
      <li><a href="/a-propos">À propos</a></li>
      <li><a href="/realisations">Réalisations</a></li>
      <li><a href="/devis">Demander un devis</a></li>
      <li><a href="/mentions-legales">Mentions légales</a></li>
      <li><a href="/confidentialite">Confidentialité</a></li>
    </ul></nav>
  </div>
  <div class="wrap footer-base">
    <p>© {date.today().year} Tinten Couverture, couvreur à Saumur depuis {B['since']}.</p>
    <p>Site réalisé par <a href="https://allositeweb.com" rel="noopener">ALLOSITEWEB</a></p>
  </div>
</footer>
<div class="callbar" role="region" aria-label="Contact rapide">
  <a class="btn btn-primary" href="tel:{B['phone_e164']}">Appeler</a>
  <a class="btn btn-light" href="/devis">Devis gratuit</a>
</div>"""


def layout(path, title, desc, body, current="", schemas=(), og_image="/assets/img/og-tinten-couverture.jpg", noindex=False):
    canonical = URL + ("/" if path in ("", "/") else "/" + path.strip("/"))
    css_v = asset_version("/assets/css/site.css")
    js_v = asset_version("/assets/js/site.js")
    robots = '<meta name="robots" content="noindex">' if noindex else '<meta name="robots" content="index, follow, max-image-preview:large">'
    ld = "".join(jsonld(s) for s in schemas)
    return f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canonical}">
{robots}
<meta name="theme-color" content="#26313a">
<meta property="og:type" content="website">
<meta property="og:locale" content="fr_FR">
<meta property="og:site_name" content="Tinten Couverture">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{URL}{og_image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/assets/img/icon-512.png" type="image/png" sizes="512x512">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preload" href="/assets/fonts/archivo-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/site.css?v={css_v}">
<script>{EARLY_JS}</script>
{ld}
</head>
<body>
{header(current)}
<main id="contenu">
{fr(body)}
</main>
{footer()}
<script src="/assets/js/site.js?v={js_v}" defer></script>
</body>
</html>
"""


def breadcrumb(items):
    lis = []
    for i, (name, path) in enumerate(items):
        if i == len(items) - 1:
            lis.append(f'<li aria-current="page">{esc(name)}</li>')
        else:
            lis.append(f'<li><a href="{path}">{esc(name)}</a></li>')
    return f'<nav class="crumbs wrap" aria-label="Fil d\'Ariane"><ol>{"".join(lis)}</ol></nav>'


def cta_band(title="Un projet de toiture ? Parlons-en.", text="Décrivez-nous la situation : nous venons voir et vous remettons un devis détaillé, gratuit et sans engagement."):
    return f"""
<section class="cta-band">
  <div class="wrap cta-in">
    <div>
      <h2>{fr(esc(title))}</h2>
      <p>{fr(esc(text))}</p>
    </div>
    <div class="cta-actions">
      {tel_link('btn btn-primary btn-lg', 'Appeler le ' + B['phone'])}
      <a class="btn btn-ghost btn-lg" href="/devis">Demander un devis</a>
    </div>
  </div>
</section>"""


def faq_block(faq, title="Questions fréquentes"):
    items = "".join(
        f'<details class="faq-item"><summary>{fr(esc(q))}</summary><div><p>{fr(esc(a))}</p></div></details>' for q, a in faq
    )
    return f'<section class="faq" aria-labelledby="faq-titre"><h2 id="faq-titre">{fr(esc(title))}</h2>{items}</section>'


def contact_aside():
    return f"""
<aside class="aside-card" aria-label="Contact">
  <h2>Devis gratuit</h2>
  <p>Nous venons voir la toiture et vous remettons un devis détaillé.</p>
  {tel_link('btn btn-primary btn-block', 'Appeler le ' + B['phone'])}
  <a class="btn btn-ghost btn-block" href="/devis">Demander par écrit</a>
  <p class="aside-meta">{fr(esc(B['hours_text']))}<br>{esc(B['street'])}, {esc(B['city'])}</p>
</aside>"""


# ---------------------------------------------------------------------------
# Schéma « anatomie d'une toiture »
# ---------------------------------------------------------------------------

def anatomy_svg():
    """Coupe en escalier d'une toiture en ardoise : chaque couche s'arrête un peu avant
    celle du dessous, pour qu'on voie toutes les épaisseurs."""
    ang = math.radians(17)
    u = (math.cos(ang), -math.sin(ang))          # le long du rampant, vers le faîtage
    n = (-math.sin(ang), -math.cos(ang))         # perpendiculaire, vers l'extérieur
    E = (0.0, 0.0)
    pts_all = []

    def P(s, t):
        p = (E[0] + s * u[0] + t * n[0], E[1] + s * u[1] + t * n[1])
        pts_all.append(p)
        return p

    def poly(pts, fill, stroke, sw=1.4):
        d = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        return f'<polygon points="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"/>'

    # Épaisseurs (t) et fins de couche (s) : la couverture s'arrête la première.
    RAF = (-84, 0)      # chevron
    MEM = (0, 7)        # écran sous-toiture
    CL = (7, 29)        # contre-liteaux
    LT = (29, 53)       # liteaux
    TH = 9              # épaisseur d'une ardoise
    END = {"raf": 900, "mem": 815, "cl": 730, "lt": 640, "sl": 545}
    START = -40
    out = []

    # Mur en tuffeau sous l'égout : le chevron repose sur la sablière en tête de mur
    tl, tr = P(-6, RAF[0]), P(96, RAF[0])
    w_bot = tl[1] + 96
    pts_all += [(tl[0], w_bot), (tr[0], w_bot)]
    out.append(poly([tl, tr, (tr[0], w_bot), (tl[0], w_bot)], "#ece5d3", "#c9bfa6"))
    for k in range(1, 4):
        yy = tl[1] + k * 26
        if yy >= w_bot - 4:
            break
        out.append(f'<line x1="{tl[0]:.1f}" y1="{yy:.1f}" x2="{tr[0]:.1f}" y2="{yy:.1f}" stroke="#d8ceb5" stroke-width="1.2"/>')
        off = 0 if k % 2 else 30
        for xx in range(int(tl[0] + 22 + off), int(tr[0]) - 4, 60):
            out.append(f'<line x1="{xx}" y1="{max(yy - 26, tl[1]):.1f}" x2="{xx}" y2="{yy:.1f}" stroke="#d8ceb5" stroke-width="1.2"/>')

    out.append(poly([P(START, RAF[0]), P(END["raf"], RAF[0]), P(END["raf"], RAF[1]), P(START, RAF[1])], "#bb8f60", "#7e5e3b"))
    # veinage du bois
    for tt in (-60, -36, -16):
        a1, b1 = P(START + 40, tt), P(END["raf"] - 30, tt + 6)
        out.append(f'<line x1="{a1[0]:.1f}" y1="{a1[1]:.1f}" x2="{b1[0]:.1f}" y2="{b1[1]:.1f}" stroke="#a87d50" stroke-width="1.2"/>')
    out.append(poly([P(START + 6, MEM[0]), P(END["mem"], MEM[0]), P(END["mem"], MEM[1]), P(START + 6, MEM[1])], "#5b7a90", "#3d586b", 1.1))
    out.append(poly([P(START + 6, CL[0]), P(END["cl"], CL[0]), P(END["cl"], CL[1]), P(START + 6, CL[1])], "#dcbd91", "#9c7a50"))

    pitch = 100
    k = 0
    batten_ends = []
    while True:
        s0 = 6 + k * pitch
        if s0 + 30 > END["lt"]:
            break
        out.append(poly([P(s0, LT[0]), P(s0 + 30, LT[0]), P(s0 + 30, LT[1]), P(s0, LT[1])], "#c99d6d", "#86663f"))
        batten_ends.append(s0)
        k += 1

    # Ardoises : coupe en dents de scie. Chaque rang recouvre la tête des deux rangs
    # inférieurs, d'où une épaisseur de trois ardoises et un ressaut à chaque pureau.
    base = LT[1]
    s_start = -34
    s_end = END["sl"]
    tails = []
    k = 0
    while s_start + k * pitch < s_end - 20:
        tails.append(s_start + k * pitch)
        k += 1
    top = []
    for idx, s0 in enumerate(tails):
        nxt = min(s0 + pitch, s_end)
        lift = TH * min(idx, 2)
        top.append(P(s0, base + lift + TH))
        top.append(P(nxt, base + lift + TH - 3 if nxt < s_end else base + 3 * TH - 3))
    band = [P(s_start, base)] + top + [P(s_end, base)]
    out.append(poly(band, "#475766", "#26313a", 1.4))
    # dessous de chaque ardoise, visible dans l'épaisseur de la coupe
    for idx, s0 in enumerate(tails):
        lift = TH * min(idx, 2)
        a1 = P(s0, base + lift)
        s1 = min(s0 + 2.3 * pitch, s_end)
        frac = (s1 - s0) / (2.3 * pitch)
        b1 = P(s1, base + lift * (1 - frac))
        if idx > 0:
            out.append(f'<line x1="{a1[0]:.1f}" y1="{a1[1]:.1f}" x2="{b1[0]:.1f}" y2="{b1[1]:.1f}" stroke="#2f3c47" stroke-width="1.2"/>')
        # face visible éclairée
        f0 = P(s0 + 4, base + lift + TH - 0.8)
        f1 = P(min(s0 + pitch, s_end) - 4, base + lift + TH - 3.6)
        out.append(f'<line x1="{f0[0]:.1f}" y1="{f0[1]:.1f}" x2="{f1[0]:.1f}" y2="{f1[1]:.1f}" stroke="#8496a3" stroke-width="2" stroke-linecap="round"/>')
        # crochet inox au pied de l'ardoise
        c0, c1 = P(s0 + 3, base + lift + TH + 2.5), P(s0 + 3, base + lift - 3)
        out.append(f'<path d="M{c0[0]:.1f},{c0[1]:.1f} L{c1[0]:.1f},{c1[1]:.1f}" stroke="#d3dade" stroke-width="2.4" stroke-linecap="round"/>')

    # Gouttière demi-ronde en zinc, suspendue à l'égout
    eave = P(-34, LT[1])
    gx, gy = eave[0] - 6, eave[1] + 30
    r = 28
    pts_all += [(gx - r - 6, gy - 4), (gx + r + 6, gy + r + 6)]
    out.append(f'<path d="M{gx - r:.1f},{gy:.1f} a{r},{r} 0 0 0 {2 * r},0 Z" fill="#c8d0d5" stroke="#6f7c84" stroke-width="2"/>')
    out.append(f'<path d="M{gx - r - 5:.1f},{gy:.1f} h{2 * r + 10}" stroke="#6f7c84" stroke-width="2.4" stroke-linecap="round"/>')
    hk = P(START + 14, MEM[1])
    out.append(f'<path d="M{hk[0]:.1f},{hk[1]:.1f} L{gx + r:.1f},{gy:.1f}" stroke="#6f7c84" stroke-width="2" fill="none"/>')

    # Repères numérotés
    marks = []

    def marker(num, target, pos):
        (tx, ty), (px, py) = target, pos
        pts_all.extend([(px - 24, py - 24), (px + 24, py + 24)])
        marks.append(
            f'<line x1="{tx:.1f}" y1="{ty:.1f}" x2="{px:.1f}" y2="{py:.1f}" stroke="#26313a" stroke-width="1.6"/>'
            f'<circle cx="{tx:.1f}" cy="{ty:.1f}" r="4.5" fill="#26313a"/>'
            f'<circle cx="{px:.1f}" cy="{py:.1f}" r="21" fill="#97b854" stroke="#26313a" stroke-width="1.6"/>'
            f'<text x="{px:.1f}" y="{py + 8:.1f}" text-anchor="middle" font-size="23" font-weight="760" fill="#1e272e">{num}</text>'
        )

    def above(s, t, dist):
        tgt = P(s, t)
        return tgt, (tgt[0] + n[0] * dist, tgt[1] + n[1] * dist)

    marker(1, *above(330, LT[1] + 3 * TH - 2, 96))
    lt_s = [b_ for b_ in batten_ends if b_ + 30 <= END["lt"] and b_ > END["sl"] - 10]
    s_bat = (lt_s[0] + 15) if lt_s else END["lt"] - 30
    marker(2, *above(s_bat, (LT[0] + LT[1]) / 2, 112))
    marker(3, *above(END["cl"] - 40, (CL[0] + CL[1]) / 2, 128))
    marker(4, *above(END["mem"] - 40, (MEM[0] + MEM[1]) / 2, 140))
    marker(5, *above(END["raf"] - 40, (RAF[0] + RAF[1]) / 2, 196))
    gt = (gx, gy + r * 0.55)
    marker(6, gt, (gx - 70, gy + 86))
    out.extend(marks)

    xs = [p_[0] for p_ in pts_all]
    ys = [p_[1] for p_ in pts_all]
    pad = 14
    x0, y0, x1, y1 = min(xs) - pad, min(ys) - pad, max(xs) + pad, max(ys) + pad
    title = "Coupe d'une toiture en ardoise : ardoises posées au crochet, liteaux, contre-liteaux, écran sous-toiture, chevron et gouttière en zinc"
    return (
        f'<svg class="anatomy-svg" viewBox="{x0:.0f} {y0:.0f} {x1 - x0:.0f} {y1 - y0:.0f}" role="img" aria-labelledby="anat-t">'
        f'<title id="anat-t">{esc(title)}</title>' + "".join(out) + "</svg>"
    )


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------

def page_home():
    s_items = "".join(
        f'<li><a class="svc" href="/{s["slug"]}"><span class="svc-name">{esc(s["nav"])}</span><span class="svc-desc">{fr(esc(s["short"]))}</span></a></li>'
        for s in C.SERVICES
    )
    legend = "".join(
        f'<li><span class="num" aria-hidden="true">{i + 1}</span><div><h3>{esc(name)}</h3><p>{fr(esc(text))}</p>'
        f'<a href="/{slug}">{esc(C.SERVICE_BY_SLUG[slug]["nav"])}</a></div></li>'
        for i, (name, text, slug) in enumerate(C.ANATOMY)
    )
    steps = "".join(
        f'<li><h3>{esc(t)}</h3><p>{fr(esc(d))}</p></li>' for t, d in C.PROCESS
    )
    gal = C.GALLERY[1:7]
    gallery = "".join(
        f'<figure class="g-item g{i + 1}">{img(slug, cap, "(min-width: 1040px) 33vw, (min-width: 720px) 50vw, 100vw")}<figcaption>{fr(esc(cap))}</figcaption></figure>'
        for i, (slug, cap) in enumerate(gal)
    )
    cities = "".join(
        f'<li><a href="/{c["slug"]}">{esc(c["name"])}</a><span>{"Siège" if not c["dist"] else f"{c["dist"]} km"}</span></li>'
        for c in C.CITIES
    )
    body = f"""
<section class="hero">
  <div class="wrap hero-in">
    <div class="hero-text">
      <h1>{esc(C.HOME['h1'])}</h1>
      <p class="lead">{fr(esc(C.HOME['lead']))}</p>
      <div class="hero-actions">
        {tel_link('btn btn-primary btn-lg', 'Appeler le ' + B['phone'])}
        <a class="btn btn-ghost btn-lg" href="/devis">Demander un devis</a>
      </div>
      <ul class="facts">
        <li><strong>Depuis {B['since']}</strong><span>couvreur à Saumur</span></li>
        <li><strong>{B['radius_km']}{chr(160)}km</strong><span>autour de Saumur</span></li>
        <li><strong>Devis gratuit</strong><span>après visite</span></li>
      </ul>
    </div>
    <figure class="hero-photo">
      {img('toiture-ardoise-lucarne-saumur', "Toiture en ardoise avec lucarne habillée de zinc, réalisée par Tinten Couverture", "(min-width: 1040px) 55vw, 100vw", eager=True)}
      <figcaption>Couverture en ardoise et lucarne refaites par nos soins.</figcaption>
    </figure>
  </div>
</section>

<section class="services" aria-labelledby="svc-t">
  <div class="wrap">
    <div class="sec-head">
      <h2 id="svc-t">Nos prestations</h2>
      <p>Couverture, zinguerie, étanchéité et façades : tout ce qui protège la maison de la pluie.</p>
    </div>
    <ul class="svc-grid">{s_items}</ul>
  </div>
</section>

<section class="anatomy" aria-labelledby="anat-titre">
  <div class="wrap">
    <div class="sec-head">
      <h2 id="anat-titre">Ce qu'il y a sous une toiture en ardoise</h2>
      <p>Une toiture étanche, c'est six couches qui travaillent ensemble. Quand l'une d'elles vieillit, c'est elle qu'il faut traiter, pas forcément tout le toit.</p>
    </div>
    <div class="anatomy-grid">
      <div class="anatomy-figure">{anatomy_svg()}</div>
      <ol class="anatomy-legend">{legend}</ol>
    </div>
  </div>
</section>

<section class="process" aria-labelledby="proc-t">
  <div class="wrap">
    <div class="sec-head"><h2 id="proc-t">Comment se passe votre chantier</h2></div>
    <ol class="steps">{steps}</ol>
  </div>
</section>

<section class="gallery-sec" aria-labelledby="gal-t">
  <div class="wrap">
    <div class="sec-head sec-head-row">
      <h2 id="gal-t">Nos chantiers en images</h2>
      <a class="link-more" href="/realisations">Voir toutes les réalisations</a>
    </div>
    <div class="gallery">{gallery}</div>
  </div>
</section>

<section class="zone-sec" aria-labelledby="zone-t">
  <div class="wrap zone-in">
    <div>
      <h2 id="zone-t">Où intervenons-nous ?</h2>
      <p>À Saumur et dans un rayon d'environ {B['radius_km']}{chr(160)}km, en Maine-et-Loire, en Indre-et-Loire, dans la Vienne et les Deux-Sèvres.</p>
      <a class="btn btn-light" href="/zone-intervention">Voir toute la zone</a>
    </div>
    <ul class="zone-list">{cities}</ul>
  </div>
</section>

<section class="about-sec" aria-labelledby="about-t">
  <div class="wrap about-in">
    <figure class="about-photo">{img('couvreur-tinten-toiture', "Le couvreur de Tinten Couverture sur une toiture en ardoise à Saumur", "(min-width: 720px) 40vw, 100vw")}</figure>
    <div>
      <h2 id="about-t">Une entreprise artisanale de Saumur</h2>
      <p>{fr("Tinten Couverture est installée boulevard des Demoiselles, à Saumur, depuis 2009. Couverture, zinguerie et ravalement : nous réalisons nous-mêmes les travaux que nous chiffrons, et nous connaissons les toitures en ardoise et en tuffeau de la région.")}</p>
      <p>{fr("Les avis de nos clients sont publiés sur notre fiche Google, où vous pouvez les consulter librement.")}</p>
      <div class="about-actions">
        <a class="btn btn-ghost" href="/a-propos">En savoir plus sur l'entreprise</a>
        <a class="btn btn-ghost" href="{B['google_reviews']}" rel="noopener">Lire les avis Google</a>
      </div>
    </div>
  </div>
</section>

<div class="wrap narrow">{faq_block(C.HOME['faq'])}</div>
{cta_band()}
"""
    website = {"@context": "https://schema.org", "@type": "WebSite", "@id": URL + "/#site", "name": "Tinten Couverture", "url": URL + "/", "inLanguage": "fr-FR", "publisher": {"@id": ORG_ID}}
    return layout("/", C.HOME["title"], C.HOME["desc"], body, "home", [org_schema(), website, faq_schema(C.HOME["faq"])])


def page_service(s):
    crumbs = [("Accueil", "/"), (s["nav"], "/" + s["slug"])]
    sections = "".join(f'<section><h2>{fr(esc(t))}</h2>{fr(h)}</section>' for t, h in s["sections"])
    steps = ""
    if s.get("steps"):
        lis = "".join(f'<li><h3>{esc(t)}</h3><p>{fr(esc(d))}</p></li>' for t, d in s["steps"])
        steps = f'<section><h2>{fr(esc(s["steps_title"]))}</h2><ol class="steps steps-v">{lis}</ol></section>'
    related = "".join(
        f'<li><a class="svc" href="/{r}"><span class="svc-name">{esc(C.SERVICE_BY_SLUG[r]["nav"])}</span><span class="svc-desc">{fr(esc(C.SERVICE_BY_SLUG[r]["short"]))}</span></a></li>'
        for r in s["related"]
    )
    cities = ", ".join(f'<a href="/{c["slug"]}">{esc(c["name"])}</a>' for c in C.CITIES)
    body = f"""
{breadcrumb(crumbs)}
<section class="page-head">
  <div class="wrap page-head-in">
    <div>
      <h1>{fr(esc(s['h1']))}</h1>
      <p class="lead">{fr(esc(s['lead']))}</p>
      <div class="hero-actions">
        {tel_link('btn btn-primary', 'Appeler le ' + B['phone'])}
        <a class="btn btn-ghost" href="/devis">Demander un devis</a>
      </div>
    </div>
    <figure class="page-photo">{img(s['photo'], s['photo_alt'], "(min-width: 1040px) 45vw, 100vw", eager=True)}</figure>
  </div>
</section>
<div class="wrap content-grid">
  <article class="prose">
    {sections}
    {steps}
    <section><h2>Où intervenons-nous ?</h2><p>{fr("À Saumur et dans un rayon d'environ 40 km :")} {cities}.</p></section>
    {faq_block(s['faq'])}
  </article>
  {contact_aside()}
</div>
<section class="related" aria-labelledby="rel-t">
  <div class="wrap">
    <h2 id="rel-t">Prestations liées</h2>
    <ul class="svc-grid">{related}</ul>
  </div>
</section>
{cta_band()}
"""
    service_ld = {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": s["nav"],
        "serviceType": s["nav"],
        "description": s["desc"],
        "url": URL + "/" + s["slug"],
        "provider": {"@id": ORG_ID},
        "areaServed": [{"@type": "City", "name": c["name"]} for c in C.CITIES],
    }
    return layout(s["slug"], s["title"], s["desc"], body, s["slug"], [service_ld, breadcrumb_schema(crumbs), faq_schema(s["faq"]), org_schema()])


def page_city(c):
    crumbs = [("Accueil", "/"), ("Zone d'intervention", "/zone-intervention"), (f"Couvreur à {c['name']}", "/" + c["slug"])]
    local = "".join(f'<section><h2>{fr(esc(t))}</h2>{fr(h)}</section>' for t, h in c["local"])
    works = "".join(
        f'<li><a class="svc" href="/{w}"><span class="svc-name">{esc(C.SERVICE_BY_SLUG[w]["nav"])}</span><span class="svc-desc">{fr(esc(C.SERVICE_BY_SLUG[w]["short"]))}</span></a></li>'
        for w in c["works"]
    )
    nearby = ", ".join(esc(n) for n in c["nearby"])
    others = "".join(f'<li><a href="/{o["slug"]}">{esc(o["name"])}</a></li>' for o in C.CITIES if o["slug"] != c["slug"])
    dist = "" if not c["dist"] else f'<p class="dist">{fr(f"À environ {c["dist"]} km de notre dépôt de Saumur")}</p>'
    body = f"""
{breadcrumb(crumbs)}
<section class="page-head">
  <div class="wrap page-head-in">
    <div>
      <h1>Couvreur à {esc(c['name'])}</h1>
      <p class="sub-h1">{esc(c['cp'])}, {esc(c['dept'])}</p>
      <p class="lead">{fr(esc(c['intro']))}</p>
      {dist}
      <div class="hero-actions">
        {tel_link('btn btn-primary', 'Appeler le ' + B['phone'])}
        <a class="btn btn-ghost" href="/devis">Demander un devis</a>
      </div>
    </div>
    <figure class="page-photo">{img(c['photo'], c['photo_alt'], "(min-width: 1040px) 45vw, 100vw", eager=True)}</figure>
  </div>
</section>
<div class="wrap content-grid">
  <article class="prose">
    {local}
    <section><h2>Nos prestations à {esc(c['name'])}</h2><ul class="svc-grid svc-grid-2">{works}</ul>
    <p>{fr("Nous intervenons aussi pour toutes nos autres prestations :")} <a href="/couverture-tuile">couverture en tuiles</a>, <a href="/ravalement-facade">ravalement</a>, <a href="/entretien-demoussage-toiture">démoussage</a> et <a href="/cheminees">souches de cheminée</a>.</p></section>
    <section><h2>Communes voisines</h2><p>{fr("Nous intervenons également autour de " + esc(c['name']) + " :")} {nearby}.</p></section>
  </article>
  {contact_aside()}
</div>
<section class="related" aria-labelledby="oc-t">
  <div class="wrap">
    <h2 id="oc-t">Autres communes</h2>
    <ul class="pill-list">{others}<li><a href="/zone-intervention">Toute la zone</a></li></ul>
  </div>
</section>
{cta_band(f"Un projet de toiture à {c['name']} ?")}
"""
    page_ld = {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": f"Couvreur à {c['name']}",
        "serviceType": "Couverture et zinguerie",
        "url": URL + "/" + c["slug"],
        "provider": {"@id": ORG_ID},
        "areaServed": {"@type": "City", "name": c["name"], "address": {"@type": "PostalAddress", "postalCode": c["cp"], "addressCountry": "FR"}},
    }
    return layout(c["slug"], c["title"], c["desc"], body, "zone-intervention", [page_ld, breadcrumb_schema(crumbs), org_schema()])


def page_zone():
    crumbs = [("Accueil", "/"), ("Zone d'intervention", "/zone-intervention")]
    cards = "".join(
        f'<li><a href="/{c["slug"]}"><span class="z-name">{esc(c["name"])}</span><span class="z-meta">{esc(c["cp"])}, {esc(c["dept"])}</span>'
        f'<span class="z-dist">{"Notre commune" if not c["dist"] else fr(f"Environ {c["dist"]} km")}</span></a></li>'
        for c in C.CITIES
    )
    groups = "".join(
        f'<div><h3>{esc(g)}</h3><p>{", ".join(esc(x) for x in lst)}.</p></div>' for g, lst in C.ZONE_EXTRA.items()
    )
    title = "Zone d'intervention : Saumur et 40 km autour | Tinten Couverture"
    desc = "Couvreur à Saumur et dans un rayon de 40 km : Doué-en-Anjou, Montreuil-Bellay, Longué-Jumelles, Gennes-Val-de-Loire, Fontevraud, Chinon, Loudun, Thouars."
    body = f"""
{breadcrumb(crumbs)}
<section class="page-head page-head-text">
  <div class="wrap">
    <h1>Zone d'intervention</h1>
    <p class="lead">{fr("Nous intervenons à Saumur et dans un rayon d'environ 40 km, sur quatre départements : Maine-et-Loire, Indre-et-Loire, Vienne et Deux-Sèvres.")}</p>
  </div>
</section>
<div class="wrap">
  <ul class="zone-cards">{cards}</ul>
  <section class="zone-groups"><h2>Autres communes desservies</h2><div class="groups">{groups}</div>
  <p>{fr("Votre commune n'apparaît pas ? Appelez-nous au")} {tel_link('', B['phone'])} {fr(": si elle est dans notre secteur, nous venons.")}</p></section>
</div>
{cta_band()}
"""
    return layout("zone-intervention", title, desc, body, "zone-intervention", [breadcrumb_schema(crumbs), org_schema()])


def page_realisations():
    crumbs = [("Accueil", "/"), ("Réalisations", "/realisations")]
    figs = "".join(
        f'<figure class="g-item">{img(slug, cap, "(min-width: 1040px) 33vw, (min-width: 720px) 50vw, 100vw")}<figcaption>{fr(esc(cap))}</figcaption></figure>'
        for slug, cap in C.GALLERY
    )
    title = "Réalisations : nos chantiers de toiture à Saumur | Tinten Couverture"
    desc = "Photos de nos chantiers dans le Saumurois : couvertures en ardoise et en tuiles, noues et gouttières en zinc, lucarnes, souches de cheminée et façades."
    body = f"""
{breadcrumb(crumbs)}
<section class="page-head page-head-text">
  <div class="wrap">
    <h1>Nos réalisations</h1>
    <p class="lead">{fr("Des photos prises sur nos chantiers : couvertures en ardoise et en tuiles, zinguerie, lucarnes et cheminées.")}</p>
  </div>
</section>
<div class="wrap"><div class="gallery gallery-full">{figs}</div></div>
{cta_band()}
"""
    return layout("realisations", title, desc, body, "realisations", [breadcrumb_schema(crumbs), org_schema()])


def page_about():
    crumbs = [("Accueil", "/"), ("À propos", "/a-propos")]
    title = "À propos : Tinten Couverture, couvreur à Saumur depuis 2009"
    desc = "Tinten Couverture, entreprise artisanale de couverture, zinguerie et ravalement installée à Saumur depuis 2009. Notre façon de travailler et nos engagements."
    body = f"""
{breadcrumb(crumbs)}
<section class="page-head">
  <div class="wrap page-head-in">
    <div>
      <h1>Couvreur à Saumur depuis {B['since']}</h1>
      <p class="lead">{fr("Tinten Couverture est une entreprise artisanale de couverture, de zinguerie et de ravalement, installée boulevard des Demoiselles, à Saumur.")}</p>
    </div>
    <figure class="page-photo page-photo-square">{img('couvreur-tinten-toiture', "Le couvreur de Tinten Couverture sur un chantier de toiture en ardoise", "(min-width: 1040px) 40vw, 100vw", eager=True)}</figure>
  </div>
</section>
<div class="wrap content-grid">
  <article class="prose">
    <section><h2>Nos métiers</h2>
      <p>{fr("Notre activité couvre tout ce qui protège une maison de la pluie : la couverture en ardoise et en tuiles, la zinguerie (gouttières, noues, abergements, bavettes), les souches de cheminée, les fenêtres de toit et le ravalement des façades.")}</p>
      <p>{fr("Dans le Saumurois, cela veut dire d'abord l'ardoise et le tuffeau : des matériaux qui demandent des gestes précis et des produits compatibles, que nous pratiquons au quotidien.")}</p>
    </section>
    <section><h2>Notre façon de travailler</h2>
      <ul>
        <li>{fr("<strong>Une visite avant tout devis</strong> : nous montons sur le toit et dans les combles pour comprendre le problème.")}</li>
        <li>{fr("<strong>Un devis détaillé</strong>, gratuit, avec les matériaux, les quantités et les démarches éventuelles.")}</li>
        <li>{fr("<strong>La réparation quand elle suffit</strong> : nous ne proposons une réfection complète que lorsqu'elle se justifie.")}</li>
        <li>{fr("<strong>Un chantier tenu</strong> : maison hors d'eau chaque soir, abords protégés, nettoyage en fin de travaux.")}</li>
        <li>{fr("<strong>Des photos avant et après</strong>, pour que vous voyiez ce qui a été fait, même là où vous ne montez pas.")}</li>
      </ul>
    </section>
    <section><h2>Garantie</h2>
      <p>{fr("Les travaux de couverture relèvent de la garantie décennale. Les références de notre assurance figurent sur chaque devis et chaque facture.")}</p>
    </section>
    <section><h2>Nous trouver</h2>
      <p>{esc(B['street'])}, {B['postcode']} {esc(B['city'])}<br>{fr(esc(B['hours_text']))}<br>Téléphone : {tel_link('', B['phone'])}</p>
      <p><a href="{B['maps']}" rel="noopener">Voir sur Google Maps</a><br><a href="{B['google_reviews']}" rel="noopener">Lire les avis Google</a></p>
    </section>
  </article>
  {contact_aside()}
</div>
{cta_band()}
"""
    return layout("a-propos", title, desc, body, "a-propos", [breadcrumb_schema(crumbs), org_schema()])


def page_devis():
    crumbs = [("Accueil", "/"), ("Demander un devis", "/devis")]
    options = "".join(f'<option value="{esc(s["nav"])}">{esc(s["nav"])}</option>' for s in C.SERVICES)
    title = "Demander un devis de toiture gratuit à Saumur | Tinten Couverture"
    desc = "Demandez un devis gratuit pour vos travaux de toiture, zinguerie ou ravalement à Saumur et dans un rayon de 40 km. Réponse par téléphone, visite sur place."
    body = f"""
{breadcrumb(crumbs)}
<section class="page-head page-head-text">
  <div class="wrap">
    <h1>Demander un devis gratuit</h1>
    <p class="lead">{fr("Décrivez votre projet ou votre problème de toiture. Nous vous rappelons pour fixer une visite, puis nous vous remettons un devis détaillé, gratuit et sans engagement.")}</p>
  </div>
</section>
<div class="wrap devis-grid">
  <form class="form" id="devis-form" action="/api/devis" method="post" novalidate>
    <div class="field-row">
      <div class="field"><label for="f-nom">Nom</label><input id="f-nom" name="nom" autocomplete="name" required maxlength="80"></div>
      <div class="field"><label for="f-tel">Téléphone</label><input id="f-tel" name="telephone" type="tel" autocomplete="tel" required maxlength="20" inputmode="tel"></div>
    </div>
    <div class="field-row">
      <div class="field"><label for="f-email">Email <span class="opt">(facultatif)</span></label><input id="f-email" name="email" type="email" autocomplete="email" maxlength="120"></div>
      <div class="field"><label for="f-commune">Commune des travaux</label><input id="f-commune" name="commune" autocomplete="address-level2" required maxlength="80"></div>
    </div>
    <div class="field"><label for="f-type">Type de travaux</label>
      <select id="f-type" name="type" required><option value="">Choisissez</option>{options}<option value="Autre">Autre</option></select></div>
    <div class="field"><label for="f-msg">Votre projet</label>
      <textarea id="f-msg" name="message" rows="6" required maxlength="3000" placeholder="Par exemple : ardoises glissées côté rue, fuite près de la cheminée après la tempête…"></textarea></div>
    <div class="field"><label for="f-rappel">Quand vous rappeler ?</label>
      <select id="f-rappel" name="rappel"><option>Indifférent</option><option>Le matin</option><option>L'après-midi</option></select></div>
    <div class="hp" aria-hidden="true"><label for="f-site">Ne pas remplir</label><input id="f-site" name="site_web" tabindex="-1" autocomplete="off"></div>
    <div class="field field-check"><input id="f-ok" name="consentement" type="checkbox" required><label for="f-ok">{fr("J'accepte que ces informations servent uniquement à répondre à ma demande (voir la")} <a href="/confidentialite">politique de confidentialité</a>).</label></div>
    <button class="btn btn-primary btn-lg" type="submit">Envoyer ma demande</button>
    <div class="form-status" id="form-status" role="status" aria-live="polite"></div>
  </form>
  <aside class="aside-card" aria-label="Coordonnées">
    <h2>Par téléphone</h2>
    {tel_link('btn btn-primary btn-block', 'Appeler le ' + B['phone'])}
    <a class="btn btn-ghost btn-block" href="https://wa.me/{B['whatsapp']}" rel="noopener">Écrire sur WhatsApp</a>
    <p class="aside-meta">{fr(esc(B['hours_text']))}</p>
    <h2>Adresse</h2>
    <p class="aside-meta">{esc(B['street'])}<br>{B['postcode']} {esc(B['city'])}<br><a href="{B['maps']}" rel="noopener">Itinéraire</a></p>
    <h2>Email</h2>
    <p class="aside-meta"><a href="mailto:{B['email']}">{B['email']}</a></p>
  </aside>
</div>
"""
    return layout("devis", title, desc, body, "devis", [breadcrumb_schema(crumbs), org_schema()])


def page_mentions():
    crumbs = [("Accueil", "/"), ("Mentions légales", "/mentions-legales")]
    body = f"""
{breadcrumb(crumbs)}
<div class="wrap narrow prose legal">
  <h1>Mentions légales</h1>
  <h2>Éditeur du site</h2>
  <p>Tinten Couverture<br>{esc(B['street'])}, {B['postcode']} {esc(B['city'])}<br>Téléphone : {B['phone']}<br>Email : {B['email']}<br>SIRET : {B['siret']}<br>Responsable de la publication : à compléter</p>
  <h2>Assurance professionnelle</h2>
  <p>Assurance responsabilité civile décennale : à compléter (assureur et zone géographique de couverture).</p>
  <h2>Médiation de la consommation</h2>
  <p>Conformément au Code de la consommation, le client consommateur peut recourir gratuitement à un médiateur de la consommation : à compléter (nom et coordonnées du médiateur).</p>
  <h2>Hébergement</h2>
  <p>Cloudflare, Inc., 101 Townsend St, San Francisco, CA 94107, États-Unis.</p>
  <h2>Conception du site</h2>
  <p>ALLOSITEWEB, Montreuil (SIREN 519 416 242).</p>
  <h2>Propriété intellectuelle</h2>
  <p>{fr("Les textes, photographies et le logo de ce site appartiennent à Tinten Couverture. Toute reproduction sans autorisation est interdite.")}</p>
</div>
"""
    return layout("mentions-legales", "Mentions légales | Tinten Couverture", "Mentions légales du site de Tinten Couverture, couvreur à Saumur.", body, "", [breadcrumb_schema(crumbs)])


def page_privacy():
    crumbs = [("Accueil", "/"), ("Confidentialité", "/confidentialite")]
    body = f"""
{breadcrumb(crumbs)}
<div class="wrap narrow prose legal">
  <h1>Politique de confidentialité</h1>
  <h2>Données collectées</h2>
  <p>{fr("Le formulaire de devis recueille votre nom, votre téléphone, votre commune, la description de votre projet et, si vous le souhaitez, votre adresse email.")}</p>
  <h2>Utilisation</h2>
  <p>{fr("Ces informations servent uniquement à vous recontacter et à établir un devis. Elles ne sont ni vendues ni cédées. Elles sont conservées le temps du traitement de votre demande, puis au plus trois ans en l'absence de suite.")}</p>
  <h2>Cookies et mesure d'audience</h2>
  <p>{fr("Ce site ne dépose pas de cookie publicitaire ni de traceur de mesure d'audience. Aucun bandeau de consentement n'est donc nécessaire.")}</p>
  <h2>Vos droits</h2>
  <p>{fr("Vous pouvez demander l'accès, la rectification ou la suppression de vos données en écrivant à")} <a href="mailto:{B['email']}">{B['email']}</a>. {fr("Vous pouvez aussi adresser une réclamation à la CNIL (cnil.fr).")}</p>
  <h2>Responsable du traitement</h2>
  <p>Tinten Couverture, {esc(B['street'])}, {B['postcode']} {esc(B['city'])}.</p>
</div>
"""
    return layout("confidentialite", "Politique de confidentialité | Tinten Couverture", "Comment Tinten Couverture utilise les informations transmises par le formulaire de devis.", body, "", [breadcrumb_schema(crumbs)])


def page_404():
    links = "".join(f'<li><a href="/{s["slug"]}">{esc(s["nav"])}</a></li>' for s in C.SERVICES[:6])
    body = f"""
<section class="page-head page-head-text">
  <div class="wrap narrow">
    <h1>Cette page n'existe pas</h1>
    <p class="lead">{fr("L'adresse a peut-être changé avec la nouvelle version du site. Voici les pages les plus consultées :")}</p>
    <ul class="pill-list">{links}<li><a href="/devis">Demander un devis</a></li></ul>
    <p><a class="btn btn-primary" href="/">Retour à l'accueil</a></p>
  </div>
</section>
"""
    return layout("404", "Page introuvable | Tinten Couverture", "Cette page n'existe pas ou a changé d'adresse.", body, "", [], noindex=True)


# ---------------------------------------------------------------------------
# Fichiers techniques
# ---------------------------------------------------------------------------

REDIRECTS = [
    # Anciennes pages du site en ligne repérées dans Google
    ("/renovation-de-toiture-couvreur-a-saumur-49400", "/renovation-toiture"),
    ("/contact-devis-gratuit-charpentier-couvreur-a-saumur-49400", "/devis"),
    ("/renovation-de-toiture-et-hydrofuge-nantes-saumur-reze", "/entretien-demoussage-toiture"),
    # Anciennes pages de la version précédente (repo)
    ("/travaux-couverture", "/renovation-toiture"),
    ("/travaux-zinguerie", "/zinguerie-gouttieres"),
    ("/pose-velux", "/fenetres-de-toit"),
    ("/isolation-combles", "/renovation-toiture"),
    ("/urgences", "/reparation-fuite-toiture"),
    ("/qui-sommes-nous", "/a-propos"),
    ("/engagements", "/a-propos"),
    ("/contact", "/devis"),
    ("/couvreur-angers", "/zone-intervention"),
    ("/doue-en-anjou", "/couvreur-doue-en-anjou"),
    ("/montreuil-bellay", "/couvreur-montreuil-bellay"),
]


def write(path, text):
    full = os.path.join(PUBLIC, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(text)


def build():
    # CSS et JS
    shutil.copy(os.path.join(SITE, "site.css"), os.path.join(PUBLIC, "assets/css/site.css"))
    shutil.copy(os.path.join(SITE, "site.js"), os.path.join(PUBLIC, "assets/js/site.js"))
    from PIL import Image
    Image.open(os.path.join(PUBLIC, "assets/img/icon-512.png")).save(os.path.join(PUBLIC, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])

    pages = {"index.html": page_home()}
    for s in C.SERVICES:
        pages[s["slug"] + ".html"] = page_service(s)
    for c in C.CITIES:
        pages[c["slug"] + ".html"] = page_city(c)
    pages["zone-intervention.html"] = page_zone()
    pages["realisations.html"] = page_realisations()
    pages["a-propos.html"] = page_about()
    pages["devis.html"] = page_devis()
    pages["mentions-legales.html"] = page_mentions()
    pages["confidentialite.html"] = page_privacy()
    pages["404.html"] = page_404()
    for name, text in pages.items():
        write(name, text)

    # Plan du site
    urls = ["/"] + ["/" + n[:-5] for n in pages if n not in ("index.html", "404.html")]
    prio = {"/": "1.0", "/devis": "0.9", "/couvreur-saumur": "0.9"}
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        sm.append(f"  <url><loc>{URL}{u if u != '/' else '/'}</loc><lastmod>{TODAY}</lastmod><priority>{prio.get(u, '0.8' if u.strip('/') in C.SERVICE_BY_SLUG else '0.7')}</priority></url>")
    sm.append("</urlset>")
    write("sitemap.xml", "\n".join(sm) + "\n")
    write("robots.txt", f"User-agent: *\nAllow: /\nDisallow: /api/\n\nSitemap: {URL}/sitemap.xml\n")

    # llms.txt : résumé lisible par les assistants IA
    llms = [f"# Tinten Couverture", "", f"> Couvreur, zingueur et ravalement à Saumur (49400) depuis {B['since']}. Intervient dans un rayon d'environ {B['radius_km']} km.", "",
            f"Adresse : {B['street']}, {B['postcode']} {B['city']}. Téléphone : {B['phone']}. {B['hours_text']}.", "", "## Prestations"]
    llms += [f"- [{s['nav']}]({URL}/{s['slug']}) : {s['short']}" for s in C.SERVICES]
    llms += ["", "## Communes"] + [f"- [Couvreur à {c['name']}]({URL}/{c['slug']}) ({c['cp']})" for c in C.CITIES]
    llms += ["", "## Contact", f"- [Demander un devis]({URL}/devis)", f"- [À propos]({URL}/a-propos)", ""]
    write("llms.txt", "\n".join(llms))

    # Redirections (Cloudflare _redirects)
    red = ["# Anciennes adresses -> nouvelles pages (301 permanentes)"]
    for src, dst in REDIRECTS:
        red.append(f"{src} {dst} 301")
        red.append(f"{src}/ {dst} 301")
        red.append(f"{src}.html {dst} 301")
    write("_redirects", "\n".join(red) + "\n")

    # En-têtes (Cloudflare _headers)
    headers = f"""/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  X-Frame-Options: DENY
  Permissions-Policy: camera=(), microphone=(), geolocation=(), interest-cohort=()
  Content-Security-Policy: default-src 'self'; img-src 'self' data:; style-src 'self'; script-src 'self' '{EARLY_JS_HASH}'; font-src 'self'; connect-src 'self'; form-action 'self' https://wa.me; frame-ancestors 'none'; base-uri 'self'

/assets/fonts/*
  Cache-Control: public, max-age=31536000, immutable

/assets/css/*
  Cache-Control: public, max-age=31536000, immutable

/assets/js/*
  Cache-Control: public, max-age=31536000, immutable

/assets/img/*
  Cache-Control: public, max-age=2592000

https://:worker.:account.workers.dev/*
  X-Robots-Tag: noindex
"""
    write("_headers", headers)

    manifest = {"name": "Tinten Couverture", "short_name": "Tinten", "start_url": "/", "display": "browser",
                "background_color": "#ffffff", "theme_color": "#26313a",
                "icons": [{"src": "/assets/img/icon-512.png", "sizes": "512x512", "type": "image/png"}]}
    write("site.webmanifest", json.dumps(manifest, ensure_ascii=False, indent=1))
    print(f"{len(pages)} pages générées, {len(urls)} URL dans le sitemap")


if __name__ == "__main__":
    build()
