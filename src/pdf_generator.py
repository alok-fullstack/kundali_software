"""
PDF Generator for Kundali Software

Generates professional PDF reports for:
1. Kundali (Birth Chart) Reports
2. Kundali Matching (Marriage Compatibility) Reports

Uses ReportLab for PDF generation with traditional Vedic astrology styling.
"""

import io
import os
import urllib.request
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, HRFlowable
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Circle
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics import renderPDF

# Import kundali modules
from .kundali import Kundali
from .config import PLANET_NAMES, Planet, BHAVA_NAMES, RASHIS
from .yogas import get_all_yogas, get_yoga_summary
from .dasha import DashaPeriod


# =============================================================================
# HINDI FONT SETUP - Noto Sans Devanagari
# =============================================================================

FONTS_DIR = Path(__file__).parent / "fonts"
HINDI_FONT_PATH = FONTS_DIR / "NotoSansDevanagari-Regular.ttf"
HINDI_FONT_BOLD_PATH = FONTS_DIR / "NotoSansDevanagari-Bold.ttf"

# Google Fonts URLs for Noto Sans Devanagari
FONT_URLS = {
    "regular": "https://github.com/google/fonts/raw/main/ofl/notosansdevanagari/NotoSansDevanagari-Regular.ttf",
    "bold": "https://github.com/google/fonts/raw/main/ofl/notosansdevanagari/NotoSansDevanagari-Bold.ttf"
}

HINDI_FONT_REGISTERED = False


def download_hindi_fonts():
    """Download Noto Sans Devanagari fonts if not present."""
    global HINDI_FONT_REGISTERED

    if HINDI_FONT_REGISTERED:
        return True

    # Create fonts directory
    FONTS_DIR.mkdir(exist_ok=True)

    try:
        # Download regular font
        if not HINDI_FONT_PATH.exists():
            print("Downloading Noto Sans Devanagari Regular font...")
            urllib.request.urlretrieve(FONT_URLS["regular"], HINDI_FONT_PATH)

        # Download bold font
        if not HINDI_FONT_BOLD_PATH.exists():
            print("Downloading Noto Sans Devanagari Bold font...")
            urllib.request.urlretrieve(FONT_URLS["bold"], HINDI_FONT_BOLD_PATH)

        return True
    except Exception as e:
        print(f"Warning: Could not download Hindi fonts: {e}")
        return False


def register_hindi_fonts():
    """Register Hindi fonts with ReportLab."""
    global HINDI_FONT_REGISTERED

    if HINDI_FONT_REGISTERED:
        return True

    # Try to download fonts first
    if not download_hindi_fonts():
        return False

    try:
        # Register fonts with ReportLab
        if HINDI_FONT_PATH.exists():
            pdfmetrics.registerFont(TTFont('NotoSansDevanagari', str(HINDI_FONT_PATH)))
            pdfmetrics.registerFont(TTFont('NotoSansDevanagari-Bold', str(HINDI_FONT_BOLD_PATH)))

            # Register font family
            pdfmetrics.registerFontFamily(
                'NotoSansDevanagari',
                normal='NotoSansDevanagari',
                bold='NotoSansDevanagari-Bold'
            )

            HINDI_FONT_REGISTERED = True
            print("Hindi fonts registered successfully!")
            return True
    except Exception as e:
        print(f"Warning: Could not register Hindi fonts: {e}")

    return False


# Register fonts on module load
register_hindi_fonts()


# =============================================================================
# COLOR THEME - Traditional Saffron/Orange Vedic Theme
# =============================================================================

class VedicColors:
    """Vedic astrology color palette."""
    SAFFRON = colors.HexColor('#FF6B00')
    SAFFRON_LIGHT = colors.HexColor('#FFA500')
    SAFFRON_DARK = colors.HexColor('#CC5500')
    GOLD = colors.HexColor('#FFD700')
    CREAM = colors.HexColor('#FFF8DC')
    MAROON = colors.HexColor('#800000')
    DEEP_RED = colors.HexColor('#8B0000')
    GREEN = colors.HexColor('#228B22')
    LIGHT_GREEN = colors.HexColor('#90EE90')
    BLUE = colors.HexColor('#1E90FF')
    LIGHT_BLUE = colors.HexColor('#ADD8E6')
    PURPLE = colors.HexColor('#800080')
    PINK = colors.HexColor('#FF69B4')
    LIGHT_PINK = colors.HexColor('#FFB6C1')
    GRAY = colors.HexColor('#666666')
    LIGHT_GRAY = colors.HexColor('#F5F5F5')
    WHITE = colors.white
    BLACK = colors.black


# =============================================================================
# HINDI TEXT MAPPINGS
# =============================================================================

RASHI_HINDI = {
    "Mesha": "मेष", "Vrishabha": "वृषभ", "Mithuna": "मिथुन", "Karka": "कर्क",
    "Simha": "सिंह", "Kanya": "कन्या", "Tula": "तुला", "Vrishchika": "वृश्चिक",
    "Dhanu": "धनु", "Makara": "मकर", "Kumbha": "कुंभ", "Meena": "मीन"
}

PLANET_HINDI = {
    "SUN": "सूर्य", "MOON": "चंद्र", "MARS": "मंगल", "MERCURY": "बुध",
    "JUPITER": "गुरु", "VENUS": "शुक्र", "SATURN": "शनि",
    "RAHU": "राहु", "KETU": "केतु"
}

PLANET_SYMBOLS = {
    "SUN": "Su", "MOON": "Mo", "MARS": "Ma", "MERCURY": "Me",
    "JUPITER": "Ju", "VENUS": "Ve", "SATURN": "Sa",
    "RAHU": "Ra", "KETU": "Ke"
}


# =============================================================================
# PDF STYLE SETUP
# =============================================================================

def get_hindi_font():
    """Get the Hindi font name (falls back to Helvetica if not available)."""
    return 'NotoSansDevanagari' if HINDI_FONT_REGISTERED else 'Helvetica'

def get_hindi_font_bold():
    """Get the Hindi bold font name (falls back to Helvetica-Bold if not available)."""
    return 'NotoSansDevanagari-Bold' if HINDI_FONT_REGISTERED else 'Helvetica-Bold'

def get_styles():
    """Get custom paragraph styles for Vedic PDF reports."""
    styles = getSampleStyleSheet()
    hindi_font = get_hindi_font()
    hindi_font_bold = get_hindi_font_bold()

    # Title style - Om symbol header
    styles.add(ParagraphStyle(
        name='VedicTitle',
        fontSize=24,
        textColor=VedicColors.SAFFRON_DARK,
        alignment=TA_CENTER,
        spaceAfter=6,
        fontName=hindi_font_bold
    ))

    # Main heading
    styles.add(ParagraphStyle(
        name='VedicHeading',
        fontSize=16,
        textColor=VedicColors.SAFFRON_DARK,
        alignment=TA_CENTER,
        spaceAfter=12,
        spaceBefore=12,
        fontName=hindi_font_bold
    ))

    # Section heading
    styles.add(ParagraphStyle(
        name='SectionHeading',
        fontSize=14,
        textColor=VedicColors.MAROON,
        alignment=TA_LEFT,
        spaceAfter=8,
        spaceBefore=16,
        fontName=hindi_font_bold
    ))

    # Subsection heading
    styles.add(ParagraphStyle(
        name='SubsectionHeading',
        fontSize=12,
        textColor=VedicColors.SAFFRON,
        alignment=TA_LEFT,
        spaceAfter=6,
        spaceBefore=10,
        fontName=hindi_font_bold
    ))

    # Normal text
    styles.add(ParagraphStyle(
        name='VedicNormal',
        fontSize=10,
        textColor=VedicColors.BLACK,
        alignment=TA_JUSTIFY,
        spaceAfter=4,
        fontName=hindi_font
    ))

    # Hindi text (bilingual)
    styles.add(ParagraphStyle(
        name='HindiText',
        fontSize=10,
        textColor=VedicColors.GRAY,
        alignment=TA_LEFT,
        spaceAfter=4,
        fontName=hindi_font
    ))

    # Footer style
    styles.add(ParagraphStyle(
        name='Footer',
        fontSize=8,
        textColor=VedicColors.GRAY,
        alignment=TA_CENTER,
        fontName=hindi_font
    ))

    # Score highlight
    styles.add(ParagraphStyle(
        name='ScoreHighlight',
        fontSize=18,
        textColor=VedicColors.GREEN,
        alignment=TA_CENTER,
        fontName=hindi_font_bold
    ))

    return styles


# =============================================================================
# KUNDALI CHART DRAWING (North Indian Style)
# =============================================================================

def draw_kundali_chart(planets_in_houses: Dict[int, List[str]],
                       lagna_num: int,
                       planets: Dict[str, Dict],
                       width: float = 300,
                       height: float = 300) -> Drawing:
    """
    Draw North Indian style Kundali chart.

    Args:
        planets_in_houses: Dictionary mapping house numbers to planet lists
        lagna_num: Lagna rashi number (0-11)
        planets: Planet data dictionary for retrograde info
        width: Drawing width
        height: Drawing height

    Returns:
        ReportLab Drawing object
    """
    d = Drawing(width, height)

    # Chart dimensions
    margin = 10
    chart_size = min(width, height) - 2 * margin
    x_start = (width - chart_size) / 2
    y_start = (height - chart_size) / 2

    # Cell size
    cell = chart_size / 4

    # Background
    d.add(Rect(x_start, y_start, chart_size, chart_size,
               fillColor=VedicColors.CREAM, strokeColor=VedicColors.SAFFRON_DARK,
               strokeWidth=2))

    # Draw the North Indian chart grid
    # North Indian chart positions (house 1 at top center)
    # Layout:
    # [12] [1]  [2]  [3]
    # [11]          [4]
    # [10]          [5]
    # [9]  [8]  [7]  [6]

    house_positions = {
        12: (0, 3), 1: (1, 3), 2: (2, 3), 3: (3, 3),
        11: (0, 2), 4: (3, 2),
        10: (0, 1), 5: (3, 1),
        9: (0, 0), 8: (1, 0), 7: (2, 0), 6: (3, 0)
    }

    # Draw diagonal lines for corner houses
    # Top-left diagonal
    d.add(Line(x_start, y_start + 3*cell, x_start + cell, y_start + 2*cell,
               strokeColor=VedicColors.SAFFRON_DARK, strokeWidth=1))
    d.add(Line(x_start + cell, y_start + 3*cell, x_start, y_start + 2*cell,
               strokeColor=VedicColors.SAFFRON_DARK, strokeWidth=1))

    # Top-right diagonal
    d.add(Line(x_start + 3*cell, y_start + 3*cell, x_start + 4*cell, y_start + 2*cell,
               strokeColor=VedicColors.SAFFRON_DARK, strokeWidth=1))
    d.add(Line(x_start + 3*cell, y_start + 2*cell, x_start + 4*cell, y_start + 3*cell,
               strokeColor=VedicColors.SAFFRON_DARK, strokeWidth=1))

    # Bottom-left diagonal
    d.add(Line(x_start, y_start + cell, x_start + cell, y_start,
               strokeColor=VedicColors.SAFFRON_DARK, strokeWidth=1))
    d.add(Line(x_start, y_start, x_start + cell, y_start + cell,
               strokeColor=VedicColors.SAFFRON_DARK, strokeWidth=1))

    # Bottom-right diagonal
    d.add(Line(x_start + 3*cell, y_start + cell, x_start + 4*cell, y_start,
               strokeColor=VedicColors.SAFFRON_DARK, strokeWidth=1))
    d.add(Line(x_start + 3*cell, y_start, x_start + 4*cell, y_start + cell,
               strokeColor=VedicColors.SAFFRON_DARK, strokeWidth=1))

    # Draw outer border lines
    d.add(Line(x_start + cell, y_start, x_start + cell, y_start + chart_size,
               strokeColor=VedicColors.SAFFRON_DARK, strokeWidth=1))
    d.add(Line(x_start + 3*cell, y_start, x_start + 3*cell, y_start + chart_size,
               strokeColor=VedicColors.SAFFRON_DARK, strokeWidth=1))
    d.add(Line(x_start, y_start + cell, x_start + chart_size, y_start + cell,
               strokeColor=VedicColors.SAFFRON_DARK, strokeWidth=1))
    d.add(Line(x_start, y_start + 3*cell, x_start + chart_size, y_start + 3*cell,
               strokeColor=VedicColors.SAFFRON_DARK, strokeWidth=1))

    # Draw center cross
    d.add(Line(x_start + cell, y_start + cell, x_start + 3*cell, y_start + 3*cell,
               strokeColor=VedicColors.SAFFRON_DARK, strokeWidth=1))
    d.add(Line(x_start + cell, y_start + 3*cell, x_start + 3*cell, y_start + cell,
               strokeColor=VedicColors.SAFFRON_DARK, strokeWidth=1))

    # Highlight Lagna house
    lagna_house = 1
    if lagna_house in house_positions:
        col, row = house_positions[lagna_house]
        # Add subtle highlight for Lagna
        d.add(Rect(x_start + col*cell + 2, y_start + row*cell + 2,
                   cell - 4, cell - 4,
                   fillColor=VedicColors.GOLD, strokeColor=None,
                   fillOpacity=0.3))

    # Add planets to houses
    for house_num, planet_list in planets_in_houses.items():
        if house_num not in house_positions:
            continue

        col, row = house_positions[house_num]

        # Calculate text position (center of cell)
        text_x = x_start + col * cell + cell / 2
        text_y = y_start + row * cell + cell / 2

        # Build planet string
        planet_strs = []
        for p in planet_list:
            symbol = PLANET_SYMBOLS.get(p, p[:2])
            is_retro = planets.get(p, {}).get('is_retrograde', False)
            planet_str = f"{symbol}{'(R)' if is_retro else ''}"
            planet_strs.append(planet_str)

        if planet_strs:
            text = ' '.join(planet_strs)
            d.add(String(text_x, text_y, text,
                        fontSize=8, textAnchor='middle',
                        fillColor=VedicColors.MAROON))

        # Add house number
        d.add(String(x_start + col * cell + 5, y_start + (row + 1) * cell - 10,
                    str(house_num),
                    fontSize=7, fillColor=VedicColors.GRAY))

    return d


# =============================================================================
# COMPATIBILITY GAUGE DRAWING
# =============================================================================

def draw_compatibility_gauge(score: float, max_score: float = 36,
                            width: float = 200, height: float = 120) -> Drawing:
    """
    Draw a semi-circular gauge for compatibility score.

    Args:
        score: Obtained score
        max_score: Maximum possible score
        width: Drawing width
        height: Drawing height

    Returns:
        ReportLab Drawing object
    """
    d = Drawing(width, height)

    percentage = (score / max_score) * 100

    # Determine color based on percentage
    if percentage >= 70:
        color = VedicColors.GREEN
        label = "Excellent"
    elif percentage >= 50:
        color = VedicColors.SAFFRON
        label = "Good"
    elif percentage >= 36:
        color = colors.HexColor('#FFA500')  # Orange
        label = "Average"
    else:
        color = VedicColors.DEEP_RED
        label = "Below Average"

    # Draw background arc (gray)
    center_x = width / 2
    center_y = 30
    radius = 60

    # Background semicircle
    d.add(Rect(0, 0, width, height, fillColor=VedicColors.WHITE, strokeColor=None))

    # Score display
    d.add(String(center_x, height - 20, f"{score:.1f} / {max_score}",
                fontSize=16, textAnchor='middle', fontName='Helvetica-Bold',
                fillColor=color))

    d.add(String(center_x, height - 38, f"({percentage:.1f}%)",
                fontSize=12, textAnchor='middle',
                fillColor=VedicColors.GRAY))

    d.add(String(center_x, height - 55, label,
                fontSize=11, textAnchor='middle', fontName='Helvetica-Bold',
                fillColor=color))

    # Draw meter segments
    import math
    num_segments = 36
    segment_angle = math.pi / num_segments

    for i in range(num_segments):
        angle = math.pi - i * segment_angle
        x1 = center_x + (radius - 15) * math.cos(angle)
        y1 = center_y + (radius - 15) * math.sin(angle)
        x2 = center_x + radius * math.cos(angle)
        y2 = center_y + radius * math.sin(angle)

        if i < score:
            seg_color = color
        else:
            seg_color = VedicColors.LIGHT_GRAY

        d.add(Line(x1, y1, x2, y2, strokeColor=seg_color, strokeWidth=4))

    return d


# =============================================================================
# KUNDALI PDF GENERATOR
# =============================================================================

class KundaliPDFGenerator:
    """Generate professional Kundali PDF reports."""

    def __init__(self, kundali: Kundali):
        self.kundali = kundali
        self.styles = get_styles()
        self.elements = []

    def _add_header(self):
        """Add report header with Om symbol and title."""
        # Om symbol (using Unicode)
        self.elements.append(Paragraph(
            '<font size="36" color="#FF6B00">&#x0950;</font>',
            self.styles['VedicTitle']
        ))

        self.elements.append(Paragraph(
            "JANAM KUNDALI / जन्म कुंडली",
            self.styles['VedicTitle']
        ))

        self.elements.append(Paragraph(
            f"<b>{self.kundali.birth_data.name}</b>",
            self.styles['VedicHeading']
        ))

        # Horizontal line
        self.elements.append(HRFlowable(
            width="100%", thickness=2, color=VedicColors.SAFFRON,
            spaceBefore=10, spaceAfter=10
        ))

    def _add_birth_details(self):
        """Add birth details section."""
        self.elements.append(Paragraph(
            "Birth Details / जन्म विवरण",
            self.styles['SectionHeading']
        ))

        birth = self.kundali.birth_data
        lagna = self.kundali.lagna
        planets = self.kundali.planets
        current_dasha = self.kundali.get_current_dasha()

        # Birth details table
        data = [
            ["Name / नाम", birth.name],
            ["Date of Birth / जन्म तिथि", birth.date.strftime('%d-%m-%Y')],
            ["Time of Birth / जन्म समय", birth.date.strftime('%I:%M %p')],
            ["Place of Birth / जन्म स्थान", birth.city],
            ["Coordinates / निर्देशांक", f"{abs(birth.latitude):.4f}°{'N' if birth.latitude >= 0 else 'S'}, {abs(birth.longitude):.4f}°{'E' if birth.longitude >= 0 else 'W'}"],
            ["Lagna / लग्न", f"{RASHI_HINDI.get(lagna['rashi'], lagna['rashi'])} ({lagna['rashi_english']})"],
            ["Moon Sign / चंद्र राशि", f"{RASHI_HINDI.get(planets['MOON']['rashi'], planets['MOON']['rashi'])}"],
            ["Nakshatra / नक्षत्र", f"{planets['MOON']['nakshatra']} Pada {planets['MOON']['pada']}"],
            ["Current Dasha / वर्तमान दशा", current_dasha.get('full_dasha', 'N/A')],
        ]

        table = Table(data, colWidths=[2.5*inch, 4*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), VedicColors.CREAM),
            ('TEXTCOLOR', (0, 0), (0, -1), VedicColors.MAROON),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('PADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, VedicColors.SAFFRON_LIGHT),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))

        self.elements.append(table)
        self.elements.append(Spacer(1, 20))

    def _add_birth_chart(self):
        """Add visual birth chart (Lagna Kundali)."""
        self.elements.append(Paragraph(
            "Lagna Kundali / लग्न कुंडली",
            self.styles['SectionHeading']
        ))

        planets_in_houses = self.kundali.get_planets_in_houses()
        lagna_num = self.kundali.lagna['rashi_num']
        planets = self.kundali.planets

        chart = draw_kundali_chart(planets_in_houses, lagna_num, planets, 280, 280)
        self.elements.append(chart)

        self.elements.append(Paragraph(
            "<font size='8' color='#666666'>(R) = Retrograde / वक्री</font>",
            ParagraphStyle('ChartNote', alignment=TA_CENTER, fontSize=8)
        ))

        self.elements.append(Spacer(1, 15))

    def _add_planet_positions(self):
        """Add planet positions table."""
        self.elements.append(Paragraph(
            "Planet Positions / ग्रह स्थिति",
            self.styles['SectionHeading']
        ))

        planets = self.kundali.planets
        planets_in_houses = self.kundali.get_planets_in_houses()

        # Header
        data = [["Planet\nग्रह", "Rashi\nराशि", "Degree\nअंश", "Nakshatra\nनक्षत्र", "House\nभाव", "Status\nगति"]]

        for p_name in ["SUN", "MOON", "MARS", "MERCURY", "JUPITER", "VENUS", "SATURN", "RAHU", "KETU"]:
            p_data = planets[p_name]
            hindi_name = PLANET_HINDI.get(p_name, p_name)
            rashi = RASHI_HINDI.get(p_data['rashi'], p_data['rashi'])

            # Find house
            house = 0
            for h, plist in planets_in_houses.items():
                if p_name in plist:
                    house = h
                    break

            status = "Retro/वक्री" if p_data['is_retrograde'] else "Direct/मार्गी"

            data.append([
                f"{p_name}\n{hindi_name}",
                rashi,
                f"{p_data['rashi_degree']:.2f}°",
                f"{p_data['nakshatra']}\nPada {p_data['pada']}",
                str(house),
                status
            ])

        table = Table(data, colWidths=[1*inch, 0.9*inch, 0.8*inch, 1.3*inch, 0.6*inch, 1*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), VedicColors.SAFFRON),
            ('TEXTCOLOR', (0, 0), (-1, 0), VedicColors.WHITE),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('PADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, VedicColors.SAFFRON_LIGHT),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [VedicColors.WHITE, VedicColors.CREAM]),
        ]))

        self.elements.append(table)
        self.elements.append(Spacer(1, 15))

    def _add_dasha_periods(self):
        """Add Vimshottari Dasha periods."""
        self.elements.append(Paragraph(
            "Vimshottari Dasha / विमशोत्तरी दशा",
            self.styles['SectionHeading']
        ))

        current_dasha = self.kundali.get_current_dasha()
        mahadashas = self.kundali.get_mahadashas(years=60)

        # Current Dasha highlight
        self.elements.append(Paragraph(
            f"<b>Current Period / वर्तमान दशा:</b> {current_dasha.get('full_dasha', 'N/A')}",
            self.styles['VedicNormal']
        ))

        self.elements.append(Spacer(1, 10))

        # Dasha table
        data = [["Mahadasha\nमहादशा", "Start Date\nआरंभ", "End Date\nसमाप्ति", "Duration\nअवधि"]]

        for maha in mahadashas[:10]:  # First 10
            hindi_planet = PLANET_HINDI.get(maha.planet, maha.planet)
            duration = f"{maha.duration_years:.1f} years"
            data.append([
                f"{maha.planet}\n{hindi_planet}",
                maha.start_date.strftime('%d-%m-%Y'),
                maha.end_date.strftime('%d-%m-%Y'),
                duration
            ])

        table = Table(data, colWidths=[1.4*inch, 1.3*inch, 1.3*inch, 1.1*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), VedicColors.MAROON),
            ('TEXTCOLOR', (0, 0), (-1, 0), VedicColors.WHITE),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('PADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, VedicColors.SAFFRON_LIGHT),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [VedicColors.WHITE, VedicColors.CREAM]),
        ]))

        self.elements.append(table)
        self.elements.append(Spacer(1, 15))

    def _add_yogas(self):
        """Add Yoga analysis section."""
        self.elements.append(Paragraph(
            "Special Yogas / विशेष योग",
            self.styles['SectionHeading']
        ))

        yogas = get_all_yogas(self.kundali)

        has_yogas = False

        # Mahapurusha Yogas
        if yogas.get('mahapurusha'):
            has_yogas = True
            self.elements.append(Paragraph(
                "<b>Panch Mahapurusha Yogas / पंच महापुरुष योग:</b>",
                self.styles['SubsectionHeading']
            ))
            for yoga in yogas['mahapurusha']:
                self.elements.append(Paragraph(
                    f"• <b>{yoga['name']}</b>: {yoga.get('effects', '')}",
                    self.styles['VedicNormal']
                ))

        # Positive Yogas
        if yogas.get('positive'):
            has_yogas = True
            self.elements.append(Paragraph(
                "<b>Auspicious Yogas / शुभ योग:</b>",
                self.styles['SubsectionHeading']
            ))
            for yoga in yogas['positive']:
                self.elements.append(Paragraph(
                    f"• <b>{yoga['name']}</b>: {yoga.get('effects', '')}",
                    self.styles['VedicNormal']
                ))

        # Dhana Yogas
        if yogas.get('dhana'):
            has_yogas = True
            self.elements.append(Paragraph(
                "<b>Wealth Yogas / धन योग:</b>",
                self.styles['SubsectionHeading']
            ))
            for yoga in yogas['dhana']:
                self.elements.append(Paragraph(
                    f"• <b>{yoga['name']}</b>: {yoga.get('effects', '')}",
                    self.styles['VedicNormal']
                ))

        # Negative Yogas / Doshas
        if yogas.get('negative'):
            has_yogas = True
            self.elements.append(Paragraph(
                "<b>Doshas / दोष (Remedies Required):</b>",
                self.styles['SubsectionHeading']
            ))
            for yoga in yogas['negative']:
                cancelled = " (Cancelled/निरस्त)" if yoga.get('cancelled') else ""
                self.elements.append(Paragraph(
                    f"• <b>{yoga['name']}{cancelled}</b>: {yoga.get('effects', '')}",
                    self.styles['VedicNormal']
                ))

        if not has_yogas:
            self.elements.append(Paragraph(
                "No significant special yogas detected in the chart.",
                self.styles['VedicNormal']
            ))

        self.elements.append(Spacer(1, 15))

    def _add_predictions_summary(self):
        """Add brief predictions summary."""
        self.elements.append(PageBreak())

        self.elements.append(Paragraph(
            "Life Areas Summary / जीवन क्षेत्र सारांश",
            self.styles['SectionHeading']
        ))

        planets_in_houses = self.kundali.get_planets_in_houses()

        # Career
        self.elements.append(Paragraph("<b>Career / करियर:</b>", self.styles['SubsectionHeading']))
        tenth_planets = planets_in_houses.get(10, [])
        if "JUPITER" in tenth_planets or "SUN" in tenth_planets:
            self.elements.append(Paragraph(
                "Strong career potential with leadership qualities. Benefic influence on 10th house indicates success in profession.",
                self.styles['VedicNormal']
            ))
        else:
            self.elements.append(Paragraph(
                "Career requires dedicated effort. Focus on building skills and networking for growth.",
                self.styles['VedicNormal']
            ))

        # Marriage
        self.elements.append(Paragraph("<b>Marriage / विवाह:</b>", self.styles['SubsectionHeading']))
        seventh_planets = planets_in_houses.get(7, [])
        if "VENUS" in seventh_planets or "JUPITER" in seventh_planets:
            self.elements.append(Paragraph(
                "Favorable indications for married life. Partner will be supportive and understanding.",
                self.styles['VedicNormal']
            ))
        elif "SATURN" in seventh_planets or "RAHU" in seventh_planets:
            self.elements.append(Paragraph(
                "May experience delays or challenges in marriage. Patience and understanding required.",
                self.styles['VedicNormal']
            ))
        else:
            self.elements.append(Paragraph(
                "Normal marriage prospects. Compatibility matching recommended before finalizing.",
                self.styles['VedicNormal']
            ))

        # Health
        self.elements.append(Paragraph("<b>Health / स्वास्थ्य:</b>", self.styles['SubsectionHeading']))
        sixth_planets = planets_in_houses.get(6, [])
        first_planets = planets_in_houses.get(1, [])
        if len(sixth_planets) == 0 and "SATURN" not in first_planets:
            self.elements.append(Paragraph(
                "Generally good health indicated. Maintain regular exercise and balanced diet.",
                self.styles['VedicNormal']
            ))
        else:
            self.elements.append(Paragraph(
                "Pay attention to health during planetary transits. Regular check-ups recommended.",
                self.styles['VedicNormal']
            ))

        # Wealth
        self.elements.append(Paragraph("<b>Wealth / धन:</b>", self.styles['SubsectionHeading']))
        second_planets = planets_in_houses.get(2, [])
        eleventh_planets = planets_in_houses.get(11, [])
        if "JUPITER" in second_planets or "VENUS" in second_planets or "JUPITER" in eleventh_planets:
            self.elements.append(Paragraph(
                "Good financial prospects. Multiple income sources possible. Save and invest wisely.",
                self.styles['VedicNormal']
            ))
        else:
            self.elements.append(Paragraph(
                "Moderate financial growth expected. Focus on savings and avoid unnecessary expenses.",
                self.styles['VedicNormal']
            ))

        self.elements.append(Spacer(1, 15))

    def _add_remedies(self):
        """Add remedies section."""
        self.elements.append(Paragraph(
            "Recommended Remedies / सुझाए गए उपाय",
            self.styles['SectionHeading']
        ))

        planets_in_houses = self.kundali.get_planets_in_houses()
        yogas = get_all_yogas(self.kundali)

        remedies = []

        # General remedies based on Lagna
        lagna_rashi = self.kundali.lagna['rashi']
        remedies.append(f"• Worship your Lagna lord for overall well-being / लग्नेश की पूजा करें")

        # Moon sign remedies
        moon_rashi = self.kundali.planets['MOON']['rashi']
        remedies.append(f"• Chant Moon mantras on Mondays / सोमवार को चंद्र मंत्र का जाप करें")

        # If negative yogas present
        if yogas.get('negative'):
            for yoga in yogas['negative']:
                if 'kaal sarp' in yoga.get('name', '').lower():
                    remedies.append("• Perform Kaal Sarp Dosh Puja / काल सर्प दोष पूजा करवाएं")
                if 'pitra' in yoga.get('name', '').lower():
                    remedies.append("• Perform Pitru Tarpan on Amavasya / अमावस्या पर पितृ तर्पण करें")

        # Saturn in difficult houses
        saturn_house = 0
        for h, plist in planets_in_houses.items():
            if "SATURN" in plist:
                saturn_house = h
                break
        if saturn_house in [1, 4, 7, 8, 12]:
            remedies.append("• Recite Hanuman Chalisa on Saturdays / शनिवार को हनुमान चालीसा पढ़ें")
            remedies.append("• Donate black items on Saturday / शनिवार को काले वस्तुएं दान करें")

        # General beneficial remedies
        remedies.append("• Wear your lucky gemstone after consultation / शुभ रत्न परामर्श के बाद धारण करें")
        remedies.append("• Perform charity according to your birth chart / कुंडली अनुसार दान करें")
        remedies.append("• Meditate daily for mental peace / मानसिक शांति के लिए दैनिक ध्यान करें")

        for remedy in remedies:
            self.elements.append(Paragraph(remedy, self.styles['VedicNormal']))

        self.elements.append(Spacer(1, 15))

    def _add_footer(self):
        """Add report footer with disclaimer."""
        self.elements.append(HRFlowable(
            width="100%", thickness=1, color=VedicColors.SAFFRON,
            spaceBefore=20, spaceAfter=10
        ))

        self.elements.append(Paragraph(
            '<font size="12" color="#FF6B00">&#x0950;</font> '
            '<font size="10">शुभम् भवतु / May Auspiciousness Prevail</font> '
            '<font size="12" color="#FF6B00">&#x0950;</font>',
            ParagraphStyle('Blessing', alignment=TA_CENTER, fontSize=10)
        ))

        self.elements.append(Spacer(1, 10))

        self.elements.append(Paragraph(
            f"Generated on: {datetime.now().strftime('%d-%m-%Y %H:%M')}",
            self.styles['Footer']
        ))

        self.elements.append(Paragraph(
            "Swiss Ephemeris (NASA JPL DE431) | Lahiri Ayanamsha",
            self.styles['Footer']
        ))

        self.elements.append(Spacer(1, 10))

        self.elements.append(Paragraph(
            "<b>Disclaimer / अस्वीकरण:</b> This report is for guidance only. "
            "For important life decisions, please consult a qualified astrologer. "
            "यह रिपोर्ट केवल मार्गदर्शन के लिए है। महत्वपूर्ण निर्णयों के लिए योग्य ज्योतिषी से परामर्श करें।",
            ParagraphStyle('Disclaimer', alignment=TA_CENTER, fontSize=7,
                          textColor=VedicColors.GRAY)
        ))

    def generate_pdf(self) -> bytes:
        """Generate complete Kundali PDF report."""
        buffer = io.BytesIO()

        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=0.5*inch,
            leftMargin=0.5*inch,
            topMargin=0.5*inch,
            bottomMargin=0.5*inch
        )

        # Build report sections
        self._add_header()
        self._add_birth_details()
        self._add_birth_chart()
        self._add_planet_positions()
        self._add_dasha_periods()
        self._add_yogas()
        self._add_predictions_summary()
        self._add_remedies()
        self._add_footer()

        # Build PDF
        doc.build(self.elements)

        buffer.seek(0)
        return buffer.getvalue()


# =============================================================================
# MATCHING PDF GENERATOR
# =============================================================================

class MatchingPDFGenerator:
    """Generate professional Kundali Matching PDF reports."""

    def __init__(self, match_result: Dict[str, Any], boy_data: Dict, girl_data: Dict):
        """
        Initialize Matching PDF Generator.

        Args:
            match_result: Complete matching result dictionary
            boy_data: Boy's birth and matching details
            girl_data: Girl's birth and matching details
        """
        self.result = match_result
        self.boy = boy_data
        self.girl = girl_data
        self.styles = get_styles()
        self.elements = []

    def _add_header(self):
        """Add report header."""
        # Om symbol
        self.elements.append(Paragraph(
            '<font size="36" color="#FF6B00">&#x0950;</font>',
            self.styles['VedicTitle']
        ))

        self.elements.append(Paragraph(
            "KUNDALI MILAN / कुंडली मिलान",
            self.styles['VedicTitle']
        ))

        self.elements.append(Paragraph(
            "Marriage Compatibility Report / विवाह अनुकूलता रिपोर्ट",
            self.styles['VedicHeading']
        ))

        self.elements.append(HRFlowable(
            width="100%", thickness=2, color=VedicColors.SAFFRON,
            spaceBefore=10, spaceAfter=15
        ))

    def _add_couple_details(self):
        """Add both persons' details side by side."""
        self.elements.append(Paragraph(
            "Couple Details / वर-वधू विवरण",
            self.styles['SectionHeading']
        ))

        # Create side-by-side table
        boy_details = [
            ["Boy / वर", ""],
            ["Name / नाम", self.boy.get('name', 'N/A')],
            ["DOB / जन्म तिथि", self.boy.get('dob', 'N/A')],
            ["Time / समय", self.boy.get('birth_time', 'N/A')],
            ["Place / स्थान", self.boy.get('city', 'N/A')],
            ["Moon Sign / राशि", self.boy.get('moon_rashi', 'N/A')],
            ["Nakshatra / नक्षत्र", self.boy.get('moon_nakshatra', 'N/A')],
            ["Lagna / लग्न", self.boy.get('lagna_rashi', 'N/A')],
        ]

        girl_details = [
            ["Girl / कन्या", ""],
            ["Name / नाम", self.girl.get('name', 'N/A')],
            ["DOB / जन्म तिथि", self.girl.get('dob', 'N/A')],
            ["Time / समय", self.girl.get('birth_time', 'N/A')],
            ["Place / स्थान", self.girl.get('city', 'N/A')],
            ["Moon Sign / राशि", self.girl.get('moon_rashi', 'N/A')],
            ["Nakshatra / नक्षत्र", self.girl.get('moon_nakshatra', 'N/A')],
            ["Lagna / लग्न", self.girl.get('lagna_rashi', 'N/A')],
        ]

        # Combine into single table with gap
        combined_data = []
        for i in range(len(boy_details)):
            combined_data.append(
                boy_details[i] + [""] + girl_details[i]
            )

        table = Table(combined_data, colWidths=[1.2*inch, 1.3*inch, 0.3*inch, 1.2*inch, 1.3*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (1, 0), VedicColors.BLUE),
            ('BACKGROUND', (3, 0), (4, 0), VedicColors.PINK),
            ('TEXTCOLOR', (0, 0), (1, 0), VedicColors.WHITE),
            ('TEXTCOLOR', (3, 0), (4, 0), VedicColors.WHITE),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('SPAN', (0, 0), (1, 0)),
            ('SPAN', (3, 0), (4, 0)),
            ('BACKGROUND', (0, 1), (1, -1), VedicColors.LIGHT_BLUE),
            ('BACKGROUND', (3, 1), (4, -1), VedicColors.LIGHT_PINK),
            ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (3, 1), (3, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('PADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (1, -1), 0.5, VedicColors.BLUE),
            ('GRID', (3, 0), (4, -1), 0.5, VedicColors.PINK),
        ]))

        self.elements.append(table)
        self.elements.append(Spacer(1, 20))

    def _add_compatibility_score(self):
        """Add overall compatibility score with gauge."""
        self.elements.append(Paragraph(
            "Compatibility Score / अनुकूलता स्कोर",
            self.styles['SectionHeading']
        ))

        total = self.result.get('total_points', 0)
        max_pts = self.result.get('max_points', 36)
        percentage = self.result.get('percentage', 0)
        level = self.result.get('compatibility_level', 'Average')

        # Draw gauge
        gauge = draw_compatibility_gauge(total, max_pts, 250, 100)
        self.elements.append(gauge)

        # Compatibility interpretation
        if percentage >= 70:
            color = VedicColors.GREEN
            interpretation = "Excellent compatibility! This is a highly recommended match. / उत्तम मिलान! विवाह के लिए अत्यंत शुभ।"
        elif percentage >= 50:
            color = VedicColors.SAFFRON
            interpretation = "Good compatibility. Marriage is recommended with minor considerations. / अच्छा मिलान। कुछ बातों का ध्यान रखते हुए विवाह शुभ।"
        elif percentage >= 36:
            color = colors.HexColor('#FFA500')
            interpretation = "Average compatibility. Consider remedies before proceeding. / सामान्य मिलान। उपाय करने के बाद विवाह पर विचार करें।"
        else:
            color = VedicColors.DEEP_RED
            interpretation = "Below average compatibility. Thorough analysis and remedies recommended. / कम मिलान। विस्तृत विश्लेषण और उपाय आवश्यक।"

        self.elements.append(Paragraph(
            interpretation,
            ParagraphStyle('Interpretation', alignment=TA_CENTER, fontSize=10,
                          textColor=color, spaceBefore=10, spaceAfter=15)
        ))

    def _add_ashtakoot_table(self):
        """Add detailed Ashtakoot Milan table."""
        self.elements.append(Paragraph(
            "Ashtakoot Milan / अष्टकूट मिलान",
            self.styles['SectionHeading']
        ))

        koota_scores = self.result.get('koota_scores', [])

        # Header
        data = [["Koota / कूट", "Max\nअधिकतम", "Obtained\nप्राप्त", "Boy\nवर", "Girl\nकन्या", "Status\nस्थिति"]]

        for koota in koota_scores:
            status = "Good / शुभ" if koota.get('is_auspicious', False) else "Attention / ध्यान"
            status_color = VedicColors.GREEN if koota.get('is_auspicious', False) else VedicColors.DEEP_RED

            data.append([
                f"{koota.get('name', '')}\n{koota.get('name_hindi', '')}",
                str(koota.get('max_points', 0)),
                str(koota.get('obtained_points', 0)),
                koota.get('boy_value', ''),
                koota.get('girl_value', ''),
                status
            ])

        # Add total row
        total_obtained = sum(k.get('obtained_points', 0) for k in koota_scores)
        data.append(["TOTAL / कुल", "36", str(total_obtained), "", "", ""])

        table = Table(data, colWidths=[1.3*inch, 0.6*inch, 0.7*inch, 1.1*inch, 1.1*inch, 0.9*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), VedicColors.SAFFRON),
            ('TEXTCOLOR', (0, 0), (-1, 0), VedicColors.WHITE),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BACKGROUND', (0, -1), (-1, -1), VedicColors.MAROON),
            ('TEXTCOLOR', (0, -1), (-1, -1), VedicColors.WHITE),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('PADDING', (0, 0), (-1, -1), 5),
            ('GRID', (0, 0), (-1, -1), 0.5, VedicColors.SAFFRON_LIGHT),
            ('ROWBACKGROUNDS', (0, 1), (-1, -2), [VedicColors.WHITE, VedicColors.CREAM]),
        ]))

        self.elements.append(table)
        self.elements.append(Spacer(1, 15))

    def _add_koota_details(self):
        """Add detailed Koota interpretations."""
        self.elements.append(PageBreak())

        self.elements.append(Paragraph(
            "Detailed Koota Analysis / विस्तृत कूट विश्लेषण",
            self.styles['SectionHeading']
        ))

        koota_interpretations = self.result.get('koota_interpretations', [])

        for ki in koota_interpretations:
            is_favorable = ki.get('is_favorable', False)
            color = VedicColors.GREEN if is_favorable else VedicColors.DEEP_RED

            self.elements.append(Paragraph(
                f"<b>{ki.get('name', '')} / {ki.get('name_hindi', '')}</b> - {ki.get('score', '')}",
                ParagraphStyle('KootaTitle', fontSize=11, textColor=color,
                              fontName='Helvetica-Bold', spaceBefore=10)
            ))

            if ki.get('detailed_interpretation'):
                self.elements.append(Paragraph(
                    ki['detailed_interpretation'],
                    self.styles['VedicNormal']
                ))

            if ki.get('effects'):
                for effect in ki['effects'][:2]:  # First 2 effects
                    self.elements.append(Paragraph(
                        f"• {effect}",
                        self.styles['VedicNormal']
                    ))

        self.elements.append(Spacer(1, 15))

    def _add_doshas(self):
        """Add Dosha analysis section."""
        doshas = self.result.get('doshas', [])

        if not doshas:
            self.elements.append(Paragraph(
                "Dosha Analysis / दोष विश्लेषण",
                self.styles['SectionHeading']
            ))
            self.elements.append(Paragraph(
                "No significant doshas detected. / कोई महत्वपूर्ण दोष नहीं पाया गया।",
                self.styles['VedicNormal']
            ))
            return

        self.elements.append(Paragraph(
            "Dosha Analysis / दोष विश्लेषण",
            self.styles['SectionHeading']
        ))

        for dosha in doshas:
            is_cancelled = dosha.get('is_cancelled', False)
            severity = dosha.get('severity', 'Medium')

            if is_cancelled:
                color = VedicColors.GREEN
                status = "(Cancelled / निरस्त)"
            elif severity == 'Critical':
                color = VedicColors.DEEP_RED
                status = "(Critical / गंभीर)"
            elif severity == 'High':
                color = colors.HexColor('#FF6600')
                status = "(High / उच्च)"
            else:
                color = VedicColors.SAFFRON
                status = "(Medium / मध्यम)"

            self.elements.append(Paragraph(
                f"<b>{dosha.get('name', '')} {status}</b>",
                ParagraphStyle('DoshaTitle', fontSize=11, textColor=color,
                              fontName='Helvetica-Bold', spaceBefore=8)
            ))

            self.elements.append(Paragraph(
                dosha.get('description', ''),
                self.styles['VedicNormal']
            ))

            if dosha.get('remedies') and not is_cancelled:
                self.elements.append(Paragraph(
                    "<i>Remedies / उपाय:</i>",
                    ParagraphStyle('RemedyHeader', fontSize=9, textColor=VedicColors.PURPLE,
                                  fontName='Helvetica-Oblique')
                ))
                for remedy in dosha['remedies'][:3]:
                    self.elements.append(Paragraph(
                        f"• {remedy}",
                        ParagraphStyle('Remedy', fontSize=9, leftIndent=15)
                    ))

        self.elements.append(Spacer(1, 15))

    def _add_marriage_timing(self):
        """Add marriage timing suggestions."""
        timing = self.result.get('marriage_timing', {})

        if not timing:
            return

        self.elements.append(Paragraph(
            "Marriage Timing / विवाह मुहूर्त",
            self.styles['SectionHeading']
        ))

        if timing.get('favorable_days'):
            self.elements.append(Paragraph(
                f"<b>Favorable Days / शुभ दिन:</b> {', '.join(timing['favorable_days'])}",
                self.styles['VedicNormal']
            ))

        if timing.get('favorable_months'):
            self.elements.append(Paragraph(
                f"<b>Favorable Months / शुभ माह:</b> {', '.join(timing['favorable_months'])}",
                self.styles['VedicNormal']
            ))

        if timing.get('avoid'):
            self.elements.append(Paragraph(
                f"<b>Avoid / त्याज्य:</b> {', '.join(timing['avoid'])}",
                self.styles['VedicNormal']
            ))

        if timing.get('general_advice'):
            self.elements.append(Paragraph("<b>General Advice / सामान्य सलाह:</b>", self.styles['SubsectionHeading']))
            for advice in timing['general_advice']:
                self.elements.append(Paragraph(f"• {advice}", self.styles['VedicNormal']))

        self.elements.append(Spacer(1, 15))

    def _add_recommendation(self):
        """Add final recommendation."""
        self.elements.append(Paragraph(
            "Final Recommendation / अंतिम सिफारिश",
            self.styles['SectionHeading']
        ))

        recommendation = self.result.get('recommendation', '')
        self.elements.append(Paragraph(recommendation, self.styles['VedicNormal']))

        # Strengths
        strengths = self.result.get('areas_of_strength', [])
        if strengths:
            self.elements.append(Paragraph("<b>Strengths / मजबूत पक्ष:</b>", self.styles['SubsectionHeading']))
            for s in strengths[:5]:
                self.elements.append(Paragraph(f"✓ {s}",
                    ParagraphStyle('Strength', fontSize=9, textColor=VedicColors.GREEN)))

        # Concerns
        concerns = self.result.get('areas_of_concern', [])
        if concerns:
            self.elements.append(Paragraph("<b>Areas of Concern / चिंता के क्षेत्र:</b>", self.styles['SubsectionHeading']))
            for c in concerns[:5]:
                self.elements.append(Paragraph(f"⚠ {c}",
                    ParagraphStyle('Concern', fontSize=9, textColor=VedicColors.DEEP_RED)))

        self.elements.append(Spacer(1, 15))

    def _add_remedies(self):
        """Add recommended remedies."""
        remedies = self.result.get('remedies', [])

        if not remedies:
            return

        self.elements.append(Paragraph(
            "Recommended Remedies / सुझाए गए उपाय",
            self.styles['SectionHeading']
        ))

        for remedy in remedies[:10]:  # Max 10 remedies
            self.elements.append(Paragraph(f"🙏 {remedy}", self.styles['VedicNormal']))

        self.elements.append(Spacer(1, 15))

    def _add_footer(self):
        """Add report footer."""
        self.elements.append(HRFlowable(
            width="100%", thickness=1, color=VedicColors.SAFFRON,
            spaceBefore=20, spaceAfter=10
        ))

        self.elements.append(Paragraph(
            '<font size="12" color="#FF6B00">&#x0950;</font> '
            '<font size="10">शुभ विवाह / Shubh Vivah</font> '
            '<font size="12" color="#FF6B00">&#x0950;</font>',
            ParagraphStyle('Blessing', alignment=TA_CENTER, fontSize=10)
        ))

        self.elements.append(Spacer(1, 10))

        self.elements.append(Paragraph(
            f"Generated on: {datetime.now().strftime('%d-%m-%Y %H:%M')}",
            self.styles['Footer']
        ))

        self.elements.append(Paragraph(
            "Based on Brihat Parashara Hora Shastra, Muhurta Chintamani, Jataka Parijata",
            self.styles['Footer']
        ))

        self.elements.append(Spacer(1, 10))

        self.elements.append(Paragraph(
            "<b>Disclaimer / अस्वीकरण:</b> This report is for guidance only. "
            "Marriage is a sacred bond that goes beyond astrological compatibility. "
            "Please consult qualified astrologers and family elders before making decisions. "
            "यह रिपोर्ट केवल मार्गदर्शन के लिए है। विवाह एक पवित्र बंधन है। "
            "निर्णय लेने से पहले योग्य ज्योतिषी और परिवार के बड़ों से परामर्श करें।",
            ParagraphStyle('Disclaimer', alignment=TA_CENTER, fontSize=7,
                          textColor=VedicColors.GRAY)
        ))

    def generate_pdf(self) -> bytes:
        """Generate complete Matching PDF report."""
        buffer = io.BytesIO()

        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=0.5*inch,
            leftMargin=0.5*inch,
            topMargin=0.5*inch,
            bottomMargin=0.5*inch
        )

        # Build report sections
        self._add_header()
        self._add_couple_details()
        self._add_compatibility_score()
        self._add_ashtakoot_table()
        self._add_koota_details()
        self._add_doshas()
        self._add_marriage_timing()
        self._add_recommendation()
        self._add_remedies()
        self._add_footer()

        # Build PDF
        doc.build(self.elements)

        buffer.seek(0)
        return buffer.getvalue()


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def generate_kundali_pdf(kundali: Kundali) -> bytes:
    """
    Generate a Kundali PDF report.

    Args:
        kundali: Kundali object with birth chart data

    Returns:
        PDF file as bytes
    """
    generator = KundaliPDFGenerator(kundali)
    return generator.generate_pdf()


def generate_matching_pdf(
    match_result: Dict[str, Any],
    boy_details: Dict[str, Any],
    girl_details: Dict[str, Any]
) -> bytes:
    """
    Generate a Kundali Matching PDF report.

    Args:
        match_result: Complete matching result dictionary
        boy_details: Boy's details dictionary
        girl_details: Girl's details dictionary

    Returns:
        PDF file as bytes
    """
    generator = MatchingPDFGenerator(match_result, boy_details, girl_details)
    return generator.generate_pdf()
