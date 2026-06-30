"""
Core module - Re-exports calculation modules from ../src/
"""

import sys
from pathlib import Path

# Add parent directory (kundali_software) to path so we can import from src/
parent_dir = Path(__file__).resolve().parent.parent.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

# Re-export key modules from src/
from src.kundali import Kundali, BirthData, create_kundali, get_coordinates
from src.chat_assistant import KundaliChatAssistant
from src.muhurta import MuhurtaCalculator, MuhurtaWindow, find_best_muhurtas
from src.muhurta_rules import EventType
from src.health_predictor import HealthPredictor, HealthWarning, RiskLevel, HealthEventType
from src.panchang import PanchangCalculator, PanchangData
from src.config import RASHIS, PLANET_NAMES, Planet, BHAVA_NAMES

__all__ = [
    # Kundali
    "Kundali",
    "BirthData",
    "create_kundali",
    "get_coordinates",
    # Chat
    "KundaliChatAssistant",
    # Muhurta
    "MuhurtaCalculator",
    "MuhurtaWindow",
    "find_best_muhurtas",
    "EventType",
    # Health
    "HealthPredictor",
    "HealthWarning",
    "RiskLevel",
    "HealthEventType",
    # Panchang
    "PanchangCalculator",
    "PanchangData",
    # Config
    "RASHIS",
    "PLANET_NAMES",
    "Planet",
    "BHAVA_NAMES",
]
