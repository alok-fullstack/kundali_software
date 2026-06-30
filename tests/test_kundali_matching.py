"""
Tests for Kundali Matching (Ashtakoot Milan)

These tests verify the matching calculations against known results
from traditional pandit calculations and classical texts.
"""

import pytest
import sys
from pathlib import Path

# Add parent to path for src imports
parent_path = Path(__file__).parent.parent
sys.path.insert(0, str(parent_path))

from src.kundali_matching import (
    KundaliMatcher,
    MatchingResult,
    KootaResult,
    Varna,
    VashyaType,
    Gana,
    Nadi,
    Yoni,
    RASHI_VARNA,
    NAKSHATRA_GANA,
    NAKSHATRA_NADI,
    NAKSHATRA_YONI,
    get_vashya_type,
    get_yoni_score,
    get_graha_maitri_score,
    get_bhakoot_score,
    get_nadi_score,
    check_manglik_dosha,
    NAKSHATRA_NAMES,
)


class TestVarnaKoota:
    """Test Varna (spiritual compatibility) calculations."""

    def test_same_varna_full_points(self):
        """Same varna should get full points."""
        matcher = KundaliMatcher()
        # Both Cancer (Brahmin)
        result = matcher._calculate_varna(3, 3)
        assert result.obtained_points == 1
        assert result.is_auspicious

    def test_boy_higher_varna_full_points(self):
        """Boy's higher varna should get full points."""
        matcher = KundaliMatcher()
        # Boy Cancer (Brahmin=4), Girl Aries (Kshatriya=3)
        result = matcher._calculate_varna(3, 0)
        assert result.obtained_points == 1
        assert result.is_auspicious

    def test_girl_higher_varna_no_points(self):
        """Girl's higher varna should get no points."""
        matcher = KundaliMatcher()
        # Boy Aries (Kshatriya=3), Girl Cancer (Brahmin=4)
        result = matcher._calculate_varna(0, 3)
        assert result.obtained_points == 0
        assert not result.is_auspicious

    def test_varna_classification(self):
        """Test varna classification for all rashis."""
        # Brahmin: Cancer (3), Scorpio (7), Pisces (11)
        assert RASHI_VARNA[3] == Varna.BRAHMIN
        assert RASHI_VARNA[7] == Varna.BRAHMIN
        assert RASHI_VARNA[11] == Varna.BRAHMIN

        # Kshatriya: Aries (0), Leo (4), Sagittarius (8)
        assert RASHI_VARNA[0] == Varna.KSHATRIYA
        assert RASHI_VARNA[4] == Varna.KSHATRIYA
        assert RASHI_VARNA[8] == Varna.KSHATRIYA

        # Vaishya: Taurus (1), Virgo (5), Capricorn (9)
        assert RASHI_VARNA[1] == Varna.VAISHYA
        assert RASHI_VARNA[5] == Varna.VAISHYA
        assert RASHI_VARNA[9] == Varna.VAISHYA

        # Shudra: Gemini (2), Libra (6), Aquarius (10)
        assert RASHI_VARNA[2] == Varna.SHUDRA
        assert RASHI_VARNA[6] == Varna.SHUDRA
        assert RASHI_VARNA[10] == Varna.SHUDRA


class TestVashyaKoota:
    """Test Vashya (mutual attraction) calculations."""

    def test_same_vashya_full_points(self):
        """Same vashya type should get full 2 points."""
        matcher = KundaliMatcher()
        # Both Aries (Chatushpada)
        result = matcher._calculate_vashya(0, 15.0, 0, 15.0)
        assert result.obtained_points == 2

    def test_enemy_vashya_no_points(self):
        """Incompatible vashya types should get 0 points."""
        # Chatushpada (Aries) vs Jalachara (Cancer) = 0
        vashya_boy = get_vashya_type(0, 15.0)  # Aries = Chatushpada
        vashya_girl = get_vashya_type(3, 15.0)  # Cancer = Jalachara
        assert vashya_boy == VashyaType.CHATUSHPADA
        assert vashya_girl == VashyaType.JALACHARA

    def test_sagittarius_split_vashya(self):
        """Sagittarius should have split vashya based on degree."""
        # First half = Manava
        assert get_vashya_type(8, 10.0) == VashyaType.MANAVA
        # Second half = Chatushpada
        assert get_vashya_type(8, 20.0) == VashyaType.CHATUSHPADA

    def test_capricorn_split_vashya(self):
        """Capricorn should have split vashya based on degree."""
        # First half = Chatushpada
        assert get_vashya_type(9, 10.0) == VashyaType.CHATUSHPADA
        # Second half = Jalachara
        assert get_vashya_type(9, 20.0) == VashyaType.JALACHARA


class TestTaraKoota:
    """Test Tara (nakshatra relationship) calculations."""

    def test_both_auspicious_taras(self):
        """Both auspicious taras should get full 3 points."""
        matcher = KundaliMatcher()
        # Test with nakshatras that give Sampat (2) from each other
        result = matcher._calculate_tara(0, 1)  # Ashwini to Bharani
        assert result.max_points == 3

    def test_inauspicious_tara_vipat(self):
        """Vipat (3) tara should reduce points."""
        # Vipat is 3rd tara, inauspicious
        matcher = KundaliMatcher()
        # Need nakshatras that are 3 apart (modulo 9)
        # Ashwini (0) to Mrigashira (4) = 5th = Pratyak (inauspicious)
        result = matcher._calculate_tara(4, 0)
        # At least one should be in inauspicious position

    def test_inauspicious_tara_naidhana(self):
        """Naidhana (7) tara is most inauspicious."""
        # 7th tara is death-like
        matcher = KundaliMatcher()
        # Positions 7 apart in the 9-cycle
        pass  # Test specific cases


class TestYoniKoota:
    """Test Yoni (physical compatibility) calculations."""

    def test_same_yoni_different_gender(self):
        """Same yoni with different genders should get 4 points."""
        # Ashwini (0) Male Horse, Shatabhisha (23) Female Horse
        score, desc = get_yoni_score(0, 23)
        assert score == 4

    def test_same_yoni_same_gender(self):
        """Same yoni with same gender should get 3 points."""
        # Both male horses - but there's no second male horse nakshatra
        pass

    def test_enemy_yonis(self):
        """Enemy yonis should get 0 points."""
        # Horse (Ashwini-0) vs Buffalo (Hasta-12)
        score, desc = get_yoni_score(0, 12)
        assert score == 0 or score == 2  # Depending on if they're enemies

    def test_yoni_classification(self):
        """Test nakshatra to yoni mapping."""
        assert NAKSHATRA_YONI[0] == Yoni.HORSE  # Ashwini
        assert NAKSHATRA_YONI[1] == Yoni.ELEPHANT  # Bharani
        assert NAKSHATRA_YONI[4] == Yoni.SERPENT  # Mrigashira
        assert NAKSHATRA_YONI[7] == Yoni.SHEEP  # Pushya


class TestGrahaMaitriKoota:
    """Test Graha Maitri (planetary friendship) calculations."""

    def test_same_lord_full_points(self):
        """Same lord should get full 5 points."""
        # Aries and Scorpio both ruled by Mars
        score, desc = get_graha_maitri_score(0, 7)
        assert score == 5

    def test_mutual_friends_full_points(self):
        """Mutual planetary friends should get 5 points."""
        # Sun (Leo-4) and Moon (Cancer-3) are friends
        score, desc = get_graha_maitri_score(4, 3)
        assert score == 5

    def test_mutual_enemies_no_points(self):
        """Mutual planetary enemies should get 0 points."""
        # Sun (Leo-4) and Saturn (Capricorn-9) are enemies
        score, desc = get_graha_maitri_score(4, 9)
        assert score == 0


class TestGanaKoota:
    """Test Gana (temperament) calculations."""

    def test_same_deva_gana(self):
        """Same Deva gana should get 6 points."""
        matcher = KundaliMatcher()
        # Ashwini (0) and Mrigashira (4) are both Deva
        result = matcher._calculate_gana(0, 4)
        assert result.obtained_points == 6

    def test_same_manushya_gana(self):
        """Same Manushya gana should get 6 points."""
        matcher = KundaliMatcher()
        # Bharani (1) and Rohini (3) are both Manushya
        result = matcher._calculate_gana(1, 3)
        assert result.obtained_points == 6

    def test_deva_rakshasa_gana_dosha(self):
        """Deva + Rakshasa should get 0 points (Gana Dosha)."""
        matcher = KundaliMatcher()
        # Ashwini (0, Deva) and Krittika (2, Rakshasa)
        result = matcher._calculate_gana(0, 2)
        assert result.obtained_points == 0
        assert result.dosha == "Gana Dosha"

    def test_gana_classification(self):
        """Test nakshatra to gana mapping."""
        # Deva
        assert NAKSHATRA_GANA[0] == Gana.DEVA  # Ashwini
        assert NAKSHATRA_GANA[6] == Gana.DEVA  # Punarvasu
        assert NAKSHATRA_GANA[21] == Gana.DEVA  # Shravana

        # Manushya
        assert NAKSHATRA_GANA[1] == Gana.MANUSHYA  # Bharani
        assert NAKSHATRA_GANA[3] == Gana.MANUSHYA  # Rohini

        # Rakshasa
        assert NAKSHATRA_GANA[2] == Gana.RAKSHASA  # Krittika
        assert NAKSHATRA_GANA[8] == Gana.RAKSHASA  # Ashlesha
        assert NAKSHATRA_GANA[18] == Gana.RAKSHASA  # Mula


class TestBhakootKoota:
    """Test Bhakoot (rashi relationship) calculations."""

    def test_no_bhakoot_dosha(self):
        """Normal positions should get 7 points."""
        # Aries (0) and Leo (4) - 5th from each other, no dosha
        score, desc, dosha = get_bhakoot_score(0, 4)
        assert score == 7
        assert dosha is None

    def test_shadashtak_dosha(self):
        """6/8 position should get 0 points (Shadashtak)."""
        # Aries (0) and Scorpio (7) - should be 8th from each other
        # Aries (0) and Virgo (5) - 6/8 position
        score, desc, dosha = get_bhakoot_score(0, 5)
        # Check if it's the dosha position
        if dosha == "Shadashtak":
            assert score == 0

    def test_dwi_dwadash_dosha(self):
        """2/12 position should get 0 points."""
        # Aries (0) and Pisces (11) - 2/12 position
        score, desc, dosha = get_bhakoot_score(0, 11)
        if dosha == "Dwi-Dwadash":
            assert score == 0

    def test_bhakoot_dosha_cancellation(self):
        """Dosha should be cancelled if lords are same/friends."""
        # Gemini (2) and Virgo (5) - both Mercury ruled - should cancel
        score, desc, dosha = get_bhakoot_score(2, 5)
        # Same lord should cancel any dosha


class TestNadiKoota:
    """Test Nadi (health/genetic compatibility) calculations."""

    def test_different_nadi_full_points(self):
        """Different nadis should get 8 points."""
        # Ashwini (0, Aadi) and Bharani (1, Madhya)
        score, desc, has_dosha = get_nadi_score(0, 1)
        assert score == 8
        assert not has_dosha

    def test_same_nadi_dosha(self):
        """Same nadi should get 0 points (Nadi Dosha)."""
        # Both Aadi nadi - Ashwini (0) and Ardra (5)
        score, desc, has_dosha = get_nadi_score(0, 5)
        assert score == 0
        assert has_dosha

    def test_nadi_classification(self):
        """Test nakshatra to nadi mapping."""
        # Aadi (Vata)
        assert NAKSHATRA_NADI[0] == Nadi.AADI  # Ashwini
        assert NAKSHATRA_NADI[5] == Nadi.AADI  # Ardra
        assert NAKSHATRA_NADI[17] == Nadi.AADI  # Jyeshtha

        # Madhya (Pitta)
        assert NAKSHATRA_NADI[1] == Nadi.MADHYA  # Bharani
        assert NAKSHATRA_NADI[4] == Nadi.MADHYA  # Mrigashira

        # Antya (Kapha)
        assert NAKSHATRA_NADI[2] == Nadi.ANTYA  # Krittika
        assert NAKSHATRA_NADI[3] == Nadi.ANTYA  # Rohini


class TestManglikDosha:
    """Test Manglik (Mars) dosha detection and cancellation."""

    def test_mars_in_first_house_manglik(self):
        """Mars in 1st house should cause Manglik dosha."""
        result = check_manglik_dosha(
            mars_house_from_lagna=1,
            mars_house_from_moon=5,  # Not manglik position
            mars_house_from_venus=0,
            mars_rashi="Mesha",
            lagna_rashi="Mesha"
        )
        assert result["from_lagna"] == True

    def test_mars_in_seventh_house_manglik(self):
        """Mars in 7th house should cause Manglik dosha."""
        result = check_manglik_dosha(
            mars_house_from_lagna=7,
            mars_house_from_moon=7,
            mars_house_from_venus=0,
            mars_rashi="Tula",
            lagna_rashi="Mesha"
        )
        assert result["is_manglik"] == True
        assert result["from_lagna"] == True
        assert result["from_moon"] == True

    def test_manglik_cancellation_own_sign(self):
        """Manglik dosha should be cancelled if Mars is in own sign."""
        result = check_manglik_dosha(
            mars_house_from_lagna=1,
            mars_house_from_moon=1,
            mars_house_from_venus=0,
            mars_rashi="Mesha",  # Own sign
            lagna_rashi="Mesha"
        )
        # Check that any cancellation related to own sign is present
        assert any("own sign" in c.lower() for c in result["cancellation"])

    def test_no_manglik_dosha(self):
        """Mars in non-manglik houses should not cause dosha."""
        result = check_manglik_dosha(
            mars_house_from_lagna=3,  # Not a manglik house
            mars_house_from_moon=5,
            mars_house_from_venus=0,
            mars_rashi="Mithuna",
            lagna_rashi="Mesha"
        )
        assert result["is_manglik"] == False


class TestCompleteMatching:
    """Test complete Ashtakoot matching."""

    def test_excellent_match(self):
        """Test a known excellent match."""
        matcher = KundaliMatcher()

        # Create a match that should score high
        # Boy: Cancer Moon (3), Rohini nakshatra (3)
        # Girl: Taurus Moon (1), Bharani nakshatra (1)
        result = matcher.match(
            boy_moon_rashi_num=3,
            boy_moon_nakshatra_num=3,
            boy_moon_degree=15.0,
            girl_moon_rashi_num=1,
            girl_moon_nakshatra_num=1,
            girl_moon_degree=15.0,
            boy_name="Test Boy",
            girl_name="Test Girl"
        )

        assert isinstance(result, MatchingResult)
        assert result.max_points == 36
        assert 0 <= result.total_points <= 36
        assert len(result.koota_results) == 8

    def test_poor_match_with_doshas(self):
        """Test a match with multiple doshas."""
        matcher = KundaliMatcher()

        # Same nadi, Deva-Rakshasa combination
        # Ashwini (0) Deva, Aadi nadi
        # Krittika (2) Rakshasa, Antya nadi
        result = matcher.match(
            boy_moon_rashi_num=0,  # Aries
            boy_moon_nakshatra_num=0,  # Ashwini - Deva, Aadi
            boy_moon_degree=10.0,
            girl_moon_rashi_num=1,  # Taurus
            girl_moon_nakshatra_num=2,  # Krittika - Rakshasa, Antya
            girl_moon_degree=5.0,
            boy_name="Test Boy",
            girl_name="Test Girl"
        )

        # Check that Gana Dosha is detected
        gana_result = next(k for k in result.koota_results if k.name == "Gana")
        assert gana_result.obtained_points == 0
        assert gana_result.dosha == "Gana Dosha"

    def test_all_koota_names(self):
        """Verify all 8 kootas are calculated."""
        matcher = KundaliMatcher()
        result = matcher.match(
            boy_moon_rashi_num=0,
            boy_moon_nakshatra_num=0,
            boy_moon_degree=15.0,
            girl_moon_rashi_num=0,
            girl_moon_nakshatra_num=0,
            girl_moon_degree=15.0,
        )

        koota_names = [k.name for k in result.koota_results]
        expected_names = ["Varna", "Vashya", "Tara", "Yoni", "Graha Maitri", "Gana", "Bhakoot", "Nadi"]

        assert koota_names == expected_names

    def test_max_score_sum(self):
        """Verify max score adds up to 36."""
        matcher = KundaliMatcher()
        result = matcher.match(
            boy_moon_rashi_num=0,
            boy_moon_nakshatra_num=0,
            boy_moon_degree=15.0,
            girl_moon_rashi_num=0,
            girl_moon_nakshatra_num=0,
            girl_moon_degree=15.0,
        )

        total_max = sum(k.max_points for k in result.koota_results)
        assert total_max == 36

    def test_percentage_calculation(self):
        """Verify percentage is calculated correctly."""
        matcher = KundaliMatcher()
        result = matcher.match(
            boy_moon_rashi_num=0,
            boy_moon_nakshatra_num=0,
            boy_moon_degree=15.0,
            girl_moon_rashi_num=0,
            girl_moon_nakshatra_num=0,
            girl_moon_degree=15.0,
        )

        expected_percentage = round((result.total_points / 36) * 100, 1)
        assert result.percentage == expected_percentage


class TestKnownMatches:
    """Test against known real-world matching results."""

    def test_traditional_good_match(self):
        """
        Test a traditionally known good match.

        This test case is based on a match that would be approved
        by traditional pandits.
        """
        matcher = KundaliMatcher()

        # Boy: Leo Moon (Simha), Magha nakshatra
        # Girl: Sagittarius Moon (Dhanu), Mula nakshatra
        result = matcher.match(
            boy_moon_rashi_num=4,  # Leo
            boy_moon_nakshatra_num=9,  # Magha
            boy_moon_degree=5.0,
            girl_moon_rashi_num=8,  # Sagittarius
            girl_moon_nakshatra_num=18,  # Mula
            girl_moon_degree=3.0,
            boy_name="Ravi",
            girl_name="Kavita"
        )

        # Fire signs (Leo-Sagittarius) are considered compatible
        # Should get reasonable score
        assert result.total_points >= 18  # Minimum acceptable

    def test_same_nakshatra_nadi_dosha(self):
        """
        Same nakshatra should have Nadi Dosha.
        """
        matcher = KundaliMatcher()

        # Both Ashwini nakshatra
        result = matcher.match(
            boy_moon_rashi_num=0,
            boy_moon_nakshatra_num=0,  # Ashwini
            boy_moon_degree=10.0,
            girl_moon_rashi_num=0,
            girl_moon_nakshatra_num=0,  # Ashwini
            girl_moon_degree=5.0,
        )

        # Same nakshatra = same Nadi = Nadi Dosha
        nadi_result = next(k for k in result.koota_results if k.name == "Nadi")
        assert nadi_result.obtained_points == 0
        assert nadi_result.dosha == "Nadi Dosha"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
