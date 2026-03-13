#!/usr/bin/env python3
"""
Génère wireframe_naf_rome.excalidraw — wireframe de l'interface NAF↔ROME.

Usage :
    python generate_wireframe.py

Ouvrir le fichier généré sur :  https://excalidraw.com  (File → Open)
Ou dans VS Code avec l'extension "Excalidraw".

Modifiez ce script pour adapter le wireframe à votre design !
"""

import json
import random
import time

random.seed(42)
TS = int(time.time() * 1000)
_id = 0


def uid() -> str:
    global _id
    _id += 1
    return f"e{_id:04d}"


def rnd() -> int:
    return random.randint(1, 999_999)


# ── Primitives ────────────────────────────────────────────────────────────────

def rect(x, y, w, h, bg="transparent", stroke="#1e1e1e",
         roughness=1, radius=8, stroke_w=2, opacity=100):
    return {
        "id": uid(), "type": "rectangle",
        "x": x, "y": y, "width": w, "height": h,
        "angle": 0, "strokeColor": stroke, "backgroundColor": bg,
        "fillStyle": "solid", "strokeWidth": stroke_w,
        "roughness": roughness, "opacity": opacity,
        "groupIds": [],
        "roundness": {"type": 3, "value": radius},
        "seed": rnd(), "version": 1, "versionNonce": rnd(),
        "isDeleted": False, "boundElements": None,
        "updated": TS, "link": None, "locked": False,
    }


def txt(x, y, content, size=13, bold=False, color="#1e1e1e",
        align="left", w=None, italic=False):
    auto_w = w or max(int(len(content) * size * 0.55), 60)
    auto_h = int(size * 1.6)
    return {
        "id": uid(), "type": "text",
        "x": x, "y": y, "width": auto_w, "height": auto_h,
        "angle": 0, "strokeColor": color, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": 1,
        "roughness": 0, "opacity": 100,
        "groupIds": [], "roundness": None,
        "seed": rnd(), "version": 1, "versionNonce": rnd(),
        "isDeleted": False, "boundElements": None,
        "updated": TS, "link": None, "locked": False,
        "text": content, "fontSize": size, "fontFamily": 1,
        "textAlign": align, "verticalAlign": "top",
        "baseline": int(size * 0.8),
        "containerId": None, "originalText": content,
        "fontStyle": ("bold" if bold else ("italic" if italic else "normal")),
    }


def arrow(x1, y1, x2, y2, color="#6366f1", label=""):
    el = {
        "id": uid(), "type": "arrow",
        "x": x1, "y": y1,
        "width": x2 - x1, "height": y2 - y1,
        "angle": 0, "strokeColor": color, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": 2,
        "roughness": 1, "opacity": 100,
        "groupIds": [], "roundness": {"type": 2},
        "seed": rnd(), "version": 1, "versionNonce": rnd(),
        "isDeleted": False, "boundElements": None,
        "updated": TS, "link": None, "locked": False,
        "points": [[0, 0], [x2 - x1, y2 - y1]],
        "lastCommittedPoint": None,
        "startBinding": None, "endBinding": None,
        "startArrowhead": None, "endArrowhead": "arrow",
    }
    return [el] + ([txt(x1 + (x2-x1)//2, y1 + (y2-y1)//2 - 16, label, 11, color="#6366f1")] if label else [])


# ── Couleurs ──────────────────────────────────────────────────────────────────
C = {
    "bg":          "#f8fafc",
    "header_bg":   "#e0e7ff",
    "card_bg":     "#f1f5f9",
    "input_bg":    "#ffffff",
    "btn_bg":      "#e2e8f0",
    "btn_active":  "#3b82f6",
    "export_btn":  "#d1fae5",
    "table_hdr":   "#f1f5f9",
    "row_alt":     "#fafafa",
    "badge_naf":   "#dbeafe",
    "badge_rome":  "#ede9fe",
    "stroke":      "#334155",
    "stroke_light":"#94a3b8",
    "annotation":  "#6366f1",
    "mobile_bg":   "#fef3c7",
}

els = []  # liste principale

# ═══════════════════════════════════════════════════════════════════════════
# TITRE GLOBAL
# ═══════════════════════════════════════════════════════════════════════════
els += [
    txt(60, 20, "TP 1.0 — Wireframe : Explorateur NAF ↔ ROME",
        size=22, bold=True, color=C["annotation"]),
    txt(60, 52, "Ouvrir sur https://excalidraw.com · Modifier le design avec generate_wireframe.py",
        size=12, italic=True, color="#64748b"),
]

# ═══════════════════════════════════════════════════════════════════════════
# ÉCRAN DESKTOP  (x=60, y=100  →  1400×1060)
# ═══════════════════════════════════════════════════════════════════════════
DX, DY, DW = 60, 100, 1400

els += [
    # Cadre principal
    rect(DX, DY, DW, 1060, stroke=C["annotation"], roughness=1, radius=4, stroke_w=3),
    txt(DX + 6, DY - 22, "Desktop — 1400 px", size=12, color=C["annotation"]),
]

# ── 1. HEADER ──────────────────────────────────────────────────────────────
HY = DY
els += [
    rect(DX, HY, DW, 72, bg=C["header_bg"], stroke=C["stroke"], roughness=1, radius=0),
    txt(DX + 20, HY + 14, "🔍", size=28),
    txt(DX + 62, HY + 12, "Explorateur NAF ↔ ROME", size=18, bold=True, color=C["stroke"]),
    txt(DX + 62, HY + 40, "Correspondances entre codes d'activité (NAF) et codes métier (ROME)", size=11, color="#475569"),
    # Badge "Source CSV — Jour 1"
    rect(DX + 1100, HY + 22, 160, 28, bg=C["badge_naf"], stroke="#3b82f6", roughness=0, radius=20, stroke_w=1),
    txt(DX + 1115, HY + 29, "Source : CSV — Jour 1", size=11, color="#1d4ed8"),
    # Badge "API — Jour 2" (grisé pour montrer la variante)
    rect(DX + 1275, HY + 22, 150, 28, bg=C["card_bg"], stroke=C["stroke_light"], roughness=0, radius=20, stroke_w=1),
    txt(DX + 1286, HY + 29, "API FastAPI — Jour 2", size=11, color="#94a3b8"),
]

# ── 2. STATS BAR ───────────────────────────────────────────────────────────
SY = DY + 90
CARD_W, CARD_H, CARD_GAP = 330, 84, 16
stats = [
    ("Total enregistrements", "40",    "#1e293b"),
    ("Codes NAF",             "20",    "#2563eb"),
    ("Codes ROME",            "20",    "#7c3aed"),
    ("Secteurs uniques",      "14",    "#059669"),
]
for i, (label, value, vcolor) in enumerate(stats):
    cx = DX + i * (CARD_W + CARD_GAP)
    els += [
        rect(cx, SY, CARD_W, CARD_H, bg=C["input_bg"], stroke=C["stroke_light"], roughness=0, radius=12, stroke_w=1),
        txt(cx + 16, SY + 12, label, size=10, color="#64748b"),
        txt(cx + 16, SY + 34, value, size=28, bold=True, color=vcolor),
    ]

# Annotation stats
els += [arrow(DX + 700, SY - 30, DX + 700, SY - 2, label="Tuiles de statistiques")]

# ── 3. ZONE DE RECHERCHE ──────────────────────────────────────────────────
RY = SY + CARD_H + 16
els += [
    rect(DX, RY, DW, 160, bg=C["input_bg"], stroke=C["stroke_light"], roughness=1, radius=12, stroke_w=1),
]

# Input mot-clé (2/3 de largeur)
KW = int(DW * 0.65) - 40
els += [
    txt(DX + 20, RY + 14, "Recherche par mot-clé", size=10, bold=True, color="#64748b"),
    rect(DX + 20, RY + 32, KW, 38, bg=C["input_bg"], stroke=C["stroke"], roughness=1, radius=8, stroke_w=1),
    txt(DX + 44, RY + 43, "🔍  ex : informatique, médecin, agriculture…", size=12, color="#94a3b8"),
]

# Input code
CX2 = DX + 20 + KW + 24
CW2 = DW - KW - 64
els += [
    txt(CX2, RY + 14, "Code NAF ou ROME", size=10, bold=True, color="#64748b"),
    rect(CX2, RY + 32, CW2, 38, bg=C["input_bg"], stroke=C["stroke"], roughness=1, radius=8, stroke_w=1),
    txt(CX2 + 16, RY + 43, "ex : 62.01Z  ou  M1805", size=12, color="#94a3b8", italic=True),
]

# Filtres type
els += [txt(DX + 20, RY + 90, "Type :", size=10, bold=True, color="#64748b")]
btns = [("Tous", True), ("NAF", False), ("ROME", False)]
BX = DX + 70
for label, active in btns:
    bg = C["btn_active"] if active else C["btn_bg"]
    fc = "#ffffff" if active else C["stroke"]
    els += [
        rect(BX, RY + 84, 64, 28, bg=bg, stroke="transparent", roughness=0, radius=20, stroke_w=0),
        txt(BX + 8, RY + 91, label, size=12, bold=active, color=fc),
    ]
    BX += 76

# Bouton réinitialiser (droit)
els += [
    txt(DX + DW - 130, RY + 91, "✕  Réinitialiser", size=12, color="#ef4444"),
]

# Annotation recherche
els += [arrow(DX - 30, RY + 80, DX + 18, RY + 80, label="Filtres type")]

# ── 4. TABLEAU DE RÉSULTATS ────────────────────────────────────────────────
TY = RY + 178
COLS = [("Type", 72), ("Code NAF", 120), ("Code ROME", 120), ("Intitulé", 380), ("Description", 660)]
ROW_H = 46

# Barre d'actions (export + pagination)
els += [
    rect(DX, TY, DW, 50, bg=C["input_bg"], stroke=C["stroke_light"], roughness=0, radius=0, stroke_w=1),
    txt(DX + 20, TY + 16, "12 résultats  sur 40", size=13, color=C["stroke"]),
    # Select lignes/page
    rect(DX + DW - 340, TY + 10, 120, 30, bg=C["input_bg"], stroke=C["stroke"], roughness=0, radius=6, stroke_w=1),
    txt(DX + DW - 332, TY + 18, "25 / page  ▾", size=12, color=C["stroke"]),
    # Bouton Export CSV
    rect(DX + DW - 200, TY + 10, 140, 30, bg=C["export_btn"], stroke="#059669", roughness=0, radius=8, stroke_w=1),
    txt(DX + DW - 190, TY + 18, "⬇  Exporter CSV", size=12, bold=True, color="#065f46"),
]

# En-tête colonnes
HY2 = TY + 50
els.append(rect(DX, HY2, DW, 38, bg=C["table_hdr"], stroke=C["stroke_light"], roughness=0, radius=0, stroke_w=1))
cx = DX
for col_name, col_w in COLS:
    els.append(txt(cx + 12, HY2 + 11, col_name + "  ↕", size=11, bold=True, color="#475569"))
    cx += col_w

# Lignes de données
sample_rows = [
    ("NAF", "62.01Z",  "M1805", "Programmation informatique",        "Écriture et test de logiciels sur mesure."),
    ("ROME", "",       "M1805", "Développement de logiciels",         "Conception d'applications web et desktop."),
    ("NAF", "86.21Z",  "J1110", "Médecine généraliste",               "Consultations et suivi de patients en cabinet."),
    ("NAF", "85.20Z",  "K2101", "Enseignement primaire",              "Éducation au niveau primaire, maternelle…"),
    ("ROME", "",       "K2101", "Enseignement du premier degré",       "Animation pédagogique et instruction."),
]
for i, (typ, naf, rome, name, desc) in enumerate(sample_rows):
    ry2 = HY2 + 38 + i * ROW_H
    row_bg = C["row_alt"] if i % 2 == 0 else C["input_bg"]
    els.append(rect(DX, ry2, DW, ROW_H, bg=row_bg, stroke=C["stroke_light"], roughness=0, radius=0, stroke_w=1))
    cx = DX
    # Colonne Type (badge coloré)
    badge_bg = C["badge_naf"] if typ == "NAF" else C["badge_rome"]
    badge_c  = "#1d4ed8" if typ == "NAF" else "#6d28d9"
    els += [
        rect(cx + 8, ry2 + 12, 54, 22, bg=badge_bg, stroke="transparent", roughness=0, radius=12, stroke_w=0),
        txt(cx + 16, ry2 + 15, typ, size=11, bold=True, color=badge_c),
    ]
    cx += COLS[0][1]
    els.append(txt(cx + 8, ry2 + 14, naf, size=12, color="#1d4ed8"))
    cx += COLS[1][1]
    els.append(txt(cx + 8, ry2 + 14, rome, size=12, color="#6d28d9"))
    cx += COLS[2][1]
    els.append(txt(cx + 8, ry2 + 14, name, size=12, bold=(i == 0), color=C["stroke"]))
    cx += COLS[3][1]
    els.append(txt(cx + 8, ry2 + 14, desc[:55] + "…", size=11, color="#64748b"))

# Surligné mot-clé (annotation)
els += [
    rect(DX + 380, HY2 + 38 + 12, 140, 22, bg="#fef9c3", stroke="#eab308", roughness=0, radius=4, stroke_w=1),
    txt(DX + 390, HY2 + 38 + 14, "mot surligné", size=11, color="#92400e"),
]

# Pagination
PAG_Y = HY2 + 38 + len(sample_rows) * ROW_H + 8
els += [
    txt(DX + 20, PAG_Y + 10, "Page 1 / 2", size=12, color="#64748b"),
    rect(DX + DW - 280, PAG_Y, 80, 32, bg=C["btn_bg"], stroke=C["stroke_light"], roughness=0, radius=8, stroke_w=1),
    txt(DX + DW - 272, PAG_Y + 9, "← Préc.", size=12, color="#94a3b8"),
    rect(DX + DW - 190, PAG_Y, 40, 32, bg=C["btn_active"], stroke="transparent", roughness=0, radius=8, stroke_w=0),
    txt(DX + DW - 180, PAG_Y + 9, "1", size=13, bold=True, color="#fff"),
    rect(DX + DW - 140, PAG_Y, 40, 32, bg=C["btn_bg"], stroke=C["stroke_light"], roughness=0, radius=8, stroke_w=1),
    txt(DX + DW - 132, PAG_Y + 9, "2", size=13, color=C["stroke"]),
    rect(DX + DW - 90, PAG_Y, 80, 32, bg=C["btn_bg"], stroke=C["stroke_light"], roughness=0, radius=8, stroke_w=1),
    txt(DX + DW - 82, PAG_Y + 9, "Suiv. →", size=12, color=C["stroke"]),
]

# Annotations tableau
els += [
    *arrow(DX + DW + 20, TY + 25, DX + DW + 20, TY + 25, label=""),  # spacer
    txt(DX + DW + 20, TY + 10, "← Export CSV", size=11, color=C["annotation"]),
    txt(DX + DW + 20, HY2 + 8, "← Tri par colonne", size=11, color=C["annotation"]),
    txt(DX + DW + 20, HY2 + 38 + 12, "← Badge type", size=11, color=C["annotation"]),
]

# ═══════════════════════════════════════════════════════════════════════════
# ÉCRAN MOBILE  (à droite du desktop, x=1600)
# ═══════════════════════════════════════════════════════════════════════════
MX, MY, MW, MH = 1560, 100, 390, 840
els += [
    rect(MX, MY, MW, MH, stroke=C["annotation"], roughness=1, radius=4, stroke_w=3),
    txt(MX + 6, MY - 22, "Mobile — 390 px", size=12, color=C["annotation"]),

    # Header mobile
    rect(MX, MY, MW, 60, bg=C["header_bg"], stroke=C["stroke"], roughness=1, radius=0),
    txt(MX + 16, MY + 12, "🔍  Explorateur NAF ↔ ROME", size=14, bold=True, color=C["stroke"]),
    txt(MX + 16, MY + 34, "Correspondances NAF / ROME", size=10, color="#475569"),

    # Stats (2×2 grid)
    rect(MX + 8,   MY + 72, 183, 60, bg=C["input_bg"], stroke=C["stroke_light"], roughness=0, radius=8, stroke_w=1),
    txt(MX + 20,   MY + 82, "Total", size=10, color="#64748b"),
    txt(MX + 20,   MY + 97, "40", size=20, bold=True, color="#1e293b"),

    rect(MX + 199, MY + 72, 183, 60, bg=C["input_bg"], stroke=C["stroke_light"], roughness=0, radius=8, stroke_w=1),
    txt(MX + 211,  MY + 82, "NAF / ROME", size=10, color="#64748b"),
    txt(MX + 211,  MY + 97, "20 / 20", size=20, bold=True, color="#2563eb"),

    # Search (stacked)
    rect(MX + 8, MY + 148, MW - 16, 44, bg=C["input_bg"], stroke=C["stroke"], roughness=1, radius=8, stroke_w=1),
    txt(MX + 28, MY + 159, "🔍  Mot-clé…", size=13, color="#94a3b8"),

    rect(MX + 8, MY + 200, MW - 16, 44, bg=C["input_bg"], stroke=C["stroke"], roughness=1, radius=8, stroke_w=1),
    txt(MX + 28, MY + 211, "Code NAF ou ROME…", size=13, color="#94a3b8"),

    # Filtres type (horizontal scroll)
    rect(MX + 8,  MY + 256, 80, 28, bg=C["btn_active"], stroke="transparent", roughness=0, radius=20),
    txt(MX + 22,  MY + 263, "Tous", size=12, bold=True, color="#fff"),
    rect(MX + 96, MY + 256, 64, 28, bg=C["btn_bg"], stroke="transparent", roughness=0, radius=20),
    txt(MX + 110, MY + 263, "NAF", size=12, color=C["stroke"]),
    rect(MX + 168, MY + 256, 72, 28, bg=C["btn_bg"], stroke="transparent", roughness=0, radius=20),
    txt(MX + 180, MY + 263, "ROME", size=12, color=C["stroke"]),

    # Tableau mobile (cartes)
    txt(MX + 16, MY + 300, "12 résultats", size=12, color=C["stroke"]),
    rect(MX + 8, MY + 316, MW - 16, 110, bg=C["input_bg"], stroke=C["stroke_light"], roughness=0, radius=10, stroke_w=1),
    rect(MX + 18, MY + 328, 44, 20, bg=C["badge_naf"], stroke="transparent", roughness=0, radius=10),
    txt(MX + 24, MY + 330, "NAF", size=10, bold=True, color="#1d4ed8"),
    txt(MX + 70, MY + 328, "62.01Z", size=10, bold=True, color="#1d4ed8"),
    txt(MX + 200, MY + 328, "M1805", size=10, bold=True, color="#6d28d9"),
    txt(MX + 18, MY + 354, "Programmation informatique", size=13, bold=True, color=C["stroke"]),
    txt(MX + 18, MY + 374, "Écriture et test de logiciels sur mesure…", size=11, color="#64748b"),
    txt(MX + 18, MY + 394, "Score similarité : 0.92", size=11, color="#059669"),

    rect(MX + 8, MY + 438, MW - 16, 110, bg=C["row_alt"], stroke=C["stroke_light"], roughness=0, radius=10, stroke_w=1),
    rect(MX + 18, MY + 450, 54, 20, bg=C["badge_rome"], stroke="transparent", roughness=0, radius=10),
    txt(MX + 24, MY + 452, "ROME", size=10, bold=True, color="#6d28d9"),
    txt(MX + 18, MY + 476, "Développement de logiciels", size=13, bold=True, color=C["stroke"]),
    txt(MX + 18, MY + 496, "Conception d'applications web et desktop…", size=11, color="#64748b"),

    rect(MX + 8, MY + 560, MW - 16, 110, bg=C["input_bg"], stroke=C["stroke_light"], roughness=0, radius=10, stroke_w=1),
    txt(MX + 18, MY + 578, "Médecine généraliste", size=13, bold=True, color=C["stroke"]),
    txt(MX + 18, MY + 598, "Consultations et suivi de patients…", size=11, color="#64748b"),

    # Export bouton mobile (bottom)
    rect(MX + 8, MY + 688, MW - 16, 46, bg=C["export_btn"], stroke="#059669", roughness=0, radius=12, stroke_w=1),
    txt(MX + MW//2 - 60, MY + 703, "⬇  Exporter CSV", size=14, bold=True, color="#065f46"),

    # Pagination mobile
    rect(MX + 8,        MY + 746, 80, 36, bg=C["btn_bg"], stroke=C["stroke_light"], roughness=0, radius=8, stroke_w=1),
    txt(MX + 18,        MY + 757, "← Préc.", size=12, color="#94a3b8"),
    rect(MX + MW//2 - 30, MY + 746, 60, 36, bg=C["btn_active"], stroke="transparent", roughness=0, radius=8),
    txt(MX + MW//2 - 12, MY + 757, "1", size=14, bold=True, color="#fff"),
    rect(MX + MW - 90,  MY + 746, 80, 36, bg=C["btn_bg"], stroke=C["stroke_light"], roughness=0, radius=8, stroke_w=1),
    txt(MX + MW - 80,   MY + 757, "Suiv. →", size=12, color=C["stroke"]),
]

# ═══════════════════════════════════════════════════════════════════════════
# LÉGENDE
# ═══════════════════════════════════════════════════════════════════════════
LX, LY = 60, 1220
els += [
    rect(LX, LY, 820, 100, bg="#f8fafc", stroke=C["annotation"], roughness=0, radius=10, stroke_w=1),
    txt(LX + 16, LY + 12, "Légende", size=13, bold=True, color=C["annotation"]),
    rect(LX + 16,  LY + 36, 44, 20, bg=C["badge_naf"],  stroke="transparent", roughness=0, radius=10),
    txt(LX + 24,   LY + 38, "NAF", size=10, bold=True, color="#1d4ed8"),
    txt(LX + 68,   LY + 38, "= Code d'activité économique (INSEE)", size=11, color=C["stroke"]),
    rect(LX + 320, LY + 36, 54, 20, bg=C["badge_rome"], stroke="transparent", roughness=0, radius=10),
    txt(LX + 326,  LY + 38, "ROME", size=10, bold=True, color="#6d28d9"),
    txt(LX + 382,  LY + 38, "= Code métier (France Travail)", size=11, color=C["stroke"]),
    txt(LX + 16,   LY + 68, "⬇ Export CSV = télécharge les résultats filtrés visibles", size=11, color="#64748b"),
    txt(LX + 400,  LY + 68, "↕ = tri ascendant/descendant sur la colonne", size=11, color="#64748b"),
]

# ═══════════════════════════════════════════════════════════════════════════
# NOTE JOUR 1 vs JOUR 2
# ═══════════════════════════════════════════════════════════════════════════
NX, NY = 900, 1220
els += [
    rect(NX, NY, 1050, 100, bg="#fff7ed", stroke="#f97316", roughness=0, radius=10, stroke_w=1),
    txt(NX + 16, NY + 12, "Jour 1 vs Jour 2", size=13, bold=True, color="#c2410c"),
    txt(NX + 16, NY + 36, "Jour 1 (badge bleu) : les données viennent du fichier CSV dans le navigateur — aucun backend requis.", size=11, color=C["stroke"]),
    txt(NX + 16, NY + 56, "Jour 2 (badge vert) : les mêmes composants Vue.js appelent l'API FastAPI sur localhost:8000.", size=11, color=C["stroke"]),
    txt(NX + 16, NY + 76, "→ Seul apiService.ts change (csvService.ts → apiService.ts). Les composants restent identiques.", size=11, bold=True, color="#c2410c"),
]

# ═══════════════════════════════════════════════════════════════════════════
# EXPORT
# ═══════════════════════════════════════════════════════════════════════════
output = {
    "type": "excalidraw",
    "version": 2,
    "source": "NAF-ROME TP Wireframe — generate_wireframe.py",
    "elements": els,
    "appState": {
        "gridSize": None,
        "viewBackgroundColor": "#f8fafc",
    },
    "files": {},
}

out_path = "wireframe_naf_rome.excalidraw"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"✅  Fichier généré : {out_path}")
print(f"   {len(els)} éléments créés")
print()
print("Pour l'ouvrir :")
print("  1. Allez sur https://excalidraw.com")
print("  2. File → Open → sélectionnez wireframe_naf_rome.excalidraw")
print()
print("Pour modifier le design :")
print("  Éditez ce script puis relancez : python generate_wireframe.py")
