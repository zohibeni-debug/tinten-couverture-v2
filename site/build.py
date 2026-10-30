# -*- coding: utf-8 -*-
"""Générateur du site Tinten Couverture.

Usage : python3 site/build.py
Produit le dossier public/ (pages HTML complètes, sitemap, robots, redirections).
"""
import base64
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
YEARS = date.today().year - B["since"]

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


def big_src(slug):
    return f"/assets/img/{slug}-{PHOTOS[slug]['sizes'][-1]}.webp"


ICONS = {
    "tel": '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 3.5h2.8l1.4 4.2-2 1.5a12 12 0 0 0 6 6l1.5-2 4.2 1.4v2.8a2 2 0 0 1-2.2 2A17 17 0 0 1 4.6 5.7a2 2 0 0 1 2-2.2z" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linejoin="round"/></svg>',
    "fleche": '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h13M13 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "check": '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12.5l4.2 4.2L19 7" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "pin": '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21s-6.5-6.2-6.5-11a6.5 6.5 0 0 1 13 0c0 4.8-6.5 11-6.5 11z" fill="none" stroke="currentColor" stroke-width="1.9"/><circle cx="12" cy="10" r="2.4" fill="none" stroke="currentColor" stroke-width="1.9"/></svg>',
    "horloge": '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="8.5" fill="none" stroke="currentColor" stroke-width="1.9"/><path d="M12 7.5V12l3 2" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round"/></svg>',
    "wa": '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M4.5 19.5l1.2-3.6A8 8 0 1 1 8.4 18.6z" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linejoin="round"/><path d="M9.2 8.6c.3 2.6 2.7 5.1 5.4 5.6l1-1.2-1.8-.9-.7.8c-.9-.4-1.9-1.4-2.3-2.3l.8-.7-.9-1.8z" fill="currentColor"/></svg>',
    "prec": '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M15 5l-7 7 7 7" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "suiv": '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M9 5l7 7-7 7" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
}


def tel_btn(cls="btn btn-primary", label=None):
    label = label or f"Appeler le {B['phone']}"
    return f'<a class="{cls}" href="tel:{B["phone_e164"]}">{ICONS["tel"]}<span>{esc(label)}</span></a>'


def devis_btn(cls="btn btn-glass", label="Demander un devis"):
    return f'<a class="{cls}" href="/devis"><span>{esc(label)}</span>{ICONS["fleche"]}</a>'


def tel_link(cls="", label=None):
    label = label or B["phone"]
    c = f' class="{cls}"' if cls else ""
    return f'<a{c} href="tel:{B["phone_e164"]}">{esc(label)}</a>'


def jsonld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + "</script>"


ORG_ID = URL + "/#entreprise"
EARLY_JS = "document.documentElement.classList.add('js')"
EARLY_JS_HASH = "sha256-" + base64.b64encode(hashlib.sha256(EARLY_JS.encode()).digest()).decode()


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
<header class="site-header" data-header>
  <div class="wrap header-in">
    <a class="brand" href="/" aria-label="Tinten Couverture, accueil">
      <img src="/assets/img/logo-entete-blanc-64.png" srcset="/assets/img/logo-entete-blanc-64.png 249w, /assets/img/logo-entete-blanc-128.png 498w, /assets/img/logo-entete-blanc-192.png 747w" sizes="(min-width: 1100px) 218px, 180px" width="249" height="64" alt="Tinten Couverture, couvreur, zingueur et ravalement">
    </a>
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
        {tel_btn('btn btn-glass nav-tel', B['phone'])}
        {devis_btn('btn btn-primary', 'Devis gratuit')}
      </div>
    </nav>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="nav" aria-label="Ouvrir le menu"><span class="burger" aria-hidden="true"></span></button>
  </div>
</header>"""


def footer():
    services = "".join(f'<li><a href="/{s["slug"]}">{esc(s["nav"])}</a></li>' for s in C.SERVICES)
    cities = "".join(f'<li><a href="/{c["slug"]}">Couvreur à {esc(c["name"])}</a></li>' for c in C.CITIES)
    return f"""
<footer class="site-footer">
  <div class="wrap footer-top">
    <div class="footer-id">
      <img src="/assets/img/logo-entete-blanc-128.png" width="249" height="64" alt="Tinten Couverture" loading="lazy">
      <p>{fr(f"Couverture, zinguerie et ravalement à Saumur depuis {B['since']}, dans un rayon de 40 km.")}</p>
      <ul class="footer-contact">
        <li>{ICONS['pin']}<span>{esc(B['street'])}, {B['postcode']} {esc(B['city'])}</span></li>
        <li>{ICONS['tel']}<a href="tel:{B['phone_e164']}">{B['phone']}</a></li>
        <li>{ICONS['horloge']}<span>{fr(esc(B['hours_text']))}</span></li>
      </ul>
    </div>
    <nav aria-label="Prestations"><h2>Prestations</h2><ul>{services}</ul></nav>
    <nav aria-label="Communes"><h2>Communes</h2><ul>{cities}<li><a href="/zone-intervention">Toute la zone</a></li></ul></nav>
    <nav aria-label="Entreprise"><h2>Entreprise</h2><ul>
      <li><a href="/a-propos">À propos</a></li>
      <li><a href="/realisations">Réalisations</a></li>
      <li><a href="/devis">Demander un devis</a></li>
      <li><a href="mailto:{B['email']}">{B['email']}</a></li>
      <li><a href="{B['facebook']}" rel="noopener">Facebook</a></li>
      <li><a href="/mentions-legales">Mentions légales</a></li>
      <li><a href="/confidentialite">Confidentialité</a></li>
    </ul></nav>
  </div>
  <div class="wrap footer-base">
    <p>© {date.today().year} Tinten Couverture</p>
    <p>Site réalisé par <a href="https://allositeweb.com" rel="noopener">ALLOSITEWEB</a></p>
  </div>
</footer>
<div class="callbar" role="region" aria-label="Contact rapide">
  {tel_btn('btn btn-primary', 'Appeler')}
  {devis_btn('btn btn-dark', 'Devis gratuit')}
</div>
<dialog class="lightbox" data-lightbox>
  <form method="dialog"><button class="lb-close" aria-label="Fermer">×</button></form>
  <figure><img alt="" data-lb-img><figcaption data-lb-cap></figcaption></figure>
</dialog>"""


def layout(path, title, desc, body, current="", schemas=(), og_image="/assets/img/og-tinten-couverture.jpg", noindex=False, page_class=""):
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
<meta name="theme-color" content="#151c22">
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
<body class="{page_class}">
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
    return f'<nav class="crumbs" aria-label="Fil d\'Ariane"><ol>{"".join(lis)}</ol></nav>'


def page_hero(crumbs, h1, lead, photo, alt, extra="", sub="", compact=False):
    media = ""
    if photo:
        media = f'<div class="page-hero-media">{img(photo, alt, "100vw", "kb", eager=True)}</div>'
    cls = "page-hero" + (" page-hero-compact" if compact or not photo else "")
    sub_html = f'<p class="hero-sub">{sub}</p>' if sub else ""
    return f"""
<section class="{cls}">
  {media}
  <div class="hero-shade" aria-hidden="true"></div>
  <div class="wrap page-hero-in">
    {breadcrumb(crumbs)}
    <h1 class="split">{h1}</h1>
    {sub_html}
    <p class="hero-lead rise r2">{lead}</p>
    {extra}
  </div>
</section>"""


def split_title(text):
    """Découpe un titre en lignes animées (chaque mot entre dans un masque)."""
    words = text.split(" ")
    return " ".join(f'<span class="w"><span>{esc(w)}</span></span>' for w in words)


def cta_band(title="Un projet de toiture ? Parlons-en.", text="Décrivez-nous la situation : nous venons voir et vous remettons un devis détaillé, gratuit et sans engagement."):
    return f"""
<section class="cta-band">
  <div class="cta-media">{img('chantier-toiture-echafaudage', '', '100vw')}</div>
  <div class="cta-shade" aria-hidden="true"></div>
  <div class="wrap cta-in" data-reveal>
    <h2>{fr(esc(title))}</h2>
    <p>{fr(esc(text))}</p>
    <div class="cta-actions">
      {tel_btn('btn btn-primary btn-lg')}
      {devis_btn('btn btn-glass btn-lg')}
    </div>
  </div>
</section>"""


def faq_block(faq, title="Questions fréquentes"):
    items = "".join(
        f'<details class="faq-item" data-reveal><summary>{fr(esc(q))}<span class="faq-ico" aria-hidden="true"></span></summary><div class="faq-a"><p>{fr(esc(a))}</p></div></details>'
        for q, a in faq
    )
    return f'<section class="faq" aria-labelledby="faq-titre"><h2 id="faq-titre" data-reveal>{fr(esc(title))}</h2>{items}</section>'


def contact_aside():
    return f"""
<aside class="aside-card" aria-label="Contact">
  <p class="aside-title">Devis gratuit</p>
  <p>Nous venons voir la toiture et vous remettons un devis détaillé.</p>
  {tel_btn('btn btn-primary btn-block')}
  {devis_btn('btn btn-outline btn-block', 'Demander par écrit')}
  <ul class="aside-meta">
    <li>{ICONS['horloge']}<span>{fr(esc(B['hours_text']))}</span></li>
    <li>{ICONS['pin']}<span>{esc(B['street'])}, {esc(B['city'])}</span></li>
  </ul>
</aside>"""


def service_cards(slugs, cls="svc-cards"):
    cards = []
    for i, slug in enumerate(slugs):
        s = C.SERVICE_BY_SLUG[slug]
        cards.append(
            f'<li data-reveal class="d{i % 3 + 1}"><a class="svc-card" href="/{slug}">'
            f'{img(s["photo"], "", "(min-width: 1100px) 30vw, (min-width: 700px) 45vw, 100vw")}'
            f'<span class="svc-body"><span class="svc-name">{esc(s["nav"])}</span>'
            f'<span class="svc-desc">{fr(esc(s["short"]))}</span>'
            f'<span class="svc-more">Découvrir{ICONS["fleche"]}</span></span></a></li>'
        )
    return f'<ul class="{cls}">{"".join(cards)}</ul>'


# ---------------------------------------------------------------------------
# Schéma « anatomie d'une toiture » (animé au défilement)
# ---------------------------------------------------------------------------

def anatomy_svg():
    """Coupe en escalier d'une toiture en ardoise : chaque couche s'arrête un peu avant
    celle du dessous. Chaque couche est un groupe animé séparément."""
    ang = math.radians(17)
    u = (math.cos(ang), -math.sin(ang))
    n = (-math.sin(ang), -math.cos(ang))
    pts_all = []

    def P(s, t):
        p = (s * u[0] + t * n[0], s * u[1] + t * n[1])
        pts_all.append(p)
        return p

    def poly(pts, fill, stroke, sw=1.4):
        d = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        return f'<polygon points="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"/>'

    def line(a, b, stroke, sw, cap=""):
        c = ' stroke-linecap="round"' if cap else ""
        return f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="{stroke}" stroke-width="{sw}"{c}/>'

    RAF, MEM, CL, LT, TH = (-84, 0), (0, 7), (7, 29), (29, 53), 9
    END = {"raf": 900, "mem": 815, "cl": 730, "lt": 640, "sl": 545}
    START = -40
    groups = {}

    # Mur en tuffeau
    tl, tr = P(-6, RAF[0]), P(96, RAF[0])
    w_bot = tl[1] + 96
    pts_all += [(tl[0], w_bot), (tr[0], w_bot)]
    wall = [poly([tl, tr, (tr[0], w_bot), (tl[0], w_bot)], "#ece5d3", "#c9bfa6")]
    for k in range(1, 4):
        yy = tl[1] + k * 26
        if yy >= w_bot - 4:
            break
        wall.append(line((tl[0], yy), (tr[0], yy), "#d8ceb5", 1.2))
        off = 0 if k % 2 else 30
        for xx in range(int(tl[0] + 22 + off), int(tr[0]) - 4, 60):
            wall.append(line((xx, max(yy - 26, tl[1])), (xx, yy), "#d8ceb5", 1.2))
    groups["wall"] = "".join(wall)

    raf = [poly([P(START, RAF[0]), P(END["raf"], RAF[0]), P(END["raf"], RAF[1]), P(START, RAF[1])], "#bb8f60", "#7e5e3b")]
    for tt in (-60, -36, -16):
        raf.append(line(P(START + 40, tt), P(END["raf"] - 30, tt + 6), "#a87d50", 1.2))
    groups["raf"] = "".join(raf)
    groups["mem"] = poly([P(START + 6, MEM[0]), P(END["mem"], MEM[0]), P(END["mem"], MEM[1]), P(START + 6, MEM[1])], "#5b7a90", "#3d586b", 1.1)
    groups["cl"] = poly([P(START + 6, CL[0]), P(END["cl"], CL[0]), P(END["cl"], CL[1]), P(START + 6, CL[1])], "#dcbd91", "#9c7a50")

    pitch = 100
    battens = []
    batten_ends = []
    k = 0
    while 6 + k * pitch + 30 <= END["lt"]:
        s0 = 6 + k * pitch
        battens.append(f'<g class="bat">{poly([P(s0, LT[0]), P(s0 + 30, LT[0]), P(s0 + 30, LT[1]), P(s0, LT[1])], "#c99d6d", "#86663f")}</g>')
        batten_ends.append(s0)
        k += 1
    groups["lt"] = "".join(battens)

    base, s_start, s_end = LT[1], -34, END["sl"]
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
    slates = [poly([P(s_start, base)] + top + [P(s_end, base)], "#475766", "#26313a", 1.4)]
    for idx, s0 in enumerate(tails):
        lift = TH * min(idx, 2)
        s1 = min(s0 + 2.3 * pitch, s_end)
        frac = (s1 - s0) / (2.3 * pitch)
        if idx > 0:
            slates.append(line(P(s0, base + lift), P(s1, base + lift * (1 - frac)), "#2f3c47", 1.2))
        slates.append(line(P(s0 + 4, base + lift + TH - 0.8), P(min(s0 + pitch, s_end) - 4, base + lift + TH - 3.6), "#8496a3", 2, "r"))
        slates.append(line(P(s0 + 3, base + lift + TH + 2.5), P(s0 + 3, base + lift - 3), "#d3dade", 2.4, "r"))
    groups["sl"] = "".join(slates)

    eave = P(-34, LT[1])
    gx, gy, r = eave[0] - 6, eave[1] + 30, 28
    pts_all += [(gx - r - 6, gy - 4), (gx + r + 6, gy + r + 6)]
    hk = P(START + 14, MEM[1])
    groups["gut"] = (
        f'<path d="M{gx - r:.1f},{gy:.1f} a{r},{r} 0 0 0 {2 * r},0 Z" fill="#c8d0d5" stroke="#6f7c84" stroke-width="2"/>'
        f'<path d="M{gx - r - 5:.1f},{gy:.1f} h{2 * r + 10}" stroke="#6f7c84" stroke-width="2.4" stroke-linecap="round"/>'
        f'<path d="M{hk[0]:.1f},{hk[1]:.1f} L{gx + r:.1f},{gy:.1f}" stroke="#6f7c84" stroke-width="2" fill="none"/>'
    )

    marks = []

    def marker(num, target, pos):
        (tx, ty), (px, py) = target, pos
        pts_all.extend([(px - 26, py - 26), (px + 26, py + 26)])
        marks.append(
            f'<g class="mk mk{num}" data-step="{num}">'
            f'{line((tx, ty), (px, py), "#e9eef1", 1.6)}'
            f'<circle cx="{tx:.1f}" cy="{ty:.1f}" r="4.5" fill="#e9eef1"/>'
            f'<g class="mk-dot"><circle cx="{px:.1f}" cy="{py:.1f}" r="22" fill="#97b854"/>'
            f'<text x="{px:.1f}" y="{py + 8:.1f}" text-anchor="middle" font-size="23" font-weight="760" fill="#151c22">{num}</text></g></g>'
        )

    def above(s, t, dist):
        tgt = P(s, t)
        return tgt, (tgt[0] + n[0] * dist, tgt[1] + n[1] * dist)

    marker(1, *above(330, LT[1] + 3 * TH - 2, 96))
    lt_s = [b_ for b_ in batten_ends if b_ > END["sl"] - 10]
    s_bat = (lt_s[0] + 15) if lt_s else END["lt"] - 30
    marker(2, *above(s_bat, (LT[0] + LT[1]) / 2, 112))
    marker(3, *above(END["cl"] - 40, (CL[0] + CL[1]) / 2, 128))
    marker(4, *above(END["mem"] - 40, (MEM[0] + MEM[1]) / 2, 140))
    marker(5, *above(END["raf"] - 40, (RAF[0] + RAF[1]) / 2, 196))
    marker(6, (gx, gy + r * 0.55), (gx - 70, gy + 86))

    xs = [p_[0] for p_ in pts_all]
    ys = [p_[1] for p_ in pts_all]
    pad = 16
    x0, y0, x1, y1 = min(xs) - pad, min(ys) - pad, max(xs) + pad, max(ys) + pad
    title = "Coupe d'une toiture en ardoise : ardoises posées au crochet, liteaux, contre-liteaux, écran sous-toiture, chevron et gouttière en zinc"
    order = ["wall", "raf", "mem", "cl", "lt", "sl", "gut"]
    layers = "".join(f'<g class="ly ly-{k}">{groups[k]}</g>' for k in order)
    return (
        f'<svg class="anatomy-svg" viewBox="{x0:.0f} {y0:.0f} {x1 - x0:.0f} {y1 - y0:.0f}" role="img" aria-labelledby="anat-t">'
        f'<title id="anat-t">{esc(title)}</title>{layers}<g class="marks">{"".join(marks)}</g></svg>'
    )


# ---------------------------------------------------------------------------
# Carte « radar » de la zone d'intervention (schéma indicatif)
# ---------------------------------------------------------------------------

# Direction (degrés depuis le nord) et distance à vol d'oiseau approximative (km)
RADAR = {
    "couvreur-longue-jumelles": (350, 13),
    "couvreur-gennes-val-de-loire": (303, 14),
    "couvreur-doue-en-anjou": (245, 17),
    "couvreur-montreuil-bellay": (192, 15),
    "couvreur-thouars": (207, 33),
    "couvreur-loudun": (157, 31),
    "couvreur-fontevraud-l-abbaye": (130, 13),
    "couvreur-chinon": (110, 26),
}
LABEL_POS = {"couvreur-fontevraud-l-abbaye": ("middle", 24, 27)}


def radar_svg(highlight=None):
    k = 4.6  # unités par km
    out = []
    # Loire (tracé schématique)
    def pol(b, d):
        a = math.radians(b)
        return (d * k * math.sin(a), -d * k * math.cos(a))
    p1, p2, p3, p4 = pol(112, 44), pol(105, 14), pol(292, 12), pol(300, 44)
    out.append(f'<path class="loire" d="M{p1[0]:.0f},{p1[1]:.0f} C{p2[0]:.0f},{p2[1]:.0f} {p3[0]:.0f},{p3[1]:.0f} {p4[0]:.0f},{p4[1]:.0f}"/>')
    lx, ly = pol(286, 41)
    out.append(f'<text class="loire-t" x="{lx:.0f}" y="{ly - 8:.0f}">Loire</text>')
    for km in (10, 20, 30, 40):
        out.append(f'<circle class="ring" cx="0" cy="0" r="{km * k:.0f}"/>')
        out.append(f'<text class="ring-t" x="4" y="{-km * k + 14:.0f}">{km} km</text>')
    out.append('<g class="sweep"><circle cx="0" cy="0" r="184" fill="none"/><path d="M0,0 L0,-184 A184,184 0 0 1 106,-150 Z"/></g>')
    for i, c in enumerate(C.CITIES):
        if c["slug"] not in RADAR:
            continue
        b, d = RADAR[c["slug"]]
        x, y = pol(b, d)
        anchor = "start" if x >= 0 else "end"
        tx, ty = x + (12 if x >= 0 else -12), y + 5
        if c["slug"] in LABEL_POS:
            anchor, dx, dy = LABEL_POS[c["slug"]]
            tx, ty = x + dx, y + dy
        hl = " is-hl" if c["slug"] == highlight else ""
        out.append(
            f'<a href="/{c["slug"]}" class="city c{i}{hl}"><circle cx="{x:.0f}" cy="{y:.0f}" r="7"/>'
            f'<text x="{tx:.0f}" y="{ty:.0f}" text-anchor="{anchor}">{esc(c["name"])}</text></a>'
        )
    out.append('<g class="home"><circle class="pulse" cx="0" cy="0" r="10"/><circle cx="0" cy="0" r="9"/></g>')
    out.append('<text class="home-t" x="0" y="30" text-anchor="middle">Saumur</text>')
    return (
        '<svg class="radar-svg" viewBox="-250 -215 500 430" role="img" aria-label="Schéma de la zone d\'intervention : Saumur au centre, cercles de 10 à 40 km">'
        + "".join(out) + "</svg>"
    )


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------

def page_home():
    marquee_items = "".join(f'<span class="mq-item">{esc(s["nav"])}</span>' for s in C.SERVICES)
    legend = "".join(
        f'<li data-step="{i + 1}"><span class="num" aria-hidden="true">{i + 1}</span><div><h3>{esc(name)}</h3><p>{fr(esc(text))}</p>'
        f'<a href="/{slug}">{esc(C.SERVICE_BY_SLUG[slug]["nav"])}</a></div></li>'
        for i, (name, text, slug) in enumerate(C.ANATOMY)
    )
    steps = "".join(
        f'<li data-reveal class="d{i + 1}"><span class="step-n" aria-hidden="true">{i + 1}</span><h3>{esc(t)}</h3><p>{fr(esc(d))}</p></li>'
        for i, (t, d) in enumerate(C.PROCESS)
    )
    gallery = "".join(
        f'<li class="g-card"><a href="{big_src(slug)}" data-lb data-cap="{esc(cap)}">{img(slug, cap, "(min-width: 1100px) 34vw, 80vw")}</a><p>{fr(esc(cap))}</p></li>'
        for slug, cap in C.GALLERY
    )
    cities = "".join(
        f'<li data-reveal><a href="/{c["slug"]}"><span>{esc(c["name"])}</span><small>{"Notre commune" if not c["dist"] else f"{c["dist"]} km"}</small></a></li>'
        for c in C.CITIES
    )
    body = f"""
<section class="hero">
  <div class="hero-media">{img('toiture-ardoise-lucarne-saumur', "Toiture en ardoise avec lucarne habillée de zinc, réalisée par Tinten Couverture", "100vw", "kb", eager=True)}</div>
  <div class="hero-shade" aria-hidden="true"></div>
  <div class="wrap hero-in">
    <p class="chip rise r0"><span class="dot" aria-hidden="true"></span>Saumur et 40 km alentour</p>
    <h1 class="split hero-title">{split_title(C.HOME['h1'])}</h1>
    <p class="hero-lead rise r2">{fr(esc(C.HOME['lead']))}</p>
    <div class="hero-actions rise r3">
      {tel_btn('btn btn-primary btn-lg')}
      {devis_btn('btn btn-glass btn-lg')}
    </div>
    <ul class="hero-facts rise r4">
      <li><strong>Depuis {B['since']}</strong><span>couvreur à Saumur</span></li>
      <li><strong>Ardoise, tuile, zinc</strong><span>et ravalement</span></li>
      <li><strong>Devis gratuit</strong><span>après visite</span></li>
    </ul>
  </div>
  <a class="scroll-cue" href="#prestations" aria-label="Voir nos prestations"><span></span></a>
</section>

<div class="marquee" aria-hidden="true"><div class="mq-track">{marquee_items}{marquee_items}</div></div>

<section class="sec sec-light" id="prestations" aria-labelledby="svc-t">
  <div class="wrap">
    <div class="sec-head" data-reveal>
      <h2 id="svc-t">Nos prestations</h2>
      <p>Couverture, zinguerie, étanchéité et façades : tout ce qui protège la maison de la pluie.</p>
    </div>
    {service_cards([s['slug'] for s in C.SERVICES])}
  </div>
</section>

<section class="sec sec-dark anatomy" aria-labelledby="anat-titre">
  <div class="wrap">
    <div class="sec-head" data-reveal>
      <h2 id="anat-titre">Ce qu'il y a sous une toiture en ardoise</h2>
      <p>Une toiture étanche, c'est six couches qui travaillent ensemble. Quand l'une d'elles vieillit, c'est elle qu'il faut traiter, pas forcément tout le toit.</p>
    </div>
    <div class="anatomy-grid">
      <figure class="anatomy-figure" data-anatomy>{anatomy_svg()}</figure>
      <ol class="anatomy-legend">{legend}</ol>
    </div>
  </div>
</section>

<section class="stats" aria-label="Tinten Couverture en chiffres">
  <div class="wrap stats-in">
    <div data-reveal><strong><span data-count="{YEARS}">{YEARS}</span> ans</strong><span>de chantiers dans le Saumurois</span></div>
    <div data-reveal class="d2"><strong><span data-count="40">40</span> km</strong><span>de rayon autour de Saumur</span></div>
    <div data-reveal class="d3"><strong><span data-count="4">4</span> départements</strong><span>Maine-et-Loire, Indre-et-Loire, Vienne, Deux-Sèvres</span></div>
  </div>
</section>

<section class="sec sec-light process" aria-labelledby="proc-t">
  <div class="wrap">
    <div class="sec-head" data-reveal><h2 id="proc-t">Comment se passe votre chantier</h2></div>
    <div class="process-track" data-progress><span class="process-line" aria-hidden="true"></span><ol class="steps">{steps}</ol></div>
  </div>
</section>

<section class="sec sec-dark gallery-sec" aria-labelledby="gal-t">
  <div class="wrap">
    <div class="sec-head sec-head-row" data-reveal>
      <h2 id="gal-t">Nos chantiers en images</h2>
      <div class="g-nav">
        <button class="g-btn" type="button" data-g-prev aria-label="Photos précédentes">{ICONS['prec']}</button>
        <button class="g-btn" type="button" data-g-next aria-label="Photos suivantes">{ICONS['suiv']}</button>
      </div>
    </div>
  </div>
  <ul class="g-track" data-g-track>{gallery}</ul>
  <div class="wrap"><a class="link-light" href="/realisations">Voir toutes les réalisations{ICONS['fleche']}</a></div>
</section>

<section class="sec sec-slate zone-sec" aria-labelledby="zone-t">
  <div class="wrap zone-in">
    <figure class="radar" data-radar>{radar_svg()}<figcaption>Schéma indicatif, distances à vol d'oiseau.</figcaption></figure>
    <div>
      <h2 id="zone-t" data-reveal>Où intervenons-nous ?</h2>
      <p data-reveal>À Saumur et dans un rayon d'environ 40 km, sur le Maine-et-Loire, l'Indre-et-Loire, la Vienne et les Deux-Sèvres.</p>
      <ul class="zone-list">{cities}</ul>
      <a class="btn btn-glass" href="/zone-intervention"><span>Toute la zone d'intervention</span>{ICONS['fleche']}</a>
    </div>
  </div>
</section>

<section class="sec sec-light about-sec" aria-labelledby="about-t">
  <div class="wrap about-in">
    <figure class="about-photo" data-reveal>
      {img('couvreur-tinten-toiture', "Le couvreur de Tinten Couverture sur une toiture en ardoise à Saumur", "(min-width: 900px) 40vw, 100vw")}
      <figcaption class="badge"><strong>{B['since']}</strong><span>création de l'entreprise</span></figcaption>
    </figure>
    <div data-reveal class="d2">
      <h2 id="about-t">Une entreprise artisanale de Saumur</h2>
      <p>Tinten Couverture est installée boulevard des Demoiselles, à Saumur, depuis {B['since']}. Couverture, zinguerie et ravalement : nous réalisons nous-mêmes les travaux que nous chiffrons, et nous connaissons les toitures en ardoise et en tuffeau de la région.</p>
      <ul class="checks">
        <li>{ICONS['check']}Une visite avant chaque devis</li>
        <li>{ICONS['check']}La réparation quand elle suffit, la réfection quand elle se justifie</li>
        <li>{ICONS['check']}Des photos avant et après chaque chantier</li>
      </ul>
      <div class="about-actions">
        <a class="btn btn-dark" href="/a-propos"><span>Découvrir l'entreprise</span>{ICONS['fleche']}</a>
        <a class="btn btn-outline" href="{B['google_reviews']}" rel="noopener"><span>Lire les avis Google</span></a>
      </div>
    </div>
  </div>
</section>

<div class="sec sec-light sec-tight"><div class="wrap narrow">{faq_block(C.HOME['faq'])}</div></div>
{cta_band()}
"""
    website = {"@context": "https://schema.org", "@type": "WebSite", "@id": URL + "/#site", "name": "Tinten Couverture", "url": URL + "/", "inLanguage": "fr-FR", "publisher": {"@id": ORG_ID}}
    return layout("/", C.HOME["title"], C.HOME["desc"], body, "home", [org_schema(), website, faq_schema(C.HOME["faq"])], page_class="p-home")


def page_service(s):
    crumbs = [("Accueil", "/"), (s["nav"], "/" + s["slug"])]
    sections = "".join(f'<section data-reveal><h2>{fr(esc(t))}</h2>{fr(h)}</section>' for t, h in s["sections"])
    steps = ""
    if s.get("steps"):
        lis = "".join(f'<li data-reveal><span class="step-n" aria-hidden="true">{i + 1}</span><div><h3>{esc(t)}</h3><p>{fr(esc(d))}</p></div></li>' for i, (t, d) in enumerate(s["steps"]))
        steps = f'<section><h2 data-reveal>{fr(esc(s["steps_title"]))}</h2><ol class="timeline">{lis}</ol></section>'
    cities = "".join(f'<li><a href="/{c["slug"]}">{esc(c["name"])}</a></li>' for c in C.CITIES)
    actions = f'<div class="hero-actions rise r3">{tel_btn("btn btn-primary btn-lg")}{devis_btn("btn btn-glass btn-lg")}</div>'
    body = f"""
{page_hero(crumbs, split_title(s['h1']), fr(esc(s['lead'])), s['photo'], s['photo_alt'], actions)}
<div class="sec sec-light">
  <div class="wrap content-grid">
    <article class="prose">
      {sections}
      {steps}
      <section data-reveal><h2>Où intervenons-nous ?</h2><p>{fr("À Saumur et dans un rayon d'environ 40 km :")}</p><ul class="pill-list">{cities}</ul></section>
      {faq_block(s['faq'])}
    </article>
    {contact_aside()}
  </div>
</div>
<section class="sec sec-tint related" aria-labelledby="rel-t">
  <div class="wrap">
    <h2 id="rel-t" data-reveal>Prestations liées</h2>
    {service_cards(s['related'], 'svc-cards svc-cards-3')}
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
    return layout(s["slug"], s["title"], s["desc"], body, s["slug"], [service_ld, breadcrumb_schema(crumbs), faq_schema(s["faq"]), org_schema()], page_class="p-inner")


def page_city(c):
    crumbs = [("Accueil", "/"), ("Zone d'intervention", "/zone-intervention"), (f"Couvreur à {c['name']}", "/" + c["slug"])]
    local = "".join(f'<section data-reveal><h2>{fr(esc(t))}</h2>{fr(h)}</section>' for t, h in c["local"])
    nearby = "".join(f"<li>{esc(n)}</li>" for n in c["nearby"])
    others = "".join(f'<li><a href="/{o["slug"]}">{esc(o["name"])}</a></li>' for o in C.CITIES if o["slug"] != c["slug"])
    chip = "" if not c["dist"] else f'<p class="chip rise r1">{ICONS["pin"]}{fr(f"À environ {c["dist"]} km de notre dépôt de Saumur")}</p>'
    actions = f'{chip}<div class="hero-actions rise r3">{tel_btn("btn btn-primary btn-lg")}{devis_btn("btn btn-glass btn-lg")}</div>'
    radar = f'<figure class="radar radar-small" data-radar>{radar_svg(c["slug"])}<figcaption>Schéma indicatif, distances à vol d\'oiseau.</figcaption></figure>'
    body = f"""
{page_hero(crumbs, split_title('Couvreur à ' + c['name']), fr(esc(c['intro'])), c['photo'], c['photo_alt'], actions, sub=f"{esc(c['cp'])}, {esc(c['dept'])}")}
<div class="sec sec-light">
  <div class="wrap content-grid">
    <article class="prose">
      {local}
      <section><h2 data-reveal>Nos prestations à {esc(c['name'])}</h2>{service_cards(c['works'], 'svc-cards svc-cards-2')}
      <p data-reveal>{fr("Nous intervenons aussi pour toutes nos autres prestations :")} <a href="/couverture-tuile">couverture en tuiles</a>, <a href="/ravalement-facade">ravalement</a>, <a href="/entretien-demoussage-toiture">démoussage</a> et <a href="/cheminees">souches de cheminée</a>.</p></section>
      <section data-reveal><h2>Communes voisines</h2><p>{fr("Nous intervenons également autour de " + esc(c['name']) + " :")}</p><ul class="pill-list pill-static">{nearby}</ul></section>
    </article>
    <div class="aside-col">{radar if c['slug'] in RADAR else ''}{contact_aside()}</div>
  </div>
</div>
<section class="sec sec-tint related" aria-labelledby="oc-t">
  <div class="wrap">
    <h2 id="oc-t" data-reveal>Autres communes</h2>
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
    return layout(c["slug"], c["title"], c["desc"], body, "zone-intervention", [page_ld, breadcrumb_schema(crumbs), org_schema()], page_class="p-inner")


def page_zone():
    crumbs = [("Accueil", "/"), ("Zone d'intervention", "/zone-intervention")]
    cards = "".join(
        f'<li data-reveal class="d{i % 3 + 1}"><a class="z-card" href="/{c["slug"]}">{img(c["photo"], "", "(min-width: 1100px) 30vw, 90vw")}'
        f'<span class="z-body"><span class="z-name">{esc(c["name"])}</span><span class="z-meta">{esc(c["cp"])}, {esc(c["dept"])}</span>'
        f'<span class="z-dist">{"Notre commune" if not c["dist"] else fr(f"Environ {c["dist"]} km")}</span></span></a></li>'
        for i, c in enumerate(C.CITIES)
    )
    groups = "".join(
        f'<div data-reveal><h3>{esc(g)}</h3><p>{", ".join(esc(x) for x in lst)}.</p></div>' for g, lst in C.ZONE_EXTRA.items()
    )
    title = "Zone d'intervention : Saumur et 40 km autour | Tinten Couverture"
    desc = "Couvreur à Saumur et dans un rayon de 40 km : Doué-en-Anjou, Montreuil-Bellay, Longué-Jumelles, Gennes-Val-de-Loire, Fontevraud, Chinon, Loudun, Thouars."
    body = f"""
{page_hero(crumbs, split_title("Zone d'intervention"), fr("Nous intervenons à Saumur et dans un rayon d'environ 40 km, sur quatre départements : Maine-et-Loire, Indre-et-Loire, Vienne et Deux-Sèvres."), 'toiture-ardoise-cheminees', '', compact=False)}
<section class="sec sec-slate">
  <div class="wrap zone-in">
    <figure class="radar" data-radar>{radar_svg()}<figcaption>Schéma indicatif, distances à vol d'oiseau.</figcaption></figure>
    <div class="groups">{groups}
      <p data-reveal>{fr("Votre commune n'apparaît pas ? Appelez-nous au")} {tel_link('', B['phone'])} {fr(": si elle est dans notre secteur, nous venons.")}</p>
    </div>
  </div>
</section>
<section class="sec sec-light">
  <div class="wrap">
    <h2 data-reveal>Nos pages par commune</h2>
    <ul class="z-cards">{cards}</ul>
  </div>
</section>
{cta_band()}
"""
    return layout("zone-intervention", title, desc, body, "zone-intervention", [breadcrumb_schema(crumbs), org_schema()], page_class="p-inner")


def page_realisations():
    crumbs = [("Accueil", "/"), ("Réalisations", "/realisations")]
    figs = "".join(
        f'<li data-reveal class="d{i % 3 + 1}"><a href="{big_src(slug)}" data-lb data-cap="{esc(cap)}">{img(slug, cap, "(min-width: 1100px) 33vw, (min-width: 700px) 50vw, 100vw")}<span class="m-cap">{fr(esc(cap))}</span></a></li>'
        for i, (slug, cap) in enumerate(C.GALLERY)
    )
    title = "Réalisations : nos chantiers de toiture à Saumur | Tinten Couverture"
    desc = "Photos de nos chantiers dans le Saumurois : couvertures en ardoise et en tuiles, noues et gouttières en zinc, lucarnes, souches de cheminée et façades."
    body = f"""
{page_hero(crumbs, split_title('Nos réalisations'), fr("Des photos prises sur nos chantiers : couvertures en ardoise et en tuiles, zinguerie, lucarnes et cheminées."), 'maison-toit-ardoise-fenetre-de-toit', '')}
<section class="sec sec-dark">
  <div class="wrap"><ul class="masonry">{figs}</ul></div>
</section>
{cta_band()}
"""
    return layout("realisations", title, desc, body, "realisations", [breadcrumb_schema(crumbs), org_schema()], page_class="p-inner")


def page_about():
    crumbs = [("Accueil", "/"), ("À propos", "/a-propos")]
    title = "À propos : Tinten Couverture, couvreur à Saumur depuis 2009"
    desc = "Tinten Couverture, entreprise artisanale de couverture, zinguerie et ravalement installée à Saumur depuis 2009. Notre façon de travailler et nos engagements."
    body = f"""
{page_hero(crumbs, split_title(f"Couvreur à Saumur depuis {B['since']}"), fr("Tinten Couverture est une entreprise artisanale de couverture, de zinguerie et de ravalement, installée boulevard des Demoiselles, à Saumur."), 'chantier-facade-echafaudage', '')}
<div class="sec sec-light">
  <div class="wrap content-grid">
    <article class="prose">
      <figure class="prose-photo" data-reveal>{img('couvreur-tinten-toiture', "Le couvreur de Tinten Couverture sur un chantier de toiture en ardoise", "(min-width: 900px) 40vw, 100vw")}</figure>
      <section data-reveal><h2>Nos métiers</h2>
        <p>Notre activité couvre tout ce qui protège une maison de la pluie : la couverture en ardoise et en tuiles, la zinguerie (gouttières, noues, abergements, bavettes), les souches de cheminée, les fenêtres de toit et le ravalement des façades.</p>
        <p>Dans le Saumurois, cela veut dire d'abord l'ardoise et le tuffeau : des matériaux qui demandent des gestes précis et des produits compatibles, que nous pratiquons au quotidien.</p>
      </section>
      <section data-reveal><h2>Notre façon de travailler</h2>
        <ul>
          <li><strong>Une visite avant tout devis</strong> : nous montons sur le toit et dans les combles pour comprendre le problème.</li>
          <li><strong>Un devis détaillé</strong>, gratuit, avec les matériaux, les quantités et les démarches éventuelles.</li>
          <li><strong>La réparation quand elle suffit</strong> : nous ne proposons une réfection complète que lorsqu'elle se justifie.</li>
          <li><strong>Un chantier tenu</strong> : maison hors d'eau chaque soir, abords protégés, nettoyage en fin de travaux.</li>
          <li><strong>Des photos avant et après</strong>, pour que vous voyiez ce qui a été fait, même là où vous ne montez pas.</li>
        </ul>
      </section>
      <section data-reveal><h2>Garantie</h2>
        <p>Les travaux de couverture relèvent de la garantie décennale. Les références de notre assurance figurent sur chaque devis et chaque facture.</p>
      </section>
      <section data-reveal><h2>Nous trouver</h2>
        <p>{esc(B['street'])}, {B['postcode']} {esc(B['city'])}<br>{esc(B['hours_text'])}<br>Téléphone : {tel_link('', B['phone'])}</p>
        <p><a href="{B['maps']}" rel="noopener">Voir sur Google Maps</a><br><a href="{B['google_reviews']}" rel="noopener">Lire les avis Google</a></p>
      </section>
    </article>
    {contact_aside()}
  </div>
</div>
{cta_band()}
"""
    return layout("a-propos", title, desc, body, "a-propos", [breadcrumb_schema(crumbs), org_schema()], page_class="p-inner")


def page_devis():
    crumbs = [("Accueil", "/"), ("Demander un devis", "/devis")]
    options = "".join(f'<option value="{esc(s["nav"])}">{esc(s["nav"])}</option>' for s in C.SERVICES)
    title = "Demander un devis de toiture gratuit à Saumur | Tinten Couverture"
    desc = "Demandez un devis gratuit pour vos travaux de toiture, zinguerie ou ravalement à Saumur et dans un rayon de 40 km. Réponse par téléphone, visite sur place."
    body = f"""
{page_hero(crumbs, split_title('Demander un devis gratuit'), fr("Décrivez votre projet ou votre problème de toiture. Nous vous rappelons pour fixer une visite, puis nous vous remettons un devis détaillé, gratuit et sans engagement."), 'rive-zinc-ardoise', '', compact=True)}
<div class="sec sec-light">
  <div class="wrap devis-grid">
    <form class="form card" id="devis-form" action="/api/devis" method="post" novalidate data-reveal>
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
      <div class="field field-check"><input id="f-ok" name="consentement" type="checkbox" required><label for="f-ok">J'accepte que ces informations servent uniquement à répondre à ma demande (voir la <a href="/confidentialite">politique de confidentialité</a>).</label></div>
      <button class="btn btn-primary btn-lg" type="submit"><span>Envoyer ma demande</span>{ICONS['fleche']}</button>
      <div class="form-status" id="form-status" role="status" aria-live="polite"></div>
    </form>
    <aside class="aside-card" aria-label="Coordonnées" data-reveal>
      <p class="aside-title">Par téléphone</p>
      {tel_btn('btn btn-primary btn-block')}
      <a class="btn btn-outline btn-block" href="https://wa.me/{B['whatsapp']}" rel="noopener">{ICONS['wa']}<span>Écrire sur WhatsApp</span></a>
      <ul class="aside-meta">
        <li>{ICONS['horloge']}<span>{esc(B['hours_text'])}</span></li>
        <li>{ICONS['pin']}<span>{esc(B['street'])}, {B['postcode']} {esc(B['city'])}<br><a href="{B['maps']}" rel="noopener">Itinéraire</a></span></li>
        <li><span><a href="mailto:{B['email']}">{B['email']}</a></span></li>
      </ul>
    </aside>
  </div>
</div>
"""
    return layout("devis", title, desc, body, "devis", [breadcrumb_schema(crumbs), org_schema()], page_class="p-inner")


def legal_page(slug, h1, inner, title, desc):
    crumbs = [("Accueil", "/"), (h1, "/" + slug)]
    body = f"""
{page_hero(crumbs, split_title(h1), "", None, '', compact=True)}
<div class="sec sec-light"><div class="wrap narrow prose legal">{inner}</div></div>
"""
    return layout(slug, title, desc, body, "", [breadcrumb_schema(crumbs)], page_class="p-inner")


def page_mentions():
    inner = f"""
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
  <p>Les textes, photographies et le logo de ce site appartiennent à Tinten Couverture. Toute reproduction sans autorisation est interdite.</p>"""
    return legal_page("mentions-legales", "Mentions légales", inner, "Mentions légales | Tinten Couverture", "Mentions légales du site de Tinten Couverture, couvreur à Saumur.")


def page_privacy():
    inner = f"""
  <h2>Données collectées</h2>
  <p>Le formulaire de devis recueille votre nom, votre téléphone, votre commune, la description de votre projet et, si vous le souhaitez, votre adresse email.</p>
  <h2>Utilisation</h2>
  <p>Ces informations servent uniquement à vous recontacter et à établir un devis. Elles ne sont ni vendues ni cédées. Elles sont conservées le temps du traitement de votre demande, puis au plus trois ans en l'absence de suite.</p>
  <h2>Cookies et mesure d'audience</h2>
  <p>Ce site ne dépose pas de cookie publicitaire ni de traceur de mesure d'audience. Aucun bandeau de consentement n'est donc nécessaire.</p>
  <h2>Vos droits</h2>
  <p>Vous pouvez demander l'accès, la rectification ou la suppression de vos données en écrivant à <a href="mailto:{B['email']}">{B['email']}</a>. Vous pouvez aussi adresser une réclamation à la CNIL (cnil.fr).</p>
  <h2>Responsable du traitement</h2>
  <p>Tinten Couverture, {esc(B['street'])}, {B['postcode']} {esc(B['city'])}.</p>"""
    return legal_page("confidentialite", "Politique de confidentialité", inner, "Politique de confidentialité | Tinten Couverture", "Comment Tinten Couverture utilise les informations transmises par le formulaire de devis.")


def page_404():
    links = "".join(f'<li><a href="/{s["slug"]}">{esc(s["nav"])}</a></li>' for s in C.SERVICES[:6])
    extra = f'<ul class="pill-list pill-dark rise r3">{links}<li><a href="/devis">Demander un devis</a></li></ul><div class="hero-actions rise r4"><a class="btn btn-primary btn-lg" href="/"><span>Retour à l\'accueil</span>{ICONS["fleche"]}</a></div>'
    body = page_hero([("Accueil", "/"), ("Page introuvable", "/404")], split_title("Cette page n'existe pas"),
                     fr("L'adresse a peut-être changé avec la nouvelle version du site. Voici les pages les plus consultées :"),
                     "toiture-ardoise-lucarne-saumur", "", extra)
    return layout("404", "Page introuvable | Tinten Couverture", "Cette page n'existe pas ou a changé d'adresse.", body, "", [], noindex=True, page_class="p-inner")


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
    # Pages de l'ancien site encore présentes dans Google (relevé du 30/10/2026)
    ("/gouttieres", "/zinguerie-gouttieres"),
    ("/entretien-velux", "/fenetres-de-toit"),
    ("/remplacement-velux", "/fenetres-de-toit"),
    ("/nettoyage-facade", "/ravalement-facade"),
    ("/avis-clients", "/a-propos"),
    ("/entretien-toiture", "/entretien-demoussage-toiture"),
    ("/demoussage-toiture", "/entretien-demoussage-toiture"),
    ("/nos-engagements", "/a-propos"),
    ("/reparation-toiture", "/reparation-fuite-toiture"),
    ("/traitement-humidite", "/ravalement-facade"),
    ("/reparation-fissures", "/ravalement-facade"),
    ("/etancheite-terrasse", "/reparation-fuite-toiture"),
]


def write(path, text):
    full = os.path.join(PUBLIC, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(text)


def build():
    shutil.copy(os.path.join(SITE, "site.css"), os.path.join(PUBLIC, "assets/css/site.css"))
    shutil.copy(os.path.join(SITE, "site.js"), os.path.join(PUBLIC, "assets/js/site.js"))
    try:
        from PIL import Image
        Image.open(os.path.join(PUBLIC, "assets/img/icon-512.png")).save(os.path.join(PUBLIC, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])
    except ImportError:
        pass

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

    urls = ["/"] + ["/" + n[:-5] for n in pages if n not in ("index.html", "404.html")]
    prio = {"/": "1.0", "/devis": "0.9", "/couvreur-saumur": "0.9"}
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        sm.append(f"  <url><loc>{URL}{u}</loc><lastmod>{TODAY}</lastmod><priority>{prio.get(u, '0.8' if u.strip('/') in C.SERVICE_BY_SLUG else '0.7')}</priority></url>")
    sm.append("</urlset>")
    write("sitemap.xml", "\n".join(sm) + "\n")
    write("robots.txt", f"User-agent: *\nAllow: /\nDisallow: /api/\n\nSitemap: {URL}/sitemap.xml\n")

    llms = ["# Tinten Couverture", "", f"> Couvreur, zingueur et ravalement à Saumur (49400) depuis {B['since']}. Intervient dans un rayon d'environ {B['radius_km']} km.", "",
            f"Adresse : {B['street']}, {B['postcode']} {B['city']}. Téléphone : {B['phone']}. {B['hours_text']}.", "", "## Prestations"]
    llms += [f"- [{s['nav']}]({URL}/{s['slug']}) : {s['short']}" for s in C.SERVICES]
    llms += ["", "## Communes"] + [f"- [Couvreur à {c['name']}]({URL}/{c['slug']}) ({c['cp']})" for c in C.CITIES]
    llms += ["", "## Contact", f"- [Demander un devis]({URL}/devis)", f"- [À propos]({URL}/a-propos)", ""]
    write("llms.txt", "\n".join(llms))

    red = ["# Anciennes adresses -> nouvelles pages (301 permanentes)"]
    for src, dst in REDIRECTS:
        red += [f"{src} {dst} 301", f"{src}/ {dst} 301", f"{src}.html {dst} 301"]
    write("_redirects", "\n".join(red) + "\n")

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
                "background_color": "#151c22", "theme_color": "#151c22",
                "icons": [{"src": "/assets/img/icon-512.png", "sizes": "512x512", "type": "image/png"}]}
    write("site.webmanifest", json.dumps(manifest, ensure_ascii=False, indent=1))
    print(f"{len(pages)} pages générées, {len(urls)} URL dans le sitemap")


if __name__ == "__main__":
    build()
