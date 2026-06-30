"""
Muhurta Calculator - Main Electional Astrology Module

Finds auspicious moments (Muhurtas) for important life events by combining:
1. Dasha/Transit analysis from EventPredictor
2. Panchang calculations (Tithi, Nakshatra, Yoga, Karana, Vara)
3. Inauspicious period avoidance (Rahu Kala, Yamaghantaka, etc.)
4. Personal compatibility (Tarabala, Chandrabala)
5. Event-specific classical rules

Based on authentic Vedic texts:
- Muhurta Chintamani
- Brihat Samhita
- Phaladeepika
"""

from datetime import datetime, time, timedelta
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
import pytz

from .panchang import PanchangCalculator, PanchangData
from .muhurta_rules import (
    EventType,
    InauspiciousPeriod,
    get_all_inauspicious_periods,
    get_event_rules,
    calculate_tarabala,
    calculate_chandrabala,
    is_nakshatra_favorable,
    find_best_time_window,
    get_hora_lord,
    is_hora_favorable,
    calculate_abhijit_muhurta,
    is_time_in_inauspicious_period,
)
from .kundali import Kundali
from .event_predictor import EventPredictor


@dataclass
class MuhurtaWindow:
    """Represents an auspicious time window for an event."""
    date: datetime
    start_time: time
    end_time: time
    panchang: PanchangData
    score: int
    reasons: List[str]
    warnings: List[str]
    tarabala_num: int
    tarabala_name: str
    tarabala_score: int
    chandrabala_house: int
    chandrabala_score: int
    inauspicious_periods: List[InauspiciousPeriod]
    abhijit_muhurta: Optional[Tuple[time, time]] = None
    hora_lord: str = ""
    dasha_info: str = ""


class MuhurtaCalculator:
    """
    Main Muhurta selection class.

    Integrates:
    - Panchang calculations
    - Inauspicious period detection
    - Personal compatibility (Tarabala, Chandrabala)
    - Event-specific rules from classical texts
    - EventPredictor for Dasha/Transit analysis
    """

    def __init__(self, natal_kundali: Kundali):
        """
        Initialize with natal chart for personal compatibility calculations.

        Args:
            natal_kundali: Kundali object containing birth chart data
        """
        self.natal_kundali = natal_kundali
        self.panchang_calc = PanchangCalculator()
        self.event_predictor = EventPredictor(natal_kundali)

        self._natal_moon_nakshatra = natal_kundali.planets["MOON"]["nakshatra_num"]
        self._natal_moon_rashi = natal_kundali.planets["MOON"]["rashi_num"]
        self._lagna_rashi = natal_kundali.lagna["rashi"]

    def find_muhurtas(
        self,
        event_type: EventType,
        start_date: datetime,
        end_date: datetime,
        use_event_predictor: bool = True,
        min_score: int = 50,
        top_n: int = 10,
        latitude: float = 28.6139,
        longitude: float = 77.2090,
        timezone: str = "Asia/Kolkata",
        gender: str = "male"
    ) -> List[MuhurtaWindow]:
        """
        Find auspicious muhurtas for an event within a date range.

        This method:
        1. Optionally narrows down dates using EventPredictor (Dasha/Transit)
        2. Scans each day for Panchang compatibility
        3. Calculates personal compatibility (Tarabala, Chandrabala)
        4. Identifies inauspicious periods to avoid
        5. Returns scored and sorted muhurta windows

        Args:
            event_type: Type of event (MARRIAGE, CAREER, PROPERTY, etc.)
            start_date: Start of search range
            end_date: End of search range
            use_event_predictor: If True, use Dasha/Transit to filter dates
            min_score: Minimum score threshold (0-100)
            top_n: Maximum number of muhurtas to return
            latitude: Location latitude
            longitude: Location longitude
            timezone: Timezone string
            gender: Gender for marriage predictions

        Returns:
            List of MuhurtaWindow objects, sorted by score (highest first)
        """
        tz = pytz.timezone(timezone)

        if start_date.tzinfo is None:
            start_date = tz.localize(start_date)
        if end_date.tzinfo is None:
            end_date = tz.localize(end_date)

        favorable_periods = []

        if use_event_predictor:
            favorable_periods = self._get_favorable_periods_from_predictor(
                event_type, start_date, end_date, gender
            )

        if not favorable_periods:
            favorable_periods = [{
                "start": start_date,
                "end": end_date,
                "dasha_score": 50,
                "dasha_reasons": [],
                "dasha_info": ""
            }]

        muhurtas = []
        event_rules = get_event_rules(event_type)

        for period in favorable_periods:
            period_muhurtas = self._scan_period(
                period["start"],
                period["end"],
                event_type,
                event_rules,
                period.get("dasha_score", 50),
                period.get("dasha_reasons", []),
                period.get("dasha_info", ""),
                latitude,
                longitude,
                timezone
            )
            muhurtas.extend(period_muhurtas)

        muhurtas.sort(key=lambda m: m.score, reverse=True)
        return [m for m in muhurtas if m.score >= min_score][:top_n]

    def _get_favorable_periods_from_predictor(
        self,
        event_type: EventType,
        start_date: datetime,
        end_date: datetime,
        gender: str
    ) -> List[Dict]:
        """Get favorable periods from EventPredictor."""
        periods = []

        try:
            if event_type == EventType.MARRIAGE:
                predictions = self.event_predictor.predict_marriage_timing(
                    start_date.year, end_date.year, gender
                )
            elif event_type == EventType.CAREER:
                predictions = self.event_predictor.predict_career_change(
                    start_date.year, end_date.year
                )
            elif event_type in [EventType.PROPERTY, EventType.GRIHA_PRAVESH]:
                predictions = self.event_predictor.predict_property_purchase(
                    start_date.year, end_date.year
                )
            else:
                return periods

            for pred in predictions:
                pred_start = pred["start_date"]
                pred_end = pred["end_date"]

                if pred_start.tzinfo is None:
                    pred_start = pytz.timezone("Asia/Kolkata").localize(pred_start)
                if pred_end.tzinfo is None:
                    pred_end = pytz.timezone("Asia/Kolkata").localize(pred_end)

                if pred_start <= end_date and pred_end >= start_date:
                    periods.append({
                        "start": max(pred_start, start_date),
                        "end": min(pred_end, end_date),
                        "dasha_score": pred.get("score", 50),
                        "dasha_reasons": pred.get("reasons", []),
                        "dasha_info": pred.get("dasha", "")
                    })

        except Exception:
            pass

        return periods

    def _scan_period(
        self,
        start_date: datetime,
        end_date: datetime,
        event_type: EventType,
        event_rules: Dict,
        dasha_score: int,
        dasha_reasons: List[str],
        dasha_info: str,
        latitude: float,
        longitude: float,
        timezone: str
    ) -> List[MuhurtaWindow]:
        """Scan a period day-by-day for auspicious muhurtas."""
        muhurtas = []
        current_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)

        while current_date <= end_date:
            panchang = self.panchang_calc.get_panchang(
                current_date, latitude, longitude, timezone
            )

            inauspicious = get_all_inauspicious_periods(
                panchang.timings.sunrise,
                panchang.timings.sunset,
                current_date.weekday()
            )

            day_score, day_reasons, day_warnings = self._score_day(
                panchang, event_type, event_rules
            )

            tarabala_num, tarabala_name, tarabala_effect, tarabala_score = calculate_tarabala(
                self._natal_moon_nakshatra,
                panchang.nakshatra.number
            )

            chandrabala_house, chandrabala_score, chandrabala_effect = calculate_chandrabala(
                self._natal_moon_rashi,
                panchang.moon_rashi_num
            )

            total_score = self._calculate_total_score(
                day_score,
                tarabala_score,
                chandrabala_score,
                dasha_score
            )

            all_reasons = dasha_reasons.copy() + day_reasons
            if tarabala_score >= 8:
                all_reasons.append(f"Tarabala: {tarabala_name} - {tarabala_effect}")
            if chandrabala_score >= 8:
                all_reasons.append(f"Chandrabala: House {chandrabala_house} - favorable")

            if tarabala_score == 0:
                day_warnings.append(f"Tarabala: {tarabala_name} - {tarabala_effect}")
            if chandrabala_score == 0:
                day_warnings.append(f"Chandrabala: House {chandrabala_house} - unfavorable")

            if total_score >= 35:
                start_time, end_time = find_best_time_window(
                    panchang.timings.sunrise,
                    panchang.timings.sunset,
                    current_date.weekday()
                )

                abhijit_start, abhijit_end = calculate_abhijit_muhurta(
                    panchang.timings.sunrise,
                    panchang.timings.sunset
                )

                mid_time = start_time + (end_time - start_time) / 2
                hora_lord = get_hora_lord(mid_time, panchang.timings.sunrise)

                hora_favorable, hora_reason = is_hora_favorable(hora_lord, event_type)
                if hora_favorable:
                    all_reasons.append(hora_reason)

                muhurtas.append(MuhurtaWindow(
                    date=current_date,
                    start_time=start_time.time(),
                    end_time=end_time.time(),
                    panchang=panchang,
                    score=total_score,
                    reasons=all_reasons,
                    warnings=day_warnings,
                    tarabala_num=tarabala_num,
                    tarabala_name=tarabala_name,
                    tarabala_score=tarabala_score,
                    chandrabala_house=chandrabala_house,
                    chandrabala_score=chandrabala_score,
                    inauspicious_periods=inauspicious,
                    abhijit_muhurta=(abhijit_start.time(), abhijit_end.time()),
                    hora_lord=hora_lord,
                    dasha_info=dasha_info
                ))

            current_date += timedelta(days=1)

        return muhurtas

    def _score_day(
        self,
        panchang: PanchangData,
        event_type: EventType,
        rules: Dict
    ) -> Tuple[int, List[str], List[str]]:
        """Score a day based on Panchang and event rules."""
        score = 50
        reasons = []
        warnings = []

        tithi_num = panchang.tithi.number
        tithi_in_paksha = tithi_num if tithi_num <= 15 else tithi_num - 15

        if tithi_in_paksha in rules.get("favorable_tithis", []):
            score += 10
            reasons.append(f"Auspicious tithi: {panchang.tithi.name} ({panchang.tithi.paksha})")

        if tithi_in_paksha in rules.get("unfavorable_tithis", []):
            score -= 15
            warnings.append(f"Inauspicious tithi: {panchang.tithi.name}")

        if panchang.tithi.is_rikta:
            score -= 10
            warnings.append(f"Rikta tithi ({panchang.tithi.name}) - avoid important works")

        if tithi_num == 30:
            score -= 20
            warnings.append("Amavasya (New Moon) - generally inauspicious")

        if panchang.nakshatra.number in rules.get("favorable_nakshatras", []):
            score += 15
            reasons.append(f"Favorable nakshatra: {panchang.nakshatra.name}")

        if panchang.nakshatra.number in rules.get("unfavorable_nakshatras", []):
            score -= 15
            warnings.append(f"Unfavorable nakshatra: {panchang.nakshatra.name}")

        if panchang.yoga.is_inauspicious:
            score -= 12
            warnings.append(f"Inauspicious yoga: {panchang.yoga.name}")
        else:
            score += 5
            reasons.append(f"Auspicious yoga: {panchang.yoga.name}")

        if panchang.karana.name == "Vishti":
            score -= 10
            warnings.append("Vishti (Bhadra) karana - avoid important works")
        elif panchang.karana.is_auspicious:
            score += 3
            reasons.append(f"Favorable karana: {panchang.karana.name}")

        if panchang.vara.number in rules.get("favorable_weekdays", []):
            score += 8
            reasons.append(f"Favorable weekday: {panchang.vara.english}")

        if panchang.vara.number in rules.get("unfavorable_weekdays", []):
            score -= 8
            warnings.append(f"Unfavorable weekday: {panchang.vara.english}")

        if rules.get("prefer_shukla_paksha", False) and panchang.tithi.paksha == "Shukla":
            score += 5
            reasons.append("Shukla Paksha (waxing moon) - auspicious")

        return score, reasons, warnings

    def _calculate_total_score(
        self,
        day_score: int,
        tarabala_score: int,
        chandrabala_score: int,
        dasha_score: int
    ) -> int:
        """
        Calculate weighted total score.

        Weights:
        - Dasha/Transit: 30%
        - Day (Panchang): 40%
        - Tarabala: 15%
        - Chandrabala: 15%
        """
        tarabala_normalized = (tarabala_score / 10) * 100
        chandrabala_normalized = (chandrabala_score / 10) * 100

        total = (
            (dasha_score * 0.30) +
            (day_score * 0.40) +
            (tarabala_normalized * 0.15) +
            (chandrabala_normalized * 0.15)
        )

        return min(100, max(0, int(total)))

    def get_panchang_for_date(
        self,
        date: datetime,
        latitude: float = 28.6139,
        longitude: float = 77.2090,
        timezone: str = "Asia/Kolkata"
    ) -> PanchangData:
        """Get Panchang for a specific date (utility method)."""
        return self.panchang_calc.get_panchang(date, latitude, longitude, timezone)

    def get_inauspicious_times(
        self,
        date: datetime,
        latitude: float = 28.6139,
        longitude: float = 77.2090,
        timezone: str = "Asia/Kolkata"
    ) -> List[InauspiciousPeriod]:
        """Get all inauspicious periods for a date (utility method)."""
        panchang = self.get_panchang_for_date(date, latitude, longitude, timezone)
        return get_all_inauspicious_periods(
            panchang.timings.sunrise,
            panchang.timings.sunset,
            date.weekday()
        )

    def get_muhurta_summary(
        self,
        muhurta: MuhurtaWindow
    ) -> Dict:
        """Get a formatted summary of a Muhurta window."""
        return {
            "date": muhurta.date.strftime("%Y-%m-%d"),
            "weekday": muhurta.panchang.vara.english,
            "time_window": f"{muhurta.start_time.strftime('%H:%M')} - {muhurta.end_time.strftime('%H:%M')}",
            "score": muhurta.score,
            "panchang": {
                "tithi": f"{muhurta.panchang.tithi.name} ({muhurta.panchang.tithi.paksha})",
                "nakshatra": f"{muhurta.panchang.nakshatra.name} (Pada {muhurta.panchang.nakshatra.pada})",
                "yoga": muhurta.panchang.yoga.name,
                "karana": muhurta.panchang.karana.name,
            },
            "personal_compatibility": {
                "tarabala": f"{muhurta.tarabala_name} (Score: {muhurta.tarabala_score}/10)",
                "chandrabala": f"House {muhurta.chandrabala_house} (Score: {muhurta.chandrabala_score}/10)",
            },
            "dasha": muhurta.dasha_info if muhurta.dasha_info else "N/A",
            "reasons": muhurta.reasons,
            "warnings": muhurta.warnings,
            "abhijit_muhurta": f"{muhurta.abhijit_muhurta[0].strftime('%H:%M')} - {muhurta.abhijit_muhurta[1].strftime('%H:%M')}" if muhurta.abhijit_muhurta else "N/A",
            "avoid_periods": [
                {
                    "name": p.name,
                    "time": f"{p.start_time.strftime('%H:%M')} - {p.end_time.strftime('%H:%M')}",
                    "severity": p.severity
                }
                for p in muhurta.inauspicious_periods
            ]
        }

    def print_muhurta(self, muhurta: MuhurtaWindow) -> None:
        """Print formatted muhurta details."""
        summary = self.get_muhurta_summary(muhurta)

        print(f"\n{'=' * 60}")
        print(f"  DATE: {summary['date']} ({summary['weekday']})")
        print(f"  SCORE: {summary['score']}/100")
        print(f"{'=' * 60}")

        print(f"\n  Recommended Time: {summary['time_window']}")
        print(f"  Abhijit Muhurta: {summary['abhijit_muhurta']}")

        print(f"\n  PANCHANG:")
        print(f"    Tithi: {summary['panchang']['tithi']}")
        print(f"    Nakshatra: {summary['panchang']['nakshatra']}")
        print(f"    Yoga: {summary['panchang']['yoga']}")
        print(f"    Karana: {summary['panchang']['karana']}")

        print(f"\n  PERSONAL COMPATIBILITY:")
        print(f"    Tarabala: {summary['personal_compatibility']['tarabala']}")
        print(f"    Chandrabala: {summary['personal_compatibility']['chandrabala']}")

        if summary['dasha'] != "N/A":
            print(f"\n  DASHA: {summary['dasha']}")

        if summary['reasons']:
            print(f"\n  FAVORABLE FACTORS:")
            for reason in summary['reasons'][:5]:
                print(f"    + {reason}")

        if summary['warnings']:
            print(f"\n  WARNINGS:")
            for warning in summary['warnings']:
                print(f"    - {warning}")

        print(f"\n  AVOID THESE PERIODS:")
        for period in summary['avoid_periods']:
            if period['severity'] == 'high':
                print(f"    [HIGH] {period['name']}: {period['time']}")
            else:
                print(f"    [{period['severity'].upper()}] {period['name']}: {period['time']}")


def find_best_muhurtas(
    kundali: Kundali,
    event_type: str,
    start_date: datetime,
    end_date: datetime,
    top_n: int = 5,
    min_score: int = 50,
    gender: str = "male"
) -> List[MuhurtaWindow]:
    """
    Convenience function to find best muhurtas.

    Args:
        kundali: Birth chart
        event_type: "marriage", "career", "property", "travel", "griha_pravesh"
        start_date: Start of search range
        end_date: End of search range
        top_n: Number of results
        min_score: Minimum score threshold
        gender: Gender for marriage predictions

    Returns:
        List of MuhurtaWindow objects
    """
    event_map = {
        "marriage": EventType.MARRIAGE,
        "career": EventType.CAREER,
        "property": EventType.PROPERTY,
        "travel": EventType.TRAVEL,
        "griha_pravesh": EventType.GRIHA_PRAVESH,
        "education": EventType.EDUCATION,
        "general": EventType.GENERAL,
    }

    event = event_map.get(event_type.lower(), EventType.GENERAL)

    calc = MuhurtaCalculator(kundali)
    return calc.find_muhurtas(
        event_type=event,
        start_date=start_date,
        end_date=end_date,
        min_score=min_score,
        top_n=top_n,
        gender=gender
    )
