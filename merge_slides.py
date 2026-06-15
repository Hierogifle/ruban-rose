# -*- coding: utf-8 -*-
"""Fusionne les résultats d'Emile (ViT-Small in21k / ConvNeXt-Tiny in1k, binaire)
DANS les diapos existantes du collègue : modèles (9), résultats (10),
par sous-type (11), hyperparamètres Optuna (15)."""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

SRC = "Soutenance_Ruban_Rose_2.pptx"

PINK_DARK = RGBColor(0xC2, 0x18, 0x5B)
PINK      = RGBColor(0xF4, 0x8F, 0xB1)
PINK_BG   = RGBColor(0xFC, 0xE4, 0xEC)
INK       = RGBColor(0x1A, 0x1A, 0x2E)
GREY      = RGBColor(0x9E, 0x9E, 0x9E)
GREY_D    = RGBColor(0x42, 0x42, 0x42)
CARD_BG   = RGBColor(0xFA, 0xFA, 0xFA)
CARD_BD   = RGBColor(0xBD, 0xBD, 0xBD)
WHITE     = RGBColor(0xFF, 0xFF, 0xFF)
BLACK     = RGBColor(0x00, 0x00, 0x00)
GREEN     = RGBColor(0x2E, 0x7D, 0x32)
ORANGE    = RGBColor(0xE6, 0x51, 0x00)
FONT      = "Calibri"

prs = Presentation(SRC)


# ── utilitaires ──────────────────────────────────────────────────────────────
def shapes(slide):
    return list(slide.shapes)


def remove(sh):
    sh._element.getparent().remove(sh._element)


def set_subtitle(slide, text):
    sh = shapes(slide)[2]
    tf = sh.text_frame
    p = tf.paragraphs[0]
    for r in list(p.runs)[1:]:
        r._r.getparent().remove(r._r)
    p.runs[0].text = text


def _run(r, text, size, bold, color, italic=False):
    r.text = text
    r.font.name = FONT
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.italic = italic
    r.font.color.rgb = color


def add_text(slide, l, t, w, h, lines, size=11.5, bold=False, color=INK,
             align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, space_after=4):
    tb = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    if isinstance(lines, str):
        lines = [(lines, {})]
    for i, item in enumerate(lines):
        txt, kw = item if isinstance(item, tuple) else (item, {})
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = kw.get("align", align)
        p.space_after = Pt(kw.get("space_after", space_after))
        p.space_before = Pt(0)
        _run(p.add_run(), txt, kw.get("size", size), kw.get("bold", bold),
             kw.get("color", color), kw.get("italic", False))
    return tb


def add_rect(slide, l, t, w, h, fill, line=None, line_w=9525, rounded=False):
    shp = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE,
        Inches(l), Inches(t), Inches(w), Inches(h))
    shp.fill.solid()
    shp.fill.fore_color.rgb = fill
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line
        shp.line.width = Emu(line_w)
    shp.shadow.inherit = False
    if rounded:
        try:
            shp.adjustments[0] = 0.06
        except Exception:
            pass
    return shp


def style_table(table):
    pr = table._tbl.tblPr
    pr.set("firstRow", "0")
    pr.set("bandRow", "0")


def fill_cell(cell, text, size=12.5, bold=False, color=BLACK, fill=WHITE,
              align=PP_ALIGN.CENTER):
    cell.fill.solid()
    cell.fill.fore_color.rgb = fill
    cell.vertical_anchor = MSO_ANCHOR.MIDDLE
    cell.margin_top = Pt(1)
    cell.margin_bottom = Pt(1)
    cell.margin_left = Pt(5)
    cell.margin_right = Pt(5)
    tf = cell.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    _run(p.add_run(), text, size, bold, color)


def build_table(slide, l, t, total_w, col_w, data, row_h=0.42,
                base_size=12.5, header_size=12.5):
    nr, nc = len(data), len(col_w)
    gt = slide.shapes.add_table(nr, nc, Inches(l), Inches(t),
                                Inches(total_w), Inches(row_h * nr))
    table = gt.table
    style_table(table)
    for ci, wv in enumerate(col_w):
        table.columns[ci].width = Inches(wv)
    for ri, row in enumerate(data):
        table.rows[ri].height = Inches(row_h)
        for ci, spec in enumerate(row):
            txt, o = spec if isinstance(spec, tuple) else (spec, {})
            head = ri == 0
            fill_cell(table.cell(ri, ci), txt,
                      size=o.get("size", header_size if head else base_size),
                      bold=o.get("bold", head),
                      color=o.get("color", WHITE if head else BLACK),
                      fill=o.get("fill", PINK_DARK if head else WHITE),
                      align=o.get("align", PP_ALIGN.LEFT if ci == 0 else PP_ALIGN.CENTER))
    return gt


def model_card(slide, l, t, w, h, header, accent, lines, f1_line):
    add_rect(slide, l, t, w, h, CARD_BG, line=CARD_BD, rounded=True)
    bar = add_rect(slide, l, t, w, 0.46, accent, rounded=True)
    add_text(slide, l + 0.05, t, w - 0.10, 0.46, header, size=12.5, bold=True,
             color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(slide, l + 0.16, t + 0.55, w - 0.30, h - 1.05, lines,
             size=10, color=GREY_D, space_after=6)
    add_text(slide, l + 0.16, t + h - 0.42, w - 0.30, 0.36, f1_line,
             size=11, bold=True, color=accent, align=PP_ALIGN.CENTER)


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 9 — Modèles entraînés (équipe + Emile)
# ═══════════════════════════════════════════════════════════════════════════
s9 = prs.slides[9]
for sh in shapes(s9)[4:]:
    remove(sh)
set_subtitle(s9, "Pipeline équipe (multi-classe, 8 sous-types)  +  étude binaire complémentaire (Emile)")

# label groupe équipe
add_text(s9, 0.35, 1.32, 9.30, 0.30,
         "Équipe — classification multi-classe", size=11, bold=True, color=PINK_DARK)
model_card(s9, 0.35, 1.65, 3.00, 1.95, "ResNet-50 v3", PINK, [
    "CNN profond (50 couches)",
    "Transfer Learning ImageNet",
    "Fine-tuning couches finales",
], "F1 macro ≈ 0.910")
model_card(s9, 3.55, 1.65, 3.00, 1.95, "ViT + Optuna", PINK, [
    "Vision Transformer (patches 16×16)",
    "Attention multi-têtes (12 heads)",
    "Optuna — 50 trials",
], "F1 macro ≈ 0.921")
model_card(s9, 6.75, 1.65, 3.00, 1.95, "ViT + Optuna + WRS  ✅", PINK_DARK, [
    "Même archi que V2",
    "WeightedRandomSampler",
    "+21 % F1 sur Papillary Carc.",
], "F1 macro ≈ 0.934  ← BEST")

# label groupe Emile
add_text(s9, 0.35, 3.72, 9.30, 0.30,
         "Emile — classification binaire (Bénin / Malin)", size=11, bold=True, color=PINK_DARK)
model_card(s9, 0.35, 4.05, 4.55, 1.25, "ViT-Small · ImageNet-21k", PINK, [
    "Transformer pré-entraîné 21k · Optuna 30 trials · split patient",
], "F1 macro ≈ 0.886 (test)")
model_card(s9, 5.10, 4.05, 4.55, 1.25, "ConvNeXt-Tiny · ImageNet-1k", PINK, [
    "CNN moderne pré-entraîné 1k · Optuna 30 trials · split patient",
], "F1 macro ≈ 0.813 (test)")

# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 10 — Résultats comparatifs (table fusionnée + bandeau caveat)
# ═══════════════════════════════════════════════════════════════════════════
s10 = prs.slides[10]
for sh in shapes(s10)[4:]:
    remove(sh)
set_subtitle(s10, "F1 macro · Precision · Recall · AUC-ROC  —  équipe (multi-classe) + Emile (binaire)")

g = {"color": GREEN, "bold": True}
pinkbg = {"fill": PINK_BG}
data10 = [
    ["Modèle", "Tâche", "F1 macro", "Precision", "Recall", "AUC-ROC"],
    ["ResNet-50 v3", "Multi (8)", "0.910", "0.914", "0.908", "0.962"],
    ["ViT + Optuna", "Multi (8)", "0.921", "0.925", "0.919", "0.971"],
    [("ViT + Optuna + WRS  ✅", g), ("Multi (8)", g), ("0.934", g), ("0.931", g),
     ("0.936", g), ("0.978", g)],
    [("ViT-Small · in21k  ✅", {**pinkbg, "color": GREEN, "bold": True}),
     ("Binaire", pinkbg), ("0.886", {**pinkbg, "color": GREEN, "bold": True}),
     ("0.889", pinkbg), ("0.883", pinkbg), ("—", pinkbg)],
    [("ConvNeXt-Tiny · in1k", pinkbg), ("Binaire", pinkbg), ("0.813", pinkbg),
     ("0.857", pinkbg), ("0.795", pinkbg), ("—", pinkbg)],
]
build_table(s10, 0.35, 1.35, 9.30, [2.65, 1.35, 1.35, 1.35, 1.30, 1.30],
            data10, row_h=0.40, base_size=12, header_size=12)

# bandeau caveat (remplace le placeholder graphique vide)
add_rect(s10, 0.35, 4.15, 9.30, 1.15, PINK_BG, rounded=True)
add_rect(s10, 0.35, 4.25, 0.07, 0.95, PINK_DARK)
add_text(s10, 0.58, 4.27, 8.95, 0.95, [
    ("⚠️  À lire avec la tâche", {"size": 11.5, "bold": True, "color": PINK_DARK, "space_after": 3}),
    ("L'équipe classe 8 sous-types (multi-classe) ; l'étude d'Emile classe en binaire Bénin/Malin — les F1 macro ne sont pas directement comparables. Côté binaire, ViT-Small (21k) devance ConvNeXt-Tiny (1k) de +7 pts : un écart dû au pré-entraînement (21k vs 1k), pas à l'architecture.",
     {"size": 10.5, "color": GREY_D}),
], anchor=MSO_ANCHOR.MIDDLE)

# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 11 — Par sous-type (ajout colonnes binaires Emile)
# ═══════════════════════════════════════════════════════════════════════════
s11 = prs.slides[11]
for sh in shapes(s11)[4:]:
    remove(sh)
set_subtitle(s11, "F1 par classe (équipe, multi-classe)  +  accuracy binaire (Emile)")

og = {"color": GREEN, "bold": True}
oo = {"color": ORANGE, "bold": True}
em = {"fill": PINK_BG}
data11 = [
    ["Sous-type", "Type", "F1 ResNet", "F1 ViT", "F1 +WRS", "Δ WRS",
     ("ViT-S†", {"fill": PINK_DARK, "color": WHITE, "bold": True}),
     ("ConvN†", {"fill": PINK_DARK, "color": WHITE, "bold": True})],
    ["Ductal Carcinoma", "Malin", "0.981", "0.985", "0.983", "≈ 0",
     ("100 %", em), ("100 %", em)],
    ["Lobular Carcinoma", "Malin", "0.974", "0.978", "0.981", "+0.7 %",
     ("100 %", em), ("100 %", em)],
    ["Mucinous Carcinoma", "Malin", "0.912", "0.918", "0.990", ("+8 %", og),
     ("90 %", em), ("99 %", em)],
    ["Papillary Carcinoma", "Malin", "0.701", "0.724", ("0.921", {"bold": True}),
     ("+21 % ✅", og), ("56 %", em), ("62 %", em)],
    ["Tubular Adenoma", "Bénin", "0.887", "0.913", "0.866", ("-4.7 % ⚠️", oo),
     ("27 %", em), ("8 %", em)],
]
build_table(s11, 0.35, 1.40, 8.95, [1.85, 0.75, 1.05, 1.0, 1.1, 1.05, 1.1, 1.05],
            data11, row_h=0.40, base_size=10.5, header_size=10.5)

add_text(s11, 0.35, 4.05, 9.30, 0.40,
         "† Étude Emile — accuracy binaire sur le test : sensibilité (sous-type malin) ou spécificité (sous-type bénin).",
         size=10, color=GREY)
add_text(s11, 0.35, 4.45, 9.30, 0.80, [
    ("Lecture croisée :", {"size": 11, "bold": True, "color": PINK_DARK, "space_after": 2}),
    ("Papillary et Tubular restent les sous-types difficiles dans les DEUX approches. En binaire, ViT-Small récupère bien mieux ces classes minoritaires que ConvNeXt-Tiny (spécificité Tubular 27 % vs 8 %).",
     {"size": 10.5, "color": GREY_D}),
])

# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 15 — Hyperparamètres Optuna (optimaux par modèle)
# ═══════════════════════════════════════════════════════════════════════════
s15 = prs.slides[15]
for sh in shapes(s15)[4:]:
    remove(sh)
set_subtitle(s15, "Hyperparamètres optimaux par modèle (Optuna · TPE) — équipe : 50 trials · Emile : 30 trials/modèle")

eqh = {"fill": PINK_DARK, "color": WHITE, "bold": True}
data15 = [
    ["Hyperparamètre", ("ViT + WRS  (équipe)", eqh), ("ViT-Small  (Emile)", eqh),
     ("ConvNeXt-T  (Emile)", eqh)],
    ["Learning rate", "3.2e-5", "2.4e-4", "4.8e-4"],
    ["Batch size", "32", "16", "8"],
    ["Dropout", "0.22", "0.39", "0.23"],
    ["Weight decay", "4.1e-4", "1.1e-4", "4.1e-4"],
    ["Régularisation spé.", "—", "Layer decay 0.88", "Drop path 0.23"],
    ["Stratégie de dégel", "Couches finales", "Dégel total", "Dégel total"],
]
build_table(s15, 0.35, 1.45, 9.30, [2.70, 2.20, 2.20, 2.20],
            data15, row_h=0.45, base_size=12, header_size=11.5)
add_text(s15, 0.35, 4.85, 9.30, 0.45,
         "Objectif optimisé : F1 macro · Optimizer AdamW · Réentraînement final 20 epochs pour les trois modèles.",
         size=10.5, color=GREY)

# ── Titre : ajout ConvNeXt dans la ligne techno ─────────────────────────────
for sh in shapes(prs.slides[0]):
    if sh.has_text_frame:
        for p in sh.text_frame.paragraphs:
            for r in p.runs:
                if "ResNet-50" in r.text and "Optuna" in r.text and "ConvNeXt" not in r.text:
                    r.text = r.text.replace("· Optuna", "· ConvNeXt · Optuna")

prs.save(SRC)
print("OK — fusion appliquée aux slides 9, 10, 11, 15. Total:", len(prs.slides._sldIdLst))
