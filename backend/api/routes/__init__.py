"""
API routes module.
"""

from .kundali import router as kundali_router
from .chat import router as chat_router
from .muhurta import router as muhurta_router
from .health import router as health_router
from .matching import router as matching_router
from .divisional_charts import router as divisional_charts_router
from .panchang import router as panchang_router
from .pdf import router as pdf_router
from .numerology import router as numerology_router
from .rashifal import router as rashifal_router
from .dosha import router as dosha_router
from .gemstone import router as gemstone_router
from .career import router as career_router
from .remedies import router as remedies_router
from .prashna import router as prashna_router

__all__ = [
    "kundali_router",
    "chat_router",
    "muhurta_router",
    "health_router",
    "matching_router",
    "divisional_charts_router",
    "panchang_router",
    "pdf_router",
    "numerology_router",
    "rashifal_router",
    "dosha_router",
    "gemstone_router",
    "career_router",
    "remedies_router",
    "prashna_router",
]
