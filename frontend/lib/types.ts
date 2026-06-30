// Input types for API requests
export interface KundaliInput {
  name: string;
  dob: string; // YYYY-MM-DD
  tob: string; // HH:MM
  city: string;
  latitude?: number | null;
  longitude?: number | null;
}

export interface ChatInput {
  kundali_id: string;
  question: string;
}

export interface MuhurtaInput {
  kundali_id: string;
  event_type: EventType;
  year: number;
}

export interface HealthInput {
  kundali_id: string;
  start_year: number;
  end_year: number;
}

// Response types
export interface KundaliResponse {
  success: boolean;
  html?: string;
  kundali_id?: string;
  error?: string;
}

export interface ChatResponse {
  answer: string;
}

export interface MuhurtaResponse {
  success: boolean;
  html?: string;
  error?: string;
}

export interface HealthResponse {
  success: boolean;
  html?: string;
  error?: string;
}

// Enum types
export type EventType = 'marriage' | 'career' | 'property' | 'travel' | 'griha_pravesh';

// Kundali data types (for structured data if needed)
export interface PlanetPosition {
  planet: string;
  rashi: string;
  rashi_degree: number;
  nakshatra: string;
  pada: number;
  house: number;
  is_retrograde: boolean;
}

export interface DashaInfo {
  planet: string;
  start: string;
  end: string;
  duration_years: number;
}

export interface CurrentDasha {
  full_dasha: string;
  mahadasha: {
    planet: string;
    start: string;
    end: string;
  };
  antardasha: {
    planet: string;
  };
  pratyantardasha: {
    planet: string;
  };
}

// Chat message types
export interface ChatMessage {
  id: string;
  type: 'user' | 'bot';
  content: string;
  timestamp: Date;
}

// Quick question buttons
export interface QuickQuestion {
  icon: string;
  label: string;
  labelHindi: string;
  question: string;
}

export const QUICK_QUESTIONS: QuickQuestion[] = [
  { icon: '💼', label: 'Career', labelHindi: 'करियर', question: 'Career ke baare mein batao' },
  { icon: '💑', label: 'Marriage', labelHindi: 'शादी', question: 'Shaadi kab hogi?' },
  { icon: '👶', label: 'Children', labelHindi: 'संतान', question: 'Bachche ke baare mein' },
  { icon: '🏥', label: 'Health', labelHindi: 'स्वास्थ्य', question: 'Health kaisi rahegi?' },
  { icon: '💰', label: 'Wealth', labelHindi: 'धन', question: 'Dhan ke baare mein batao' },
  { icon: '📅', label: 'Dasha', labelHindi: 'दशा', question: 'Dasha ka prabhav?' },
  { icon: '🌍', label: 'Transit', labelHindi: 'गोचर', question: 'Gochar ke baare mein batao' },
  { icon: '⚠️', label: 'Sade Sati', labelHindi: 'साढ़े साती', question: 'Sade sati ke baare mein batao' },
  { icon: '💎', label: 'Gemstone', labelHindi: 'रत्न', question: 'Shubh ratna konsa hai?' },
  { icon: '🙏', label: 'Remedies', labelHindi: 'उपाय', question: 'Upay batao' },
];

// Event type options
export interface EventTypeOption {
  value: EventType;
  label: string;
  labelHindi: string;
}

export const EVENT_TYPE_OPTIONS: EventTypeOption[] = [
  { value: 'marriage', label: 'Marriage', labelHindi: 'विवाह' },
  { value: 'career', label: 'Career/Job', labelHindi: 'करियर' },
  { value: 'property', label: 'Property', labelHindi: 'संपत्ति' },
  { value: 'griha_pravesh', label: 'House Warming', labelHindi: 'गृह प्रवेश' },
  { value: 'travel', label: 'Travel', labelHindi: 'यात्रा' },
];

// Year options for muhurta and health
export const MUHURTA_YEARS = Array.from({ length: 6 }, (_, i) => 2025 + i);
export const HEALTH_START_YEARS = [1995, 2000, 2005, 2010, 2015, 2020, 2024, 2025, 2026, 2027, 2028, 2029, 2030];
export const HEALTH_END_YEARS = [2000, 2005, 2010, 2015, 2020, 2024, 2025, 2026, 2027, 2028, 2029, 2030, 2035, 2040];

// =============================================================================
// KUNDALI MATCHING TYPES
// =============================================================================

export interface PersonDetails {
  name: string;
  dob: string; // YYYY-MM-DD
  tob: string; // HH:MM
  city: string;
  latitude?: number | null;
  longitude?: number | null;
  timezone?: string;
}

export interface MatchInput {
  boy: PersonDetails;
  girl: PersonDetails;
}

export interface KootaScore {
  name: string;
  name_hindi: string;
  max_points: number;
  obtained_points: number;
  boy_value: string;
  girl_value: string;
  description: string;
  is_auspicious: boolean;
  dosha?: string | null;
}

export interface KootaInterpretation {
  name: string;
  name_hindi: string;
  score: string;
  percentage: number;
  boy_value: string;
  girl_value: string;
  is_favorable: boolean;
  description: string;
  title: string;
  detailed_interpretation: string;
  effects: string[];
  remedies: string[];
  dosha?: string | null;
  // Hindi translations
  title_hindi?: string;
  detailed_interpretation_hindi?: string;
  effects_hindi?: string[];
}

export interface DoshaInfo {
  name: string;
  type: string;
  severity: string;
  description: string;
  remedies: string[];
  is_cancelled: boolean;
}

export interface MarriageTiming {
  favorable_days: string[];
  favorable_months: string[];
  avoid: string[];
  general_advice: string[];
}

export interface MatchingScores {
  varna: number;
  vashya: number;
  tara: number;
  yoni: number;
  graha_maitri: number;
  gana: number;
  bhakoot: number;
  nadi: number;
}

export interface PersonMatchDetails {
  name: string;
  dob: string;
  birth_time?: string;
  city: string;
  moon_rashi: string;
  moon_nakshatra: string;
  lagna_rashi: string;
  varna?: string;
  gana?: string;
  nadi?: string;
  yoni?: string;
  nakshatra_lord?: string;
}

export interface MatchResponse {
  success: boolean;
  boy_name: string;
  girl_name: string;
  total_points: number;
  max_points: number;
  percentage: number;
  compatibility_level: string;
  koota_scores: KootaScore[];
  koota_interpretations: KootaInterpretation[];
  doshas: DoshaInfo[];
  score_breakdown: MatchingScores;
  recommendation: string;
  remedies: string[];
  areas_of_strength: string[];
  areas_of_concern: string[];
  boy_details: PersonMatchDetails;
  girl_details: PersonMatchDetails;
  marriage_timing?: MarriageTiming;
  html?: string;
  message: string;
  error?: string;
}

// =============================================================================
// DIVISIONAL CHARTS (VARGA) TYPES
// =============================================================================

export type VargaType =
  | 'D1_RASHI'
  | 'D2_HORA'
  | 'D3_DREKKANA'
  | 'D4_CHATURTHAMSA'
  | 'D7_SAPTAMSA'
  | 'D9_NAVAMSA'
  | 'D10_DASAMSA'
  | 'D12_DWADASAMSA'
  | 'D16_SHODASAMSA'
  | 'D20_VIMSAMSA'
  | 'D24_CHATURVIMSAMSA'
  | 'D27_BHAMSA'
  | 'D30_TRIMSAMSA'
  | 'D40_KHAVEDAMSA'
  | 'D45_AKSHAVEDAMSA'
  | 'D60_SHASHTIAMSA';

export interface DivisionalPosition {
  planet: string;
  original_longitude: number;
  original_rashi: string;
  original_degree: number;
  varga_rashi: string;
  varga_rashi_english: string;
  varga_degree: number;
  division_number: number;
  is_own_sign: boolean;
  is_exalted: boolean;
  is_debilitated: boolean;
}

export interface DivisionalChart {
  varga_name: string;
  varga_description: string;
  division_count: number;
  lagna: DivisionalPosition;
  planets: Record<string, DivisionalPosition>;
  planets_in_houses: Record<string, string[]>;
}

export interface VargaListResponse {
  success: boolean;
  kundali_id: string;
  charts: Record<VargaType, DivisionalChart>;
  message: string;
}

export interface SingleVargaResponse {
  success: boolean;
  kundali_id: string;
  varga_type: VargaType;
  chart: DivisionalChart;
  message: string;
}

export interface VargaPredictionItem {
  category: string;
  aspect: string;
  prediction: string;
  strength: string;
  is_favorable: boolean;
  supporting_factors: string[];
  remedies: string[];
}

export interface NavamsaAnalysis {
  success: boolean;
  kundali_id: string;
  navamsa_lagna: {
    rashi: string;
    rashi_english: string;
    interpretation: string;
    element: string;
  };
  spouse_characteristics: {
    seventh_house_rashi: string;
    seventh_house_rashi_english: string;
    appearance: string;
    nature: string;
    key_traits: string;
    seventh_lord: string;
    planets_in_seventh: string[];
    planet_influences: Array<{
      planet: string;
      effect: string;
      timing: string;
      quality: string;
    }>;
  };
  marriage_timing_factors: {
    overall_indication: string;
    factors: string[];
  };
  marriage_quality: {
    quality_score: number;
    quality_level: string;
    positive_factors: string[];
    negative_factors: string[];
  };
  spiritual_aspects: {
    dharmic_strengths: string[];
    spiritual_path: string;
  };
  predictions: VargaPredictionItem[];
  message: string;
}

export interface DasamsaAnalysis {
  success: boolean;
  kundali_id: string;
  career_lagna: {
    rashi: string;
    rashi_english: string;
    professional_approach: string;
    suitable_careers: string[];
  };
  tenth_house_analysis: {
    rashi: string;
    rashi_english: string;
    tenth_lord: string;
    planets_in_10th: string[];
    indicated_domains: string[];
  };
  career_indicators: Array<{
    planet: string;
    indication: string;
    favorable: boolean;
  }>;
  professional_strengths: {
    strengths: string[];
    weaknesses: string[];
  };
  career_timing: {
    growth_pattern: string;
    factors: string[];
  };
  predictions: VargaPredictionItem[];
  message: string;
}

export interface CompleteVargaAnalysis {
  success: boolean;
  kundali_id: string;
  navamsa_analysis: NavamsaAnalysis;
  dasamsa_analysis: DasamsaAnalysis;
  saptamsa_analysis: any;
  vimshopaka_bala: Record<string, any>;
  summary: {
    marriage_outlook: string;
    career_outlook: string;
    children_outlook: string;
  };
  message: string;
}

// Varga chart info for display
export interface VargaChartInfo {
  type: VargaType;
  name: string;
  nameHindi: string;
  description: string;
  divisions: number;
  importance: 'high' | 'medium' | 'low';
}

export const VARGA_CHART_INFO: VargaChartInfo[] = [
  { type: 'D1_RASHI', name: 'Rashi', nameHindi: 'राशि', description: 'Main birth chart', divisions: 1, importance: 'high' },
  { type: 'D9_NAVAMSA', name: 'Navamsa', nameHindi: 'नवांश', description: 'Marriage & Spouse', divisions: 9, importance: 'high' },
  { type: 'D10_DASAMSA', name: 'Dasamsa', nameHindi: 'दशांश', description: 'Career & Profession', divisions: 10, importance: 'high' },
  { type: 'D2_HORA', name: 'Hora', nameHindi: 'होरा', description: 'Wealth', divisions: 2, importance: 'medium' },
  { type: 'D3_DREKKANA', name: 'Drekkana', nameHindi: 'द्रेक्काण', description: 'Siblings & Courage', divisions: 3, importance: 'medium' },
  { type: 'D4_CHATURTHAMSA', name: 'Chaturthamsa', nameHindi: 'चतुर्थांश', description: 'Property & Fortune', divisions: 4, importance: 'medium' },
  { type: 'D7_SAPTAMSA', name: 'Saptamsa', nameHindi: 'सप्तांश', description: 'Children', divisions: 7, importance: 'high' },
  { type: 'D12_DWADASAMSA', name: 'Dwadasamsa', nameHindi: 'द्वादशांश', description: 'Parents', divisions: 12, importance: 'medium' },
  { type: 'D16_SHODASAMSA', name: 'Shodasamsa', nameHindi: 'षोडशांश', description: 'Vehicles & Comforts', divisions: 16, importance: 'low' },
  { type: 'D20_VIMSAMSA', name: 'Vimsamsa', nameHindi: 'विंशांश', description: 'Spiritual Progress', divisions: 20, importance: 'medium' },
  { type: 'D24_CHATURVIMSAMSA', name: 'Siddhamsa', nameHindi: 'सिद्धांश', description: 'Education', divisions: 24, importance: 'medium' },
  { type: 'D27_BHAMSA', name: 'Bhamsa', nameHindi: 'भांश', description: 'Strength & Weakness', divisions: 27, importance: 'low' },
  { type: 'D30_TRIMSAMSA', name: 'Trimsamsa', nameHindi: 'त्रिंशांश', description: 'Evils & Misfortune', divisions: 5, importance: 'medium' },
  { type: 'D40_KHAVEDAMSA', name: 'Khavedamsa', nameHindi: 'खवेदांश', description: 'Auspicious Effects', divisions: 40, importance: 'low' },
  { type: 'D45_AKSHAVEDAMSA', name: 'Akshavedamsa', nameHindi: 'अक्षवेदांश', description: 'General Indications', divisions: 45, importance: 'low' },
  { type: 'D60_SHASHTIAMSA', name: 'Shashtiamsa', nameHindi: 'षष्ठ्यांश', description: 'Past Life Karma', divisions: 60, importance: 'high' },
];

// =============================================================================
// GEMSTONE RECOMMENDATION TYPES
// =============================================================================

export interface GemstoneInfo {
  name_hindi: string;
  name_english: string;
  name_sanskrit: string;
  color: string;
  finger: string;
  finger_hindi: string;
  metal: string;
  metal_hindi: string;
  minimum_weight_ratti: number;
  minimum_weight_carat: number;
  day: string;
  day_hindi: string;
  time: string;
  time_hindi: string;
  nakshatra: string[];
  mantra: string;
  mantra_count: number;
  alternative_stones: string[];
  benefits: string[];
  precautions: string[];
}

export interface GemstoneRecommendation {
  planet: string;
  planet_hindi: string;
  gemstone: GemstoneInfo;
  reason: string;
  reason_hindi: string;
  priority: number;
  priority_label: string;
  priority_label_hindi: string;
  current_dasha_relevant: boolean;
  contraindications: string[];
  special_instructions: string[];
}

export interface StoneToAvoid {
  planet: string;
  planet_hindi: string;
  gemstone_english: string;
  gemstone_hindi: string;
  reason: string;
  reason_hindi: string;
}

export interface GuidelineSection {
  title: string;
  guidelines: string[];
}

export interface GemstoneDisclaimer {
  hindi: string;
  english: string;
}

export interface GemstoneResponse {
  success: boolean;
  lagna: {
    rashi: string;
    rashi_english: string;
    lord: string;
  };
  moon_sign: {
    rashi: string;
    lord: string;
  };
  yogakaraka: string | null;
  current_dasha: {
    mahadasha: string;
    antardasha: string;
    full_dasha: string;
  };
  primary_recommendations: GemstoneRecommendation[];
  secondary_recommendations: GemstoneRecommendation[];
  stones_to_avoid: StoneToAvoid[];
  general_guidelines: GuidelineSection[];
  disclaimer: GemstoneDisclaimer;
  error?: string;
}

// =============================================================================
// RASHIFAL (HOROSCOPE) TYPES
// =============================================================================

export type RashifalPeriod = 'daily' | 'weekly' | 'monthly' | 'yearly';

export interface RashifalCategoryPrediction {
  category: string;
  category_hindi: string;
  prediction_hindi: string;
  prediction_english: string;
  score: number;
  favorable: boolean;
  key_advice: string;
}

export interface RashifalPlanetaryInfluence {
  planet: string;
  planet_hindi: string;
  transit_rashi: string;
  transit_rashi_hindi: string;
  house_from_moon: number;
  effect: 'shubh' | 'ashubh' | 'mishra';
  is_retrograde: boolean;
  significance: 'high' | 'medium' | 'low';
}

export interface RashifalData {
  rashi_num: number;
  rashi_name: string;
  rashi_hindi: string;
  rashi_symbol: string;
  period: string;
  start_date: string;
  end_date: string;
  overall_score: number;
  overall_prediction_hindi: string;
  overall_prediction_english: string;
  category_predictions: RashifalCategoryPrediction[];
  planetary_influences: RashifalPlanetaryInfluence[];
  key_transits: string[];
  lucky_color: string;
  lucky_number: string;
  lucky_day: string;
  mantra: string;
  deity: string;
  dos: string[];
  donts: string[];
  generated_at: string;
}

export interface RashiInfo {
  rashi_num: number;
  name: string;
  english: string;
  hindi: string;
  symbol: string;
  lord: string;
  element: string;
}

export interface RashifalResponse {
  success: boolean;
  data?: RashifalData;
  error?: string;
}

export interface AllRashifalResponse {
  success: boolean;
  data?: RashifalData[];
  error?: string;
}

// Rashi list constant
export const RASHI_LIST: RashiInfo[] = [
  { rashi_num: 0, name: 'Mesha', english: 'Aries', hindi: 'मेष', symbol: '1', lord: 'Mars', element: 'Fire' },
  { rashi_num: 1, name: 'Vrishabha', english: 'Taurus', hindi: 'वृषभ', symbol: '2', lord: 'Venus', element: 'Earth' },
  { rashi_num: 2, name: 'Mithuna', english: 'Gemini', hindi: 'मिथुन', symbol: '3', lord: 'Mercury', element: 'Air' },
  { rashi_num: 3, name: 'Karka', english: 'Cancer', hindi: 'कर्क', symbol: '4', lord: 'Moon', element: 'Water' },
  { rashi_num: 4, name: 'Simha', english: 'Leo', hindi: 'सिंह', symbol: '5', lord: 'Sun', element: 'Fire' },
  { rashi_num: 5, name: 'Kanya', english: 'Virgo', hindi: 'कन्या', symbol: '6', lord: 'Mercury', element: 'Earth' },
  { rashi_num: 6, name: 'Tula', english: 'Libra', hindi: 'तुला', symbol: '7', lord: 'Venus', element: 'Air' },
  { rashi_num: 7, name: 'Vrishchika', english: 'Scorpio', hindi: 'वृश्चिक', symbol: '8', lord: 'Mars', element: 'Water' },
  { rashi_num: 8, name: 'Dhanu', english: 'Sagittarius', hindi: 'धनु', symbol: '9', lord: 'Jupiter', element: 'Fire' },
  { rashi_num: 9, name: 'Makara', english: 'Capricorn', hindi: 'मकर', symbol: '10', lord: 'Saturn', element: 'Earth' },
  { rashi_num: 10, name: 'Kumbha', english: 'Aquarius', hindi: 'कुंभ', symbol: '11', lord: 'Saturn', element: 'Air' },
  { rashi_num: 11, name: 'Meena', english: 'Pisces', hindi: 'मीन', symbol: '12', lord: 'Jupiter', element: 'Water' },
];

// Rashifal period options
export const RASHIFAL_PERIOD_OPTIONS: { value: RashifalPeriod; label: string; labelHindi: string }[] = [
  { value: 'daily', label: 'Daily', labelHindi: 'आज का' },
  { value: 'weekly', label: 'Weekly', labelHindi: 'साप्ताहिक' },
  { value: 'monthly', label: 'Monthly', labelHindi: 'मासिक' },
  { value: 'yearly', label: 'Yearly', labelHindi: 'वार्षिक' },
];

// =============================================================================
// PANCHANG TYPES
// =============================================================================

export interface PanchangRequest {
  date: string;
  latitude?: number;
  longitude?: number;
  timezone?: string;
  location?: string;
}

export interface TithiInfo {
  name: string;
  hindi: string;
  number: number;
  paksha: string;
  paksha_hindi: string;
  lord: string;
  is_rikta: boolean;
  percentage_elapsed: number;
}

export interface NakshatraInfo {
  name: string;
  hindi: string;
  lord: string;
  deity: string;
  pada: number;
  percentage_elapsed: number;
}

export interface YogaInfo {
  name: string;
  hindi: string;
  is_inauspicious: boolean;
  description: string;
}

export interface KaranaInfo {
  name: string;
  hindi: string;
  type: string;
  is_auspicious: boolean;
  is_vishti: boolean;
}

export interface VaraInfo {
  name: string;
  hindi: string;
  lord: string;
  is_auspicious: boolean;
}

export interface SunMoonTimings {
  sunrise: string;
  sunset: string;
  moonrise: string | null;
  moonset: string | null;
  day_duration: string;
}

export interface ChoghadiyaItem {
  name: string;
  hindi: string;
  start: string;
  end: string;
  quality: string;
  is_auspicious: boolean;
}

export interface InauspiciousPeriodInfo {
  start: string;
  end: string;
  hindi: string;
}

export interface AuspiciousnessInfo {
  is_shubh_din: boolean;
  score: number;
  positive_factors: string[];
  negative_factors: string[];
  recommendations: string[];
}

export interface PanchangData {
  date: string;
  date_hindi: string;
  location: string;
  vara: VaraInfo;
  tithi: TithiInfo;
  nakshatra: NakshatraInfo;
  yoga: YogaInfo;
  karana: KaranaInfo;
  timings: SunMoonTimings;
  moon_rashi: {
    name: string;
    hindi: string;
  };
  day_choghadiya: ChoghadiyaItem[];
  night_choghadiya: ChoghadiyaItem[];
  current_choghadiya: ChoghadiyaItem | null;
  rahu_kaal: InauspiciousPeriodInfo;
  yamaghantaka: InauspiciousPeriodInfo;
  gulika_kaal: InauspiciousPeriodInfo;
  abhijit_muhurta: {
    start: string;
    end: string;
  } | null;
  auspiciousness: AuspiciousnessInfo;
  ayanamsa: number;
  moon_longitude: number;
  sun_longitude: number;
}

export interface PanchangResponse {
  success: boolean;
  data?: PanchangData;
  message?: string;
  error?: string;
}

// =============================================================================
// NUMEROLOGY (ANK JYOTISH) TYPES
// =============================================================================

export interface NumerologyCoreNumber {
  value: number;
  planet: string;
  description: string;
}

export interface NumerologyGemstone {
  name: string;
  sanskrit: string;
  planet: string;
}

export interface LetterBreakdown {
  letter: string;
  chaldean: number;
  pythagorean: number;
  is_vowel: boolean;
}

export interface NumerologyNameAnalysis {
  name: string;
  letter_breakdown: LetterBreakdown[];
  chaldean_total: number;
  chaldean_reduced: number;
  pythagorean_total: number;
  pythagorean_reduced: number;
  soul_number: number;
  personality_number: number;
  soul_number_desc: string;
  personality_number_desc: string;
}

export interface NumerologyResponse {
  name: string;
  birth_date: string;
  core_numbers: {
    moolank: NumerologyCoreNumber;
    bhagyank: NumerologyCoreNumber;
    namank_chaldean: NumerologyCoreNumber;
    namank_pythagorean: NumerologyCoreNumber;
  };
  personality: {
    traits: string[];
    description: string;
  };
  life_path: {
    description: string;
  };
  lucky_elements: {
    numbers: number[];
    colors: string[];
    days: string[];
    gemstone: NumerologyGemstone;
  };
  number_relationships: {
    friendly_numbers: number[];
    unfriendly_numbers: number[];
    compatibility_numbers: number[];
  };
  name_analysis: NumerologyNameAnalysis;
}

export interface NumerologyCompatibilityResponse {
  person1: {
    name: string;
    moolank: number;
    bhagyank: number;
  };
  person2: {
    name: string;
    moolank: number;
    bhagyank: number;
  };
  compatibility_score: number;
  compatibility_level: string;
  strengths: string[];
  challenges: string[];
  remedies: string[];
}

export interface BusinessNumerologyResponse {
  business_name: string;
  namank_chaldean: number;
  namank_pythagorean: number;
  ruling_planet: {
    planet: string;
    hindi: string;
  };
  owner_moolank: number;
  owner_bhagyank: number;
  is_compatible: boolean;
  is_auspicious: boolean;
  compatibility_level: string;
  recommendations: string[];
  lucky_days_for_business: string[];
  lucky_colors_for_business: string[];
}

export interface NameSuggestion {
  original_name: string;
  suggested_name: string;
  original_number: number;
  new_number: number;
  change_description: string;
  benefit: string;
}
