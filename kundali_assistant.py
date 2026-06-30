"""
Kundali AI Assistant - Interactive Q&A
Ask questions about your kundali in Hindi or English
"""

import re
from datetime import datetime
from src.kundali import create_kundali
from src.config import RASHIS, PLANET_NAMES, Planet, BHAVA_NAMES
from src.predictions import (
    GRAHA_BHAVA_PHAL, CAREER_BY_LAGNA, MARRIAGE_PREDICTIONS,
    CHILDREN_PREDICTIONS, HEALTH_PREDICTIONS, DASHA_EFFECTS
)


class KundaliAssistant:
    """Interactive AI Assistant for Kundali Q&A"""

    def __init__(self, name, year, month, day, hour, minute, city, latitude=None, longitude=None):
        print("\n" + "=" * 60)
        print("    KUNDALI AI ASSISTANT")
        print("    Loading your horoscope...")
        print("=" * 60)

        if latitude and longitude:
            self.kundali = create_kundali(
                name=name, year=year, month=month, day=day,
                hour=hour, minute=minute, city=city,
                latitude=latitude, longitude=longitude
            )
        else:
            self.kundali = create_kundali(
                name=name, year=year, month=month, day=day,
                hour=hour, minute=minute, city=city
            )

        self.name = name
        self.planets_in_houses = self.kundali.get_planets_in_houses()
        self.mahadashas = self.kundali.get_mahadashas(years=100)
        self.current_dasha = self.kundali.get_current_dasha()

        # Calculate house rashis
        lagna_num = self.kundali.lagna["rashi_num"]
        self.house_rashis = {}
        for i in range(1, 13):
            rashi_num = (lagna_num + i - 1) % 12
            self.house_rashis[i] = RASHIS[rashi_num]["name"]

        print(f"\nNamaste {name}! Main aapka Kundali Assistant hoon.")
        print(f"Aapka Lagna: {self.kundali.lagna['rashi']} ({self.kundali.lagna['rashi_english']})")
        print(f"Moon Sign: {self.kundali.planets['MOON']['rashi']}")
        print(f"Current Dasha: {self.current_dasha['full_dasha']}")
        print("\nAap mujhse kuch bhi puch sakte ho!")
        print("Type 'quit' or 'exit' to end.\n")

    def get_response(self, question):
        """Process question and return appropriate response"""
        q = question.lower().strip()

        # Exit commands
        if q in ['quit', 'exit', 'bye', 'q', 'band karo', 'bas']:
            return "EXIT"

        # Career questions
        if any(word in q for word in ['career', 'job', 'naukri', 'kaam', 'profession', 'business', 'vyapar', 'vyavsay', 'rojgar']):
            return self.get_career_answer()

        # Marriage questions
        if any(word in q for word in ['marriage', 'shaadi', 'vivah', 'wife', 'husband', 'patni', 'pati', 'partner', 'love', 'pyar', 'relationship']):
            return self.get_marriage_answer()

        # Children questions
        if any(word in q for word in ['children', 'child', 'bachche', 'bachcha', 'santan', 'baby', 'kids', 'putra', 'putri', 'beti', 'beta']):
            return self.get_children_answer()

        # Health questions
        if any(word in q for word in ['health', 'swasthya', 'sehat', 'bimari', 'disease', 'illness', 'doctor', 'medical', 'fit', 'body']):
            return self.get_health_answer()

        # Money/Wealth questions
        if any(word in q for word in ['money', 'paisa', 'dhan', 'wealth', 'income', 'salary', 'rich', 'amir', 'property', 'sampatti', 'finance']):
            return self.get_wealth_answer()

        # Dasha questions
        if any(word in q for word in ['dasha', 'mahadasha', 'antardasha', 'period', 'time', 'samay', 'kab', 'when', 'future']):
            return self.get_dasha_answer()

        # Lagna/Ascendant questions
        if any(word in q for word in ['lagna', 'ascendant', 'rising', 'personality', 'nature', 'swabhav']):
            return self.get_lagna_answer()

        # Planet questions
        if any(word in q for word in ['planet', 'graha', 'sun', 'moon', 'mars', 'mercury', 'jupiter', 'venus', 'saturn', 'rahu', 'ketu',
                                       'surya', 'chandra', 'mangal', 'budh', 'guru', 'shukra', 'shani']):
            return self.get_planet_answer(q)

        # Moon sign questions
        if any(word in q for word in ['rashi', 'moon sign', 'chandra rashi', 'zodiac']):
            return self.get_rashi_answer()

        # Education questions
        if any(word in q for word in ['education', 'padhai', 'shiksha', 'study', 'college', 'degree', 'exam']):
            return self.get_education_answer()

        # Foreign/Travel questions
        if any(word in q for word in ['foreign', 'videsh', 'abroad', 'travel', 'yatra', 'immigration', 'visa']):
            return self.get_foreign_answer()

        # Lucky things
        if any(word in q for word in ['lucky', 'shubh', 'color', 'rang', 'number', 'ank', 'day', 'din', 'gemstone', 'ratna', 'stone']):
            return self.get_lucky_answer()

        # General/Summary
        if any(word in q for word in ['summary', 'overall', 'general', 'kundali', 'horoscope', 'chart', 'batao', 'tell']):
            return self.get_summary_answer()

        # Default response
        return self.get_default_answer()

    def get_career_answer(self):
        lagna = self.kundali.lagna['rashi']
        tenth_rashi = self.house_rashis[10]
        tenth_planets = self.planets_in_houses.get(10, [])
        second_planets = self.planets_in_houses.get(2, [])

        response = f"""
CAREER ANALYSIS:

Aapka Lagna: {lagna}
Suitable Fields: {CAREER_BY_LAGNA.get(lagna, 'Various fields')}

10th House (Career): {tenth_rashi}
"""
        if tenth_planets:
            response += f"10th House mein Planets: {', '.join(tenth_planets)}\n"
            for p in tenth_planets:
                response += f"  - {p}: {GRAHA_BHAVA_PHAL[p][10]}\n"
        else:
            response += "10th House khali hai - 10th lord ki position important hai\n"

        if second_planets:
            response += f"\n2nd House (Wealth from work): {', '.join(second_planets)}\n"
            response += "4 planets 2nd house mein = Multiple income sources!\n"

        # Saturn position for career timing
        saturn_house = None
        for h, planets in self.planets_in_houses.items():
            if "SATURN" in planets:
                saturn_house = h
                break

        if saturn_house:
            response += f"\nShani {saturn_house}th house mein: {GRAHA_BHAVA_PHAL['SATURN'][saturn_house]}\n"

        # Current dasha effect on career
        maha = self.current_dasha['mahadasha']['planet']
        response += f"\nCurrent {maha} Mahadasha: {DASHA_EFFECTS.get(maha, '')}\n"

        return response

    def get_marriage_answer(self):
        seventh_rashi = self.house_rashis[7]
        seventh_planets = self.planets_in_houses.get(7, [])
        venus_house = None
        for h, planets in self.planets_in_houses.items():
            if "VENUS" in planets:
                venus_house = h
                break

        response = f"""
MARRIAGE ANALYSIS:

7th House (Marriage): {seventh_rashi}
{MARRIAGE_PREDICTIONS.get(seventh_rashi, '')}

"""
        if seventh_planets:
            response += f"7th House mein Planets: {', '.join(seventh_planets)}\n"
            for p in seventh_planets:
                response += f"  - {p}: {GRAHA_BHAVA_PHAL[p][7]}\n"
        else:
            response += "7th House khali hai - 7th lord (Jupiter for you) ki position dekho\n"

        if venus_house:
            response += f"\nShukra (Marriage karaka) {venus_house}th house mein:\n"
            response += f"  {GRAHA_BHAVA_PHAL['VENUS'][venus_house]}\n"

        # Marriage timing
        response += "\nMARRIAGE TIMING:\n"
        response += "Jupiter Mahadasha (current) mein vivah yogya samay:\n"
        response += "  - Jupiter-Saturn antardasha (2024-2027)\n"
        response += "  - Saturn Mahadasha start (2026+) bhi shubh\n"

        return response

    def get_children_answer(self):
        fifth_rashi = self.house_rashis[5]
        fifth_planets = self.planets_in_houses.get(5, [])

        response = f"""
CHILDREN ANALYSIS:

5th House (Children): {fifth_rashi}
{CHILDREN_PREDICTIONS.get(fifth_rashi, '')}

"""
        if fifth_planets:
            response += f"5th House mein Planets: {', '.join(fifth_planets)}\n"
            for p in fifth_planets:
                response += f"  - {p}: {GRAHA_BHAVA_PHAL[p][5]}\n"

        # Jupiter position (putra karaka)
        jupiter_house = None
        for h, planets in self.planets_in_houses.items():
            if "JUPITER" in planets:
                jupiter_house = h
                break

        if jupiter_house:
            response += f"\nGuru (Putra Karaka) {jupiter_house}nd house mein:\n"
            response += f"  {GRAHA_BHAVA_PHAL['JUPITER'][jupiter_house]}\n"

        response += """
CHILDREN TIMING:
  - Saturn 5th mein = Thodi deri ho sakti hai
  - But Saturn in own sign = Eventually good children
  - Best time: Saturn Mahadasha ke baad (2030+)
"""
        return response

    def get_health_answer(self):
        lagna = self.kundali.lagna['rashi']
        sixth_planets = self.planets_in_houses.get(6, [])
        eighth_planets = self.planets_in_houses.get(8, [])

        response = f"""
HEALTH ANALYSIS:

Lagna: {lagna}
{HEALTH_PREDICTIONS.get(lagna, '')}

"""
        if sixth_planets:
            response += f"6th House (Disease): {', '.join(sixth_planets)}\n"
            for p in sixth_planets:
                response += f"  - {p}: {GRAHA_BHAVA_PHAL[p][6]}\n"

        if eighth_planets:
            response += f"\n8th House (Longevity): {', '.join(eighth_planets)}\n"

        response += """
HEALTH TIPS:
  - Moon 6th mein = Mental health ka dhyan rakho
  - Meditation aur yoga karo
  - Stress se bache
  - Pani paryapt piyo
  - Digestive system ka khayal rakho (Kanya lagna)
"""
        return response

    def get_wealth_answer(self):
        second_planets = self.planets_in_houses.get(2, [])
        eleventh_planets = self.planets_in_houses.get(11, [])

        response = f"""
WEALTH ANALYSIS:

2nd House (Wealth): {', '.join(second_planets) if second_planets else 'Empty'}
11th House (Income/Gains): {', '.join(eleventh_planets) if eleventh_planets else 'Empty'}

"""
        if second_planets:
            response += "2nd House mein 4 Planets = EXCELLENT DHANA YOGA!\n"
            for p in second_planets:
                response += f"  - {p}: {GRAHA_BHAVA_PHAL[p][2]}\n"

        response += """
WEALTH PREDICTION:
  - Multiple income sources possible
  - 30+ age ke baad income badhegi
  - Property se labh (Saturn 5th + Mars 2nd)
  - Side business se extra income
  - Saturn Mahadasha (2026+) mein financial stability
"""
        return response

    def get_dasha_answer(self):
        response = f"""
DASHA ANALYSIS:

CURRENT DASHA: {self.current_dasha['full_dasha']}

Mahadasha: {self.current_dasha['mahadasha']['planet']}
  From: {self.current_dasha['mahadasha']['start'].strftime('%d-%m-%Y')}
  To: {self.current_dasha['mahadasha']['end'].strftime('%d-%m-%Y')}

Antardasha: {self.current_dasha['antardasha']['planet']}
  From: {self.current_dasha['antardasha']['start'].strftime('%d-%m-%Y')}
  To: {self.current_dasha['antardasha']['end'].strftime('%d-%m-%Y')}

MAHADASHA TIMELINE:
"""
        for m in self.mahadashas[:8]:
            marker = " <-- CURRENT" if m.planet == self.current_dasha['mahadasha']['planet'] else ""
            response += f"  {m.planet:8}: {m.start_date.strftime('%Y')} - {m.end_date.strftime('%Y')} ({m.duration_years:.0f} yrs){marker}\n"

        maha = self.current_dasha['mahadasha']['planet']
        response += f"\n{maha} MAHADASHA EFFECT:\n{DASHA_EFFECTS.get(maha, '')}\n"

        return response

    def get_lagna_answer(self):
        lagna = self.kundali.lagna
        lagna_planets = self.planets_in_houses.get(1, [])

        response = f"""
LAGNA (ASCENDANT) ANALYSIS:

Lagna Rashi: {lagna['rashi']} ({lagna['rashi_english']})
Lagna Degree: {lagna['rashi_degree']:.2f}
Lagna Nakshatra: {lagna['nakshatra']} Pada {lagna['pada']}

"""
        if lagna_planets:
            response += f"Lagna mein Planets: {', '.join(lagna_planets)}\n"
            for p in lagna_planets:
                response += f"  - {p}: {GRAHA_BHAVA_PHAL[p][1]}\n"

        response += """
KANYA LAGNA CHARACTERISTICS:
  - Analytical aur detail-oriented
  - Perfectionist nature
  - Health conscious
  - Practical thinking
  - Service-oriented
  - Good at problem solving
  - Mercury ruled = Communication skills
"""
        return response

    def get_planet_answer(self, question):
        # Find which planet is being asked about
        planet_map = {
            'sun': 'SUN', 'surya': 'SUN',
            'moon': 'MOON', 'chandra': 'MOON',
            'mars': 'MARS', 'mangal': 'MARS',
            'mercury': 'MERCURY', 'budh': 'MERCURY',
            'jupiter': 'JUPITER', 'guru': 'JUPITER',
            'venus': 'VENUS', 'shukra': 'VENUS',
            'saturn': 'SATURN', 'shani': 'SATURN',
            'rahu': 'RAHU',
            'ketu': 'KETU'
        }

        asked_planet = None
        for key, value in planet_map.items():
            if key in question:
                asked_planet = value
                break

        if asked_planet:
            data = self.kundali.planets[asked_planet]
            # Find house
            planet_house = None
            for h, planets in self.planets_in_houses.items():
                if asked_planet in planets:
                    planet_house = h
                    break

            hindi_name = PLANET_NAMES[Planet[asked_planet]]['hindi']
            response = f"""
{asked_planet} ({hindi_name}) ANALYSIS:

Position: {data['rashi']} at {data['rashi_degree']:.2f}
Nakshatra: {data['nakshatra']} Pada {data['pada']}
House: {planet_house}
Retrograde: {'Yes (Vakri)' if data['is_retrograde'] else 'No (Margi)'}

Effect in House {planet_house}:
{GRAHA_BHAVA_PHAL[asked_planet][planet_house]}
"""
            return response

        # General planet overview
        response = "ALL PLANETS OVERVIEW:\n\n"
        for name, data in self.kundali.planets.items():
            planet_house = None
            for h, planets in self.planets_in_houses.items():
                if name in planets:
                    planet_house = h
                    break
            retro = " (R)" if data['is_retrograde'] else ""
            response += f"{name:10}: {data['rashi']:12} House {planet_house}{retro}\n"

        return response

    def get_rashi_answer(self):
        moon = self.kundali.planets['MOON']
        sun = self.kundali.planets['SUN']

        response = f"""
RASHI ANALYSIS:

CHANDRA RASHI (Moon Sign): {moon['rashi']}
  - Nakshatra: {moon['nakshatra']} Pada {moon['pada']}
  - This is your emotional nature
  - Used for daily/monthly predictions

SURYA RASHI (Sun Sign): {sun['rashi']}
  - Western astrology uses this
  - Your core identity

LAGNA RASHI: {self.kundali.lagna['rashi']}
  - Most important in Vedic astrology
  - Your physical self and life path

Aap {moon['rashi']} Rashi ke ho (Moon Sign based).
"""
        return response

    def get_education_answer(self):
        fourth_planets = self.planets_in_houses.get(4, [])
        fifth_planets = self.planets_in_houses.get(5, [])
        ninth_planets = self.planets_in_houses.get(9, [])

        response = f"""
EDUCATION ANALYSIS:

4th House (Basic Education): {self.house_rashis[4]}
  Planets: {', '.join(fourth_planets) if fourth_planets else 'Empty'}

5th House (Intelligence): {self.house_rashis[5]}
  Planets: {', '.join(fifth_planets) if fifth_planets else 'Empty'}

9th House (Higher Education): {self.house_rashis[9]}
  Planets: {', '.join(ninth_planets) if ninth_planets else 'Empty'}

EDUCATION PREDICTION:
  - Mercury + Jupiter 2nd mein = Good education
  - Saturn 5th mein = May need extra effort
  - But Saturn in own sign = Eventually successful
  - Technical/Analytical subjects favored (Kanya Lagna)
  - IT, Science, Commerce suitable
"""
        return response

    def get_foreign_answer(self):
        twelfth_planets = self.planets_in_houses.get(12, [])
        ninth_planets = self.planets_in_houses.get(9, [])
        rahu_house = None
        for h, planets in self.planets_in_houses.items():
            if "RAHU" in planets:
                rahu_house = h
                break

        response = f"""
FOREIGN/TRAVEL ANALYSIS:

9th House (Long Travel): {self.house_rashis[9]}
  Planets: {', '.join(ninth_planets) if ninth_planets else 'Empty'}

12th House (Foreign Land): {self.house_rashis[12]}
  Planets: {', '.join(twelfth_planets) if twelfth_planets else 'Empty'}

Rahu Position: House {rahu_house}
  Rahu indicates foreign connections

FOREIGN PREDICTION:
  - Ketu 9th mein = Previous life foreign karma
  - Rahu 3rd mein = Foreign communication/work possible
  - 12th house empty = Not strong foreign settlement yoga
  - But work-related foreign travel possible
  - Rahu Mahadasha already passed (1993-2010)
"""
        return response

    def get_lucky_answer(self):
        lagna = self.kundali.lagna['rashi']
        moon_rashi = self.kundali.planets['MOON']['rashi']

        lucky_data = {
            'Kanya': {
                'color': 'Green, Light Yellow',
                'number': '5, 14, 23',
                'day': 'Wednesday (Budhwar)',
                'stone': 'Emerald (Panna)',
                'metal': 'Bronze',
                'direction': 'North'
            }
        }

        data = lucky_data.get(lagna, {})
        response = f"""
LUCKY ELEMENTS (Kanya Lagna):

Lucky Colors: {data.get('color', 'Green')}
Lucky Numbers: {data.get('number', '5')}
Lucky Day: {data.get('day', 'Wednesday')}
Lucky Stone: {data.get('stone', 'Emerald')}
Lucky Metal: {data.get('metal', 'Bronze')}
Lucky Direction: {data.get('direction', 'North')}

RECOMMENDED GEMSTONES:
  - Primary: Panna (Emerald) for Mercury
  - Secondary: Neelam (Blue Sapphire) for Saturn - ONLY after trial
  - Alternative: Peridot for budget option

MANTRA:
  - Om Budhaya Namaha (Mercury)
  - Om Sham Shanicharaya Namaha (Saturn)
"""
        return response

    def get_summary_answer(self):
        response = f"""
KUNDALI SUMMARY - {self.name}

BASIC INFO:
  Lagna: {self.kundali.lagna['rashi']} ({self.kundali.lagna['rashi_english']})
  Moon Sign: {self.kundali.planets['MOON']['rashi']}
  Nakshatra: {self.kundali.planets['MOON']['nakshatra']}
  Sun Sign: {self.kundali.planets['SUN']['rashi']}
  Current Dasha: {self.current_dasha['full_dasha']}

SPECIAL YOGAS:
  - Budhaditya Yoga (Sun+Mercury) - Intelligence
  - Guru-Mangal Yoga - Wealth & Property
  - Shani Swarashi - Long-term success
  - Shukra Lagna - Attractive personality

KEY PREDICTIONS:
  Career: IT/Finance best, success after 35
  Marriage: Good yoga, 2024-2027 favorable
  Children: Slight delay, but good
  Health: Watch mental health, digestion
  Wealth: Excellent! 4 planets in 2nd house

IMPORTANT PERIODS:
  - Current: Jupiter Mahadasha (till 2026)
  - Next: Saturn Mahadasha (2026-2045) - Golden period!
  - Best years: 2035-2038 (Saturn-Venus)
"""
        return response

    def get_default_answer(self):
        return """
Main samajh nahi paya. Aap ye topics puch sakte ho:

TOPICS:
  - Career / Job / Naukri
  - Marriage / Shaadi / Vivah
  - Children / Bachche / Santan
  - Health / Swasthya / Sehat
  - Money / Paisa / Dhan
  - Dasha / Mahadasha / Future
  - Lagna / Personality
  - Planet / Graha (Sun, Moon, etc.)
  - Rashi / Moon Sign
  - Education / Padhai
  - Foreign / Videsh
  - Lucky color / number / stone

Example questions:
  - "Mera career kaisa rahega?"
  - "Shaadi kab hogi?"
  - "Health ke baare mein batao"
  - "Saturn ka effect kya hai?"
  - "Lucky color kya hai?"
"""

    def chat(self):
        """Start interactive chat"""
        while True:
            try:
                question = input("\nYou: ").strip()
                if not question:
                    continue

                response = self.get_response(question)
                if response == "EXIT":
                    print("\nDhanyavaad! Shubh din! Namaste!")
                    break

                print(f"\nAssistant: {response}")

            except KeyboardInterrupt:
                print("\n\nDhanyavaad! Namaste!")
                break
            except Exception as e:
                print(f"\nError: {e}")


def main():
    """Start the Kundali Assistant for Alok"""
    assistant = KundaliAssistant(
        name='Alok Yadav',
        year=1993, month=10, day=25,
        hour=5, minute=15,
        city='Amethi'
    )
    assistant.chat()


if __name__ == "__main__":
    main()
