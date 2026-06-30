"""
Hindi Kundali HTML Generator
Generate beautiful kundali reports in Hindi
"""

import os
from datetime import datetime
from src.kundali import create_kundali
from src.html_generator import generate_kundali_html


def generate_hindi_kundali(
    name: str,
    year: int, month: int, day: int,
    hour: int, minute: int,
    city: str = "Delhi",
    latitude: float = None,
    longitude: float = None,
    output_folder: str = None
) -> str:
    """
    Generate Hindi Kundali HTML report.

    Args:
        name: Person's name
        year, month, day: Birth date
        hour, minute: Birth time (24-hour format)
        city: Birth city
        latitude, longitude: Coordinates (optional, auto-detected from city)
        output_folder: Folder to save HTML (default: same as script)

    Returns:
        Path to generated HTML file
    """
    print("\n" + "=" * 50)
    print("    हिंदी कुंडली जनरेटर")
    print("    Swiss Ephemeris (NASA JPL DE431)")
    print("=" * 50)

    # Create kundali
    print(f"\nकुंडली बना रहे हैं: {name}...")

    if latitude and longitude:
        kundali = create_kundali(
            name=name,
            year=year, month=month, day=day,
            hour=hour, minute=minute,
            city=city,
            latitude=latitude,
            longitude=longitude
        )
    else:
        kundali = create_kundali(
            name=name,
            year=year, month=month, day=day,
            hour=hour, minute=minute,
            city=city
        )

    # Generate output path
    if output_folder is None:
        output_folder = os.path.dirname(os.path.abspath(__file__))

    safe_name = "".join(c if c.isalnum() else "_" for c in name)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"Kundali_{safe_name}_{timestamp}.html"
    output_path = os.path.join(output_folder, filename)

    # Generate HTML
    generate_kundali_html(kundali, output_path)

    print(f"\n✅ कुंडली सफलतापूर्वक बनाई गई!")
    print(f"📄 फाइल: {output_path}")
    print("\nब्राउज़र में खोलने के लिए फाइल पर डबल-क्लिक करें।")

    return output_path


def interactive_mode():
    """Interactive mode for generating kundali."""
    print("\n" + "=" * 50)
    print("    हिंदी कुंडली जनरेटर - Interactive Mode")
    print("=" * 50)

    print("\nजन्म विवरण दर्ज करें:")

    name = input("नाम (Name): ").strip() or "अज्ञात"

    print("\nजन्म तिथि:")
    year = int(input("  वर्ष (Year, e.g., 1990): "))
    month = int(input("  महीना (Month, 1-12): "))
    day = int(input("  दिन (Day, 1-31): "))

    print("\nजन्म समय (24-hour format):")
    hour = int(input("  घंटा (Hour, 0-23): "))
    minute = int(input("  मिनट (Minute, 0-59): "))

    city = input("\nजन्म स्थान (City, e.g., Delhi): ").strip() or "Delhi"

    use_coords = input("\nक्या आप coordinates देना चाहते हैं? (y/n): ").strip().lower()
    if use_coords == 'y':
        latitude = float(input("  Latitude (e.g., 28.6139): "))
        longitude = float(input("  Longitude (e.g., 77.2090): "))
    else:
        latitude = None
        longitude = None

    return generate_hindi_kundali(
        name=name,
        year=year, month=month, day=day,
        hour=hour, minute=minute,
        city=city,
        latitude=latitude,
        longitude=longitude
    )


def example_kundali():
    """Generate an example kundali."""
    return generate_hindi_kundali(
        name="उदाहरण व्यक्ति",
        year=1990, month=5, day=15,
        hour=10, minute=30,
        city="Delhi",
        latitude=28.6139,
        longitude=77.2090
    )


if __name__ == "__main__":
    print("\nविकल्प चुनें:")
    print("  1. उदाहरण कुंडली (Example)")
    print("  2. अपनी कुंडली बनाएं (Interactive)")

    choice = input("\nचुनाव (1 या 2): ").strip()

    if choice == "2":
        interactive_mode()
    else:
        example_kundali()
