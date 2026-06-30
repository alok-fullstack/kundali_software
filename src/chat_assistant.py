"""
Kundali Chat Assistant
Answer questions about generated kundali
"""

from .config import (
    RASHIS, PLANET_NAMES, Planet, BHAVA_NAMES,
    HOUSE_LORDSHIPS, FUNCTIONAL_BENEFICS, FUNCTIONAL_MALEFICS, YOGAKARAKA, NATURAL_RELATIONSHIPS
)
from .predictions import (
    GRAHA_BHAVA_PHAL, CAREER_BY_LAGNA, MARRIAGE_PREDICTIONS, CHILDREN_PREDICTIONS,
    HEALTH_PREDICTIONS, DASHA_LORDSHIP_EFFECTS, PLANET_HINDI_NAMES,
    RETROGRADE_EFFECTS, check_sade_sati,
    get_planet_lordships, is_functional_benefic, is_functional_malefic, is_yogakaraka,
    get_dasha_relationship, get_lordship_based_dasha_prediction, get_natural_relationship
)
from .full_predictions import get_lagna_specific_dasha_effect
from .yogas import check_kaal_sarp_dosh, check_pitra_dosh, check_neecha_bhanga_raja_yoga


class KundaliChatAssistant:
    """Chat assistant for answering kundali questions."""

    def __init__(self, kundali):
        self.kundali = kundali
        self.name = kundali.birth_data.name  # Store person's name
        self.planets = kundali.planets
        self.lagna = kundali.lagna
        self.planets_in_houses = kundali.get_planets_in_houses()
        self.mahadashas = kundali.get_mahadashas(years=100)
        self.current_dasha = kundali.get_current_dasha()

        # Calculate house rashis
        lagna_num = self.lagna["rashi_num"]
        self.house_rashis = {}
        for i in range(1, 13):
            rashi_num = (lagna_num + i - 1) % 12
            self.house_rashis[i] = RASHIS[rashi_num]

        # Find planet houses
        self.planet_houses = {}
        for h, planets in self.planets_in_houses.items():
            for p in planets:
                self.planet_houses[p] = h

        self.rashi_hindi = {
            "Mesha": "मेष", "Vrishabha": "वृषभ", "Mithuna": "मिथुन", "Karka": "कर्क",
            "Simha": "सिंह", "Kanya": "कन्या", "Tula": "तुला", "Vrishchika": "वृश्चिक",
            "Dhanu": "धनु", "Makara": "मकर", "Kumbha": "कुंभ", "Meena": "मीन"
        }

    def get_response(self, question):
        """Get response for a question."""
        q = question.lower().strip()

        # Marriage TIMING questions (must come BEFORE general marriage)
        if any(phrase in q for phrase in ['marriage timing', 'shaadi kab', 'vivah kab', 'when marriage', 'shaadi samay', 'विवाह कब', 'शादी कब', 'kab hogi shaadi', 'kab milega']):
            return self.marriage_timing_answer()

        # Career TIMING questions (must come BEFORE general career)
        if any(phrase in q for phrase in ['career timing', 'job kab', 'promotion kab', 'career change', 'करियर कब', 'नौकरी कब', 'job milega']):
            return self.career_timing_answer()

        # Property TIMING questions
        if any(phrase in q for phrase in ['property kab', 'ghar kab', 'house kab', 'makan kab', 'घर कब', 'मकान कब']):
            return self.property_timing_answer()

        # Career questions
        if any(word in q for word in ['career', 'job', 'naukri', 'kaam', 'profession', 'business', 'vyapar', 'rojgar', 'काम', 'नौकरी', 'करियर']):
            return self.career_answer()

        # Marriage questions
        if any(word in q for word in ['marriage', 'shaadi', 'vivah', 'wife', 'husband', 'patni', 'pati', 'partner', 'love', 'pyar', 'शादी', 'विवाह', 'पत्नी', 'पति']):
            return self.marriage_answer()

        # Children questions
        if any(word in q for word in ['children', 'child', 'bachche', 'bachcha', 'santan', 'baby', 'kids', 'putra', 'बच्चे', 'संतान', 'पुत्र']):
            return self.children_answer()

        # Health questions
        if any(word in q for word in ['health', 'swasthya', 'sehat', 'bimari', 'disease', 'doctor', 'medical', 'स्वास्थ्य', 'सेहत', 'बीमारी']):
            return self.health_answer()

        # Money/Wealth questions
        if any(word in q for word in ['money', 'paisa', 'dhan', 'wealth', 'income', 'salary', 'property', 'पैसा', 'धन', 'आय', 'संपत्ति']):
            return self.wealth_answer()

        # Dasha questions
        if any(word in q for word in ['dasha', 'mahadasha', 'antardasha', 'period', 'time', 'samay', 'kab', 'when', 'future', 'दशा', 'भविष्य', 'कब']):
            return self.dasha_answer()

        # Lagna questions
        if any(word in q for word in ['lagna', 'ascendant', 'rising', 'personality', 'nature', 'swabhav', 'लग्न', 'स्वभाव']):
            return self.lagna_answer()

        # Rashi questions
        if any(word in q for word in ['rashi', 'moon sign', 'chandra', 'राशि', 'चंद्र']):
            return self.rashi_answer()

        # Planet questions
        if any(word in q for word in ['planet', 'graha', 'sun', 'moon', 'mars', 'mercury', 'jupiter', 'venus', 'saturn', 'rahu', 'ketu',
                                       'surya', 'chandra', 'mangal', 'budh', 'guru', 'shukra', 'shani', 'ग्रह', 'सूर्य', 'चंद्र', 'मंगल', 'बुध', 'गुरु', 'शुक्र', 'शनि', 'राहु', 'केतु']):
            return self.planet_answer(q)

        # Education questions
        if any(word in q for word in ['education', 'padhai', 'study', 'exam', 'shiksha', 'पढ़ाई', 'शिक्षा', 'परीक्षा']):
            return self.education_answer()

        # Foreign questions
        if any(word in q for word in ['foreign', 'videsh', 'abroad', 'travel', 'विदेश', 'यात्रा']):
            return self.foreign_answer()

        # Lucky questions
        if any(word in q for word in ['lucky', 'shubh', 'color', 'rang', 'number', 'stone', 'ratna', 'gemstone', 'शुभ', 'रंग', 'रत्न']):
            return self.lucky_answer()

        # Remedy questions
        if any(word in q for word in ['remedy', 'upay', 'mantra', 'puja', 'उपाय', 'मंत्र', 'पूजा']):
            return self.remedy_answer()

        # Sade Sati questions
        if any(word in q for word in ['sade sati', 'sadesati', 'sade-sati', 'shani', 'साढ़े साती', 'साढ़ेसाती', 'शनि दोष']):
            return self.sade_sati_answer()

        # Kaal Sarp Dosh questions
        if any(word in q for word in ['kaal sarp', 'kaalsarp', 'kalsarp', 'kal sarp', 'snake', 'naag', 'काल सर्प', 'कालसर्प', 'नाग']):
            return self.kaal_sarp_answer()

        # Pitra Dosh questions
        if any(word in q for word in ['pitra', 'pitr', 'pitru', 'ancestor', 'purvaj', 'पितृ', 'पितर', 'पूर्वज']):
            return self.pitra_dosh_answer()

        # Neecha Bhanga Raja Yoga questions
        if any(word in q for word in ['neecha bhanga', 'neechabhanga', 'debilitation cancel', 'नीच भंग', 'नीचभंग']):
            return self.neecha_bhanga_answer()

        # Transit/Gochar questions
        if any(word in q for word in ['transit', 'gochar', 'gochara', 'current position', 'गोचर', 'वर्तमान स्थिति']):
            return self.transit_answer()

        # Summary
        if any(word in q for word in ['summary', 'overall', 'kundali', 'batao', 'tell', 'सारांश', 'बताओ']):
            return self.summary_answer()

        # Default
        return self.default_answer()

    def career_answer(self):
        lagna = self.lagna['rashi']
        tenth_planets = self.planets_in_houses.get(10, [])
        second_planets = self.planets_in_houses.get(2, [])

        response = f"""<b>💼 {self.name} का करियर विश्लेषण:</b><br><br>
<b>लग्न:</b> {self.rashi_hindi.get(lagna, lagna)}<br>
<b>उपयुक्त क्षेत्र:</b> {CAREER_BY_LAGNA.get(lagna, 'विविध क्षेत्र')}<br><br>
"""
        if second_planets:
            response += f"<b>विशेष:</b> आपके द्वितीय भाव में {len(second_planets)} ग्रह हैं - यह धन योग है!<br><br>"

        saturn_house = self.planet_houses.get('SATURN')
        if saturn_house and saturn_house >= 1:
            effect = GRAHA_BHAVA_PHAL.get('SATURN', {}).get(saturn_house, '')
            if effect:
                response += f"<b>शनि भाव {saturn_house} में:</b> {effect}<br><br>"

        # Dynamic dasha effect based on lagna
        maha = self.current_dasha['mahadasha']['planet']
        lagna_name = self.kundali.lagna['rashi']
        dasha_effect = get_lagna_specific_dasha_effect(maha, lagna_name)
        response += f"<b>वर्तमान {maha} महादशा:</b> {dasha_effect['effect']}<br><br>"

        # Career suggestion based on 10th lord
        tenth_lord = self._get_house_lord(10, lagna_name)
        tenth_effect = get_lagna_specific_dasha_effect(tenth_lord, lagna_name)
        if tenth_effect['is_benefic']:
            response += f"<b>करियर सुझाव:</b> {tenth_lord} दशमेश शुभ है - करियर में अच्छे अवसर।"
        else:
            response += f"<b>करियर सुझाव:</b> {tenth_lord} दशमेश के लिए उपाय करें।"

        return response

    def _get_house_lord(self, house_num, lagna_name):
        """Get the lord of a house based on lagna."""
        RASHI_LORDS = {
            "Mesha": "Mars", "Vrishabha": "Venus", "Mithuna": "Mercury", "Karka": "Moon",
            "Simha": "Sun", "Kanya": "Mercury", "Tula": "Venus", "Vrishchika": "Mars",
            "Dhanu": "Jupiter", "Makara": "Saturn", "Kumbha": "Saturn", "Meena": "Jupiter"
        }
        rashi_order = ["Mesha", "Vrishabha", "Mithuna", "Karka", "Simha", "Kanya",
                       "Tula", "Vrishchika", "Dhanu", "Makara", "Kumbha", "Meena"]
        lagna_idx = rashi_order.index(lagna_name)
        house_rashi = rashi_order[(lagna_idx + house_num - 1) % 12]
        return RASHI_LORDS[house_rashi]

    def _get_house_from_reference(self, planet_rashi_num, reference_rashi_num):
        """Get house number of a planet from a reference point (Lagna, Moon, Venus)."""
        return ((planet_rashi_num - reference_rashi_num) % 12) + 1

    def _check_manglik_cancellations(self, mars_house, mars_rashi, reference_name):
        """
        Check all Manglik cancellation rules (BPHS authentic).
        Returns a list of cancellation reasons if any apply.
        """
        cancellations = []
        mars_rashi_name = mars_rashi

        # 1. Mars in own sign (Mesha/Aries, Vrishchika/Scorpio)
        if mars_rashi_name in ['Mesha', 'Vrishchika']:
            cancellations.append(f"मंगल स्वराशि में ({self.rashi_hindi.get(mars_rashi_name, mars_rashi_name)})")

        # 2. Mars exalted (Makara/Capricorn)
        if mars_rashi_name == 'Makara':
            cancellations.append(f"मंगल उच्च राशि में ({self.rashi_hindi.get(mars_rashi_name, mars_rashi_name)})")

        # 3. Mars in Leo (Simha) - some texts consider this cancellation
        if mars_rashi_name == 'Simha':
            cancellations.append(f"मंगल सिंह राशि में (कुछ ग्रंथों में दोष निवारण)")

        # 4. Jupiter aspect on Mars (Jupiter aspects 5th, 7th, 9th from its position)
        jupiter_house = self.planet_houses.get('JUPITER', 0)
        mars_house_from_lagna = self.planet_houses.get('MARS', 0)
        if jupiter_house and mars_house_from_lagna:
            diff = (mars_house_from_lagna - jupiter_house) % 12
            if diff in [4, 6, 8]:  # 5th (4 houses away), 7th (6), 9th (8)
                cancellations.append("गुरु की दृष्टि मंगल पर")

        # 5. Mars conjunct Jupiter or Venus (benefic conjunction)
        venus_house = self.planet_houses.get('VENUS', 0)
        if mars_house_from_lagna == jupiter_house and jupiter_house != 0:
            cancellations.append("मंगल-गुरु युति (शुभ ग्रह संयोग)")
        if mars_house_from_lagna == venus_house and venus_house != 0:
            cancellations.append("मंगल-शुक्र युति (शुभ ग्रह संयोग)")

        # 6. Jupiter or Venus in Kendra (1, 4, 7, 10) - IMPORTANT BPHS RULE
        kendra_houses = [1, 4, 7, 10]
        if jupiter_house in kendra_houses:
            cancellations.append(f"गुरु केंद्र में (भाव {jupiter_house}) - मांगलिक दोष शांत")
        if venus_house in kendra_houses:
            cancellations.append(f"शुक्र केंद्र में (भाव {venus_house}) - मांगलिक दोष शांत")

        # 7. Saturn in 1, 4, 7, 8, 12 - SHANI MANGLIK (cancels Manglik)
        saturn_house = self.planet_houses.get('SATURN', 0)
        if saturn_house in [1, 4, 7, 8, 12]:
            cancellations.append(f"शनि मांगलिक (शनि भाव {saturn_house} में) - दोष परस्पर निवारण")

        # 8-12. House-specific cancellations based on sign
        if mars_house == 2 and mars_rashi_name in ['Mithuna', 'Kanya']:
            cancellations.append(f"द्वितीय भाव में मंगल {self.rashi_hindi.get(mars_rashi_name, mars_rashi_name)} राशि में")

        if mars_house == 4 and mars_rashi_name in ['Mesha', 'Vrishchika']:
            cancellations.append(f"चतुर्थ भाव में मंगल {self.rashi_hindi.get(mars_rashi_name, mars_rashi_name)} राशि में")

        # Mars in Karka/Simha in 7th OR 8th (both houses)
        if mars_house == 7 and mars_rashi_name in ['Karka', 'Makara', 'Simha']:
            cancellations.append(f"सप्तम भाव में मंगल {self.rashi_hindi.get(mars_rashi_name, mars_rashi_name)} राशि में")

        if mars_house == 8 and mars_rashi_name in ['Dhanu', 'Meena', 'Karka', 'Simha']:
            cancellations.append(f"अष्टम भाव में मंगल {self.rashi_hindi.get(mars_rashi_name, mars_rashi_name)} राशि में")

        if mars_house == 12 and mars_rashi_name in ['Vrishabha', 'Tula']:
            cancellations.append(f"द्वादश भाव में मंगल {self.rashi_hindi.get(mars_rashi_name, mars_rashi_name)} राशि में")

        # 13. Mars in 1st house in fire signs (Mesha, Simha, Dhanu)
        if mars_house == 1 and mars_rashi_name in ['Mesha', 'Simha', 'Dhanu']:
            cancellations.append(f"लग्न में मंगल अग्नि तत्व राशि में ({self.rashi_hindi.get(mars_rashi_name, mars_rashi_name)})")

        return cancellations

    def _get_manglik_severity(self, house):
        """Get severity level of Manglik based on house."""
        if house in [7, 8]:
            return ("तीव्र", "Severe", 100)
        elif house in [1, 12]:
            return ("मध्यम", "Medium", 70)
        elif house in [2, 4]:
            return ("सौम्य", "Mild", 40)
        return ("कोई नहीं", "None", 0)

    def _analyze_manglik_from_reference(self, reference_name, reference_rashi_num):
        """
        Analyze Manglik dosha from a specific reference point.
        Returns dict with is_manglik, house, severity, cancellations.
        """
        mars_rashi_num = self.planets['MARS']['rashi_num']
        mars_rashi = self.planets['MARS']['rashi']
        mars_house = self._get_house_from_reference(mars_rashi_num, reference_rashi_num)

        manglik_houses = [1, 2, 4, 7, 8, 12]
        is_manglik = mars_house in manglik_houses

        result = {
            'reference': reference_name,
            'is_manglik': is_manglik,
            'mars_house': mars_house,
            'mars_rashi': mars_rashi,
            'severity': ("कोई नहीं", "None", 0),
            'cancellations': []
        }

        if is_manglik:
            result['severity'] = self._get_manglik_severity(mars_house)
            result['cancellations'] = self._check_manglik_cancellations(mars_house, mars_rashi, reference_name)

        return result

    def _calculate_manglik_percentage(self, lagna_result, moon_result, venus_result):
        """
        Calculate overall Manglik percentage (0-100%).
        - Full Manglik from all three = 100%
        - Partial based on positions
        - Cancellations reduce percentage
        Weights as per BPHS: Lagna (primary) > Moon (secondary) > Venus (tertiary)
        """
        total_score = 0
        max_score = 0

        # Weights: Lagna 50% (primary), Moon 35% (secondary), Venus 15% (tertiary)
        for result, weight in [(lagna_result, 50), (moon_result, 35), (venus_result, 15)]:
            max_score += weight
            if result['is_manglik']:
                # Base score from severity
                severity_percent = result['severity'][2]  # 100, 70, or 40
                base_score = (severity_percent / 100) * weight

                # Reduce for cancellations (each cancellation reduces by 15%)
                cancellation_reduction = min(len(result['cancellations']) * 0.15, 0.9)
                adjusted_score = base_score * (1 - cancellation_reduction)

                total_score += adjusted_score

        percentage = (total_score / max_score) * 100 if max_score > 0 else 0
        return round(percentage, 1)

    def marriage_answer(self):
        seventh_rashi = self.house_rashis[7]['name']
        seventh_planets = self.planets_in_houses.get(7, [])
        venus_house = self.planet_houses.get('VENUS', 0)

        response = f"""<b>💑 {self.name} का विवाह विश्लेषण:</b><br><br>
<b>सप्तम भाव राशि:</b> {self.rashi_hindi.get(seventh_rashi, seventh_rashi)}<br>
<b>जीवनसाथी के गुण:</b> {MARRIAGE_PREDICTIONS.get(seventh_rashi, '')}<br><br>
"""
        if venus_house and venus_house >= 1:
            effect = GRAHA_BHAVA_PHAL.get('VENUS', {}).get(venus_house, '')
            if effect:
                response += f"<b>शुक्र भाव {venus_house} में:</b> {effect}<br><br>"

        # ========== COMPREHENSIVE MANGLIK DOSH ANALYSIS ==========
        response += "<b>🔴 मांगलिक दोष विश्लेषण (Manglik Dosh Analysis):</b><br><br>"

        # Get reference points
        lagna_rashi_num = self.lagna['rashi_num']
        moon_rashi_num = self.planets['MOON']['rashi_num']
        venus_rashi_num = self.planets['VENUS']['rashi_num']

        # Analyze from all three reference points
        lagna_result = self._analyze_manglik_from_reference("Lagna", lagna_rashi_num)
        moon_result = self._analyze_manglik_from_reference("Moon", moon_rashi_num)
        venus_result = self._analyze_manglik_from_reference("Venus", venus_rashi_num)

        mars_rashi = self.planets['MARS']['rashi']

        # Display results for each reference
        response += f"<b>मंगल की स्थिति:</b> {self.rashi_hindi.get(mars_rashi, mars_rashi)} राशि में<br><br>"

        # 1. From Lagna
        response += f"<b>1. लग्न से (From Lagna):</b><br>"
        response += f"   • मंगल भाव: {lagna_result['mars_house']}<br>"
        if lagna_result['is_manglik']:
            severity_hindi, severity_eng, _ = lagna_result['severity']
            response += f"   • स्थिति: ⚠️ मांगलिक ({severity_hindi}/{severity_eng})<br>"
            if lagna_result['cancellations']:
                response += f"   • निवारण: {', '.join(lagna_result['cancellations'][:2])}<br>"
        else:
            response += f"   • स्थिति: ✅ मांगलिक नहीं<br>"

        # 2. From Moon (Chandra Lagna)
        response += f"<br><b>2. चंद्र से (From Moon/Chandra Lagna):</b><br>"
        response += f"   • मंगल भाव: {moon_result['mars_house']}<br>"
        if moon_result['is_manglik']:
            severity_hindi, severity_eng, _ = moon_result['severity']
            response += f"   • स्थिति: ⚠️ मांगलिक ({severity_hindi}/{severity_eng})<br>"
            if moon_result['cancellations']:
                response += f"   • निवारण: {', '.join(moon_result['cancellations'][:2])}<br>"
        else:
            response += f"   • स्थिति: ✅ मांगलिक नहीं<br>"

        # 3. From Venus (Shukra)
        response += f"<br><b>3. शुक्र से (From Venus/Shukra):</b><br>"
        response += f"   • मंगल भाव: {venus_result['mars_house']}<br>"
        if venus_result['is_manglik']:
            severity_hindi, severity_eng, _ = venus_result['severity']
            response += f"   • स्थिति: ⚠️ मांगलिक ({severity_hindi}/{severity_eng})<br>"
            if venus_result['cancellations']:
                response += f"   • निवारण: {', '.join(venus_result['cancellations'][:2])}<br>"
        else:
            response += f"   • स्थिति: ✅ मांगलिक नहीं<br>"

        # Calculate overall percentage
        manglik_percentage = self._calculate_manglik_percentage(lagna_result, moon_result, venus_result)

        # Collect all unique cancellations
        all_cancellations = set()
        for result in [lagna_result, moon_result, venus_result]:
            all_cancellations.update(result['cancellations'])

        # Overall summary
        response += f"<br><b>📊 समग्र मांगलिक प्रतिशत: {manglik_percentage}%</b><br><br>"

        # Display all cancellations if any
        if all_cancellations:
            response += "<b>🔹 दोष निवारण कारण (Cancellation Factors):</b><br>"
            for idx, cancel in enumerate(list(all_cancellations)[:5], 1):
                response += f"   {idx}. {cancel}<br>"
            response += "<br>"

        # Final recommendation
        response += "<b>📋 निष्कर्ष (Conclusion):</b><br>"
        if manglik_percentage == 0:
            response += "✅ <b>मांगलिक दोष नहीं है।</b> विवाह में कोई मांगलिक संबंधी बाधा नहीं।<br>"
            recommendation = "कोई विशेष मांगलिक चिंता नहीं।"
        elif manglik_percentage <= 20:
            response += "✅ <b>नगण्य मांगलिक प्रभाव।</b> दोष निवारण कारकों से प्रभाव समाप्त।<br>"
            recommendation = "कोई विशेष मांगलिक चिंता नहीं।"
        elif manglik_percentage <= 40:
            response += "ℹ️ <b>अल्प/सौम्य मांगलिक।</b> प्रभाव कम है।<br>"
            recommendation = "मांगलिक/गैर-मांगलिक दोनों से विवाह संभव।"
        elif manglik_percentage <= 60:
            response += "⚠️ <b>आंशिक मांगलिक (Partial Manglik)।</b><br>"
            recommendation = "मांगलिक साथी से विवाह अधिक उत्तम।"
        elif manglik_percentage <= 80:
            response += "⚠️ <b>मध्यम मांगलिक।</b> ध्यान देना आवश्यक।<br>"
            recommendation = "मांगलिक साथी से विवाह उत्तम। मंगल शांति पूजा करवाएं।"
        else:
            response += "🔴 <b>पूर्ण मांगलिक (Full Manglik)।</b><br>"
            recommendation = "मांगलिक साथी से ही विवाह करें। मंगल शांति पूजा अवश्य करवाएं।"

        response += f"<b>सुझाव:</b> {recommendation}<br><br>"

        # Marriage timing - dynamic based on actual dashas
        seventh_lord = self._get_seventh_lord()
        response += f"""<b>विवाह समय - शुभ दशाएं:</b><br>
• सप्तमेश ({seventh_lord}) की महादशा/अंतर्दशा<br>
• शुक्र की दशा (विवाह कारक)<br>
• गुरु की दशा (शुभ ग्रह)<br>
<em>विस्तृत दशा समय के लिए कुंडली में दशा विश्लेषण देखें।</em>"""

        return response

    def _get_seventh_lord(self):
        """Get the lord of 7th house based on 7th rashi."""
        seventh_rashi = self.house_rashis[7]['name']
        rashi_lords = {
            "Mesha": "मंगल", "Vrishabha": "शुक्र", "Mithuna": "बुध",
            "Karka": "चंद्र", "Simha": "सूर्य", "Kanya": "बुध",
            "Tula": "शुक्र", "Vrishchika": "मंगल", "Dhanu": "गुरु",
            "Makara": "शनि", "Kumbha": "शनि", "Meena": "गुरु"
        }
        return rashi_lords.get(seventh_rashi, "अज्ञात")

    def children_answer(self):
        fifth_rashi = self.house_rashis[5]['name']
        fifth_planets = self.planets_in_houses.get(5, [])
        jupiter_house = self.planet_houses.get('JUPITER', 0)

        response = f"""<b>👶 संतान विश्लेषण:</b><br><br>
<b>पंचम भाव राशि:</b> {self.rashi_hindi.get(fifth_rashi, fifth_rashi)}<br>
<b>संतान के गुण:</b> {CHILDREN_PREDICTIONS.get(fifth_rashi, '')}<br><br>
"""
        if fifth_planets:
            response += f"<b>पंचम भाव में ग्रह:</b> {', '.join([PLANET_NAMES[Planet[p]]['hindi'] for p in fifth_planets])}<br><br>"

        if jupiter_house and jupiter_house >= 1:
            effect = GRAHA_BHAVA_PHAL.get('JUPITER', {}).get(jupiter_house, '')
            if effect:
                response += f"<b>गुरु (पुत्र कारक) भाव {jupiter_house} में:</b> {effect}<br><br>"

        # Dynamic children prediction based on actual chart
        lagna_name = self.kundali.lagna['rashi']
        fifth_lord = self._get_house_lord(5, lagna_name)
        fifth_lord_effect = get_lagna_specific_dasha_effect(fifth_lord, lagna_name)

        response += "<b>संतान भविष्यवाणी:</b><br>"
        response += f"• पंचमेश {fifth_lord} - {fifth_lord_effect['effect']}<br>"

        # Only mention Saturn in 5th if Saturn is actually there
        if "SATURN" in fifth_planets:
            saturn_effect = get_lagna_specific_dasha_effect("Saturn", lagna_name)
            if saturn_effect['is_benefic']:
                response += "• शनि पंचम में - संतान अनुशासित और जिम्मेदार होगी<br>"
            else:
                response += "• शनि पंचम में - संतान में देरी संभव<br>"

        if "JUPITER" in fifth_planets:
            jupiter_effect = get_lagna_specific_dasha_effect("Jupiter", lagna_name)
            if jupiter_effect['is_benefic']:
                response += "• गुरु पंचम में - संतान बुद्धिमान होगी<br>"

        return response

    def health_answer(self):
        lagna = self.lagna['rashi']
        sixth_planets = self.planets_in_houses.get(6, [])
        moon_house = self.planet_houses.get('MOON', 0)

        response = f"""<b>🏥 {self.name} का स्वास्थ्य विश्लेषण:</b><br><br>
<b>लग्न:</b> {self.rashi_hindi.get(lagna, lagna)}<br>
<b>स्वास्थ्य सुझाव:</b> {HEALTH_PREDICTIONS.get(lagna, '')}<br><br>
"""
        if sixth_planets:
            response += f"<b>षष्ठ भाव में ग्रह:</b> {', '.join([PLANET_NAMES[Planet[p]]['hindi'] for p in sixth_planets])}<br><br>"

        if moon_house == 6:
            response += "⚠️ <b>चंद्र 6th भाव में:</b> मानसिक स्वास्थ्य पर ध्यान दें, तनाव से बचें।<br><br>"

        # Check Sade Sati and its impact on health
        moon_rashi_num = self.planets['MOON']['rashi_num']
        saturn_rashi_num = self.planets['SATURN']['rashi_num']
        sade_sati = check_sade_sati(moon_rashi_num, saturn_rashi_num)

        if sade_sati["active"]:
            response += f"""⚠️ <b>साढ़े साती सक्रिय - स्वास्थ्य प्रभाव:</b><br>
• चरण: {sade_sati["phase"]}<br>
• {sade_sati["effects"]}<br>
• विशेष सावधानी: तनाव प्रबंधन, नियमित जांच<br><br>
"""

        # Prakriti-based health tips (lagna-specific)
        PRAKRITI_TIPS = {
            "Mesha": ("पित्त", "ठंडे पेय लें, क्रोध से बचें, सिर की मालिश करें"),
            "Vrishabha": ("कफ", "हल्का भोजन लें, सुबह व्यायाम करें, गले का ध्यान रखें"),
            "Mithuna": ("वात", "नियमित दिनचर्या रखें, तेल मालिश करें, फेफड़ों की देखभाल"),
            "Karka": ("कफ", "पाचन का ध्यान रखें, भावनात्मक संतुलन, पेट की देखभाल"),
            "Simha": ("पित्त", "हृदय स्वास्थ्य, अहंकार से बचें, ठंडे भोजन लें"),
            "Kanya": ("वात", "पाचन तंत्र की देखभाल, तनाव कम करें, हल्का भोजन"),
            "Tula": ("वात", "किडनी का ध्यान, संतुलित जीवनशैली, गर्म भोजन लें"),
            "Vrishchika": ("पित्त", "प्रजनन स्वास्थ्य, क्रोध नियंत्रण, योग करें"),
            "Dhanu": ("पित्त", "जांघ और यकृत की देखभाल, संयम रखें, हल्का व्यायाम"),
            "Makara": ("वात", "जोड़ों की देखभाल, गर्म रहें, तेल मालिश करें"),
            "Kumbha": ("वात", "रक्त संचार, टखने की देखभाल, नियमित व्यायाम"),
            "Meena": ("कफ", "पैरों की देखभाल, ध्यान करें, शराब से बचें"),
        }

        prakriti, tips = PRAKRITI_TIPS.get(lagna, ("सामान्य", "योग और ध्यान करें"))
        response += f"<b>स्वास्थ्य टिप्स ({prakriti} प्रकृति - {lagna} लग्न):</b><br>"
        response += f"• {tips}<br>"
        response += "• पानी पर्याप्त पिएं<br>"
        response += "• नियमित दिनचर्या रखें"

        return response

    def wealth_answer(self):
        second_planets = self.planets_in_houses.get(2, [])
        eleventh_planets = self.planets_in_houses.get(11, [])

        response = f"""<b>💰 धन विश्लेषण:</b><br><br>
<b>द्वितीय भाव (धन स्थान):</b> {len(second_planets)} ग्रह<br>
<b>एकादश भाव (लाभ स्थान):</b> {len(eleventh_planets)} ग्रह<br><br>
"""
        if second_planets:
            response += f"<b>🌟 विशेष धन योग!</b> {len(second_planets)} ग्रह धन भाव में:<br>"
            for p in second_planets:
                try:
                    hindi = PLANET_NAMES[Planet[p]]['hindi']
                    effect = GRAHA_BHAVA_PHAL.get(p, {}).get(2, 'धन भाव में शुभ')
                    response += f"• {hindi}: {effect}<br>"
                except:
                    pass
            response += "<br>"

        # Dynamic wealth prediction based on actual chart
        lagna_name = self.kundali.lagna['rashi']
        second_lord = self._get_house_lord(2, lagna_name)
        second_lord_effect = get_lagna_specific_dasha_effect(second_lord, lagna_name)

        response += "<b>धन भविष्यवाणी:</b><br>"
        response += f"• द्वितीयेश {second_lord} - {second_lord_effect['effect']}<br>"

        # Property yoga only if Saturn/Mars in relevant houses
        saturn_house = self.planet_houses.get('SATURN')
        mars_house = self.planet_houses.get('MARS')
        if saturn_house in [4, 5, 10] or mars_house in [2, 4]:
            response += "• Property से लाभ संभव<br>"

        # Current dasha wealth effect
        current_maha = self.current_dasha['mahadasha']['planet']
        maha_effect = get_lagna_specific_dasha_effect(current_maha, lagna_name)
        if maha_effect['is_benefic']:
            response += f"• {current_maha} महादशा में आर्थिक स्थिरता<br>"

        return response

    def dasha_answer(self):
        """Enhanced dasha prediction with lordship-based analysis."""
        lagna = self.lagna['rashi']
        maha_planet = self.current_dasha['mahadasha']['planet']
        antar_planet = self.current_dasha['antardasha']['planet']
        pratyantar_planet = self.current_dasha['pratyantardasha']['planet']

        response = f"""<b>📅 {self.name} का दशा विश्लेषण ({self.rashi_hindi.get(lagna, lagna)} लग्न):</b><br><br>
<b>वर्तमान दशा:</b> {self.current_dasha['full_dasha']}<br><br>
"""

        # ========== MAHADASHA LORDSHIP ANALYSIS ==========
        response += f"<b>═══════════════════════════════════════</b><br>"
        response += f"<b>🌟 महादशा: {PLANET_HINDI_NAMES.get(maha_planet, maha_planet)} ({maha_planet})</b><br>"
        response += f"<b>अवधि:</b> {self.current_dasha['mahadasha']['start'].strftime('%Y')} - {self.current_dasha['mahadasha']['end'].strftime('%Y')}<br>"
        response += f"<b>═══════════════════════════════════════</b><br><br>"

        # Get lordship-based prediction for Mahadasha
        maha_prediction = get_lordship_based_dasha_prediction(maha_planet, lagna)

        # Display lordships
        if maha_prediction['lordships']:
            lordship_str = ', '.join([str(h) for h in maha_prediction['lordships']])
            response += f"<b>भाव स्वामित्व:</b> {PLANET_HINDI_NAMES.get(maha_planet, maha_planet)} भाव {lordship_str} का स्वामी है<br><br>"

            # Show what each house signifies
            response += f"<b>इन भावों से संबंधित फल:</b><br>"
            for lord_info in maha_prediction['lordship_effects']:
                house = lord_info['house']
                effect = lord_info['effect']
                response += f"• <b>भाव {house}:</b> {effect}<br>"
            response += "<br>"
        else:
            # For Rahu/Ketu, show house-based effects (not generic)
            response += f"<b>विशेष नोट:</b> {maha_planet} छाया ग्रह है, इसका कोई राशि स्वामित्व नहीं।<br>"
            rahu_ketu_house = self.planet_houses.get(maha_planet.upper(), 1)
            rahu_ketu_effect = get_lagna_specific_dasha_effect(maha_planet, lagna)
            response += f"<b>भाव {rahu_ketu_house} में प्रभाव:</b> {rahu_ketu_effect['effect']}<br><br>"

        # Display functional nature
        response += f"<b>{self.rashi_hindi.get(lagna, lagna)} लग्न के लिए {PLANET_HINDI_NAMES.get(maha_planet, maha_planet)} की प्रकृति:</b><br>"

        if maha_prediction['is_yogakaraka']:
            response += f"🌟 <b>योगकारक (Yogakaraka)!</b> - अत्यंत शुभ ग्रह इस लग्न के लिए<br>"
        elif maha_prediction['is_benefic'] and not maha_prediction['is_malefic']:
            response += f"✅ <b>शुभ (Functional Benefic)</b> - लाभदायक परिणाम अपेक्षित<br>"
        elif maha_prediction['is_malefic'] and not maha_prediction['is_benefic']:
            response += f"⚠️ <b>अशुभ (Functional Malefic)</b> - सावधानी आवश्यक<br>"
        else:
            response += f"ℹ️ <b>मिश्रित (Mixed)</b> - शुभ और अशुभ दोनों प्रभाव संभव<br>"

        response += f"<br><b>महादशा समग्र फल:</b> {maha_prediction['overall_prediction']}<br><br>"

        # ========== ANTARDASHA LORDSHIP ANALYSIS ==========
        response += f"<b>───────────────────────────────────────</b><br>"
        response += f"<b>📌 वर्तमान अंतर्दशा: {PLANET_HINDI_NAMES.get(antar_planet, antar_planet)} ({antar_planet})</b><br>"
        response += f"<b>───────────────────────────────────────</b><br><br>"

        # Get lordship-based prediction for Antardasha
        antar_prediction = get_lordship_based_dasha_prediction(antar_planet, lagna)

        if antar_prediction['lordships']:
            lordship_str = ', '.join([str(h) for h in antar_prediction['lordships']])
            response += f"<b>भाव स्वामित्व:</b> {PLANET_HINDI_NAMES.get(antar_planet, antar_planet)} भाव {lordship_str} का स्वामी है<br>"

            # Show effects briefly
            effects = [f"भाव {info['house']}: {info['effect']}" for info in antar_prediction['lordship_effects']]
            response += f"<b>फल:</b> {'; '.join(effects)}<br><br>"

        # Check functional nature of antardasha lord
        if antar_prediction['is_yogakaraka']:
            response += f"🌟 <b>{PLANET_HINDI_NAMES.get(antar_planet, antar_planet)} योगकारक है!</b><br>"
        elif antar_prediction['is_benefic']:
            response += f"✅ <b>{PLANET_HINDI_NAMES.get(antar_planet, antar_planet)} शुभ ग्रह है</b><br>"
        elif antar_prediction['is_malefic']:
            response += f"⚠️ <b>{PLANET_HINDI_NAMES.get(antar_planet, antar_planet)} अशुभ ग्रह है</b><br>"

        # ========== MAHADASHA-ANTARDASHA RELATIONSHIP ==========
        response += f"<br><b>महादशा-अंतर्दशा संबंध विश्लेषण:</b><br>"

        # Natural relationship
        natural_rel = get_natural_relationship(maha_planet, antar_planet)
        rel_hindi = {"friend": "मित्र", "enemy": "शत्रु", "neutral": "सम"}
        response += f"• <b>प्राकृतिक संबंध:</b> {PLANET_HINDI_NAMES.get(maha_planet, maha_planet)} और {PLANET_HINDI_NAMES.get(antar_planet, antar_planet)} {rel_hindi.get(natural_rel, natural_rel)} हैं<br>"

        # Overall relationship quality
        relationship = get_dasha_relationship(maha_planet, antar_planet, lagna)
        rel_emoji = {"Excellent": "🌟", "Good": "✅", "Mixed": "ℹ️", "Challenging": "⚠️"}
        rel_hindi_full = {"Excellent": "उत्कृष्ट", "Good": "अच्छा", "Mixed": "मिश्रित", "Challenging": "चुनौतीपूर्ण"}

        response += f"• <b>समग्र संबंध गुणवत्ता:</b> {rel_emoji.get(relationship, '')} {rel_hindi_full.get(relationship, relationship)}<br><br>"

        # Interpretation based on relationship
        if relationship == "Excellent":
            response += f"<b>व्याख्या:</b> यह अवधि अत्यंत शुभ है। दोनों ग्रह आपके लग्न के लिए लाभदायक हैं और आपस में मित्र भी हैं। सभी कार्यों में सफलता मिलेगी।<br><br>"
        elif relationship == "Good":
            response += f"<b>व्याख्या:</b> यह अवधि सामान्यतः शुभ है। अधिकांश कार्यों में अनुकूल परिणाम मिलेंगे।<br><br>"
        elif relationship == "Mixed":
            response += f"<b>व्याख्या:</b> यह अवधि मिश्रित फल देगी। कुछ क्षेत्रों में लाभ और कुछ में चुनौतियां हो सकती हैं।<br><br>"
        else:  # Challenging
            response += f"<b>व्याख्या:</b> यह अवधि चुनौतीपूर्ण हो सकती है। सावधानी और धैर्य रखें। शुभ कार्यों से पहले मुहूर्त देखें।<br><br>"

        # ========== UPCOMING MAHADASHAS ==========
        response += "<b>आने वाली महादशाएं:</b><br>"
        for m in self.mahadashas[:5]:
            marker = " ← <b>वर्तमान</b>" if m.planet == maha_planet else ""
            m_prediction = get_lordship_based_dasha_prediction(m.planet, lagna)
            nature = ""
            if m_prediction['is_yogakaraka']:
                nature = " 🌟योगकारक"
            elif m_prediction['is_benefic']:
                nature = " ✅शुभ"
            elif m_prediction['is_malefic']:
                nature = " ⚠️अशुभ"
            response += f"• {PLANET_HINDI_NAMES.get(m.planet, m.planet)}: {m.start_date.strftime('%Y')} - {m.end_date.strftime('%Y')}{nature}{marker}<br>"

        return response

    def lagna_answer(self):
        lagna = self.lagna
        lagna_planets = self.planets_in_houses.get(1, [])

        # Dynamic lagna characteristics
        lagna_traits = {
            "Mesha": ["साहसी और ऊर्जावान", "नेतृत्व गुण", "स्वतंत्र विचार", "जोश और उत्साह", "Quick decision maker"],
            "Vrishabha": ["धैर्यवान और स्थिर", "कला और सौंदर्य प्रेमी", "भौतिक सुख की इच्छा", "विश्वसनीय", "Practical approach"],
            "Mithuna": ["बुद्धिमान और जिज्ञासु", "Communication में निपुण", "बहुमुखी प्रतिभा", "Adaptable", "Quick learner"],
            "Karka": ["भावुक और संवेदनशील", "परिवार प्रेमी", "Nurturing nature", "Intuitive", "Home loving"],
            "Simha": ["आत्मविश्वासी", "नेतृत्व क्षमता", "Royal personality", "Creative", "Generous heart"],
            "Kanya": ["Analytical और detail-oriented", "Perfectionist स्वभाव", "Health conscious", "Practical thinking", "Problem solving में निपुण"],
            "Tula": ["संतुलित और न्यायप्रिय", "कला प्रेमी", "Diplomatic", "Social nature", "Partnership oriented"],
            "Vrishchika": ["गहन और रहस्यमय", "दृढ़ इच्छाशक्ति", "Research oriented", "Intense", "Transformative"],
            "Dhanu": ["आशावादी और दार्शनिक", "ज्ञान प्रेमी", "Adventurous", "Honest", "Freedom loving"],
            "Makara": ["महत्वाकांक्षी और अनुशासित", "मेहनती", "Practical goals", "Patient", "Responsible"],
            "Kumbha": ["अनोखे विचार", "मानवतावादी", "Innovative", "Independent thinker", "Future oriented"],
            "Meena": ["आध्यात्मिक और कल्पनाशील", "दयालु", "Artistic", "Intuitive", "Compassionate"]
        }

        traits = lagna_traits.get(lagna['rashi'], ["गुणवान व्यक्तित्व"])

        response = f"""<b>🌟 लग्न विश्लेषण:</b><br><br>
<b>लग्न राशि:</b> {self.rashi_hindi.get(lagna['rashi'], lagna['rashi'])} ({lagna['rashi_english']})<br>
<b>लग्न अंश:</b> {lagna['rashi_degree']:.2f}°<br>
<b>लग्न नक्षत्र:</b> {lagna['nakshatra']} पाद {lagna['pada']}<br><br>
"""
        if lagna_planets:
            response += f"<b>लग्न में ग्रह:</b> {', '.join([PLANET_NAMES[Planet[p]]['hindi'] for p in lagna_planets])}<br><br>"

        response += f"<b>{self.rashi_hindi.get(lagna['rashi'], lagna['rashi'])} लग्न के गुण:</b><br>"
        for trait in traits:
            response += f"• {trait}<br>"

        return response

    def rashi_answer(self):
        moon = self.planets['MOON']
        sun = self.planets['SUN']

        response = f"""<b>🌙 {self.name} की राशि विश्लेषण:</b><br><br>
<b>चंद्र राशि (Moon Sign):</b> {self.rashi_hindi.get(moon['rashi'], moon['rashi'])}<br>
<b>जन्म नक्षत्र:</b> {moon['nakshatra']} पाद {moon['pada']}<br><br>
<b>सूर्य राशि (Sun Sign):</b> {self.rashi_hindi.get(sun['rashi'], sun['rashi'])}<br><br>
<b>लग्न राशि:</b> {self.rashi_hindi.get(self.lagna['rashi'], self.lagna['rashi'])}<br><br>
<b>नोट:</b> वैदिक ज्योतिष में चंद्र राशि सबसे महत्वपूर्ण मानी जाती है। <b>{self.name}</b> {self.rashi_hindi.get(moon['rashi'], moon['rashi'])} राशि के हैं।"""

        return response

    def planet_answer(self, question):
        planet_map = {
            'sun': 'SUN', 'surya': 'SUN', 'सूर्य': 'SUN',
            'moon': 'MOON', 'chandra': 'MOON', 'चंद्र': 'MOON',
            'mars': 'MARS', 'mangal': 'MARS', 'मंगल': 'MARS',
            'mercury': 'MERCURY', 'budh': 'MERCURY', 'बुध': 'MERCURY',
            'jupiter': 'JUPITER', 'guru': 'JUPITER', 'गुरु': 'JUPITER',
            'venus': 'VENUS', 'shukra': 'VENUS', 'शुक्र': 'VENUS',
            'saturn': 'SATURN', 'shani': 'SATURN', 'शनि': 'SATURN',
            'rahu': 'RAHU', 'राहु': 'RAHU',
            'ketu': 'KETU', 'केतु': 'KETU'
        }

        asked_planet = None
        for key, value in planet_map.items():
            if key in question:
                asked_planet = value
                break

        if asked_planet:
            data = self.planets[asked_planet]
            planet_house = self.planet_houses.get(asked_planet, 1)  # Default to 1 instead of 0
            hindi = PLANET_NAMES[Planet[asked_planet]]['hindi']

            # Get effect safely
            effect = GRAHA_BHAVA_PHAL.get(asked_planet, {}).get(planet_house, 'प्रभाव उपलब्ध नहीं')

            response = f"""<b>🌟 {hindi} विश्लेषण:</b><br><br>
<b>राशि:</b> {self.rashi_hindi.get(data['rashi'], data['rashi'])} ({data['rashi_degree']:.2f}°)<br>
<b>नक्षत्र:</b> {data['nakshatra']} पाद {data['pada']}<br>
<b>भाव:</b> {planet_house}<br>
<b>गति:</b> {'वक्री (Retrograde)' if data['is_retrograde'] else 'मार्गी (Direct)'}<br><br>
<b>भाव {planet_house} में प्रभाव:</b><br>
{effect}"""

            # Add retrograde effects if applicable (balanced - positive and challenges)
            if data['is_retrograde'] and asked_planet in RETROGRADE_EFFECTS:
                retro_data = RETROGRADE_EFFECTS[asked_planet]
                response += f"<br><br><b>वक्री प्रभाव:</b><br>"
                response += f"<b>✅ लाभ:</b> {retro_data['positive']}<br>"
                response += f"<b>⚠️ सावधानी:</b> {retro_data['challenges']}<br>"
                response += f"<b>सारांश:</b> {retro_data['summary']}"

            return response

        # All planets overview
        response = "<b>🌟 सभी ग्रहों की स्थिति:</b><br><br>"
        for p_name in ["SUN", "MOON", "MARS", "MERCURY", "JUPITER", "VENUS", "SATURN", "RAHU", "KETU"]:
            data = self.planets[p_name]
            hindi = PLANET_NAMES[Planet[p_name]]['hindi']
            house = self.planet_houses.get(p_name, 1)  # Default to 1 instead of 0
            retro = " (व)" if data['is_retrograde'] else ""
            response += f"• {hindi}: {self.rashi_hindi.get(data['rashi'], data['rashi'])} - भाव {house}{retro}<br>"

        return response

    def education_answer(self):
        fourth_planets = self.planets_in_houses.get(4, [])
        fifth_planets = self.planets_in_houses.get(5, [])
        lagna_name = self.kundali.lagna['rashi']

        response = f"""<b>📚 शिक्षा विश्लेषण:</b><br><br>
<b>चतुर्थ भाव (प्राथमिक शिक्षा):</b> {len(fourth_planets)} ग्रह<br>
<b>पंचम भाव (बुद्धि):</b> {len(fifth_planets)} ग्रह<br><br>
"""
        # Dynamic education predictions based on chart
        fourth_lord = self._get_house_lord(4, lagna_name)
        fifth_lord = self._get_house_lord(5, lagna_name)
        fourth_effect = get_lagna_specific_dasha_effect(fourth_lord, lagna_name)
        fifth_effect = get_lagna_specific_dasha_effect(fifth_lord, lagna_name)

        response += "<b>शिक्षा भविष्यवाणी:</b><br>"
        response += f"• चतुर्थेश {fourth_lord} - {fourth_effect['effect']}<br>"
        response += f"• पंचमेश {fifth_lord} - {fifth_effect['effect']}<br>"

        # Mercury + Jupiter only if they are actually conjunct
        mercury_house = self.planet_houses.get('MERCURY')
        jupiter_house = self.planet_houses.get('JUPITER')
        if mercury_house and jupiter_house and mercury_house == jupiter_house:
            response += f"• बुध + गुरु भाव {mercury_house} में = उत्तम शिक्षा योग<br>"

        # Higher education based on 9th lord
        ninth_lord = self._get_house_lord(9, lagna_name)
        ninth_effect = get_lagna_specific_dasha_effect(ninth_lord, lagna_name)
        if ninth_effect['is_benefic']:
            response += "• उच्च शिक्षा में सफलता संभव<br>"

        return response

    def foreign_answer(self):
        twelfth_planets = self.planets_in_houses.get(12, [])
        rahu_house = self.planet_houses.get('RAHU', 0)
        lagna_name = self.kundali.lagna['rashi']

        response = f"""<b>✈️ विदेश विश्लेषण:</b><br><br>
<b>द्वादश भाव (विदेश):</b> {len(twelfth_planets)} ग्रह<br>
<b>राहु की स्थिति:</b> भाव {rahu_house}<br><br>
"""
        # Dynamic foreign predictions based on actual chart
        twelfth_lord = self._get_house_lord(12, lagna_name)
        twelfth_effect = get_lagna_specific_dasha_effect(twelfth_lord, lagna_name)

        response += "<b>विदेश योग:</b><br>"
        response += f"• द्वादशेश {twelfth_lord} - {twelfth_effect['effect']}<br>"

        # Rahu position analysis (only if actually in 3, 9, or 12)
        if rahu_house == 3:
            response += "• राहु 3rd में = विदेशी संपर्क अनुकूल<br>"
        elif rahu_house == 9:
            response += "• राहु 9th में = विदेश यात्रा योग<br>"
        elif rahu_house == 12:
            response += "• राहु 12th में = विदेश निवास संभव<br>"

        # 12th house analysis
        if twelfth_planets:
            response += f"• 12th में {len(twelfth_planets)} ग्रह = विदेश योग प्रबल<br>"
        else:
            response += "• 12th भाव खाली = विदेश योग सामान्य<br>"

        return response

    def lucky_answer(self):
        lagna = self.lagna['rashi']

        # Lagna-wise primary gemstone recommendations based on Vedic astrology
        lagna_lucky = {
            "Mesha": {"ratna": "मूंगा (Red Coral)", "rang": "लाल, नारंगी", "din": "मंगलवार", "ank": "9, 18, 27", "dhatu": "तांबा", "disha": "दक्षिण", "finger": "अनामिका", "planet": "मंगल"},
            "Vrishabha": {"ratna": "हीरा (Diamond)", "rang": "सफेद, गुलाबी", "din": "शुक्रवार", "ank": "6, 15, 24", "dhatu": "चांदी", "disha": "दक्षिण-पूर्व", "finger": "मध्यमा", "planet": "शुक्र"},
            "Mithuna": {"ratna": "पन्ना (Emerald)", "rang": "हरा", "din": "बुधवार", "ank": "5, 14, 23", "dhatu": "कांसा", "disha": "उत्तर", "finger": "कनिष्ठा", "planet": "बुध"},
            "Karka": {"ratna": "मोती (Pearl)", "rang": "सफेद, चांदी", "din": "सोमवार", "ank": "2, 11, 20", "dhatu": "चांदी", "disha": "उत्तर-पश्चिम", "finger": "कनिष्ठा", "planet": "चंद्र"},
            "Simha": {"ratna": "माणिक्य (Ruby)", "rang": "सुनहरा, नारंगी", "din": "रविवार", "ank": "1, 10, 19", "dhatu": "सोना", "disha": "पूर्व", "finger": "अनामिका", "planet": "सूर्य"},
            "Kanya": {"ratna": "पन्ना (Emerald)", "rang": "हरा, हल्का पीला", "din": "बुधवार", "ank": "5, 14, 23", "dhatu": "कांसा", "disha": "उत्तर", "finger": "कनिष्ठा", "planet": "बुध"},
            "Tula": {"ratna": "हीरा (Diamond)", "rang": "सफेद, हल्का नीला", "din": "शुक्रवार", "ank": "6, 15, 24", "dhatu": "चांदी", "disha": "पश्चिम", "finger": "मध्यमा", "planet": "शुक्र"},
            "Vrishchika": {"ratna": "मूंगा (Red Coral)", "rang": "लाल, मैरून", "din": "मंगलवार", "ank": "9, 18, 27", "dhatu": "तांबा", "disha": "दक्षिण", "finger": "अनामिका", "planet": "मंगल"},
            "Dhanu": {"ratna": "पुखराज (Yellow Sapphire)", "rang": "पीला, सुनहरा", "din": "गुरुवार", "ank": "3, 12, 21", "dhatu": "सोना", "disha": "उत्तर-पूर्व", "finger": "तर्जनी", "planet": "गुरु"},
            "Makara": {"ratna": "नीलम (Blue Sapphire)", "rang": "नीला, काला", "din": "शनिवार", "ank": "8, 17, 26", "dhatu": "लोहा", "disha": "पश्चिम", "finger": "मध्यमा", "planet": "शनि"},
            "Kumbha": {"ratna": "नीलम (Blue Sapphire)", "rang": "नीला, बैंगनी", "din": "शनिवार", "ank": "8, 17, 26", "dhatu": "लोहा", "disha": "पश्चिम", "finger": "मध्यमा", "planet": "शनि"},
            "Meena": {"ratna": "पुखराज (Yellow Sapphire)", "rang": "पीला, सुनहरा", "din": "गुरुवार", "ank": "3, 12, 21", "dhatu": "सोना", "disha": "उत्तर-पूर्व", "finger": "तर्जनी", "planet": "गुरु"},
        }

        # Alternative beneficial gemstones (5th and 9th lord stones)
        ALTERNATIVE_GEMSTONES = {
            "Mesha": ["माणिक्य (Ruby) - 5th lord सूर्य", "पुखराज (Yellow Sapphire) - 9th lord गुरु"],
            "Vrishabha": ["पन्ना (Emerald) - 5th lord बुध", "नीलम (Blue Sapphire) - 9th lord शनि"],
            "Mithuna": ["हीरा (Diamond) - 5th lord शुक्र", "नीलम (Blue Sapphire) - 9th lord शनि"],
            "Karka": ["मूंगा (Red Coral) - 5th lord मंगल (Yogakaraka)", "पुखराज (Yellow Sapphire) - 9th lord गुरु"],
            "Simha": ["पुखराज (Yellow Sapphire) - 5th lord गुरु", "मूंगा (Red Coral) - 9th lord मंगल"],
            "Kanya": ["नीलम (Blue Sapphire) - 5th lord शनि", "हीरा (Diamond) - 9th lord शुक्र"],
            "Tula": ["नीलम (Blue Sapphire) - 5th lord शनि", "पन्ना (Emerald) - 9th lord बुध"],
            "Vrishchika": ["पुखराज (Yellow Sapphire) - 5th lord गुरु", "चंद्र मोती (Pearl) - 9th lord चंद्र"],
            "Dhanu": ["मूंगा (Red Coral) - 5th lord मंगल", "माणिक्य (Ruby) - 9th lord सूर्य"],
            "Makara": ["हीरा (Diamond) - 5th lord शुक्र", "पन्ना (Emerald) - 9th lord बुध"],
            "Kumbha": ["पन्ना (Emerald) - 5th lord बुध", "हीरा (Diamond) - 9th lord शुक्र"],
            "Meena": ["चंद्र मोती (Pearl) - 5th lord चंद्र", "मूंगा (Red Coral) - 9th lord मंगल"],
        }

        # Gemstones to AVOID based on functional malefics
        GEMSTONES_TO_AVOID = {
            "Mesha": {"stones": ["पन्ना (Emerald)", "हीरा (Diamond)", "नीलम (Blue Sapphire)"],
                      "reason": "बुध, शुक्र, शनि 3rd/6th/10th/11th lord - मिश्रित"},
            "Vrishabha": {"stones": ["मूंगा (Red Coral)", "पुखराज (Yellow Sapphire)"],
                          "reason": "मंगल 7th/12th lord, गुरु 8th/11th lord"},
            "Mithuna": {"stones": ["मूंगा (Red Coral)", "माणिक्य (Ruby)"],
                        "reason": "मंगल 6th/11th lord, सूर्य 3rd lord"},
            "Karka": {"stones": ["नीलम (Blue Sapphire)", "पन्ना (Emerald)", "हीरा (Diamond)"],
                      "reason": "शनि 7th/8th lord (Maraka), बुध 3rd/12th lord, शुक्र 4th/11th lord"},
            "Simha": {"stones": ["नीलम (Blue Sapphire)", "हीरा (Diamond)"],
                      "reason": "शनि 6th/7th lord, शुक्र 3rd/10th lord"},
            "Kanya": {"stones": ["मूंगा (Red Coral)", "मोती (Pearl)", "पुखराज (Yellow Sapphire)"],
                      "reason": "मंगल 3rd/8th lord, चंद्र 11th lord, गुरु 4th/7th lord"},
            "Tula": {"stones": ["माणिक्य (Ruby)", "मूंगा (Red Coral)", "पुखराज (Yellow Sapphire)"],
                     "reason": "सूर्य 11th lord, मंगल 2nd/7th lord, गुरु 3rd/6th lord"},
            "Vrishchika": {"stones": ["पन्ना (Emerald)", "हीरा (Diamond)"],
                           "reason": "बुध 8th/11th lord, शुक्र 7th/12th lord"},
            "Dhanu": {"stones": ["हीरा (Diamond)", "नीलम (Blue Sapphire)", "पन्ना (Emerald)"],
                      "reason": "शुक्र 6th/11th lord, शनि 2nd/3rd lord, बुध 7th/10th lord"},
            "Makara": {"stones": ["मूंगा (Red Coral)", "मोती (Pearl)", "पुखराज (Yellow Sapphire)"],
                       "reason": "मंगल 4th/11th lord, चंद्र 7th lord, गुरु 3rd/12th lord"},
            "Kumbha": {"stones": ["मोती (Pearl)", "मूंगा (Red Coral)", "पुखराज (Yellow Sapphire)"],
                       "reason": "चंद्र 6th lord, मंगल 3rd/10th lord, गुरु 2nd/11th lord"},
            "Meena": {"stones": ["माणिक्य (Ruby)", "हीरा (Diamond)", "नीलम (Blue Sapphire)", "पन्ना (Emerald)"],
                      "reason": "सूर्य 6th lord, शुक्र 3rd/8th lord, शनि 11th/12th lord, बुध 4th/7th lord"},
        }

        # Gemstone weight recommendations
        GEMSTONE_WEIGHTS = {
            "Ruby": "3-6 रत्ती (Minimum 3 for effect)",
            "Pearl": "4-6 रत्ती",
            "Coral": "6-9 रत्ती",
            "Emerald": "3-5 रत्ती",
            "Yellow Sapphire": "3-5 रत्ती",
            "Diamond": "0.5-1 कैरेट",
            "Blue Sapphire": "2-5 रत्ती (Trial first!)",
            "Hessonite": "4-6 रत्ती",
            "Cat's Eye": "3-5 रत्ती",
        }

        lucky = lagna_lucky.get(lagna, lagna_lucky["Mesha"])
        alternatives = ALTERNATIVE_GEMSTONES.get(lagna, [])
        avoid_info = GEMSTONES_TO_AVOID.get(lagna, {"stones": [], "reason": ""})

        # Format alternative stones
        alternative_stones_str = "<br>".join([f"  • {stone}" for stone in alternatives]) if alternatives else "कोई नहीं"

        # Format stones to avoid
        avoid_stones_str = ", ".join(avoid_info["stones"]) if avoid_info["stones"] else "कोई नहीं"

        # Determine primary stone weight recommendation
        primary_stone = lucky['ratna']
        weight_key = None
        if "Ruby" in primary_stone or "माणिक्य" in primary_stone:
            weight_key = "Ruby"
        elif "Pearl" in primary_stone or "मोती" in primary_stone:
            weight_key = "Pearl"
        elif "Coral" in primary_stone or "मूंगा" in primary_stone:
            weight_key = "Coral"
        elif "Emerald" in primary_stone or "पन्ना" in primary_stone:
            weight_key = "Emerald"
        elif "Yellow Sapphire" in primary_stone or "पुखराज" in primary_stone:
            weight_key = "Yellow Sapphire"
        elif "Diamond" in primary_stone or "हीरा" in primary_stone:
            weight_key = "Diamond"
        elif "Blue Sapphire" in primary_stone or "नीलम" in primary_stone:
            weight_key = "Blue Sapphire"

        weight_recommendation = GEMSTONE_WEIGHTS.get(weight_key, "3-5 रत्ती")

        # Rahu/Ketu gemstone recommendations with caution
        rahu_house = self.planet_houses.get('RAHU', 0)
        ketu_house = self.planet_houses.get('KETU', 0)

        rahu_ketu_section = ""
        # Rahu is well placed in 3, 6, 10, 11
        if rahu_house in [3, 6, 10, 11]:
            rahu_ketu_section += f"""<br><b>राहु रत्न (सावधानी से):</b><br>
• गोमेद (Hessonite) - {GEMSTONE_WEIGHTS['Hessonite']}<br>
• राहु भाव {rahu_house} में शुभ स्थिति<br>
• पहनने से पहले 3 दिन trial करें<br>"""

        # Ketu is well placed in 3, 6, 9, 12
        if ketu_house in [3, 6, 9, 12]:
            rahu_ketu_section += f"""<br><b>केतु रत्न (सावधानी से):</b><br>
• लहसुनिया (Cat's Eye) - {GEMSTONE_WEIGHTS["Cat's Eye"]}<br>
• केतु भाव {ketu_house} में शुभ स्थिति<br>
• आध्यात्मिक उन्नति हेतु उपयुक्त<br>"""

        response = f"""<b>🍀 {self.name} के शुभ तत्व:</b><br><br>
<b>{self.rashi_hindi.get(lagna, lagna)} लग्न के लिए:</b><br><br>

<b>✅ पहनने योग्य रत्न:</b><br>
• <b>प्राथमिक:</b> {lucky['ratna']}<br>
• <b>वैकल्पिक (5th/9th Lord):</b><br>
{alternative_stones_str}<br><br>

<b>❌ न पहनें (Avoid):</b><br>
• {avoid_stones_str}<br>
• <b>कारण:</b> {avoid_info['reason']}<br><br>

<b>शुभ रंग:</b> {lucky['rang']}<br>
<b>शुभ अंक:</b> {lucky['ank']}<br>
<b>शुभ दिन:</b> {lucky['din']}<br>
<b>शुभ धातु:</b> {lucky['dhatu']}<br>
<b>शुभ दिशा:</b> {lucky['disha']}<br><br>

<b>रत्न धारण विधि:</b><br>
• {lucky['ratna']} - {weight_recommendation}<br>
• सोने/चांदी की अंगूठी में<br>
• {lucky['finger']} अंगुली में<br>
• {lucky['din']} सूर्योदय के समय<br>
• {lucky['planet']} मंत्र जाप के साथ<br><br>

<b>रत्न वजन मार्गदर्शिका:</b><br>
• माणिक्य (Ruby): {GEMSTONE_WEIGHTS['Ruby']}<br>
• मोती (Pearl): {GEMSTONE_WEIGHTS['Pearl']}<br>
• मूंगा (Coral): {GEMSTONE_WEIGHTS['Coral']}<br>
• पन्ना (Emerald): {GEMSTONE_WEIGHTS['Emerald']}<br>
• पुखराज (Yellow Sapphire): {GEMSTONE_WEIGHTS['Yellow Sapphire']}<br>
• हीरा (Diamond): {GEMSTONE_WEIGHTS['Diamond']}<br>
• नीलम (Blue Sapphire): {GEMSTONE_WEIGHTS['Blue Sapphire']}{rahu_ketu_section}"""

        return response

    def remedy_answer(self):
        """Generate chart-specific remedies based on lagna and weak planets."""
        lagna_name = self.kundali.lagna['rashi']
        current_maha = self.current_dasha['mahadasha']['planet']

        # Planet remedy data
        PLANET_REMEDIES = {
            "Sun": {"mantra": "ॐ ह्रां ह्रीं ह्रौं सः सूर्याय नमः", "day": "रविवार", "color": "लाल/नारंगी", "donation": "गेहूं, गुड़, तांबा", "deity": "सूर्य देव"},
            "Moon": {"mantra": "ॐ सों सोमाय नमः", "day": "सोमवार", "color": "सफेद", "donation": "चावल, दूध, चांदी", "deity": "शिव जी"},
            "Mars": {"mantra": "ॐ अं अंगारकाय नमः", "day": "मंगलवार", "color": "लाल", "donation": "मसूर दाल, लाल वस्त्र", "deity": "हनुमान जी"},
            "Mercury": {"mantra": "ॐ बुं बुधाय नमः", "day": "बुधवार", "color": "हरा", "donation": "मूंग दाल, हरी सब्जी", "deity": "गणेश जी"},
            "Jupiter": {"mantra": "ॐ बृं बृहस्पतये नमः", "day": "गुरुवार", "color": "पीला", "donation": "चना दाल, केला, हल्दी", "deity": "विष्णु भगवान"},
            "Venus": {"mantra": "ॐ शुं शुक्राय नमः", "day": "शुक्रवार", "color": "सफेद/गुलाबी", "donation": "चावल, कपूर, मिठाई", "deity": "लक्ष्मी जी"},
            "Saturn": {"mantra": "ॐ शं शनैश्चराय नमः", "day": "शनिवार", "color": "काला/नीला", "donation": "काले तिल, सरसों तेल", "deity": "शनि देव/हनुमान जी"},
            "Rahu": {"mantra": "ॐ रां राहवे नमः", "day": "शनिवार", "color": "गहरा नीला", "donation": "कोयला, काला कपड़ा", "deity": "दुर्गा माता"},
            "Ketu": {"mantra": "ॐ कें केतवे नमः", "day": "मंगलवार", "color": "भूरा/धूसर", "donation": "कंबल, तिल", "deity": "गणेश जी"},
        }

        response = f"<b>🙏 {self.name} के लिए विशेष उपाय ({lagna_name} लग्न):</b><br><br>"

        # 1. Lagna lord remedy (most important)
        lagna_lord = self._get_house_lord(1, lagna_name)
        lagna_remedy = PLANET_REMEDIES.get(lagna_lord, {})
        response += f"<b>लग्नेश {lagna_lord} के उपाय (सर्वप्रथम):</b><br>"
        response += f"• मंत्र: {lagna_remedy.get('mantra', '')} (108 बार, {lagna_remedy.get('day', '')})<br>"
        response += f"• रंग: {lagna_remedy.get('color', '')} के वस्त्र {lagna_remedy.get('day', '')} को<br>"
        response += f"• देवता: {lagna_remedy.get('deity', '')} की पूजा<br><br>"

        # 2. Current dasha lord remedy (if different from lagna lord)
        if current_maha != lagna_lord:
            maha_effect = get_lagna_specific_dasha_effect(current_maha, lagna_name)
            maha_remedy = PLANET_REMEDIES.get(current_maha, {})
            status = "शुभ" if maha_effect['is_benefic'] else "उपाय आवश्यक"
            response += f"<b>वर्तमान महादशा {current_maha} ({status}):</b><br>"
            response += f"• मंत्र: {maha_remedy.get('mantra', '')} ({maha_remedy.get('day', '')})<br>"
            if not maha_effect['is_benefic']:
                response += f"• दान: {maha_remedy.get('donation', '')} {maha_remedy.get('day', '')} को<br>"
            response += "<br>"

        # 3. Weak planet remedies (planets in 6, 8, 12 or debilitated)
        weak_planets = []
        for h in [6, 8, 12]:
            weak_planets.extend(self.planets_in_houses.get(h, []))

        if weak_planets:
            response += "<b>कमजोर ग्रहों के उपाय:</b><br>"
            for planet in set(weak_planets):
                if planet in ["RAHU", "KETU"]:
                    continue  # Shadow planets handled separately
                p_remedy = PLANET_REMEDIES.get(planet, {})
                if p_remedy:
                    response += f"• {planet}: {p_remedy.get('donation', '')} का दान {p_remedy.get('day', '')} को<br>"

        return response

    def sade_sati_answer(self):
        """Answer questions about Sade Sati with real transit-based predictions."""
        from datetime import datetime

        moon_rashi_num = self.planets['MOON']['rashi_num']
        moon_rashi = self.planets['MOON']['rashi']

        try:
            from .sade_sati_transit import SadeSatiTracker
            tracker = SadeSatiTracker(moon_rashi_num)

            # Check current status using real Saturn transit
            current_status = tracker.is_sade_sati_active(datetime.now())

            if current_status["active"]:
                phase_hindi = {"Rising": "आरंभ (12वां भाव)", "Peak": "चरम (चंद्र पर)", "Setting": "अंत (2रा भाव)"}.get(current_status["phase"], current_status["phase"])
                severity_hindi = {"High": "उच्च", "Medium": "मध्यम", "Low": "निम्न"}.get(current_status["severity"], current_status["severity"])

                response = f"""<b>⚠️ साढ़े साती वर्तमान में सक्रिय!</b><br><br>
<b>चंद्र राशि:</b> {self.rashi_hindi.get(moon_rashi, moon_rashi)}<br>
<b>शनि वर्तमान राशि:</b> {current_status.get('saturn_rashi', 'N/A')}<br><br>
<b>चरण:</b> {phase_hindi}<br>
<b>तीव्रता:</b> {severity_hindi}<br><br>"""

                # Get progress if available
                progress = tracker.get_current_sade_sati_progress()
                if progress:
                    response += f"""<b>प्रगति:</b> {progress.get('percent_complete', 0):.1f}% पूर्ण<br>
<b>शेष दिन:</b> ~{progress.get('days_remaining', 0)} दिन<br><br>"""

                response += """<b>उपाय:</b><br>
• शनिवार व्रत रखें<br>
• हनुमान चालीसा का पाठ करें<br>
• शनि मंत्र: ॐ शं शनैश्चराय नमः (108 बार)<br>
• काले तिल और सरसों तेल दान करें"""
            else:
                # Get next Sade Sati period
                next_ss = tracker.get_next_sade_sati(datetime.now())

                response = f"""✅ <b>साढ़े साती वर्तमान में सक्रिय नहीं है।</b><br><br>
<b>चंद्र राशि:</b> {self.rashi_hindi.get(moon_rashi, moon_rashi)}<br><br>"""

                if next_ss:
                    response += f"""<b>📅 अगली साढ़े साती:</b><br>
• <b>शुरू:</b> {next_ss['start_date'].strftime('%d %B %Y')}<br>
• <b>समाप्त:</b> {next_ss['end_date'].strftime('%d %B %Y')}<br>
• <b>कितने वर्ष बाद:</b> {next_ss['years_from_now']:.1f} वर्ष<br><br>"""

                # Get 30-year timeline
                timeline = tracker.get_sade_sati_timeline(30)
                if timeline:
                    response += "<b>🗓️ आगामी 30 वर्षों का साढ़े साती कैलेंडर:</b><br>"
                    for period in timeline[:3]:  # Show max 3 periods
                        response += f"• {period['total_start_date'].strftime('%Y')} - {period['total_end_date'].strftime('%Y')}<br>"

        except Exception as e:
            # Fallback to birth chart based check
            saturn_rashi_num = self.planets['SATURN']['rashi_num']
            saturn_rashi = self.planets['SATURN']['rashi']
            sade_sati = check_sade_sati(moon_rashi_num, saturn_rashi_num)

            if sade_sati["active"]:
                response = f"""<b>⚠️ जन्म कुंडली में साढ़े साती योग:</b><br><br>
<b>चंद्र राशि:</b> {self.rashi_hindi.get(moon_rashi, moon_rashi)}<br>
<b>शनि राशि (जन्म):</b> {self.rashi_hindi.get(saturn_rashi, saturn_rashi)}<br>
<b>चरण:</b> {sade_sati["phase"]}<br>"""
            else:
                response = f"""✅ <b>जन्म कुंडली में साढ़े साती योग नहीं है।</b><br><br>
<b>चंद्र राशि:</b> {self.rashi_hindi.get(moon_rashi, moon_rashi)}<br>
<b>नोट:</b> वास्तविक तिथियों के लिए गोचर विश्लेषण आवश्यक।"""

        return response

    def kaal_sarp_answer(self):
        """Answer questions about Kaal Sarp Dosh with cancellations."""
        kaal_sarp = check_kaal_sarp_dosh(self.planets, self.planets_in_houses)

        if kaal_sarp["present"]:
            cancelled = kaal_sarp.get("cancelled", False)
            partial = kaal_sarp.get("partial", False)
            cancellations = kaal_sarp.get("cancellations", [])

            rahu_house = 0
            ketu_house = 0
            for house, planets in self.planets_in_houses.items():
                if 'RAHU' in planets:
                    rahu_house = house
                if 'KETU' in planets:
                    ketu_house = house

            if cancelled:
                response = f"""<b>🐍 काल सर्प दोष (निरस्त!)</b><br><br>
<b>राहु भाव:</b> {rahu_house}<br>
<b>केतु भाव:</b> {ketu_house}<br><br>
<b>स्थिति:</b> सभी ग्रह राहु-केतु अक्ष में हैं।<br><br>
<b>🎉 शुभ समाचार - दोष निरस्त:</b><br>"""
                for c in cancellations:
                    response += f"• ✅ {c}<br>"
                response += """<br><b>सारांश:</b> शुभ योगों के कारण काल सर्प दोष का प्रभाव नगण्य है।"""
            elif partial:
                response = f"""<b>🐍 काल सर्प दोष (आंशिक)</b><br><br>
<b>राहु भाव:</b> {rahu_house}<br>
<b>केतु भाव:</b> {ketu_house}<br><br>
<b>स्थिति:</b> सभी ग्रह राहु-केतु अक्ष में हैं।<br><br>
<b>आंशिक निवारण:</b><br>"""
                for c in cancellations:
                    response += f"• {c}<br>"
                response += """<br><b>प्रभाव:</b> मध्यम - उपाय से लाभ होगा।<br><br>
<b>उपाय:</b><br>
• नाग पंचमी पर नाग पूजा<br>
• राहु मंत्र: ॐ रां राहवे नमः (18,000 जाप)<br>
• केतु मंत्र: ॐ कें केतवे नमः (17,000 जाप)<br>
• सर्प शांति पूजा करवाएं"""
            else:
                response = f"""<b>🐍 काल सर्प दोष सक्रिय!</b><br><br>
<b>राहु भाव:</b> {rahu_house}<br>
<b>केतु भाव:</b> {ketu_house}<br><br>
<b>स्थिति:</b> सभी ग्रह राहु-केतु अक्ष में हैं।<br><br>
<b>प्रभाव:</b><br>
• जीवन में अचानक बाधाएं और विलंब<br>
• कार्यों में अप्रत्याशित समस्याएं<br>
• मानसिक तनाव की संभावना<br><br>
<b>उपाय:</b><br>
• नाग पंचमी पर नाग पूजा अवश्य करें<br>
• राहु मंत्र: ॐ रां राहवे नमः (18,000 जाप)<br>
• केतु मंत्र: ॐ कें केतवे नमः (17,000 जाप)<br>
• त्र्यंबकेश्वर या कालहस्ती में सर्प दोष शांति करवाएं<br>
• गोमेद रत्न धारण करें (ज्योतिषी से परामर्श लें)"""
        else:
            response = """✅ <b>काल सर्प दोष नहीं है!</b><br><br>
<b>जानकारी:</b> जब सभी ग्रह राहु-केतु अक्ष के एक तरफ हों तो काल सर्प दोष बनता है।<br><br>
आपकी कुंडली में ग्रह राहु-केतु अक्ष के दोनों तरफ हैं, इसलिए यह दोष नहीं है।"""

        return response

    def pitra_dosh_answer(self):
        """Answer questions about Pitra Dosh with cancellations."""
        pitra_dosh = check_pitra_dosh(self.planets, self.planets_in_houses, self.lagna)

        if pitra_dosh["present"]:
            cancelled = pitra_dosh.get("cancelled", False)
            reasons = pitra_dosh.get("reasons", [])
            cancellations = pitra_dosh.get("cancellations", [])

            if cancelled:
                response = f"""<b>🙏 पितृ दोष (शांत)</b><br><br>
<b>दोष कारण:</b><br>"""
                for r in reasons:
                    response += f"• {r}<br>"
                response += """<br><b>🎉 शुभ समाचार - दोष शांति:</b><br>"""
                for c in cancellations:
                    response += f"• ✅ {c}<br>"
                response += """<br><b>सारांश:</b> शुभ योगों के कारण पितृ दोष का प्रभाव नगण्य है। पितृ कृपा प्राप्त है।"""
            else:
                response = f"""<b>⚠️ पितृ दोष सक्रिय!</b><br><br>
<b>दोष कारण:</b><br>"""
                for r in reasons:
                    response += f"• {r}<br>"
                if cancellations:
                    response += """<br><b>आंशिक शांति:</b><br>"""
                    for c in cancellations:
                        response += f"• {c}<br>"
                response += """<br><b>प्रभाव:</b><br>
• पैतृक संपत्ति में समस्या<br>
• संतान सुख में बाधा<br>
• करियर में अवरोध<br><br>
<b>उपाय:</b><br>
• पितृ पक्ष में श्राद्ध अवश्य करें<br>
• अमावस्या को पिंड दान करें<br>
• पितृ गायत्री मंत्र का जाप करें<br>
• गया जी में पिंड दान अत्यंत लाभकारी<br>
• पितृों को जल अर्पण करें (प्रतिदिन)"""
        else:
            response = """✅ <b>पितृ दोष नहीं है!</b><br><br>
<b>जानकारी:</b> पितृ दोष तब बनता है जब:<br>
• सूर्य राहु या केतु के साथ हो<br>
• 9वें भाव में राहु, केतु या शनि हो<br><br>
आपकी कुंडली में ये योग नहीं हैं। पितृ कृपा प्राप्त है।"""

        return response

    def neecha_bhanga_answer(self):
        """Answer questions about Neecha Bhanga Raja Yoga."""
        neecha_bhanga = check_neecha_bhanga_raja_yoga(self.planets, self.planets_in_houses, self.lagna)

        if neecha_bhanga["present"]:
            yoga_planets = neecha_bhanga.get("planets", [])
            all_reasons = neecha_bhanga.get("reasons", [])

            response = f"""<b>🌟 नीच भंग राज योग - अत्यंत शुभ!</b><br><br>
<b>प्रभावित ग्रह:</b><br>"""
            for yp in yoga_planets:
                response += f"• <b>{yp['planet_hindi']}</b> नीच राशि में, पर भंग!<br>"
                for r in yp['reasons']:
                    response += f"  - {r}<br>"
            response += """<br><b>फल:</b><br>
• नीच ग्रह राजयोग देता है!<br>
• कठिनाई से अप्रत्याशित सफलता<br>
• उच्च पद और सम्मान<br>
• विपरीत परिस्थितियों में विजय<br><br>
<b>विशेष:</b> यह योग बताता है कि आप मुश्किल परिस्थितियों को अवसर में बदल सकते हैं।<br>
जो ग्रह कमजोर दिखता है, वही सबसे बड़ा लाभ देगा!"""
        else:
            response = """<b>नीच भंग राज योग</b><br><br>
<b>जानकारी:</b> जब कोई ग्रह नीच राशि में हो पर उसका भंग (cancellation) हो जाए तो नीच भंग राज योग बनता है।<br><br>
<b>भंग के कारण:</b><br>
• नीच राशि का स्वामी केंद्र में हो<br>
• उच्च राशि का स्वामी केंद्र में हो<br>
• नीच ग्रह स्वयं केंद्र में हो<br>
• नीच ग्रह पर उसके स्वामी की दृष्टि हो<br><br>
आपकी कुंडली में यह विशेष योग नहीं है।"""

        return response

    def summary_answer(self):
        response = f"""<b>📝 {self.name} की कुंडली सारांश:</b><br><br>
<b>मूल जानकारी:</b><br>
• नाम: <b>{self.name}</b><br>
• लग्न: {self.rashi_hindi.get(self.lagna['rashi'], self.lagna['rashi'])}<br>
• चंद्र राशि: {self.rashi_hindi.get(self.planets['MOON']['rashi'], self.planets['MOON']['rashi'])}<br>
• नक्षत्र: {self.planets['MOON']['nakshatra']}<br>
• वर्तमान दशा: {self.current_dasha['full_dasha']}<br><br>
"""

        # Add retrograde planets list
        retrograde_planets = []
        for p_name in ["MARS", "MERCURY", "JUPITER", "VENUS", "SATURN", "RAHU", "KETU"]:
            if self.planets[p_name]['is_retrograde']:
                hindi = PLANET_NAMES[Planet[p_name]]['hindi']
                retrograde_planets.append(hindi)

        if retrograde_planets:
            response += f"<b>वक्री ग्रह:</b> {', '.join(retrograde_planets)}<br><br>"

        # Check and add Sade Sati status
        moon_rashi_num = self.planets['MOON']['rashi_num']
        saturn_rashi_num = self.planets['SATURN']['rashi_num']
        sade_sati = check_sade_sati(moon_rashi_num, saturn_rashi_num)

        if sade_sati["active"]:
            response += f"""⚠️ <b>साढ़े साती सक्रिय:</b> {sade_sati["phase"]} ({sade_sati["severity"]})<br><br>
"""

        # Dynamic ratings based on actual chart
        career_rating = self._calculate_rating('career')
        marriage_rating = self._calculate_rating('marriage')
        children_rating = self._calculate_rating('children')
        health_rating = self._calculate_rating('health')
        wealth_rating = self._calculate_rating('wealth')

        second_planets = self.planets_in_houses.get(2, [])
        wealth_note = f"({len(second_planets)} ग्रह धन भाव में)" if len(second_planets) >= 2 else ""

        # Get current mahadasha for golden period
        current_maha = self.mahadashas[0].planet if self.mahadashas else "अज्ञात"

        response += f"""<b>जीवन क्षेत्र रेटिंग:</b><br>
• करियर: {career_rating} ({CAREER_BY_LAGNA.get(self.lagna['rashi'], 'विविध क्षेत्र')[:20]}...)<br>
• विवाह: {marriage_rating}<br>
• संतान: {children_rating}<br>
• स्वास्थ्य: {health_rating}<br>
• धन: {wealth_rating} {wealth_note}<br><br>
<b>वर्तमान महादशा:</b> {current_maha}"""

        return response

    def _calculate_rating(self, area):
        """Calculate star rating for different life areas."""
        score = 3  # Base score

        if area == 'career':
            tenth_planets = self.planets_in_houses.get(10, [])
            if "JUPITER" in tenth_planets or "VENUS" in tenth_planets:
                score += 1
            if "SUN" in tenth_planets:
                score += 1
        elif area == 'marriage':
            venus_house = self.planet_houses.get('VENUS', 0)
            if venus_house in [1, 2, 4, 5, 7, 9, 11]:
                score += 1
            seventh_planets = self.planets_in_houses.get(7, [])
            if "SATURN" in seventh_planets or "RAHU" in seventh_planets:
                score -= 0.5
        elif area == 'children':
            jupiter_house = self.planet_houses.get('JUPITER', 0)
            if jupiter_house in [1, 2, 5, 9, 11]:
                score += 1
            fifth_planets = self.planets_in_houses.get(5, [])
            if "SATURN" in fifth_planets:
                score -= 0.5
        elif area == 'health':
            first_planets = self.planets_in_houses.get(1, [])
            if "JUPITER" in first_planets or "VENUS" in first_planets:
                score += 1
            sixth_planets = self.planets_in_houses.get(6, [])
            if len(sixth_planets) >= 2:
                score -= 0.5
        elif area == 'wealth':
            second_planets = self.planets_in_houses.get(2, [])
            if len(second_planets) >= 2:
                score += 1
            if len(second_planets) >= 3:
                score += 1

        return "⭐" * min(5, max(1, int(score)))

    def transit_answer(self):
        """Answer questions about current transits (Gochara)."""
        from datetime import datetime

        moon_rashi_num = self.planets['MOON']['rashi_num']
        moon_rashi = self.planets['MOON']['rashi']
        saturn_rashi_num = self.planets['SATURN']['rashi_num']
        saturn_rashi = self.planets['SATURN']['rashi']
        jupiter_rashi_num = self.planets['JUPITER']['rashi_num']
        jupiter_rashi = self.planets['JUPITER']['rashi']
        rahu_rashi_num = self.planets['RAHU']['rashi_num']
        rahu_rashi = self.planets['RAHU']['rashi']
        ketu_rashi_num = self.planets['KETU']['rashi_num']
        ketu_rashi = self.planets['KETU']['rashi']

        # Calculate houses from Moon
        def house_from_moon(planet_rashi_num):
            return ((planet_rashi_num - moon_rashi_num) % 12) + 1

        saturn_house = house_from_moon(saturn_rashi_num)
        jupiter_house = house_from_moon(jupiter_rashi_num)
        rahu_house = house_from_moon(rahu_rashi_num)
        ketu_house = house_from_moon(ketu_rashi_num)

        # Transit effects
        saturn_effect = self._get_saturn_gochara_effect(saturn_house)
        jupiter_effect = self._get_jupiter_gochara_effect(jupiter_house)

        response = f"""<b>🌍 {self.name} का गोचर विश्लेषण:</b><br><br>
<b>चंद्र राशि:</b> {self.rashi_hindi.get(moon_rashi, moon_rashi)}<br><br>

<b>प्रमुख ग्रहों की स्थिति (चंद्र से):</b><br>
<table style="width:100%; border-collapse:collapse; margin:10px 0;">
<tr style="background:#ff6b35; color:white;">
<th style="padding:8px; border:1px solid #ddd;">ग्रह</th>
<th style="padding:8px; border:1px solid #ddd;">राशि</th>
<th style="padding:8px; border:1px solid #ddd;">चंद्र से भाव</th>
<th style="padding:8px; border:1px solid #ddd;">प्रभाव</th>
</tr>
<tr>
<td style="padding:8px; border:1px solid #ddd;"><b>शनि</b></td>
<td style="padding:8px; border:1px solid #ddd;">{self.rashi_hindi.get(saturn_rashi, saturn_rashi)}</td>
<td style="padding:8px; border:1px solid #ddd;">{saturn_house}</td>
<td style="padding:8px; border:1px solid #ddd;">{saturn_effect}</td>
</tr>
<tr>
<td style="padding:8px; border:1px solid #ddd;"><b>गुरु</b></td>
<td style="padding:8px; border:1px solid #ddd;">{self.rashi_hindi.get(jupiter_rashi, jupiter_rashi)}</td>
<td style="padding:8px; border:1px solid #ddd;">{jupiter_house}</td>
<td style="padding:8px; border:1px solid #ddd;">{jupiter_effect}</td>
</tr>
<tr>
<td style="padding:8px; border:1px solid #ddd;"><b>राहु</b></td>
<td style="padding:8px; border:1px solid #ddd;">{self.rashi_hindi.get(rahu_rashi, rahu_rashi)}</td>
<td style="padding:8px; border:1px solid #ddd;">{rahu_house}</td>
<td style="padding:8px; border:1px solid #ddd;">{self._get_rahu_gochara_effect(rahu_house)}</td>
</tr>
<tr>
<td style="padding:8px; border:1px solid #ddd;"><b>केतु</b></td>
<td style="padding:8px; border:1px solid #ddd;">{self.rashi_hindi.get(ketu_rashi, ketu_rashi)}</td>
<td style="padding:8px; border:1px solid #ddd;">{ketu_house}</td>
<td style="padding:8px; border:1px solid #ddd;">{self._get_ketu_gochara_effect(ketu_house)}</td>
</tr>
</table>

<b>नोट:</b> यह जन्म कुंडली के ग्रह स्थिति पर आधारित है। वास्तविक गोचर फल के लिए वर्तमान ग्रह स्थिति देखें।
"""
        return response

    def _get_saturn_gochara_effect(self, house):
        """Get Saturn transit effect based on house from Moon."""
        effects = {
            1: "साढ़े साती शिखर - सावधानी",
            2: "साढ़े साती अंतिम - वित्तीय तनाव",
            3: "शुभ - साहस वृद्धि",
            4: "चुनौतीपूर्ण - गृह चिंता",
            5: "मिश्रित - संतान/शिक्षा विलंब",
            6: "शुभ - शत्रु विजय",
            7: "चुनौतीपूर्ण - वैवाहिक तनाव",
            8: "कठिन - अष्टम शनि",
            9: "मिश्रित - भाग्य विलंब",
            10: "मिश्रित - करियर मेहनत",
            11: "शुभ - आय वृद्धि",
            12: "साढ़े साती प्रारंभ - खर्च वृद्धि"
        }
        return effects.get(house, "सामान्य प्रभाव")

    def _get_jupiter_gochara_effect(self, house):
        """Get Jupiter transit effect based on house from Moon."""
        effects = {
            1: "अत्यंत शुभ - सम्मान, समृद्धि",
            2: "शुभ - धन लाभ",
            3: "मिश्रित - भाई मतभेद",
            4: "मिश्रित - गृह परिवर्तन",
            5: "अत्यंत शुभ - संतान सुख",
            6: "चुनौतीपूर्ण - रोग सावधानी",
            7: "अत्यंत शुभ - विवाह योग",
            8: "चुनौतीपूर्ण - बाधाएं",
            9: "अत्यंत शुभ - भाग्योदय",
            10: "शुभ - करियर उन्नति",
            11: "अत्यंत शुभ - सर्वत्र लाभ",
            12: "चुनौतीपूर्ण - खर्च वृद्धि"
        }
        return effects.get(house, "सामान्य प्रभाव")

    def _get_rahu_gochara_effect(self, house):
        """Get Rahu transit effect based on house from Moon."""
        effects = {
            1: "मिश्रित - परिवर्तन", 2: "चुनौतीपूर्ण - धन समस्या",
            3: "शुभ - साहस", 4: "चुनौतीपूर्ण - मन अशांति",
            5: "मिश्रित - संतान चिंता", 6: "शुभ - शत्रु विजय",
            7: "चुनौतीपूर्ण - संबंध उलझन", 8: "मिश्रित - गुप्त लाभ/हानि",
            9: "मिश्रित - धर्म अरुचि", 10: "शुभ - करियर उन्नति",
            11: "शुभ - विदेशी लाभ", 12: "मिश्रित - विदेश यात्रा"
        }
        return effects.get(house, "सामान्य")

    def _get_ketu_gochara_effect(self, house):
        """Get Ketu transit effect based on house from Moon."""
        effects = {
            1: "मिश्रित - आत्मचिंतन", 2: "चुनौतीपूर्ण - वाणी कटुता",
            3: "शुभ - आध्यात्मिक साहस", 4: "चुनौतीपूर्ण - विरक्ति",
            5: "मिश्रित - आध्यात्मिक रुझान", 6: "शुभ - रोग मुक्ति",
            7: "चुनौतीपूर्ण - साथी विरक्ति", 8: "मिश्रित - मोक्ष मार्ग",
            9: "शुभ - आध्यात्मिक उन्नति", 10: "चुनौतीपूर्ण - करियर अनिश्चितता",
            11: "शुभ - आध्यात्मिक मित्र", 12: "शुभ - मोक्ष साधना"
        }
        return effects.get(house, "सामान्य")

    def marriage_timing_answer(self):
        """Answer questions about marriage timing."""
        from datetime import datetime

        try:
            from .event_predictor import EventPredictor
            predictor = EventPredictor(self.kundali)
            current_year = datetime.now().year

            predictions = predictor.get_best_periods("marriage", current_year, current_year + 5, top_n=3)

            response = f"""<b>💑 {self.name} के विवाह का शुभ समय:</b><br><br>"""

            if predictions:
                response += "<b>अगले 5 वर्षों में शुभ समय:</b><br>"
                for i, pred in enumerate(predictions, 1):
                    favorability = "उच्च ⭐⭐⭐" if pred['favorability'] == "High" else "मध्यम ⭐⭐" if pred['favorability'] == "Medium" else "निम्न ⭐"
                    response += f"""
<br><b>{i}. {pred['period']}</b><br>
• दशा: {pred['dasha']}<br>
• अनुकूलता: {favorability}<br>
• कारण: {'; '.join(pred['reasons'][:2])}<br>
"""
            else:
                response += """<p>इस अवधि में विशेष शुभ योग नहीं मिले। दशा विश्लेषण देखें।</p>"""

            response += """<br><b>विवाह के लिए शुभ दशाएं:</b><br>
• शुक्र की दशा (विवाह कारक)<br>
• सप्तमेश की दशा<br>
• गुरु की दशा (शुभ ग्रह)"""

        except Exception as e:
            lagna = self.kundali.lagna.get('rashi', 'Mesha')
            seventh_lord = self._get_house_lord(7, lagna)
            response = f"""<b>💑 {self.name} के विवाह समय विश्लेषण:</b><br><br>
<p><b>आपके लिए शुभ दशाएं ({lagna} लग्न):</b></p>
<ul>
<li>शुक्र की दशा - विवाह कारक</li>
<li>{seventh_lord} (आपके सप्तमेश) की दशा - विवाह भाव स्वामी</li>
<li>गुरु का गोचर सप्तम भाव पर</li>
</ul>
"""
        return response

    def career_timing_answer(self):
        """Answer questions about career timing."""
        from datetime import datetime

        try:
            from .event_predictor import EventPredictor
            predictor = EventPredictor(self.kundali)
            current_year = datetime.now().year

            predictions = predictor.get_best_periods("career", current_year, current_year + 5, top_n=3)

            response = f"""<b>💼 {self.name} के करियर उन्नति का शुभ समय:</b><br><br>"""

            if predictions:
                response += "<b>अगले 5 वर्षों में शुभ समय:</b><br>"
                for i, pred in enumerate(predictions, 1):
                    favorability = "उच्च ⭐⭐⭐" if pred['favorability'] == "High" else "मध्यम ⭐⭐" if pred['favorability'] == "Medium" else "निम्न ⭐"
                    response += f"""
<br><b>{i}. {pred['period']}</b><br>
• दशा: {pred['dasha']}<br>
• अनुकूलता: {favorability}<br>
• कारण: {'; '.join(pred['reasons'][:2])}<br>
"""
            else:
                response += """<p>इस अवधि में विशेष शुभ योग नहीं मिले।</p>"""

            response += """<br><b>करियर के लिए शुभ दशाएं:</b><br>
• दशमेश की दशा<br>
• शनि की दशा (पेशा कारक)<br>
• सूर्य की दशा (अधिकार)"""

        except Exception as e:
            response = f"""<b>💼 करियर समय विश्लेषण:</b><br><br>
<p>विस्तृत विश्लेषण के लिए दशा खंड देखें।</p>
<p><b>सामान्य सिद्धांत:</b></p>
<ul>
<li>दशमेश की दशा करियर उन्नति</li>
<li>शनि की दशा में स्थिरता</li>
<li>गुरु का गोचर दशम भाव पर शुभ</li>
</ul>
"""
        return response

    def property_timing_answer(self):
        """Answer questions about property timing."""
        from datetime import datetime

        try:
            from .event_predictor import EventPredictor
            predictor = EventPredictor(self.kundali)
            current_year = datetime.now().year

            predictions = predictor.get_best_periods("property", current_year, current_year + 5, top_n=3)

            response = f"""<b>🏠 {self.name} के संपत्ति खरीद का शुभ समय:</b><br><br>"""

            if predictions:
                response += "<b>अगले 5 वर्षों में शुभ समय:</b><br>"
                for i, pred in enumerate(predictions, 1):
                    favorability = "उच्च ⭐⭐⭐" if pred['favorability'] == "High" else "मध्यम ⭐⭐" if pred['favorability'] == "Medium" else "निम्न ⭐"
                    response += f"""
<br><b>{i}. {pred['period']}</b><br>
• दशा: {pred['dasha']}<br>
• अनुकूलता: {favorability}<br>
• कारण: {'; '.join(pred['reasons'][:2])}<br>
"""
            else:
                response += """<p>इस अवधि में विशेष शुभ योग नहीं मिले।</p>"""

            response += """<br><b>संपत्ति के लिए शुभ दशाएं:</b><br>
• चतुर्थेश की दशा (गृह)<br>
• मंगल की दशा (भूमि कारक)<br>
• शनि की दशा (निर्माण)"""

        except Exception as e:
            response = f"""<b>🏠 संपत्ति समय विश्लेषण:</b><br><br>
<p>विस्तृत विश्लेषण के लिए दशा खंड देखें।</p>
<p><b>सामान्य सिद्धांत:</b></p>
<ul>
<li>चतुर्थेश की दशा में गृह सुख</li>
<li>मंगल की दशा में भूमि लाभ</li>
<li>गुरु का गोचर चतुर्थ भाव पर शुभ</li>
</ul>
"""
        return response

    def default_answer(self):
        return """<b>🔮 मैं इन विषयों पर सहायता कर सकता हूं:</b><br><br>
<b>जीवन क्षेत्र:</b><br>
• करियर / नौकरी / व्यापार<br>
• विवाह / शादी / पति/पत्नी<br>
• संतान / बच्चे<br>
• स्वास्थ्य / सेहत<br>
• धन / पैसा / संपत्ति<br><br>
<b>ज्योतिष:</b><br>
• दशा / महादशा / भविष्य<br>
• लग्न / राशि<br>
• ग्रह (सूर्य, चंद्र, मंगल, आदि)<br>
• साढ़े साती / शनि दोष<br>
• गोचर / Transit<br>
• शुभ रंग / अंक / रत्न<br>
• उपाय / मंत्र<br><br>
<b>समय भविष्यवाणी:</b><br>
• शादी कब होगी?<br>
• करियर कब बदलेगा?<br>
• घर/संपत्ति कब मिलेगी?<br><br>
<b>उदाहरण प्रश्न:</b><br>
• "करियर के बारे में बताओ"<br>
• "शादी कब होगी?"<br>
• "शनि का प्रभाव क्या है?"<br>
• "साढ़े साती के बारे में बताओ"<br>
• "गोचर के बारे में बताओ"<br>
• "शुभ रत्न कौन सा है?"
"""
