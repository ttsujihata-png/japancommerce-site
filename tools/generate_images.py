#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LIVER COMPASS by CAP — オリジナルイラスト生成スクリプト
「かっこいい × 可愛い」テイストの共通デザインシステムに沿って、
記事ヒーロー画像・トップページ画像を全てSVGで自動生成する。
picsum.photos(ストックフォト)からの完全置き換え用。
"""
import hashlib
import os
import math

BASE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(BASE, "assets", "images")
os.makedirs(OUT_DIR, exist_ok=True)

# ---------- カラーテーマ(カテゴリ別) ----------
THEMES = {
    "agency-selection": {"bg1": "#14213D", "bg2": "#4A3F8C", "bg3": "#7C6CF2", "accent": "#FF5A7A", "accent2": "#40C9C6", "label": "AGENCY GUIDE"},
    "beginner-income":  {"bg1": "#B23A5C", "bg2": "#FF5A7A", "bg3": "#F4A340", "accent": "#7C6CF2", "accent2": "#FFFFFF", "label": "START GUIDE"},
    "app-purpose":      {"bg1": "#0E5C63", "bg2": "#40C9C6", "bg3": "#7C6CF2", "accent": "#FF5A7A", "accent2": "#F4A340", "label": "APP GUIDE"},
    "home":             {"bg1": "#14213D", "bg2": "#7C6CF2", "bg3": "#FF5A7A", "accent": "#40C9C6", "accent2": "#F4A340", "label": "LIVER COMPASS"},
}

SKIN = "#FFDDBB"
HAIR_OPTIONS = ["#241B2F", "#3A2B22", "#5B3A29", "#2E2540"]
OUTFIT_ACCENTS = ["#FF5A7A", "#7C6CF2", "#40C9C6", "#F4A340"]


def h(seed, salt=""):
    return int(hashlib.md5((seed + "::" + salt).encode()).hexdigest(), 16)


def rnd(seed, salt, lo, hi):
    r = (h(seed, salt) % 100000) / 100000.0
    return lo + r * (hi - lo)


def pick(seed, salt, options):
    return options[h(seed, salt) % len(options)]


def sparkle(x, y, size, color, opacity=0.9):
    s = size
    return f'''<g transform="translate({x},{y})" opacity="{opacity}">
      <path d="M0 {-s} C {s*0.15} {-s*0.15}, {s*0.15} {-s*0.15}, {s} 0 C {s*0.15} {s*0.15}, {s*0.15} {s*0.15}, 0 {s} C {-s*0.15} {s*0.15}, {-s*0.15} {s*0.15}, {-s} 0 C {-s*0.15} {-s*0.15}, {-s*0.15} {-s*0.15}, 0 {-s} Z" fill="{color}"/>
    </g>'''


def heart(x, y, size, color, opacity=0.9, rot=0):
    s = size
    return f'''<g transform="translate({x},{y}) rotate({rot}) scale({s/24})" opacity="{opacity}">
      <path d="M12 21s-7.5-4.6-10.2-9.1C.3 9.1 1.3 5.2 5 4.2c2.2-.6 4.2.4 5.8 2.4l1.2 1.5 1.2-1.5c1.6-2 3.6-3 5.8-2.4 3.7 1 4.7 4.9 3.2 7.7C19.5 16.4 12 21 12 21z" fill="{color}"/>
    </g>'''


def dotgrid(seed, w, h_, color, opacity=0.12):
    dots = []
    step = 34
    cols = int(w / step)
    rows = int(h_ / step)
    for r in range(rows):
        for c in range(cols):
            if (r + c) % 2 == 0:
                continue
            dots.append(f'<circle cx="{c*step+18}" cy="{r*step+18}" r="1.6" fill="{color}"/>')
    return f'<g opacity="{opacity}">{"".join(dots)}</g>'


def blob(cx, cy, rx, ry, color, opacity, rot=0):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{color}" opacity="{opacity}" transform="rotate({rot} {cx} {cy})"/>'


def live_badge(x, y, scale=1.0):
    return f'''<g transform="translate({x},{y}) scale({scale})">
      <rect x="0" y="0" width="74" height="30" rx="15" fill="#FF5A7A"/>
      <circle cx="16" cy="15" r="5" fill="#fff"><animate attributeName="opacity" values="1;.35;1" dur="1.6s" repeatCount="indefinite"/></circle>
      <text x="30" y="20" font-family="Manrope,Arial,sans-serif" font-weight="800" font-size="14" fill="#fff">LIVE</text>
    </g>'''


def chat_bubble(x, y, w_, h_, color, text, rot=0):
    return f'''<g transform="translate({x},{y}) rotate({rot})">
      <rect x="0" y="0" width="{w_}" height="{h_}" rx="{h_/2}" fill="{color}"/>
      <path d="M{w_*0.22} {h_} L{w_*0.12} {h_+10} L{w_*0.34} {h_} Z" fill="{color}"/>
      <text x="{w_/2}" y="{h_/2+5}" text-anchor="middle" font-family="Manrope,Arial,sans-serif" font-weight="700" font-size="{h_*0.42}" fill="#ffffff">{text}</text>
    </g>'''


def character(seed, theme, cx, cy, scale=1.0, pose="mic"):
    """かわいい系フラットイラストのキャラクター(チビ体型)。pose: mic / phone / wave / laptop / heart"""
    hair = pick(seed, "hair", HAIR_OPTIONS)
    outfit = theme["accent"] if h(seed, "outfit") % 2 == 0 else theme["bg3"]
    blush = "#FF9EB0"
    g = [f'<g transform="translate({cx},{cy}) scale({scale})">']

    # 影
    g.append(f'<ellipse cx="0" cy="168" rx="86" ry="14" fill="#14213D" opacity="0.12"/>')

    # 体(パーカー風)
    g.append(f'<path d="M-58 150 C-64 90 -50 40 0 40 C50 40 64 90 58 150 Z" fill="{outfit}"/>')
    g.append(f'<path d="M-58 150 C-64 90 -50 40 0 40 C50 40 64 90 58 150 Z" fill="#000" opacity="0.06"/>')
    # 襟・アクセントライン
    g.append(f'<path d="M-20 42 Q0 62 20 42" stroke="#fff" stroke-width="4" fill="none" opacity="0.55"/>')

    # 腕(ポーズ別)
    if pose == "phone":
        g.append(f'<path d="M-56 95 Q-92 100 -90 60" stroke="{outfit}" stroke-width="22" fill="none" stroke-linecap="round"/>')
        g.append(f'<rect x="-108" y="30" width="40" height="62" rx="8" fill="#1B2340"/>')
        g.append(f'<rect x="-103" y="36" width="30" height="46" rx="3" fill="{theme["bg3"]}"/>')
        heart_x, heart_y = -95, 20
        g.append(heart(heart_x, heart_y, 16, theme["accent"]))
        g.append(f'<path d="M54 95 Q88 78 64 40" stroke="{outfit}" stroke-width="22" fill="none" stroke-linecap="round"/>')
    elif pose == "mic":
        g.append(f'<path d="M-56 95 Q-86 70 -62 32" stroke="{outfit}" stroke-width="22" fill="none" stroke-linecap="round"/>')
        g.append(f'<circle cx="-64" cy="24" r="15" fill="#E8EAF2"/>')
        g.append(f'<rect x="-70" y="24" width="12" height="30" rx="6" fill="#C7CBDA"/>')
        g.append(f'<path d="M54 95 Q86 92 78 58" stroke="{outfit}" stroke-width="22" fill="none" stroke-linecap="round"/>')
    elif pose == "wave":
        g.append(f'<path d="M-56 95 Q-90 60 -50 20" stroke="{outfit}" stroke-width="22" fill="none" stroke-linecap="round"/>')
        g.append(f'<circle cx="-50" cy="14" r="17" fill="{SKIN}"/>')
        g.append(f'<path d="M54 95 Q86 92 78 58" stroke="{outfit}" stroke-width="22" fill="none" stroke-linecap="round"/>')
    elif pose == "laptop":
        g.append(f'<rect x="-52" y="86" width="104" height="10" rx="4" fill="#1B2340"/>')
        g.append(f'<rect x="-46" y="46" width="92" height="42" rx="4" fill="#2A3358"/>')
        g.append(f'<rect x="-40" y="52" width="80" height="30" rx="2" fill="{theme["bg3"]}"/>')
        g.append(f'<path d="M-56 95 Q-70 92 -60 78" stroke="{outfit}" stroke-width="20" fill="none" stroke-linecap="round"/>')
        g.append(f'<path d="M54 95 Q70 92 60 78" stroke="{outfit}" stroke-width="20" fill="none" stroke-linecap="round"/>')
    else:  # heart
        g.append(f'<path d="M-56 95 Q-40 60 -12 58" stroke="{outfit}" stroke-width="22" fill="none" stroke-linecap="round"/>')
        g.append(f'<path d="M54 95 Q40 60 12 58" stroke="{outfit}" stroke-width="22" fill="none" stroke-linecap="round"/>')
        g.append(heart(0, 50, 30, theme["accent"]))

    # 首
    g.append(f'<rect x="-14" y="26" width="28" height="20" fill="{SKIN}"/>')

    # 顔
    g.append(f'<circle cx="0" cy="-10" r="62" fill="{SKIN}"/>')
    # 頬
    g.append(f'<ellipse cx="-34" cy="8" rx="11" ry="7" fill="{blush}" opacity="0.65"/>')
    g.append(f'<ellipse cx="34" cy="8" rx="11" ry="7" fill="{blush}" opacity="0.65"/>')
    # 目
    eye_y = -12
    g.append(f'<circle cx="-22" cy="{eye_y}" r="6.4" fill="#241B2F"/>')
    g.append(f'<circle cx="22" cy="{eye_y}" r="6.4" fill="#241B2F"/>')
    g.append(f'<circle cx="-24.4" cy="{eye_y-2.4}" r="2.1" fill="#fff"/>')
    g.append(f'<circle cx="19.6" cy="{eye_y-2.4}" r="2.1" fill="#fff"/>')
    # 口
    g.append(f'<path d="M-10 14 Q0 22 10 14" stroke="#241B2F" stroke-width="3.4" fill="none" stroke-linecap="round"/>')
    # 前髪
    g.append(f'<path d="M-62 -18 C-66 -70 -34 -96 0 -96 C34 -96 66 -70 62 -18 C58 -46 44 -60 30 -46 C22 -62 -22 -62 -30 -46 C-44 -60 -58 -46 -62 -18 Z" fill="{hair}"/>')
    # ヘアアクセ(耳のリボン/イヤホン風)
    g.append(f'<circle cx="-58" cy="-12" r="9" fill="{theme["accent"]}" opacity="0.9"/>')
    g.append(f'<circle cx="58" cy="-12" r="9" fill="{theme["accent"]}" opacity="0.9"/>')

    g.append('</g>')
    return "".join(g)


def phone_mock(x, y, w_, h_, theme, seed):
    """スマホ配信画面のモックアップ(グラスモーフィズム)"""
    return f'''<g transform="translate({x},{y})">
      <rect x="0" y="0" width="{w_}" height="{h_}" rx="34" fill="#0D1226" opacity="0.92"/>
      <rect x="8" y="8" width="{w_-16}" height="{h_-16}" rx="28" fill="url(#phoneScreen{seed})"/>
      <rect x="8" y="8" width="{w_-16}" height="{h_-16}" rx="28" fill="#fff" opacity="0.04"/>
      {live_badge(24, 26, 0.85)}
      <circle cx="{w_-42}" cy="34" r="14" fill="#fff" opacity="0.25"/>
      <path d="M{w_-48} 34 l5 4 l8 -9" stroke="#fff" stroke-width="2.4" fill="none" stroke-linecap="round" stroke-linejoin="round" opacity="0.9"/>
      {heart(w_-30, h_-40, 20, theme["accent"], 0.95)}
      {heart(w_-60, h_-70, 14, "#fff", 0.7)}
      <rect x="20" y="{h_-46}" width="{w_*0.55}" height="14" rx="7" fill="#fff" opacity="0.22"/>
    </g>'''


def defs_gradients(seed, theme, w, h_):
    return f'''<defs>
      <linearGradient id="bgGrad{seed}" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="{theme['bg1']}"/>
        <stop offset="55%" stop-color="{theme['bg2']}"/>
        <stop offset="100%" stop-color="{theme['bg3']}"/>
      </linearGradient>
      <linearGradient id="phoneScreen{seed}" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="{theme['bg2']}"/>
        <stop offset="100%" stop-color="{theme['bg1']}"/>
      </linearGradient>
      <radialGradient id="glow{seed}" cx="50%" cy="30%" r="70%">
        <stop offset="0%" stop-color="#ffffff" stop-opacity="0.16"/>
        <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
      </radialGradient>
    </defs>'''


CHAR_TOP = -96   # キャラクターSVGローカル座標の頭頂部
CHAR_BOTTOM = 182  # 影を含む最下部


def fit_character(w, h_, height_ratio, cx_ratio=0.68, bottom_margin_ratio=0.03):
    """フレームに対してキャラクターがちょうど収まるscale/位置を計算する"""
    target_h = h_ * height_ratio
    scale = target_h / (CHAR_BOTTOM - CHAR_TOP)
    cy = h_ * (1 - bottom_margin_ratio) - CHAR_BOTTOM * scale
    cx = w * cx_ratio
    return cx, cy, scale


def article_hero(slug, category, w=1200, h_=675):
    theme = THEMES[category]
    pose = pick(slug, "pose", ["mic", "phone", "wave", "laptop", "heart"])
    cx_ratio = rnd(slug, "cx", 0.64, 0.72)
    height_ratio = rnd(slug, "hr", 0.60, 0.68)
    char_x, char_y, char_scale = fit_character(w, h_, height_ratio, cx_ratio)
    rot1 = rnd(slug, "rot1", -8, 8)

    svg = [f'<svg viewBox="0 0 {w} {h_}" xmlns="http://www.w3.org/2000/svg">']
    svg.append(defs_gradients(slug, theme, w, h_))
    svg.append(f'<rect width="{w}" height="{h_}" fill="url(#bgGrad{slug})"/>')
    svg.append(f'<rect width="{w}" height="{h_}" fill="url(#glow{slug})"/>')
    # blobs
    svg.append(blob(w*0.14, h_*0.22, 200, 150, "#ffffff", 0.06, rot1))
    svg.append(blob(w*0.92, h_*0.85, 260, 200, "#000000", 0.10, -rot1))
    svg.append(blob(w*0.85, h_*0.12, 150, 120, theme["accent"], 0.16, rot1*2))
    svg.append(dotgrid(slug, w, h_, "#ffffff", 0.10))
    # decorative sparkles/hearts scattered (seeded)
    for i in range(5):
        sx = rnd(slug, f"sx{i}", 40, w-40)
        sy = rnd(slug, f"sy{i}", 30, h_*0.55)
        ss = rnd(slug, f"ss{i}", 8, 20)
        col = pick(slug, f"scol{i}", ["#ffffff", theme["accent2"], theme["accent"]])
        if i % 2 == 0:
            svg.append(sparkle(sx, sy, ss, col, rnd(slug, f"so{i}", 0.35, 0.85)))
        else:
            svg.append(heart(sx, sy, ss, col, rnd(slug, f"ho{i}", 0.35, 0.75)))
    # phone mock top-left area
    pw, ph = 190, 240
    svg.append(phone_mock(w*0.08, h_*0.14, pw, ph, theme, slug))
    # chat bubbles
    svg.append(chat_bubble(w*0.30, h_*0.10, 96, 34, "#ffffff", "♪", rnd(slug,"bub1",-6,10)))
    svg.append(chat_bubble(w*0.40, h_*0.30, 70, 28, theme["accent2"], "♡", rnd(slug,"bub2",-10,6)))
    # character
    svg.append(character(slug, theme, char_x, char_y, char_scale, pose))
    # corner label
    svg.append(f'<text x="{w-28}" y="{h_-26}" text-anchor="end" font-family="Manrope,Arial,sans-serif" font-weight="800" font-size="15" letter-spacing="2" fill="#ffffff" opacity="0.55">{theme["label"]}</text>')
    svg.append(f'<text x="28" y="{h_-26}" font-family="Manrope,Arial,sans-serif" font-weight="800" font-size="15" letter-spacing="1" fill="#ffffff" opacity="0.5">LIVER COMPASS</text>')
    svg.append('</svg>')
    return "".join(svg)


def home_hero(w=800, h_=1000):
    theme = THEMES["home"]
    slug = "hero-liver"
    svg = [f'<svg viewBox="0 0 {w} {h_}" xmlns="http://www.w3.org/2000/svg">']
    svg.append(defs_gradients(slug, theme, w, h_))
    svg.append(f'<rect width="{w}" height="{h_}" fill="url(#bgGrad{slug})"/>')
    svg.append(f'<rect width="{w}" height="{h_}" fill="url(#glow{slug})"/>')
    svg.append(blob(w*0.15, h_*0.18, 220, 180, "#ffffff", 0.08, 8))
    svg.append(blob(w*0.9, h_*0.75, 260, 300, "#000000", 0.14, -10))
    svg.append(blob(w*0.82, h_*0.15, 170, 140, theme["accent"], 0.20, 12))
    svg.append(dotgrid(slug, w, h_, "#ffffff", 0.09))
    for i in range(7):
        sx = rnd(slug, f"sx{i}", 40, w-40)
        sy = rnd(slug, f"sy{i}", 30, h_*0.5)
        ss = rnd(slug, f"ss{i}", 10, 24)
        col = pick(slug, f"scol{i}", ["#ffffff", theme["accent2"], theme["accent"]])
        if i % 2 == 0:
            svg.append(sparkle(sx, sy, ss, col, rnd(slug, f"so{i}", 0.4, 0.9)))
        else:
            svg.append(heart(sx, sy, ss, col, rnd(slug, f"ho{i}", 0.4, 0.8)))
    svg.append(phone_mock(w*0.10, h_*0.10, 210, 270, theme, slug))
    svg.append(chat_bubble(w*0.52, h_*0.08, 110, 38, "#ffffff", "♪", 6))
    svg.append(chat_bubble(w*0.66, h_*0.22, 80, 30, theme["accent2"], "♡", -8))
    hx, hy, hs = fit_character(w, h_, 0.42, 0.56, 0.04)
    svg.append(character(slug, theme, hx, hy, hs, "phone"))
    svg.append(f'<text x="{w-30}" y="{h_-32}" text-anchor="end" font-family="Manrope,Arial,sans-serif" font-weight="800" font-size="16" letter-spacing="2" fill="#ffffff" opacity="0.55">LIVER COMPASS</text>')
    svg.append('</svg>')
    return "".join(svg)


def cap_staff_avatar(w=160, h_=160):
    theme = THEMES["home"]
    slug = "cap-staff"
    svg = [f'<svg viewBox="0 0 {w} {h_}" xmlns="http://www.w3.org/2000/svg">']
    svg.append(defs_gradients(slug, theme, w, h_))
    svg.append(f'<circle cx="{w/2}" cy="{h_/2}" r="{w/2}" fill="url(#bgGrad{slug})"/>')
    cx, cy, sc = fit_character(w, h_, 0.66, 0.5, -0.08)
    svg.append(character(slug, theme, cx, cy, sc, "wave"))
    svg.append('</svg>')
    return "".join(svg)


def cap_office(w=700, h_=440):
    theme = THEMES["agency-selection"]
    slug = "cap-office"
    svg = [f'<svg viewBox="0 0 {w} {h_}" xmlns="http://www.w3.org/2000/svg">']
    svg.append(defs_gradients(slug, theme, w, h_))
    svg.append(f'<rect width="{w}" height="{h_}" rx="28" fill="url(#bgGrad{slug})"/>')
    svg.append(f'<rect width="{w}" height="{h_}" rx="28" fill="url(#glow{slug})"/>')
    svg.append(dotgrid(slug, w, h_, "#ffffff", 0.08))
    svg.append(blob(w*0.9, h_*0.85, 180, 140, theme["accent"], 0.16, 10))
    # table
    svg.append(f'<rect x="{w*0.18}" y="{h_*0.68}" width="{w*0.64}" height="18" rx="9" fill="#ffffff" opacity="0.18"/>')
    svg.append(character("cap-office-a", theme, w*0.34, h_*0.66, 1.0, "mic"))
    svg.append(character("cap-office-b", THEMES["app-purpose"], w*0.68, h_*0.66, 0.95, "laptop"))
    svg.append(chat_bubble(w*0.30, h_*0.14, 96, 34, "#ffffff", "♪", -6))
    svg.append(chat_bubble(w*0.58, h_*0.20, 70, 28, theme["accent2"], "♡", 8))
    svg.append(f'<text x="{w-24}" y="{h_-20}" text-anchor="end" font-family="Manrope,Arial,sans-serif" font-weight="800" font-size="14" letter-spacing="2" fill="#ffffff" opacity="0.5">CAP CONSULTATION</text>')
    svg.append('</svg>')
    return "".join(svg)


def story_avatar(w=200, h_=200):
    theme = THEMES["beginner-income"]
    slug = "story1"
    svg = [f'<svg viewBox="0 0 {w} {h_}" xmlns="http://www.w3.org/2000/svg">']
    svg.append(defs_gradients(slug, theme, w, h_))
    svg.append(f'<circle cx="{w/2}" cy="{h_/2}" r="{w/2}" fill="url(#bgGrad{slug})"/>')
    cx, cy, sc = fit_character(w, h_, 0.66, 0.5, -0.08)
    svg.append(character(slug, theme, cx, cy, sc, "heart"))
    svg.append('</svg>')
    return "".join(svg)


PURPOSE_SPECS = {
    "purpose-beginner": ("beginner-income", "wave"),
    "purpose-sidejob":  ("beginner-income", "laptop"),
    "purpose-singer":   ("app-purpose", "mic"),
    "purpose-vliver":   ("app-purpose", "phone"),
    "purpose-transfer": ("agency-selection", "heart"),
}


def purpose_card(slug, category, pose, w=600, h_=338):
    theme = THEMES[category]
    svg = [f'<svg viewBox="0 0 {w} {h_}" xmlns="http://www.w3.org/2000/svg">']
    svg.append(defs_gradients(slug, theme, w, h_))
    svg.append(f'<rect width="{w}" height="{h_}" fill="url(#bgGrad{slug})"/>')
    svg.append(f'<rect width="{w}" height="{h_}" fill="url(#glow{slug})"/>')
    svg.append(dotgrid(slug, w, h_, "#ffffff", 0.10))
    svg.append(blob(w*0.88, h_*0.18, 130, 100, theme["accent"], 0.18, 10))
    svg.append(blob(w*0.08, h_*0.9, 140, 100, "#000000", 0.12, -8))
    for i in range(3):
        sx = rnd(slug, f"sx{i}", 30, w-30)
        sy = rnd(slug, f"sy{i}", 20, h_*0.4)
        ss = rnd(slug, f"ss{i}", 8, 16)
        col = pick(slug, f"scol{i}", ["#ffffff", theme["accent2"]])
        svg.append(sparkle(sx, sy, ss, col, 0.6))
    cx, cy, sc = fit_character(w, h_, 0.66, 0.70, 0.03)
    svg.append(character(slug, theme, cx, cy, sc, pose))
    svg.append('</svg>')
    return "".join(svg)


def write(name, content):
    path = os.path.join(OUT_DIR, f"{name}.svg")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", path)


ARTICLES = {
    "liver-agency-merit-demerit": "agency-selection",
    "agency-how-to-choose-10": "agency-selection",
    "agency-review-check": "agency-selection",
    "suspicious-agency-signs": "agency-selection",
    "contract-checklist": "agency-selection",
    "kangenritsu-explained": "agency-selection",
    "norma-nashi-caution": "agency-selection",
    "free-liver-vs-agency": "agency-selection",
    "agency-transfer-method": "agency-selection",
    "scout-dm-check": "agency-selection",
    "manager-role": "agency-selection",
    "how-to-start-liver": "beginner-income",
    "live-streaming-equipment": "beginner-income",
    "first-stream-topics": "beginner-income",
    "side-job-liver-start": "beginner-income",
    "liver-income-structure": "beginner-income",
    "how-to-continue-streaming": "beginner-income",
    "protect-personal-info": "beginner-income",
    "dealing-with-troll-viewers": "beginner-income",
    "tax-basics-for-livers": "beginner-income",
    "minor-streaming-caution": "beginner-income",
    "tiktok-live-guide": "app-purpose",
    "pococha-guide": "app-purpose",
    "iriam-vliver-guide": "app-purpose",
    "reality-guide": "app-purpose",
    "faceless-streaming": "app-purpose",
    "singer-liver-path": "app-purpose",
    "mom-housewife-streaming": "app-purpose",
    "rural-liver-possibility": "app-purpose",
    "liver-30s-start": "app-purpose",
    "liver-to-influencer": "app-purpose",
}

def generate_one(slug, category):
    """毎日の記事自動生成タスクから呼び出す単発生成用。
    使い方: python3 generate_images.py --slug <slug> --category <agency-selection|beginner-income|app-purpose>
    -> outputs/assets/images/<slug>.svg を生成する。"""
    if category not in THEMES:
        raise SystemExit(f"unknown category: {category} (must be one of {list(THEMES)})")
    write(slug, article_hero(slug, category))


if __name__ == "__main__":
    import sys
    if "--slug" in sys.argv:
        slug = sys.argv[sys.argv.index("--slug") + 1]
        category = sys.argv[sys.argv.index("--category") + 1]
        generate_one(slug, category)
    else:
        for slug, cat in ARTICLES.items():
            write(slug, article_hero(slug, cat))
        write("hero-liver", home_hero())
        write("cap-staff", cap_staff_avatar())
        write("cap-office", cap_office())
        write("story1", story_avatar())
        for slug, (cat, pose) in PURPOSE_SPECS.items():
            write(slug, purpose_card(slug, cat, pose))
        print(f"Done. {len(ARTICLES) + 5 + len(PURPOSE_SPECS)} images generated.")
