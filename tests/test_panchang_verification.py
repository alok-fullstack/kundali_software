"""
Verification tests for Panchang calculations.
Tests the accuracy of Tithi, Yoga, Nakshatra, and Karana formulas.
"""

import sys
sys.path.insert(0, '..')

from datetime import datetime
from src.panchang import PanchangCalculator


def verify_tithi_formula():
    """Verify Tithi = (Moon - Sun) / 12 degrees"""
    print("\n=== TITHI FORMULA VERIFICATION ===")
    print("Formula: Tithi = (Moon_longitude - Sun_longitude) / 12")

    calc = PanchangCalculator()

    # Test with manual calculation
    # Note: Tithi N spans from (N-1)*12 to N*12 degrees
    # So at exactly 12 degrees, we're at boundary = Tithi 2
    test_cases = [
        # (sun_long, moon_long, expected_tithi)
        (0, 0, 1),       # 0 deg diff = Tithi 1 (Pratipada)
        (0, 11.9, 1),    # Tithi 1 (just before boundary)
        (0, 12, 2),      # 12 deg diff = Tithi 2 (at boundary)
        (0, 168, 15),    # 168 deg = Tithi 15 (approaching Purnima)
        (0, 180, 16),    # 180 deg = Tithi 16 (Krishna Pratipada)
        (0, 90, 8),      # 90 deg = Tithi 8
        (0, 84, 8),      # 84 deg = Tithi 8 (7*12=84)
    ]

    all_passed = True
    for sun, moon, expected in test_cases:
        angle_diff = (moon - sun) % 360
        tithi = int(angle_diff / 12) + 1
        if tithi != expected:
            print(f"  FAIL: Sun={sun}, Moon={moon}, Expected tithi {expected}, Got {tithi}")
            all_passed = False

    if all_passed:
        print("  Formula verification: PASSED")

    return all_passed


def verify_yoga_formula():
    """Verify Yoga = (Sun + Moon) / (360/27) degrees"""
    print("\n=== YOGA FORMULA VERIFICATION ===")
    print("Formula: Yoga = (Sun_longitude + Moon_longitude) / 13.333...")

    # Test with manual calculation
    test_cases = [
        # (sun_long, moon_long, expected_yoga 1-27)
        (0, 0, 1),       # Yoga 1 (Vishkumbha)
        (0, 13.33, 1),   # Still Yoga 1
        (0, 13.34, 2),   # Yoga 2
        (180, 180, 1),   # 360 mod 360 = 0, Yoga 1
    ]

    yoga_span = 360 / 27  # 13.333...
    all_passed = True
    for sun, moon, expected in test_cases:
        angle_sum = (sun + moon) % 360
        yoga = int(angle_sum / yoga_span) + 1
        if yoga != expected:
            print(f"  FAIL: Sun={sun}, Moon={moon}, Expected yoga {expected}, Got {yoga}")
            all_passed = False

    if all_passed:
        print("  Formula verification: PASSED")

    return all_passed


def verify_range_constraints():
    """Verify all Panchang elements are within valid ranges"""
    print("\n=== RANGE CONSTRAINT VERIFICATION ===")

    calc = PanchangCalculator()
    test_dates = [
        datetime(2026, 6, 26, 12, 0, 0),   # Today
        datetime(2024, 1, 1, 12, 0, 0),    # Historical
        datetime(2023, 4, 15, 18, 30, 0),  # Historical
        datetime(2020, 11, 14, 6, 0, 0),   # Historical
        datetime(2025, 3, 20, 12, 0, 0),   # Equinox
    ]

    issues = []
    for dt in test_dates:
        try:
            panchang = calc.get_panchang(dt)

            # Check Tithi range (1-30)
            if not (1 <= panchang.tithi.number <= 30):
                issues.append(f"  {dt}: Tithi {panchang.tithi.number} out of range [1-30]")

            # Check Yoga range (1-27)
            if not (1 <= panchang.yoga.number <= 27):
                issues.append(f"  {dt}: Yoga {panchang.yoga.number} out of range [1-27]")

            # Check Nakshatra range (0-26)
            if not (0 <= panchang.nakshatra_num <= 26):
                issues.append(f"  {dt}: Nakshatra {panchang.nakshatra_num} out of range [0-26]")

            # Check Karana range (1-11)
            if not (1 <= panchang.karana.number <= 11):
                issues.append(f"  {dt}: Karana {panchang.karana.number} out of range [1-11]")

            # Check Vara range (0-6)
            if not (0 <= panchang.vara.number <= 6):
                issues.append(f"  {dt}: Vara {panchang.vara.number} out of range [0-6]")

            # Check Nakshatra Pada range (1-4)
            if not (1 <= panchang.nakshatra_pada <= 4):
                issues.append(f"  {dt}: Nakshatra Pada {panchang.nakshatra_pada} out of range [1-4]")

            # Check Paksha is valid
            if panchang.tithi.paksha not in ["Shukla", "Krishna"]:
                issues.append(f"  {dt}: Invalid Paksha '{panchang.tithi.paksha}'")

            # Check longitude ranges (0-360)
            if not (0 <= panchang.moon_longitude < 360):
                issues.append(f"  {dt}: Moon longitude {panchang.moon_longitude} out of range [0-360)")
            if not (0 <= panchang.sun_longitude < 360):
                issues.append(f"  {dt}: Sun longitude {panchang.sun_longitude} out of range [0-360)")

        except Exception as e:
            issues.append(f"  {dt}: Exception - {str(e)}")

    if issues:
        print("  Issues found:")
        for issue in issues:
            print(issue)
        return False
    else:
        print(f"  All {len(test_dates)} test dates PASSED range validation")
        return True


def calculate_panchang_for_dates():
    """Calculate and display Panchang for today and historical dates"""
    print("\n=== PANCHANG CALCULATION RESULTS ===")

    calc = PanchangCalculator()
    test_dates = [
        ("Today (2026-06-26)", datetime(2026, 6, 26, 12, 0, 0)),
        ("Historical (2024-01-01)", datetime(2024, 1, 1, 12, 0, 0)),
        ("Historical (2023-04-15)", datetime(2023, 4, 15, 18, 30, 0)),
    ]

    for label, dt in test_dates:
        print(f"\n--- {label} ---")
        try:
            p = calc.get_panchang(dt)
            print(f"  Date: {dt.strftime('%Y-%m-%d %H:%M')}")
            print(f"  Vara: {p.vara.english}")
            print(f"  Tithi: {p.tithi.number} - {p.tithi.name} ({p.tithi.paksha} Paksha)")
            print(f"  Nakshatra: {p.nakshatra_num} - {p.nakshatra} (Pada {p.nakshatra_pada})")
            print(f"  Yoga: {p.yoga.number} - {p.yoga.name}")
            print(f"  Karana: {p.karana.number} - {p.karana.name}")
            print(f"  Moon: {p.moon_longitude:.4f}deg in {p.moon_rashi}")
            print(f"  Sun: {p.sun_longitude:.4f}deg")
            print(f"  Ayanamsa (Lahiri): {p.ayanamsa:.6f}deg")
        except Exception as e:
            print(f"  ERROR: {str(e)}")


def verify_consistency():
    """Verify internal consistency of calculations"""
    print("\n=== INTERNAL CONSISTENCY CHECKS ===")

    calc = PanchangCalculator()
    dt = datetime(2026, 6, 26, 12, 0, 0)
    p = calc.get_panchang(dt)

    issues = []

    # Verify Tithi-Paksha consistency
    if p.tithi.number <= 15 and p.tithi.paksha != "Shukla":
        issues.append(f"  Tithi {p.tithi.number} should be Shukla Paksha")
    if p.tithi.number > 15 and p.tithi.paksha != "Krishna":
        issues.append(f"  Tithi {p.tithi.number} should be Krishna Paksha")

    # Verify Nakshatra-Moon longitude consistency
    nakshatra_span = 360 / 27
    expected_nakshatra = int(p.moon_longitude / nakshatra_span) % 27
    if expected_nakshatra != p.nakshatra_num:
        issues.append(f"  Nakshatra inconsistent: Moon at {p.moon_longitude}deg, expected nakshatra {expected_nakshatra}, got {p.nakshatra_num}")

    # Verify Yoga calculation consistency
    angle_sum = (p.sun_longitude + p.moon_longitude) % 360
    yoga_span = 360 / 27
    expected_yoga = int(angle_sum / yoga_span) + 1
    if expected_yoga != p.yoga.number:
        issues.append(f"  Yoga inconsistent: Sum={angle_sum:.4f}deg, expected yoga {expected_yoga}, got {p.yoga.number}")

    # Verify Tithi calculation consistency
    angle_diff = (p.moon_longitude - p.sun_longitude) % 360
    expected_tithi = int(angle_diff / 12) + 1
    if expected_tithi != p.tithi.number:
        issues.append(f"  Tithi inconsistent: Diff={angle_diff:.4f}deg, expected tithi {expected_tithi}, got {p.tithi.number}")

    if issues:
        print("  Issues found:")
        for issue in issues:
            print(issue)
        return False
    else:
        print("  All consistency checks PASSED")
        return True


def main():
    """Run all verification tests"""
    print("=" * 60)
    print("PANCHANG CALCULATION VERIFICATION TEST SUITE")
    print("=" * 60)

    results = {
        "tithi_formula": verify_tithi_formula(),
        "yoga_formula": verify_yoga_formula(),
        "range_constraints": verify_range_constraints(),
        "consistency": verify_consistency(),
    }

    calculate_panchang_for_dates()

    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    all_passed = all(results.values())
    for test_name, passed in results.items():
        status = "PASS" if passed else "FAIL"
        print(f"  {test_name}: {status}")

    print("-" * 60)
    if all_passed:
        print("ALL TESTS PASSED")
    else:
        print("SOME TESTS FAILED - Review issues above")

    return 0 if all_passed else 1


if __name__ == "__main__":
    exit(main())
