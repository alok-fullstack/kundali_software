"""
Sade Sati Transit Tracking

Sade Sati is a 7.5-year period when Saturn transits through the 12th, 1st, and 2nd
houses from the natal Moon position. It is one of the most significant transit periods
in Vedic astrology, associated with challenges, transformation, and karmic lessons.

Phases:
- Rising (12th from Moon): Beginning of challenges, subtle difficulties emerge
- Peak (1st/over Moon): Maximum intensity, major life transformations
- Setting (2nd from Moon): Challenges easing, consolidation of lessons learned

Saturn takes approximately 29.5 years to complete one zodiac cycle, spending
roughly 2.5 years in each sign.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from bisect import bisect_left

from .planets import PlanetaryCalculator
from .config import Planet, RASHIS


class SadeSatiTracker:
    """
    Tracks Sade Sati periods based on Saturn's transit relative to natal Moon position.

    Sade Sati occurs when Saturn transits through:
    - 12th house from Moon (Rising phase) - ~2.5 years
    - 1st house from Moon (Peak phase) - ~2.5 years
    - 2nd house from Moon (Setting phase) - ~2.5 years
    Total duration: ~7.5 years

    Saturn's orbital period: ~29.5 years
    Average time per sign: ~2.5 years (but varies due to retrograde motion)
    """

    # Phase definitions relative to natal Moon rashi
    PHASE_RISING = "Rising"      # 12th from Moon
    PHASE_PEAK = "Peak"          # Over Moon (1st from Moon)
    PHASE_SETTING = "Setting"    # 2nd from Moon

    # Severity levels
    SEVERITY_HIGH = "High"
    SEVERITY_MEDIUM = "Medium"
    SEVERITY_LOW = "Low"

    def __init__(self, natal_moon_rashi_num: int):
        """
        Initialize Sade Sati tracker with natal Moon's rashi position.

        Args:
            natal_moon_rashi_num: Natal Moon's rashi number (0-11)
                0 = Mesha/Aries, 1 = Vrishabha/Taurus, etc.
        """
        if not 0 <= natal_moon_rashi_num <= 11:
            raise ValueError(f"Rashi number must be 0-11, got {natal_moon_rashi_num}")

        self.natal_moon_rashi_num = natal_moon_rashi_num
        self.natal_moon_rashi = RASHIS[natal_moon_rashi_num]["name"]
        self.natal_moon_rashi_english = RASHIS[natal_moon_rashi_num]["english"]
        self.calculator = PlanetaryCalculator()

        # Calculate the three Sade Sati rashis
        self._sade_sati_rashis = self._calculate_sade_sati_rashis()

        # Cache for Saturn sign transitions
        self._transition_cache: Dict[Tuple[int, int], List[Dict]] = {}

    def _calculate_sade_sati_rashis(self) -> Dict[str, int]:
        """Calculate the three rashis involved in Sade Sati."""
        moon_rashi = self.natal_moon_rashi_num
        return {
            self.PHASE_RISING: (moon_rashi - 1) % 12,   # 12th from Moon
            self.PHASE_PEAK: moon_rashi,                # Over Moon
            self.PHASE_SETTING: (moon_rashi + 1) % 12,  # 2nd from Moon
        }

    def _get_phase_for_rashi(self, saturn_rashi_num: int) -> Optional[str]:
        """Get the Sade Sati phase for a given Saturn rashi position."""
        for phase, rashi_num in self._sade_sati_rashis.items():
            if saturn_rashi_num == rashi_num:
                return phase
        return None

    def _get_severity_for_phase(self, phase: str) -> str:
        """Get severity level based on Sade Sati phase."""
        if phase == self.PHASE_PEAK:
            return self.SEVERITY_HIGH
        elif phase in (self.PHASE_RISING, self.PHASE_SETTING):
            return self.SEVERITY_MEDIUM
        return self.SEVERITY_LOW

    def _get_saturn_rashi(self, dt: datetime) -> Tuple[int, str, str, float]:
        """
        Get Saturn's rashi position for a given date.

        Returns:
            Tuple of (rashi_num, rashi_name, rashi_english, longitude)
        """
        jd = self.calculator.datetime_to_jd(dt)
        saturn_pos = self.calculator.get_planet_position(Planet.SATURN, jd)
        return (
            saturn_pos["rashi_num"],
            saturn_pos["rashi"],
            saturn_pos["rashi_english"],
            saturn_pos["longitude"]
        )

    def _find_saturn_sign_transitions(
        self,
        start_date: datetime,
        end_date: datetime,
        precision_days: int = 1
    ) -> List[Dict]:
        """
        Find all dates when Saturn changes signs within a date range.

        Uses binary search refinement for accurate transition dates.

        Args:
            start_date: Start of search range
            end_date: End of search range
            precision_days: Final precision for transition dates

        Returns:
            List of transition dictionaries with date and sign info
        """
        transitions = []

        # Start with coarse search (weekly intervals) then refine
        current_date = start_date
        prev_rashi, prev_name, prev_english, _ = self._get_saturn_rashi(current_date)

        # Coarse search with 7-day intervals
        while current_date <= end_date:
            curr_rashi, curr_name, curr_english, _ = self._get_saturn_rashi(current_date)

            if curr_rashi != prev_rashi:
                # Refine the transition date using binary search
                transition_date = self._refine_transition_date(
                    current_date - timedelta(days=7),
                    current_date,
                    prev_rashi,
                    precision_days
                )

                # Verify the transition
                new_rashi, new_name, new_english, _ = self._get_saturn_rashi(transition_date)

                transitions.append({
                    "date": transition_date,
                    "from_rashi_num": prev_rashi,
                    "from_rashi": RASHIS[prev_rashi]["name"],
                    "from_rashi_english": RASHIS[prev_rashi]["english"],
                    "to_rashi_num": new_rashi,
                    "to_rashi": new_name,
                    "to_rashi_english": new_english,
                })

            prev_rashi, prev_name, prev_english = curr_rashi, curr_name, curr_english
            current_date += timedelta(days=7)

        return transitions

    def _refine_transition_date(
        self,
        start: datetime,
        end: datetime,
        original_rashi: int,
        precision_days: int
    ) -> datetime:
        """
        Use binary search to find precise transition date.

        Args:
            start: Date when Saturn was still in original_rashi
            end: Date when Saturn has moved to new rashi
            original_rashi: The rashi Saturn was in at start
            precision_days: Desired precision in days

        Returns:
            Precise transition date
        """
        while (end - start).days > precision_days:
            mid = start + (end - start) / 2
            mid_rashi, _, _, _ = self._get_saturn_rashi(mid)

            if mid_rashi == original_rashi:
                start = mid
            else:
                end = mid

        return end

    def is_sade_sati_active(self, date: datetime) -> Dict:
        """
        Check if Sade Sati is active on a given date.

        Args:
            date: Date to check

        Returns:
            Dictionary with:
            - active: bool - Whether Sade Sati is active
            - phase: str - Current phase (Rising/Peak/Setting) or None
            - saturn_rashi: str - Saturn's current rashi name
            - saturn_rashi_english: str - Saturn's current rashi (English)
            - saturn_rashi_num: int - Saturn's current rashi number
            - severity: str - Severity level (High/Medium/Low)
            - natal_moon_rashi: str - Natal Moon's rashi name
            - phase_description: str - Description of current phase
        """
        saturn_rashi_num, saturn_rashi, saturn_rashi_english, longitude = self._get_saturn_rashi(date)
        phase = self._get_phase_for_rashi(saturn_rashi_num)

        result = {
            "active": phase is not None,
            "phase": phase,
            "saturn_rashi": saturn_rashi,
            "saturn_rashi_english": saturn_rashi_english,
            "saturn_rashi_num": saturn_rashi_num,
            "saturn_longitude": round(longitude, 4),
            "natal_moon_rashi": self.natal_moon_rashi,
            "natal_moon_rashi_english": self.natal_moon_rashi_english,
            "severity": self._get_severity_for_phase(phase) if phase else None,
            "phase_description": self._get_phase_description(phase) if phase else None,
        }

        return result

    def _get_phase_description(self, phase: str) -> str:
        """Get a description for the current Sade Sati phase."""
        descriptions = {
            self.PHASE_RISING: (
                "Beginning of Sade Sati. Saturn transits the 12th house from Moon. "
                "Subtle challenges emerge - increased expenses, sleep disturbances, "
                "and hidden obstacles. A period of preparation for transformation."
            ),
            self.PHASE_PEAK: (
                "Peak of Sade Sati. Saturn transits directly over natal Moon. "
                "Maximum intensity - emotional challenges, health concerns, "
                "career changes, and family responsibilities. A time of major "
                "life transformation and karmic lessons."
            ),
            self.PHASE_SETTING: (
                "Final phase of Sade Sati. Saturn transits the 2nd house from Moon. "
                "Challenges begin to ease. Focus on finances, family, and speech. "
                "Integration of lessons learned and gradual return to normalcy."
            ),
        }
        return descriptions.get(phase, "")

    def get_sade_sati_periods(
        self,
        start_year: int,
        end_year: int
    ) -> List[Dict]:
        """
        Get all Sade Sati periods within a date range.

        Args:
            start_year: Start year of the range
            end_year: End year of the range

        Returns:
            List of Sade Sati periods, each containing:
            - phase: str - Phase name (Rising/Peak/Setting)
            - start_date: datetime - When this phase starts
            - end_date: datetime - When this phase ends
            - duration_days: int - Duration in days
            - duration_years: float - Duration in years
            - severity: str - Severity level
            - saturn_rashi: str - Saturn's rashi during this phase
            - saturn_rashi_english: str - Saturn's rashi (English)
        """
        start_date = datetime(start_year, 1, 1)
        end_date = datetime(end_year, 12, 31)

        # Get all Saturn sign transitions
        transitions = self._find_saturn_sign_transitions(start_date, end_date)

        periods = []

        # Get Saturn's position at start
        initial_rashi, _, _, _ = self._get_saturn_rashi(start_date)
        initial_phase = self._get_phase_for_rashi(initial_rashi)

        # If we start in a Sade Sati period, record it
        if initial_phase:
            # Find when this phase ends
            phase_end = None
            for t in transitions:
                if self._get_phase_for_rashi(t["to_rashi_num"]) != initial_phase:
                    phase_end = t["date"]
                    break

            if phase_end is None:
                phase_end = end_date

            periods.append(self._create_period_dict(
                phase=initial_phase,
                start_date=start_date,
                end_date=phase_end,
                saturn_rashi_num=initial_rashi
            ))

        # Process transitions
        for i, transition in enumerate(transitions):
            to_rashi = transition["to_rashi_num"]
            phase = self._get_phase_for_rashi(to_rashi)

            if phase:
                # Find when this phase ends
                phase_start = transition["date"]
                phase_end = None

                for j in range(i + 1, len(transitions)):
                    next_rashi = transitions[j]["to_rashi_num"]
                    next_phase = self._get_phase_for_rashi(next_rashi)
                    if next_phase != phase:
                        phase_end = transitions[j]["date"]
                        break

                if phase_end is None:
                    phase_end = end_date

                # Avoid duplicates (check if we already have this period)
                if not periods or (
                    periods[-1]["phase"] != phase or
                    periods[-1]["start_date"] != phase_start
                ):
                    periods.append(self._create_period_dict(
                        phase=phase,
                        start_date=phase_start,
                        end_date=phase_end,
                        saturn_rashi_num=to_rashi
                    ))

        return periods

    def _create_period_dict(
        self,
        phase: str,
        start_date: datetime,
        end_date: datetime,
        saturn_rashi_num: int
    ) -> Dict:
        """Create a standardized period dictionary."""
        duration_days = (end_date - start_date).days
        return {
            "phase": phase,
            "start_date": start_date,
            "end_date": end_date,
            "duration_days": duration_days,
            "duration_years": round(duration_days / 365.25, 2),
            "severity": self._get_severity_for_phase(phase),
            "saturn_rashi": RASHIS[saturn_rashi_num]["name"],
            "saturn_rashi_english": RASHIS[saturn_rashi_num]["english"],
            "saturn_rashi_num": saturn_rashi_num,
            "description": self._get_phase_description(phase),
        }

    def get_next_sade_sati(self, from_date: datetime) -> Dict:
        """
        Find when the next Sade Sati period will start.

        If currently in Sade Sati, returns the next complete cycle.

        Args:
            from_date: Date to search from

        Returns:
            Dictionary with:
            - start_date: datetime - When next Sade Sati starts
            - end_date: datetime - When next Sade Sati ends (approx.)
            - years_from_now: float - Years until it starts
            - first_phase: str - Starting phase (typically Rising)
            - saturn_entering_rashi: str - Rashi Saturn enters
        """
        current_status = self.is_sade_sati_active(from_date)

        # Search up to 30 years ahead (Saturn's full cycle)
        search_end = from_date + timedelta(days=365 * 35)

        # Get all Saturn sign transitions
        transitions = self._find_saturn_sign_transitions(from_date, search_end)

        rising_rashi = self._sade_sati_rashis[self.PHASE_RISING]
        peak_rashi = self._sade_sati_rashis[self.PHASE_PEAK]
        setting_rashi = self._sade_sati_rashis[self.PHASE_SETTING]

        # Find next entry into Rising phase (12th from Moon)
        # If currently in Sade Sati, skip past current cycle
        in_current_cycle = current_status["active"]
        found_exit = not in_current_cycle

        for transition in transitions:
            to_rashi = transition["to_rashi_num"]

            if in_current_cycle and not found_exit:
                # Wait until we exit current Sade Sati
                if self._get_phase_for_rashi(to_rashi) is None:
                    found_exit = True
                continue

            if to_rashi == rising_rashi:
                # Found next Sade Sati start
                start_date = transition["date"]

                # Estimate end date (approximately 7.5 years later)
                # Find when Saturn leaves the Setting rashi
                end_date = None
                for t in transitions:
                    if t["date"] > start_date and t["from_rashi_num"] == setting_rashi:
                        end_date = t["date"]
                        break

                if end_date is None:
                    # Approximate if not found in search range
                    end_date = start_date + timedelta(days=int(7.5 * 365.25))

                years_from_now = (start_date - from_date).days / 365.25

                return {
                    "start_date": start_date,
                    "end_date": end_date,
                    "years_from_now": round(years_from_now, 2),
                    "days_from_now": (start_date - from_date).days,
                    "first_phase": self.PHASE_RISING,
                    "saturn_entering_rashi": RASHIS[rising_rashi]["name"],
                    "saturn_entering_rashi_english": RASHIS[rising_rashi]["english"],
                    "estimated_duration_years": round((end_date - start_date).days / 365.25, 2),
                }

        return {
            "start_date": None,
            "end_date": None,
            "years_from_now": None,
            "message": "No Sade Sati found in search range (35 years)",
        }

    def get_sade_sati_timeline(self, years_ahead: int = 30) -> List[Dict]:
        """
        Generate a complete timeline of Sade Sati periods for the next N years.

        Args:
            years_ahead: Number of years to look ahead (default 30)

        Returns:
            List of complete Sade Sati cycles, each containing:
            - cycle_number: int - Sequential cycle number
            - total_start_date: datetime - When this Sade Sati begins
            - total_end_date: datetime - When this Sade Sati ends
            - total_duration_years: float - Total duration in years
            - phases: List[Dict] - Individual phase details
            - status: str - "active", "upcoming", or "completed"
        """
        from_date = datetime.now()
        end_date = from_date + timedelta(days=365 * years_ahead)

        # Get all periods
        periods = self.get_sade_sati_periods(
            from_date.year,
            from_date.year + years_ahead
        )

        if not periods:
            return []

        # Group periods into complete Sade Sati cycles
        cycles = []
        current_cycle_phases = []
        cycle_number = 1

        for period in periods:
            if period["phase"] == self.PHASE_RISING and current_cycle_phases:
                # Start of new cycle, save previous
                if current_cycle_phases:
                    cycles.append(self._create_cycle_dict(
                        cycle_number,
                        current_cycle_phases,
                        from_date
                    ))
                    cycle_number += 1
                current_cycle_phases = []

            current_cycle_phases.append(period)

        # Add final cycle
        if current_cycle_phases:
            cycles.append(self._create_cycle_dict(
                cycle_number,
                current_cycle_phases,
                from_date
            ))

        return cycles

    def _create_cycle_dict(
        self,
        cycle_number: int,
        phases: List[Dict],
        reference_date: datetime
    ) -> Dict:
        """Create a cycle summary dictionary."""
        total_start = phases[0]["start_date"]
        total_end = phases[-1]["end_date"]
        total_duration = (total_end - total_start).days / 365.25

        # Determine status
        if reference_date < total_start:
            status = "upcoming"
        elif reference_date > total_end:
            status = "completed"
        else:
            status = "active"

        return {
            "cycle_number": cycle_number,
            "total_start_date": total_start,
            "total_end_date": total_end,
            "total_duration_years": round(total_duration, 2),
            "phases": phases,
            "status": status,
            "natal_moon_rashi": self.natal_moon_rashi,
            "natal_moon_rashi_english": self.natal_moon_rashi_english,
        }

    def get_current_sade_sati_progress(self) -> Optional[Dict]:
        """
        Get detailed progress information if currently in Sade Sati.

        Returns:
            Dictionary with progress details or None if not in Sade Sati
        """
        now = datetime.now()
        status = self.is_sade_sati_active(now)

        if not status["active"]:
            return None

        # Get current cycle
        timeline = self.get_sade_sati_timeline(10)

        for cycle in timeline:
            if cycle["status"] == "active":
                total_days = (cycle["total_end_date"] - cycle["total_start_date"]).days
                elapsed_days = (now - cycle["total_start_date"]).days
                remaining_days = (cycle["total_end_date"] - now).days

                # Find current phase progress
                current_phase = None
                phase_elapsed = 0
                phase_remaining = 0

                for phase in cycle["phases"]:
                    if phase["start_date"] <= now <= phase["end_date"]:
                        current_phase = phase
                        phase_elapsed = (now - phase["start_date"]).days
                        phase_remaining = (phase["end_date"] - now).days
                        break

                return {
                    "current_phase": status["phase"],
                    "phase_details": current_phase,
                    "overall_progress_percent": round((elapsed_days / total_days) * 100, 1),
                    "phase_progress_percent": round(
                        (phase_elapsed / current_phase["duration_days"]) * 100, 1
                    ) if current_phase else 0,
                    "total_elapsed_days": elapsed_days,
                    "total_elapsed_years": round(elapsed_days / 365.25, 2),
                    "total_remaining_days": remaining_days,
                    "total_remaining_years": round(remaining_days / 365.25, 2),
                    "phase_elapsed_days": phase_elapsed,
                    "phase_remaining_days": phase_remaining,
                    "cycle_start_date": cycle["total_start_date"],
                    "cycle_end_date": cycle["total_end_date"],
                    "severity": status["severity"],
                    "saturn_position": {
                        "rashi": status["saturn_rashi"],
                        "rashi_english": status["saturn_rashi_english"],
                        "longitude": status["saturn_longitude"],
                    },
                }

        return None

    def get_remedies(self, phase: Optional[str] = None) -> Dict:
        """
        Get traditional Vedic remedies for Sade Sati.

        Args:
            phase: Specific phase to get remedies for, or None for general remedies

        Returns:
            Dictionary with remedy recommendations
        """
        general_remedies = {
            "mantras": [
                {
                    "mantra": "Om Sham Shanicharaya Namah",
                    "meaning": "Salutations to Lord Saturn",
                    "frequency": "108 times daily, especially on Saturdays",
                },
                {
                    "mantra": "Om Praam Preem Praum Sah Shanaischaraya Namah",
                    "meaning": "Beej (seed) mantra of Saturn",
                    "frequency": "108 times daily",
                },
                {
                    "mantra": "Hanuman Chalisa",
                    "meaning": "Prayer to Lord Hanuman",
                    "frequency": "Daily recitation, especially on Tuesdays and Saturdays",
                },
            ],
            "donations": [
                "Black sesame seeds (til) on Saturdays",
                "Black cloth or blanket to the needy",
                "Mustard oil",
                "Iron items",
                "Blue or black sapphire (only after proper consultation)",
            ],
            "fasting": [
                "Observe fast on Saturdays",
                "Consume only one meal after sunset",
                "Avoid salt during the fast if possible",
            ],
            "worship": [
                "Visit Shani temple on Saturdays",
                "Light mustard oil lamp under Peepal tree on Saturdays",
                "Feed crows (Saturn's vehicle) with cooked rice",
                "Worship Lord Hanuman regularly",
            ],
            "gemstone": {
                "name": "Blue Sapphire (Neelam)",
                "caution": "Must be worn only after proper astrological consultation",
                "alternative": "Amethyst or Iolite as lighter alternatives",
            },
            "lifestyle": [
                "Practice patience and humility",
                "Help the elderly and disabled",
                "Avoid disputes and litigation if possible",
                "Maintain ethical conduct in all dealings",
                "Regular meditation and spiritual practice",
            ],
        }

        phase_specific = {
            self.PHASE_RISING: {
                "focus": "Preparation and acceptance",
                "additional_remedies": [
                    "Begin the above remedies before challenges intensify",
                    "Create financial reserves",
                    "Strengthen health through proper diet and exercise",
                    "Address any pending legal or financial matters",
                ],
            },
            self.PHASE_PEAK: {
                "focus": "Endurance and transformation",
                "additional_remedies": [
                    "Intensify spiritual practices",
                    "Recite Shani Stotra daily",
                    "Perform Shani Shanti Puja",
                    "Consider wearing iron ring on middle finger (Saturday)",
                    "Be extra cautious in health matters",
                ],
            },
            self.PHASE_SETTING: {
                "focus": "Integration and recovery",
                "additional_remedies": [
                    "Continue remedies with gratitude",
                    "Focus on rebuilding finances",
                    "Express gratitude for lessons learned",
                    "Gradually reduce intensity of remedies as period ends",
                ],
            },
        }

        result = {
            "general_remedies": general_remedies,
            "important_note": (
                "These are traditional remedies. The most important remedy is "
                "righteous conduct, patience, and acceptance of karmic lessons. "
                "Sade Sati is a time for growth through challenges."
            ),
        }

        if phase and phase in phase_specific:
            result["phase_specific"] = phase_specific[phase]
        elif phase is None:
            result["phase_specific_remedies"] = phase_specific

        return result

    def get_summary(self) -> Dict:
        """
        Get a comprehensive summary of Sade Sati status and outlook.

        Returns:
            Dictionary with complete Sade Sati information
        """
        now = datetime.now()
        current_status = self.is_sade_sati_active(now)

        summary = {
            "natal_moon": {
                "rashi": self.natal_moon_rashi,
                "rashi_english": self.natal_moon_rashi_english,
                "rashi_num": self.natal_moon_rashi_num,
            },
            "sade_sati_rashis": {
                phase: {
                    "rashi_num": rashi_num,
                    "rashi": RASHIS[rashi_num]["name"],
                    "rashi_english": RASHIS[rashi_num]["english"],
                }
                for phase, rashi_num in self._sade_sati_rashis.items()
            },
            "current_status": current_status,
            "current_date": now,
        }

        if current_status["active"]:
            summary["progress"] = self.get_current_sade_sati_progress()
            summary["remedies"] = self.get_remedies(current_status["phase"])
        else:
            summary["next_sade_sati"] = self.get_next_sade_sati(now)

        return summary


def get_sade_sati_info_for_moon_sign(moon_sign: str) -> SadeSatiTracker:
    """
    Factory function to create SadeSatiTracker from Moon sign name.

    Args:
        moon_sign: Moon sign name (e.g., "Mesha", "Aries", "Vrishabha", "Taurus")

    Returns:
        SadeSatiTracker instance
    """
    # Build lookup from RASHIS
    sign_to_num = {}
    for num, data in RASHIS.items():
        sign_to_num[data["name"].lower()] = num
        sign_to_num[data["english"].lower()] = num

    moon_sign_lower = moon_sign.lower()
    if moon_sign_lower not in sign_to_num:
        valid_signs = list(set(
            [RASHIS[i]["name"] for i in range(12)] +
            [RASHIS[i]["english"] for i in range(12)]
        ))
        raise ValueError(
            f"Unknown Moon sign: {moon_sign}. "
            f"Valid signs: {', '.join(sorted(valid_signs))}"
        )

    return SadeSatiTracker(sign_to_num[moon_sign_lower])


def format_sade_sati_report(tracker: SadeSatiTracker) -> str:
    """
    Generate a formatted text report of Sade Sati status.

    Args:
        tracker: SadeSatiTracker instance

    Returns:
        Formatted text report
    """
    summary = tracker.get_summary()
    lines = []

    lines.append("=" * 60)
    lines.append("SADE SATI ANALYSIS REPORT")
    lines.append("=" * 60)
    lines.append("")

    # Natal Moon info
    natal = summary["natal_moon"]
    lines.append(f"Natal Moon Sign: {natal['rashi']} ({natal['rashi_english']})")
    lines.append("")

    # Sade Sati rashis
    lines.append("Sade Sati Affecting Signs:")
    for phase, info in summary["sade_sati_rashis"].items():
        lines.append(f"  {phase}: {info['rashi']} ({info['rashi_english']})")
    lines.append("")

    # Current status
    status = summary["current_status"]
    lines.append("-" * 40)
    if status["active"]:
        lines.append(f"STATUS: SADE SATI IS CURRENTLY ACTIVE")
        lines.append(f"Current Phase: {status['phase']}")
        lines.append(f"Severity: {status['severity']}")
        lines.append(f"Saturn in: {status['saturn_rashi']} ({status['saturn_rashi_english']})")
        lines.append("")
        lines.append("Phase Description:")
        lines.append(status['phase_description'])

        if summary.get("progress"):
            prog = summary["progress"]
            lines.append("")
            lines.append("-" * 40)
            lines.append("PROGRESS:")
            lines.append(f"Overall Progress: {prog['overall_progress_percent']}%")
            lines.append(f"Phase Progress: {prog['phase_progress_percent']}%")
            lines.append(f"Time Elapsed: {prog['total_elapsed_years']} years")
            lines.append(f"Time Remaining: {prog['total_remaining_years']} years")
    else:
        lines.append("STATUS: NO ACTIVE SADE SATI")
        lines.append(f"Saturn currently in: {status['saturn_rashi']} ({status['saturn_rashi_english']})")

        if summary.get("next_sade_sati"):
            next_ss = summary["next_sade_sati"]
            if next_ss.get("start_date"):
                lines.append("")
                lines.append("NEXT SADE SATI:")
                lines.append(f"  Starts: {next_ss['start_date'].strftime('%B %d, %Y')}")
                lines.append(f"  Years from now: {next_ss['years_from_now']}")
                lines.append(f"  Saturn enters: {next_ss['saturn_entering_rashi']}")

    lines.append("")
    lines.append("=" * 60)

    return "\n".join(lines)
