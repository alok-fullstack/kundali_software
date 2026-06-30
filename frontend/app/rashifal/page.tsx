'use client';

import React, { useState, useEffect, useCallback } from 'react';
import Link from 'next/link';

// =============================================================================
// TYPES
// =============================================================================

type RashifalPeriod = 'daily' | 'weekly' | 'monthly' | 'yearly';

interface CategoryPrediction {
  category: string;
  category_hindi: string;
  prediction_hindi: string;
  prediction_english: string;
  score: number;
  favorable: boolean;
  key_advice: string;
}

interface PlanetaryInfluence {
  planet: string;
  planet_hindi: string;
  transit_rashi: string;
  transit_rashi_hindi: string;
  house_from_moon: number;
  effect: 'shubh' | 'ashubh' | 'mishra';
  is_retrograde: boolean;
  significance: 'high' | 'medium' | 'low';
}

interface RashifalData {
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
  category_predictions: CategoryPrediction[];
  planetary_influences: PlanetaryInfluence[];
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

interface RashiInfo {
  rashi_num: number;
  name: string;
  english: string;
  hindi: string;
  symbol: string;
  lord: string;
  element: string;
}

// =============================================================================
// CONSTANTS
// =============================================================================

const RASHI_LIST: RashiInfo[] = [
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

const PERIOD_OPTIONS: { value: RashifalPeriod; label: string; labelHindi: string }[] = [
  { value: 'daily', label: 'Daily', labelHindi: 'आज का' },
  { value: 'weekly', label: 'Weekly', labelHindi: 'साप्ताहिक' },
  { value: 'monthly', label: 'Monthly', labelHindi: 'मासिक' },
  { value: 'yearly', label: 'Yearly', labelHindi: 'वार्षिक' },
];

const CATEGORY_ICONS: Record<string, string> = {
  career: '=',
  finance: '$',
  health: '+',
  relationships: '<3',
  family: '^',
  overall: '*',
};

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000/api';

// =============================================================================
// HELPER FUNCTIONS
// =============================================================================

function formatDateForAPI(date: Date): string {
  return date.toISOString().split('T')[0]; // YYYY-MM-DD
}

function formatDateForDisplay(date: Date, locale: string = 'hi-IN'): string {
  return date.toLocaleDateString(locale, {
    weekday: 'long',
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  });
}

// =============================================================================
// API FUNCTIONS
// =============================================================================

async function fetchRashifal(rashiNum: number, period: RashifalPeriod, date?: Date): Promise<RashifalData> {
  let url = `${API_BASE}/rashifal?rashi=${rashiNum}&period=${period}`;
  if (date) {
    url += `&date=${formatDateForAPI(date)}`;
  }
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error('Failed to fetch rashifal');
  }
  return response.json();
}

async function fetchAllRashifal(period: RashifalPeriod, date?: Date): Promise<RashifalData[]> {
  let url = `${API_BASE}/rashifal/all?period=${period}`;
  if (date) {
    url += `&date=${formatDateForAPI(date)}`;
  }
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error('Failed to fetch all rashifal');
  }
  return response.json();
}

// =============================================================================
// COMPONENTS
// =============================================================================

function ScoreIndicator({ score }: { score: number }) {
  const getScoreColor = (s: number) => {
    if (s >= 8) return 'bg-green-500';
    if (s >= 6) return 'bg-lime-500';
    if (s >= 4) return 'bg-yellow-500';
    if (s >= 2) return 'bg-orange-500';
    return 'bg-red-500';
  };

  const getScoreText = (s: number) => {
    if (s >= 8) return 'Excellent / उत्तम';
    if (s >= 6) return 'Good / अच्छा';
    if (s >= 4) return 'Average / सामान्य';
    if (s >= 2) return 'Challenging / चुनौतीपूर्ण';
    return 'Difficult / कठिन';
  };

  return (
    <div className="flex flex-col items-center">
      <div className="relative w-24 h-24">
        <svg className="w-24 h-24 transform -rotate-90">
          <circle
            cx="48"
            cy="48"
            r="40"
            fill="none"
            stroke="#e5e7eb"
            strokeWidth="8"
          />
          <circle
            cx="48"
            cy="48"
            r="40"
            fill="none"
            stroke="currentColor"
            strokeWidth="8"
            strokeDasharray={`${(score / 10) * 251.2} 251.2`}
            className={`${getScoreColor(score)} text-current`}
            style={{ color: 'inherit' }}
          />
        </svg>
        <div className="absolute inset-0 flex items-center justify-center">
          <span className="text-2xl font-bold text-gray-800">{score}/10</span>
        </div>
      </div>
      <span className={`mt-2 text-sm font-medium ${score >= 6 ? 'text-green-600' : score >= 4 ? 'text-yellow-600' : 'text-red-600'}`}>
        {getScoreText(score)}
      </span>
    </div>
  );
}

function CategoryCard({ prediction }: { prediction: CategoryPrediction }) {
  const icon = CATEGORY_ICONS[prediction.category] || '*';

  return (
    <div className={`p-4 rounded-lg border ${prediction.favorable ? 'bg-green-50 border-green-200' : 'bg-orange-50 border-orange-200'}`}>
      <div className="flex items-center gap-2 mb-2">
        <span className="text-xl">{icon}</span>
        <h4 className="font-semibold text-gray-800">{prediction.category_hindi}</h4>
        <span className={`ml-auto px-2 py-0.5 text-xs rounded-full ${prediction.favorable ? 'bg-green-200 text-green-800' : 'bg-orange-200 text-orange-800'}`}>
          {prediction.score}/10
        </span>
      </div>
      <p className="text-sm text-gray-700 mb-2">{prediction.prediction_hindi}</p>
      <p className="text-xs text-gray-500 italic">{prediction.key_advice}</p>
    </div>
  );
}

function PlanetaryInfluenceCard({ influence }: { influence: PlanetaryInfluence }) {
  const effectColors = {
    shubh: 'bg-green-100 border-green-300 text-green-800',
    ashubh: 'bg-red-100 border-red-300 text-red-800',
    mishra: 'bg-yellow-100 border-yellow-300 text-yellow-800',
  };

  const effectLabels = {
    shubh: 'Shubh / शुभ',
    ashubh: 'Ashubh / अशुभ',
    mishra: 'Mishra / मिश्रित',
  };

  return (
    <div className={`p-3 rounded-lg border ${effectColors[influence.effect]}`}>
      <div className="flex items-center justify-between mb-1">
        <span className="font-semibold">{influence.planet_hindi}</span>
        {influence.is_retrograde && (
          <span className="text-xs bg-purple-100 text-purple-700 px-1.5 py-0.5 rounded">(R) Vakri</span>
        )}
      </div>
      <div className="text-sm">
        <span>{influence.transit_rashi_hindi} mein</span>
        <span className="mx-1">|</span>
        <span>{influence.house_from_moon}th bhav</span>
      </div>
      <div className="mt-1 text-xs font-medium">{effectLabels[influence.effect]}</div>
    </div>
  );
}

function RashiSelector({
  selectedRashi,
  onSelect,
}: {
  selectedRashi: number | null;
  onSelect: (rashi: number) => void;
}) {
  return (
    <div className="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-6 gap-3">
      {RASHI_LIST.map((rashi) => (
        <button
          key={rashi.rashi_num}
          onClick={() => onSelect(rashi.rashi_num)}
          className={`p-3 rounded-lg border-2 transition-all hover:shadow-md ${
            selectedRashi === rashi.rashi_num
              ? 'border-orange-500 bg-orange-50 shadow-md'
              : 'border-gray-200 bg-white hover:border-orange-300'
          }`}
        >
          <div className="text-2xl text-center mb-1">{rashi.symbol}</div>
          <div className="text-sm font-semibold text-gray-800 text-center">{rashi.hindi}</div>
          <div className="text-xs text-gray-500 text-center">{rashi.english}</div>
        </button>
      ))}
    </div>
  );
}

function RashifalDisplay({ data }: { data: RashifalData }) {
  const [showTransits, setShowTransits] = useState(false);

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('hi-IN', {
      day: 'numeric',
      month: 'long',
      year: 'numeric',
    });
  };

  return (
    <div className="bg-white rounded-xl shadow-lg overflow-hidden">
      {/* Header */}
      <div className="bg-gradient-to-r from-orange-500 to-yellow-400 text-white p-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="text-5xl">{data.rashi_symbol}</div>
            <div>
              <h2 className="text-2xl font-bold">{data.rashi_hindi} राशिफल</h2>
              <p className="text-white/80">{data.rashi_name} ({RASHI_LIST[data.rashi_num].english})</p>
              <p className="text-sm text-white/70 mt-1">
                {formatDate(data.start_date)} - {formatDate(data.end_date)}
              </p>
            </div>
          </div>
          <ScoreIndicator score={data.overall_score} />
        </div>
      </div>

      {/* Overall Prediction */}
      <div className="p-6 bg-gradient-to-r from-orange-50 to-yellow-50 border-b">
        <h3 className="font-bold text-lg text-gray-800 mb-2">Samagra Phal / समग्र फल</h3>
        <p className="text-gray-700">{data.overall_prediction_hindi}</p>
      </div>

      {/* Lucky Elements */}
      <div className="p-4 border-b bg-white">
        <h3 className="font-bold text-gray-800 mb-3">Shubh Tatva / शुभ तत्व</h3>
        <div className="grid grid-cols-2 sm:grid-cols-5 gap-3 text-sm">
          <div className="bg-gray-50 rounded-lg p-3 text-center">
            <div className="text-gray-500 text-xs mb-1">Rang / Color</div>
            <div className="font-semibold text-gray-800">{data.lucky_color}</div>
          </div>
          <div className="bg-gray-50 rounded-lg p-3 text-center">
            <div className="text-gray-500 text-xs mb-1">Ank / Number</div>
            <div className="font-semibold text-gray-800">{data.lucky_number}</div>
          </div>
          <div className="bg-gray-50 rounded-lg p-3 text-center">
            <div className="text-gray-500 text-xs mb-1">Din / Day</div>
            <div className="font-semibold text-gray-800">{data.lucky_day}</div>
          </div>
          <div className="bg-gray-50 rounded-lg p-3 text-center">
            <div className="text-gray-500 text-xs mb-1">Devta / Deity</div>
            <div className="font-semibold text-gray-800">{data.deity}</div>
          </div>
          <div className="bg-gray-50 rounded-lg p-3 text-center col-span-2 sm:col-span-1">
            <div className="text-gray-500 text-xs mb-1">Mantra</div>
            <div className="font-semibold text-gray-800 text-xs">{data.mantra}</div>
          </div>
        </div>
      </div>

      {/* Category Predictions */}
      <div className="p-6 border-b">
        <h3 className="font-bold text-gray-800 mb-4">Vibhinn Kshetra / विभिन्न क्षेत्र</h3>
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {data.category_predictions.map((pred, idx) => (
            <CategoryCard key={idx} prediction={pred} />
          ))}
        </div>
      </div>

      {/* Do's and Don'ts */}
      <div className="p-6 border-b">
        <div className="grid md:grid-cols-2 gap-6">
          <div>
            <h3 className="font-bold text-green-700 mb-3 flex items-center gap-2">
              <span>+</span> Kya Karein / क्या करें
            </h3>
            <ul className="space-y-2">
              {data.dos.map((item, idx) => (
                <li key={idx} className="flex items-start gap-2 text-sm">
                  <span className="text-green-500 mt-0.5">-&gt;</span>
                  <span className="text-gray-700">{item}</span>
                </li>
              ))}
            </ul>
          </div>
          <div>
            <h3 className="font-bold text-red-700 mb-3 flex items-center gap-2">
              <span>x</span> Kya Na Karein / क्या न करें
            </h3>
            <ul className="space-y-2">
              {data.donts.map((item, idx) => (
                <li key={idx} className="flex items-start gap-2 text-sm">
                  <span className="text-red-500 mt-0.5">-&gt;</span>
                  <span className="text-gray-700">{item}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>

      {/* Key Transits */}
      <div className="p-6 border-b">
        <div className="flex items-center justify-between mb-3">
          <h3 className="font-bold text-gray-800">Pramukh Gochar / प्रमुख गोचर</h3>
          <button
            onClick={() => setShowTransits(!showTransits)}
            className="text-sm text-orange-600 hover:text-orange-700"
          >
            {showTransits ? 'Kam Dikhayein' : 'Aur Dikhayein'}
          </button>
        </div>
        <ul className="space-y-2">
          {data.key_transits.map((transit, idx) => (
            <li key={idx} className="text-sm text-gray-700 flex items-start gap-2">
              <span className="text-orange-500 mt-0.5">*</span>
              {transit}
            </li>
          ))}
        </ul>

        {showTransits && (
          <div className="mt-4 pt-4 border-t">
            <h4 className="font-semibold text-gray-700 mb-3">Sabhi Graha Gochar / सभी ग्रह गोचर</h4>
            <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-3">
              {data.planetary_influences.slice(0, 9).map((influence, idx) => (
                <PlanetaryInfluenceCard key={idx} influence={influence} />
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="p-4 bg-gray-50 text-center text-xs text-gray-500">
        <p>Brihat Parashara Hora Shastra aur Phaladeepika ke aadhar par</p>
        <p className="mt-1">Based on Brihat Parashara Hora Shastra & Phaladeepika</p>
      </div>
    </div>
  );
}

function AllRashifalGrid({ data, onSelectRashi }: { data: RashifalData[]; onSelectRashi: (num: number) => void }) {
  return (
    <div className="grid sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
      {data.map((rashifal) => {
        const rashi = RASHI_LIST[rashifal.rashi_num];
        return (
          <div
            key={rashifal.rashi_num}
            onClick={() => onSelectRashi(rashifal.rashi_num)}
            className="bg-white rounded-xl shadow-md overflow-hidden cursor-pointer hover:shadow-lg transition-shadow border border-gray-100"
          >
            <div className={`p-4 ${rashifal.overall_score >= 6 ? 'bg-gradient-to-r from-green-500 to-emerald-400' : rashifal.overall_score >= 4 ? 'bg-gradient-to-r from-yellow-500 to-amber-400' : 'bg-gradient-to-r from-orange-500 to-red-400'} text-white`}>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <span className="text-3xl">{rashi.symbol}</span>
                  <div>
                    <h3 className="font-bold">{rashifal.rashi_hindi}</h3>
                    <p className="text-xs text-white/80">{rashi.english}</p>
                  </div>
                </div>
                <div className="text-2xl font-bold">{rashifal.overall_score}/10</div>
              </div>
            </div>
            <div className="p-4">
              <p className="text-sm text-gray-700 line-clamp-3">{rashifal.overall_prediction_hindi}</p>
              <div className="mt-3 flex flex-wrap gap-2">
                {rashifal.category_predictions.slice(0, 3).map((cat, idx) => (
                  <span
                    key={idx}
                    className={`text-xs px-2 py-1 rounded-full ${cat.favorable ? 'bg-green-100 text-green-700' : 'bg-orange-100 text-orange-700'}`}
                  >
                    {cat.category_hindi}: {cat.score}
                  </span>
                ))}
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}

// =============================================================================
// MAIN PAGE COMPONENT
// =============================================================================

export default function RashifalPage() {
  const [selectedPeriod, setSelectedPeriod] = useState<RashifalPeriod>('daily');
  const [selectedRashi, setSelectedRashi] = useState<number | null>(null);
  const [selectedDate, setSelectedDate] = useState<Date>(new Date());
  const [rashifalData, setRashifalData] = useState<RashifalData | null>(null);
  const [allRashifalData, setAllRashifalData] = useState<RashifalData[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [viewMode, setViewMode] = useState<'select' | 'single' | 'all'>('select');

  // Fetch single rashifal
  const loadRashifal = useCallback(async (rashiNum: number, period: RashifalPeriod, date: Date) => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await fetchRashifal(rashiNum, period, date);
      setRashifalData(data);
      setViewMode('single');
    } catch (err) {
      setError('Rashifal load karne mein samasya aayi. Kripya dobara try karein.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Fetch all rashifal
  const loadAllRashifal = useCallback(async (period: RashifalPeriod, date: Date) => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await fetchAllRashifal(period, date);
      setAllRashifalData(data);
      setViewMode('all');
    } catch (err) {
      setError('Sabhi rashifal load karne mein samasya aayi. Kripya dobara try karein.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Handle rashi selection
  const handleRashiSelect = (rashiNum: number) => {
    setSelectedRashi(rashiNum);
    loadRashifal(rashiNum, selectedPeriod, selectedDate);
  };

  // Handle period change
  const handlePeriodChange = (period: RashifalPeriod) => {
    setSelectedPeriod(period);
    if (viewMode === 'single' && selectedRashi !== null) {
      loadRashifal(selectedRashi, period, selectedDate);
    } else if (viewMode === 'all') {
      loadAllRashifal(period, selectedDate);
    }
  };

  // Handle date change
  const handleDateChange = (newDate: Date) => {
    setSelectedDate(newDate);
    if (viewMode === 'single' && selectedRashi !== null) {
      loadRashifal(selectedRashi, selectedPeriod, newDate);
    } else if (viewMode === 'all') {
      loadAllRashifal(selectedPeriod, newDate);
    }
  };

  // Quick date navigation
  const goToToday = () => handleDateChange(new Date());
  const goToPreviousDay = () => handleDateChange(new Date(selectedDate.getTime() - 86400000));
  const goToNextDay = () => handleDateChange(new Date(selectedDate.getTime() + 86400000));

  // Handle view all
  const handleViewAll = () => {
    loadAllRashifal(selectedPeriod, selectedDate);
  };

  // Reset to selection view
  const handleReset = () => {
    setViewMode('select');
    setSelectedRashi(null);
    setRashifalData(null);
    setAllRashifalData([]);
    setError(null);
  };

  return (
    <main className="min-h-screen py-5 px-4 bg-gradient-to-br from-orange-50 to-yellow-50">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-6">
          <Link href="/" className="inline-flex items-center text-orange-600 hover:text-orange-700 mb-4">
            <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            Wapas Jayen / Back to Kundali
          </Link>
          <h1 className="text-3xl font-bold text-gray-800 mb-2">
            <span className="text-orange-500">Rashifal / राशिफल</span>
          </h1>
          <p className="text-gray-600">Rashifal - Bhoot, Vartaman, Bhavishya / Past, Present, Future</p>
          <p className="text-sm text-gray-500 mt-1">Brihat Parashara Hora Shastra ke aadhar par | Koi bhi din chunein</p>
        </div>

        {/* Period Selector */}
        <div className="flex justify-center gap-2 mb-4">
          {PERIOD_OPTIONS.map((period) => (
            <button
              key={period.value}
              onClick={() => handlePeriodChange(period.value)}
              className={`px-4 py-2 rounded-lg font-medium transition-all ${
                selectedPeriod === period.value
                  ? 'bg-orange-500 text-white shadow-md'
                  : 'bg-white text-gray-700 hover:bg-orange-100 border border-gray-200'
              }`}
            >
              <span>{period.labelHindi}</span>
              <span className="text-xs ml-1 opacity-70">/ {period.label}</span>
            </button>
          ))}
        </div>

        {/* Date Picker */}
        <div className="flex justify-center items-center gap-3 mb-6">
          <button
            onClick={goToPreviousDay}
            className="p-2 rounded-lg bg-white border border-gray-200 hover:bg-orange-50 hover:border-orange-300 transition-all"
            title="Pichla Din / Previous Day"
          >
            <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
          </button>

          <div className="flex items-center gap-2 bg-white rounded-lg border border-gray-200 px-3 py-2">
            <svg className="w-5 h-5 text-orange-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            <input
              type="date"
              value={formatDateForAPI(selectedDate)}
              onChange={(e) => handleDateChange(new Date(e.target.value))}
              className="bg-transparent text-gray-700 font-medium outline-none cursor-pointer"
            />
          </div>

          <button
            onClick={goToNextDay}
            className="p-2 rounded-lg bg-white border border-gray-200 hover:bg-orange-50 hover:border-orange-300 transition-all"
            title="Agla Din / Next Day"
          >
            <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
          </button>

          <button
            onClick={goToToday}
            className={`px-3 py-2 rounded-lg font-medium transition-all ${
              formatDateForAPI(selectedDate) === formatDateForAPI(new Date())
                ? 'bg-orange-100 text-orange-700 border border-orange-300'
                : 'bg-white text-gray-600 border border-gray-200 hover:bg-orange-50'
            }`}
          >
            Aaj / Today
          </button>
        </div>

        {/* Selected Date Display */}
        <div className="text-center mb-4">
          <p className="text-gray-600 text-sm">
            <span className="font-medium text-orange-600">{formatDateForDisplay(selectedDate)}</span>
            {formatDateForAPI(selectedDate) !== formatDateForAPI(new Date()) && (
              <span className="ml-2 text-xs bg-yellow-100 text-yellow-700 px-2 py-0.5 rounded-full">
                {selectedDate > new Date() ? 'Bhavishya / Future' : 'Bhoot / Past'}
              </span>
            )}
          </p>
        </div>

        {/* Error Display */}
        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700 text-center">
            {error}
            <button
              onClick={handleReset}
              className="ml-4 text-sm underline hover:no-underline"
            >
              Dobara try karein
            </button>
          </div>
        )}

        {/* Loading State */}
        {isLoading && (
          <div className="flex justify-center items-center py-20">
            <div className="animate-spin rounded-full h-12 w-12 border-4 border-orange-500 border-t-transparent"></div>
            <span className="ml-4 text-gray-600">Rashifal load ho raha hai...</span>
          </div>
        )}

        {/* Rashi Selection View */}
        {viewMode === 'select' && !isLoading && (
          <div className="space-y-6">
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h2 className="font-bold text-lg text-gray-800 mb-4 text-center">
                Apni Rashi Chunein / Select Your Sign
              </h2>
              <RashiSelector selectedRashi={selectedRashi} onSelect={handleRashiSelect} />
            </div>

            <div className="text-center">
              <button
                onClick={handleViewAll}
                className="px-6 py-3 bg-gradient-to-r from-orange-500 to-yellow-500 text-white rounded-lg font-semibold hover:shadow-lg transition-all"
              >
                Sabhi Rashiyon Ka Rashifal Dekhein / View All Signs
              </button>
            </div>
          </div>
        )}

        {/* Single Rashifal View */}
        {viewMode === 'single' && !isLoading && rashifalData && (
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <button
                onClick={handleReset}
                className="px-4 py-2 text-orange-600 hover:text-orange-700 font-medium flex items-center gap-1"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                </svg>
                Wapas
              </button>
              <button
                onClick={handleViewAll}
                className="px-4 py-2 text-orange-600 hover:text-orange-700 font-medium"
              >
                Sabhi Rashi Dekhein
              </button>
            </div>
            <RashifalDisplay data={rashifalData} />
          </div>
        )}

        {/* All Rashifal View */}
        {viewMode === 'all' && !isLoading && allRashifalData.length > 0 && (
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <button
                onClick={handleReset}
                className="px-4 py-2 text-orange-600 hover:text-orange-700 font-medium flex items-center gap-1"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                </svg>
                Wapas
              </button>
              <h2 className="font-bold text-lg text-gray-800">
                {PERIOD_OPTIONS.find(p => p.value === selectedPeriod)?.labelHindi} Rashifal - Sabhi Rashi
              </h2>
              <div className="w-20"></div>
            </div>
            <AllRashifalGrid
              data={allRashifalData}
              onSelectRashi={(num) => {
                setSelectedRashi(num);
                const selected = allRashifalData.find(r => r.rashi_num === num);
                if (selected) {
                  setRashifalData(selected);
                  setViewMode('single');
                }
              }}
            />
          </div>
        )}

        {/* Info Box */}
        {viewMode === 'select' && !isLoading && (
          <div className="mt-8 p-4 bg-white rounded-lg shadow text-center">
            <h3 className="font-semibold text-gray-800 mb-2">Rashifal Kya Hai? / What is Rashifal?</h3>
            <p className="text-sm text-gray-600">
              Rashifal aapki Chandra Rashi (Moon Sign) ke aadhar par graha gochar (planetary transits) ka vishleshan hai.
              Yeh Brihat Parashara Hora Shastra aur Phaladeepika jaise prachin Vedic granth mein varnnit siddhanton par aadharit hai.
            </p>
            <p className="text-xs text-gray-500 mt-2">
              Note: Apni Chandra Rashi jaanne ke liye, pahle apni kundali banayen. Moon sign aapke janm ke samay
              Chandra ki rashi position hai, jo Sun sign (Western zodiac) se alag hai.
            </p>
          </div>
        )}

        {/* Disclaimer */}
        <div className="mt-8 p-4 bg-gray-100 rounded-lg text-center text-xs text-gray-500">
          <p>Yeh rashifal samanya margdarshan ke liye hai. Vyaktigat phal aapki sampurn kundali par nirbhar karte hain.</p>
          <p className="mt-1">This horoscope is for general guidance. Individual results depend on your complete birth chart.</p>
        </div>
      </div>
    </main>
  );
}
