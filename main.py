"""
Kundali Software - Main Entry Point
High-accuracy Vedic Astrology calculator using Swiss Ephemeris

Usage:
    python main.py

Or import and use programmatically:
    from src.kundali import create_kundali
    kundali = create_kundali("Name", 1990, 1, 15, 10, 30, "Mumbai")
    kundali.print_kundali()
"""

from datetime import datetime
from src.kundali import create_kundali, Kundali, BirthData


def example_kundali():
    """Generate an example kundali."""
    print("\n" + "=" * 60)
    print("       KUNDALI SOFTWARE v1.0")
    print("       Swiss Ephemeris Based (NASA JPL DE431)")
    print("       Accuracy: < 0.001 arc-second")
    print("=" * 60)

    # Example: Create kundali for a sample birth
    # You can change these values
    kundali = create_kundali(
        name="Example Person",
        year=1990,
        month=5,
        day=15,
        hour=10,
        minute=30,
        city="Delhi",
        timezone="Asia/Kolkata"
    )

    # Print full kundali
    kundali.print_kundali()

    # Get planets in houses
    print("\n" + "-" * 40)
    print("BHAVA CHART (Planets in Houses)")
    print("-" * 40)
    planets_in_houses = kundali.get_planets_in_houses()
    for house_num, planets in planets_in_houses.items():
        if planets:
            print(f"  House {house_num:2d}: {', '.join(planets)}")

    # Get Mahadasha timeline
    print("\n" + "-" * 40)
    print("MAHADASHA TIMELINE")
    print("-" * 40)
    mahadashas = kundali.get_mahadashas(years=80)
    for maha in mahadashas[:10]:  # Show first 10
        print(f"  {maha.planet:8} : {maha.start_date.strftime('%Y-%m-%d')} to {maha.end_date.strftime('%Y-%m-%d')} ({maha.duration_years:.1f} years)")

    return kundali


def interactive_mode():
    """Interactive CLI for generating kundali."""
    print("\n" + "=" * 60)
    print("       KUNDALI SOFTWARE - Interactive Mode")
    print("=" * 60)

    name = input("\nEnter name: ").strip() or "User"

    print("\nEnter birth date:")
    year = int(input("  Year (e.g., 1990): "))
    month = int(input("  Month (1-12): "))
    day = int(input("  Day (1-31): "))

    print("\nEnter birth time (24-hour format):")
    hour = int(input("  Hour (0-23): "))
    minute = int(input("  Minute (0-59): "))

    city = input("\nEnter birth city (e.g., Delhi, Mumbai): ").strip() or "Delhi"

    print("\nGenerating Kundali...")

    try:
        kundali = create_kundali(
            name=name,
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute,
            city=city,
            timezone="Asia/Kolkata"
        )

        kundali.print_kundali()

        # Show Mahadasha timeline
        print("\n" + "-" * 40)
        print("MAHADASHA TIMELINE (Next 80 years)")
        print("-" * 40)
        mahadashas = kundali.get_mahadashas(years=80)
        for maha in mahadashas[:12]:
            print(f"  {maha.planet:8} : {maha.start_date.strftime('%Y-%m-%d')} to {maha.end_date.strftime('%Y-%m-%d')}")

        return kundali

    except Exception as e:
        print(f"\nError generating kundali: {e}")
        return None


def main():
    """Main entry point."""
    print("\nSelect mode:")
    print("  1. Example Kundali")
    print("  2. Interactive Mode (Enter your details)")

    choice = input("\nEnter choice (1 or 2): ").strip()

    if choice == "2":
        interactive_mode()
    else:
        example_kundali()


if __name__ == "__main__":
    main()
