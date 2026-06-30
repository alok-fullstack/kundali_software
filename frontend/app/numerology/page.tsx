'use client';

import React, { useState, useRef, useEffect } from 'react';
import Link from 'next/link';
import { CustomDatePicker } from '../components/ui/DateTimePicker';

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000/api';

interface CoreNumber {
  value: number;
  planet: string;
  description: string;
}

interface GemstoneInfo {
  name: string;
  sanskrit: string;
  planet: string;
}

interface LetterBreakdown {
  letter: string;
  chaldean: number;
  pythagorean: number;
  is_vowel: boolean;
}

interface NameAnalysis {
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

interface NumerologyResult {
  name: string;
  birth_date: string;
  core_numbers: {
    moolank: CoreNumber;
    bhagyank: CoreNumber;
    namank_chaldean: CoreNumber;
    namank_pythagorean: CoreNumber;
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
    gemstone: GemstoneInfo;
  };
  number_relationships: {
    friendly_numbers: number[];
    unfriendly_numbers: number[];
    compatibility_numbers: number[];
  };
  name_analysis: NameAnalysis;
}

interface NameSuggestion {
  original_name: string;
  suggested_name: string;
  original_number: number;
  new_number: number;
  change_description: string;
  benefit: string;
}

interface CompatibilityResult {
  person1: { name: string; moolank: number; bhagyank: number };
  person2: { name: string; moolank: number; bhagyank: number };
  compatibility_score: number;
  compatibility_level: string;
  strengths: string[];
  challenges: string[];
  remedies: string[];
}

interface BusinessAnalysis {
  business_name: string;
  namank_chaldean: number;
  namank_pythagorean: number;
  ruling_planet: { planet: string; hindi: string };
  owner_moolank: number;
  owner_bhagyank: number;
  is_compatible: boolean;
  is_auspicious: boolean;
  compatibility_level: string;
  recommendations: string[];
  lucky_days_for_business: string[];
  lucky_colors_for_business: string[];
}

type TabType = 'personal' | 'compatibility' | 'business' | 'name-correction';

// Number color map for visual display
const numberColors: Record<number, string> = {
  1: 'from-yellow-400 to-orange-500',
  2: 'from-gray-200 to-gray-400',
  3: 'from-yellow-300 to-amber-500',
  4: 'from-blue-400 to-indigo-500',
  5: 'from-green-400 to-emerald-500',
  6: 'from-pink-400 to-rose-500',
  7: 'from-purple-400 to-violet-500',
  8: 'from-slate-600 to-slate-800',
  9: 'from-red-400 to-red-600',
};

function NumberBadge({ number, size = 'md' }: { number: number; size?: 'sm' | 'md' | 'lg' }) {
  const sizeClasses = {
    sm: 'w-8 h-8 text-sm',
    md: 'w-12 h-12 text-xl',
    lg: 'w-16 h-16 text-2xl',
  };

  return (
    <div
      className={`${sizeClasses[size]} bg-gradient-to-br ${numberColors[number] || 'from-gray-400 to-gray-600'} rounded-full flex items-center justify-center text-white font-bold shadow-lg`}
    >
      {number}
    </div>
  );
}

export default function NumerologyPage() {
  const [activeTab, setActiveTab] = useState<TabType>('personal');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Personal Analysis State
  const [name, setName] = useState('');
  const [birthDate, setBirthDate] = useState<Date | null>(null);
  const [result, setResult] = useState<NumerologyResult | null>(null);
  const [nameSuggestions, setNameSuggestions] = useState<NameSuggestion[]>([]);

  // Compatibility State
  const [person1Name, setPerson1Name] = useState('');
  const [person1Dob, setPerson1Dob] = useState<Date | null>(null);
  const [person2Name, setPerson2Name] = useState('');
  const [person2Dob, setPerson2Dob] = useState<Date | null>(null);
  const [compatibilityResult, setCompatibilityResult] = useState<CompatibilityResult | null>(null);

  // Business Analysis State
  const [businessName, setBusinessName] = useState('');
  const [ownerDob, setOwnerDob] = useState<Date | null>(null);
  const [businessResult, setBusinessResult] = useState<BusinessAnalysis | null>(null);

  const resultsRef = useRef<HTMLDivElement>(null);

  const formatDate = (date: Date): string => {
    const year = date.getFullYear();
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    const day = date.getDate().toString().padStart(2, '0');
    return `${year}-${month}-${day}`;
  };

  const handlePersonalAnalysis = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name || !birthDate) {
      setError('Please fill all fields / Sabhi jankari bharein');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch(`${API_BASE}/numerology/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: name,
          birth_date: formatDate(birthDate),
        }),
      });

      if (!response.ok) throw new Error('Failed to analyze');

      const data = await response.json();
      setResult(data);

      // Also fetch name suggestions
      const suggestResponse = await fetch(`${API_BASE}/numerology/suggest-name`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: name,
          birth_date: formatDate(birthDate),
        }),
      });

      if (suggestResponse.ok) {
        const suggestions = await suggestResponse.json();
        setNameSuggestions(suggestions);
      }

      setTimeout(() => {
        resultsRef.current?.scrollIntoView({ behavior: 'smooth' });
      }, 100);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  const handleCompatibilityAnalysis = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!person1Name || !person1Dob || !person2Name || !person2Dob) {
      setError('Please fill all fields / Sabhi jankari bharein');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch(`${API_BASE}/numerology/compatibility`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          person1_name: person1Name,
          person1_dob: formatDate(person1Dob),
          person2_name: person2Name,
          person2_dob: formatDate(person2Dob),
        }),
      });

      if (!response.ok) throw new Error('Failed to analyze');

      const data = await response.json();
      setCompatibilityResult(data);

      setTimeout(() => {
        resultsRef.current?.scrollIntoView({ behavior: 'smooth' });
      }, 100);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  const handleBusinessAnalysis = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!businessName || !ownerDob) {
      setError('Please fill all fields / Sabhi jankari bharein');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch(`${API_BASE}/numerology/business`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          business_name: businessName,
          owner_dob: formatDate(ownerDob),
        }),
      });

      if (!response.ok) throw new Error('Failed to analyze');

      const data = await response.json();
      setBusinessResult(data);

      setTimeout(() => {
        resultsRef.current?.scrollIntoView({ behavior: 'smooth' });
      }, 100);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setResult(null);
    setCompatibilityResult(null);
    setBusinessResult(null);
    setNameSuggestions([]);
    setError(null);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <main className="min-h-screen py-5 px-4 bg-gradient-to-br from-purple-50 to-indigo-50">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-6">
          <Link href="/" className="inline-flex items-center text-purple-600 hover:text-purple-700 mb-4">
            <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            वापस कुंडली / Back to Kundali
          </Link>
          <h1 className="text-3xl font-bold text-gray-800 mb-2">
            <span className="text-purple-600">अंक ज्योतिष / Numerology</span>
          </h1>
          <p className="text-gray-600">वैदिक अंक शास्त्र - नाम और जन्म तिथि का रहस्य / Vedic Number Science</p>
          <p className="text-sm text-gray-500 mt-1">Based on Cheiro & Vedic Numerology traditions</p>
        </div>

        {/* Tab Navigation */}
        <div className="flex flex-wrap justify-center gap-2 mb-6">
          {[
            { id: 'personal', label: 'Personal Analysis', labelHindi: 'व्यक्तिगत' },
            { id: 'compatibility', label: 'Compatibility', labelHindi: 'अनुकूलता' },
            { id: 'business', label: 'Business Name', labelHindi: 'व्यापार नाम' },
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => {
                setActiveTab(tab.id as TabType);
                handleReset();
              }}
              className={`px-4 py-2 rounded-lg font-medium transition-all ${
                activeTab === tab.id
                  ? 'bg-purple-600 text-white shadow-lg'
                  : 'bg-white text-gray-600 hover:bg-purple-50 border border-gray-200'
              }`}
            >
              <span>{tab.labelHindi}</span>
              <span className="text-xs ml-1 opacity-75">/ {tab.label}</span>
            </button>
          ))}
        </div>

        {/* Error Display */}
        {error && (
          <div className="mb-4 p-3 bg-red-50 border-l-4 border-red-500 rounded-r-lg text-red-700">
            {error}
          </div>
        )}

        {/* Personal Analysis Form */}
        {activeTab === 'personal' && !result && (
          <form onSubmit={handlePersonalAnalysis} className="bg-white rounded-xl shadow-lg p-6 mb-6">
            <div className="grid md:grid-cols-2 gap-6">
              <div>
                <label className="block mb-1.5 font-medium text-gray-700 text-sm">
                  <span className="text-purple-500">नाम</span>
                  <span className="text-gray-400 text-xs ml-1">/ Name *</span>
                </label>
                <input
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="अपना पूरा नाम लिखें / Enter your full name..."
                  className="w-full px-3 py-2.5 border border-gray-200 rounded-lg focus:border-purple-500 focus:ring-1 focus:ring-purple-200 transition-all"
                  required
                />
              </div>
              <div>
                <label className="block mb-1.5 font-medium text-gray-700 text-sm">
                  <span className="text-purple-500">जन्म तिथि</span>
                  <span className="text-gray-400 text-xs ml-1">/ Date of Birth *</span>
                </label>
                <CustomDatePicker
                  value={birthDate}
                  onChange={setBirthDate}
                  placeholder="जन्म तिथि चुनें / Select date..."
                  minYear={1900}
                  maxYear={new Date().getFullYear()}
                />
              </div>
            </div>
            <div className="mt-6 flex justify-center">
              <button
                type="submit"
                disabled={isLoading}
                className="px-8 py-3 bg-gradient-to-r from-purple-500 to-indigo-500 hover:from-purple-600 hover:to-indigo-600 text-white font-semibold rounded-lg shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all disabled:opacity-50"
              >
                {isLoading ? (
                  <span className="flex items-center gap-2">
                    <svg className="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Analyzing...
                  </span>
                ) : (
                  'अंक गणना करें / Calculate'
                )}
              </button>
            </div>
          </form>
        )}

        {/* Compatibility Form */}
        {activeTab === 'compatibility' && !compatibilityResult && (
          <form onSubmit={handleCompatibilityAnalysis} className="bg-white rounded-xl shadow-lg p-6 mb-6">
            <div className="grid md:grid-cols-2 gap-6">
              {/* Person 1 */}
              <div className="space-y-4 p-4 bg-blue-50 rounded-lg">
                <h3 className="font-semibold text-blue-800">व्यक्ति 1 / Person 1</h3>
                <div>
                  <label className="block mb-1.5 font-medium text-gray-700 text-sm">नाम / Name *</label>
                  <input
                    type="text"
                    value={person1Name}
                    onChange={(e) => setPerson1Name(e.target.value)}
                    placeholder="नाम लिखें / Enter name..."
                    className="w-full px-3 py-2.5 border border-gray-200 rounded-lg focus:border-blue-500 focus:ring-1 focus:ring-blue-200"
                    required
                  />
                </div>
                <div>
                  <label className="block mb-1.5 font-medium text-gray-700 text-sm">जन्म तिथि / DOB *</label>
                  <CustomDatePicker
                    value={person1Dob}
                    onChange={setPerson1Dob}
                    placeholder="तिथि चुनें / Select date..."
                    minYear={1900}
                    maxYear={new Date().getFullYear()}
                  />
                </div>
              </div>

              {/* Person 2 */}
              <div className="space-y-4 p-4 bg-pink-50 rounded-lg">
                <h3 className="font-semibold text-pink-800">Vyakti 2 / Person 2</h3>
                <div>
                  <label className="block mb-1.5 font-medium text-gray-700 text-sm">Naam / Name *</label>
                  <input
                    type="text"
                    value={person2Name}
                    onChange={(e) => setPerson2Name(e.target.value)}
                    placeholder="Naam likhein..."
                    className="w-full px-3 py-2.5 border border-gray-200 rounded-lg focus:border-pink-500 focus:ring-1 focus:ring-pink-200"
                    required
                  />
                </div>
                <div>
                  <label className="block mb-1.5 font-medium text-gray-700 text-sm">Janam Tithi / DOB *</label>
                  <CustomDatePicker
                    value={person2Dob}
                    onChange={setPerson2Dob}
                    placeholder="Tithi chunein..."
                    minYear={1900}
                    maxYear={new Date().getFullYear()}
                  />
                </div>
              </div>
            </div>
            <div className="mt-6 flex justify-center">
              <button
                type="submit"
                disabled={isLoading}
                className="px-8 py-3 bg-gradient-to-r from-blue-500 to-pink-500 hover:from-blue-600 hover:to-pink-600 text-white font-semibold rounded-lg shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all disabled:opacity-50"
              >
                {isLoading ? 'Analyzing...' : 'Anukoolata Jaanchein / Check Compatibility'}
              </button>
            </div>
          </form>
        )}

        {/* Business Analysis Form */}
        {activeTab === 'business' && !businessResult && (
          <form onSubmit={handleBusinessAnalysis} className="bg-white rounded-xl shadow-lg p-6 mb-6">
            <div className="grid md:grid-cols-2 gap-6">
              <div>
                <label className="block mb-1.5 font-medium text-gray-700 text-sm">
                  <span className="text-purple-500">Vyapar ka Naam</span>
                  <span className="text-gray-400 text-xs ml-1">/ Business Name *</span>
                </label>
                <input
                  type="text"
                  value={businessName}
                  onChange={(e) => setBusinessName(e.target.value)}
                  placeholder="Business naam likhein..."
                  className="w-full px-3 py-2.5 border border-gray-200 rounded-lg focus:border-purple-500 focus:ring-1 focus:ring-purple-200 transition-all"
                  required
                />
              </div>
              <div>
                <label className="block mb-1.5 font-medium text-gray-700 text-sm">
                  <span className="text-purple-500">Maalik ki Janam Tithi</span>
                  <span className="text-gray-400 text-xs ml-1">/ Owner&apos;s DOB *</span>
                </label>
                <CustomDatePicker
                  value={ownerDob}
                  onChange={setOwnerDob}
                  placeholder="Tithi chunein..."
                  minYear={1900}
                  maxYear={new Date().getFullYear()}
                />
              </div>
            </div>
            <div className="mt-6 flex justify-center">
              <button
                type="submit"
                disabled={isLoading}
                className="px-8 py-3 bg-gradient-to-r from-green-500 to-emerald-500 hover:from-green-600 hover:to-emerald-600 text-white font-semibold rounded-lg shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all disabled:opacity-50"
              >
                {isLoading ? 'Analyzing...' : 'Vyapar Naam Jaanchein / Analyze Business Name'}
              </button>
            </div>
          </form>
        )}

        {/* Personal Analysis Results */}
        {result && activeTab === 'personal' && (
          <div ref={resultsRef} className="space-y-6">
            {/* Core Numbers Section */}
            <div className="bg-white rounded-xl shadow-lg overflow-hidden">
              <div className="bg-gradient-to-r from-purple-500 to-indigo-500 text-white p-4">
                <h2 className="text-xl font-bold">Mool Ank / Core Numbers</h2>
                <p className="text-sm text-purple-100">{result.name} - {result.birth_date}</p>
              </div>
              <div className="p-6">
                <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
                  {/* Moolank */}
                  <div className="bg-gradient-to-br from-yellow-50 to-orange-50 rounded-lg p-4 border border-yellow-200">
                    <div className="flex items-center gap-3 mb-2">
                      <NumberBadge number={result.core_numbers.moolank.value} />
                      <div>
                        <h3 className="font-bold text-gray-800">Moolank</h3>
                        <p className="text-xs text-gray-500">Root Number</p>
                      </div>
                    </div>
                    <p className="text-sm text-gray-600">{result.core_numbers.moolank.planet}</p>
                    <p className="text-xs text-gray-400 mt-1">{result.core_numbers.moolank.description}</p>
                  </div>

                  {/* Bhagyank */}
                  <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-lg p-4 border border-blue-200">
                    <div className="flex items-center gap-3 mb-2">
                      <NumberBadge number={result.core_numbers.bhagyank.value} />
                      <div>
                        <h3 className="font-bold text-gray-800">Bhagyank</h3>
                        <p className="text-xs text-gray-500">Destiny Number</p>
                      </div>
                    </div>
                    <p className="text-sm text-gray-600">{result.core_numbers.bhagyank.planet}</p>
                    <p className="text-xs text-gray-400 mt-1">{result.core_numbers.bhagyank.description}</p>
                  </div>

                  {/* Namank Chaldean */}
                  <div className="bg-gradient-to-br from-green-50 to-emerald-50 rounded-lg p-4 border border-green-200">
                    <div className="flex items-center gap-3 mb-2">
                      <NumberBadge number={result.core_numbers.namank_chaldean.value} />
                      <div>
                        <h3 className="font-bold text-gray-800">Namank</h3>
                        <p className="text-xs text-gray-500">Chaldean</p>
                      </div>
                    </div>
                    <p className="text-sm text-gray-600">{result.core_numbers.namank_chaldean.planet}</p>
                  </div>

                  {/* Namank Pythagorean */}
                  <div className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-lg p-4 border border-purple-200">
                    <div className="flex items-center gap-3 mb-2">
                      <NumberBadge number={result.core_numbers.namank_pythagorean.value} />
                      <div>
                        <h3 className="font-bold text-gray-800">Namank</h3>
                        <p className="text-xs text-gray-500">Pythagorean</p>
                      </div>
                    </div>
                    <p className="text-sm text-gray-600">{result.core_numbers.namank_pythagorean.planet}</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Personality & Life Path */}
            <div className="grid md:grid-cols-2 gap-6">
              {/* Personality */}
              <div className="bg-white rounded-xl shadow-lg overflow-hidden">
                <div className="bg-gradient-to-r from-amber-500 to-orange-500 text-white p-4">
                  <h2 className="text-lg font-bold">Vyaktitva / Personality</h2>
                </div>
                <div className="p-4">
                  <p className="text-sm text-gray-700 mb-4">{result.personality.description}</p>
                  <h4 className="font-semibold text-gray-800 mb-2">Gun / Traits:</h4>
                  <ul className="space-y-1">
                    {result.personality.traits.map((trait, idx) => (
                      <li key={idx} className="flex items-start gap-2 text-sm">
                        <span className="text-amber-500 mt-0.5">*</span>
                        <span className="text-gray-600">{trait}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>

              {/* Life Path */}
              <div className="bg-white rounded-xl shadow-lg overflow-hidden">
                <div className="bg-gradient-to-r from-blue-500 to-cyan-500 text-white p-4">
                  <h2 className="text-lg font-bold">Jeevan Path / Life Path</h2>
                </div>
                <div className="p-4">
                  <p className="text-sm text-gray-700 leading-relaxed">{result.life_path.description}</p>
                </div>
              </div>
            </div>

            {/* Lucky Elements */}
            <div className="bg-white rounded-xl shadow-lg overflow-hidden">
              <div className="bg-gradient-to-r from-green-500 to-teal-500 text-white p-4">
                <h2 className="text-lg font-bold">Shubh Tatva / Lucky Elements</h2>
              </div>
              <div className="p-4 grid md:grid-cols-2 lg:grid-cols-4 gap-4">
                {/* Lucky Numbers */}
                <div className="bg-green-50 rounded-lg p-3 border border-green-200">
                  <h4 className="font-semibold text-green-800 mb-2">Shubh Ank / Lucky Numbers</h4>
                  <div className="flex flex-wrap gap-2">
                    {result.lucky_elements.numbers.map((num) => (
                      <NumberBadge key={num} number={num} size="sm" />
                    ))}
                  </div>
                </div>

                {/* Lucky Colors */}
                <div className="bg-pink-50 rounded-lg p-3 border border-pink-200">
                  <h4 className="font-semibold text-pink-800 mb-2">Shubh Rang / Lucky Colors</h4>
                  <div className="space-y-1">
                    {result.lucky_elements.colors.map((color, idx) => (
                      <span key={idx} className="inline-block px-2 py-0.5 bg-white rounded text-sm text-gray-700 mr-1 mb-1">
                        {color}
                      </span>
                    ))}
                  </div>
                </div>

                {/* Lucky Days */}
                <div className="bg-blue-50 rounded-lg p-3 border border-blue-200">
                  <h4 className="font-semibold text-blue-800 mb-2">Shubh Din / Lucky Days</h4>
                  <div className="space-y-1">
                    {result.lucky_elements.days.map((day, idx) => (
                      <span key={idx} className="inline-block px-2 py-0.5 bg-white rounded text-sm text-gray-700 mr-1 mb-1">
                        {day}
                      </span>
                    ))}
                  </div>
                </div>

                {/* Lucky Gemstone */}
                <div className="bg-purple-50 rounded-lg p-3 border border-purple-200">
                  <h4 className="font-semibold text-purple-800 mb-2">Shubh Ratna / Lucky Gemstone</h4>
                  <p className="text-gray-700 font-medium">{result.lucky_elements.gemstone.name}</p>
                  <p className="text-xs text-gray-500">{result.lucky_elements.gemstone.sanskrit}</p>
                  <p className="text-xs text-purple-600 mt-1">Planet: {result.lucky_elements.gemstone.planet}</p>
                </div>
              </div>
            </div>

            {/* Number Relationships */}
            <div className="bg-white rounded-xl shadow-lg overflow-hidden">
              <div className="bg-gradient-to-r from-indigo-500 to-purple-500 text-white p-4">
                <h2 className="text-lg font-bold">Ank Sambandh / Number Relationships</h2>
              </div>
              <div className="p-4 grid md:grid-cols-3 gap-4">
                <div className="bg-green-50 rounded-lg p-3 border border-green-200">
                  <h4 className="font-semibold text-green-800 mb-2">Mitra Ank / Friendly Numbers</h4>
                  <div className="flex flex-wrap gap-2">
                    {result.number_relationships.friendly_numbers.map((num) => (
                      <NumberBadge key={num} number={num} size="sm" />
                    ))}
                  </div>
                </div>
                <div className="bg-red-50 rounded-lg p-3 border border-red-200">
                  <h4 className="font-semibold text-red-800 mb-2">Shatru Ank / Unfriendly Numbers</h4>
                  <div className="flex flex-wrap gap-2">
                    {result.number_relationships.unfriendly_numbers.map((num) => (
                      <NumberBadge key={num} number={num} size="sm" />
                    ))}
                  </div>
                </div>
                <div className="bg-blue-50 rounded-lg p-3 border border-blue-200">
                  <h4 className="font-semibold text-blue-800 mb-2">Anukool Ank / Compatible Numbers</h4>
                  <div className="flex flex-wrap gap-2">
                    {result.number_relationships.compatibility_numbers.map((num) => (
                      <NumberBadge key={num} number={num} size="sm" />
                    ))}
                  </div>
                </div>
              </div>
            </div>

            {/* Name Analysis */}
            <div className="bg-white rounded-xl shadow-lg overflow-hidden">
              <div className="bg-gradient-to-r from-rose-500 to-pink-500 text-white p-4">
                <h2 className="text-lg font-bold">Naam Vishleshan / Name Analysis</h2>
              </div>
              <div className="p-4">
                <div className="grid md:grid-cols-2 gap-4 mb-4">
                  <div className="bg-pink-50 rounded-lg p-3">
                    <h4 className="font-semibold text-pink-800">Aatma Ank / Soul Number</h4>
                    <div className="flex items-center gap-2 mt-1">
                      <NumberBadge number={result.name_analysis.soul_number} size="sm" />
                      <span className="text-sm text-gray-600">{result.name_analysis.soul_number_desc}</span>
                    </div>
                  </div>
                  <div className="bg-indigo-50 rounded-lg p-3">
                    <h4 className="font-semibold text-indigo-800">Vyaktitva Ank / Personality Number</h4>
                    <div className="flex items-center gap-2 mt-1">
                      <NumberBadge number={result.name_analysis.personality_number} size="sm" />
                      <span className="text-sm text-gray-600">{result.name_analysis.personality_number_desc}</span>
                    </div>
                  </div>
                </div>

                {/* Letter Breakdown Table */}
                <h4 className="font-semibold text-gray-800 mb-2">Akshar Vishleshan / Letter Breakdown</h4>
                <div className="overflow-x-auto">
                  <table className="w-full text-sm">
                    <thead>
                      <tr className="bg-gray-100">
                        <th className="px-3 py-2 text-left">Letter</th>
                        <th className="px-3 py-2 text-center">Chaldean</th>
                        <th className="px-3 py-2 text-center">Pythagorean</th>
                        <th className="px-3 py-2 text-center">Type</th>
                      </tr>
                    </thead>
                    <tbody>
                      {result.name_analysis.letter_breakdown.map((letter, idx) => (
                        <tr key={idx} className="border-b">
                          <td className="px-3 py-2 font-bold text-purple-600">{letter.letter}</td>
                          <td className="px-3 py-2 text-center">{letter.chaldean}</td>
                          <td className="px-3 py-2 text-center">{letter.pythagorean}</td>
                          <td className="px-3 py-2 text-center">
                            <span className={`px-2 py-0.5 rounded text-xs ${letter.is_vowel ? 'bg-pink-100 text-pink-700' : 'bg-blue-100 text-blue-700'}`}>
                              {letter.is_vowel ? 'Vowel' : 'Consonant'}
                            </span>
                          </td>
                        </tr>
                      ))}
                      <tr className="bg-gray-50 font-semibold">
                        <td className="px-3 py-2">Total</td>
                        <td className="px-3 py-2 text-center">{result.name_analysis.chaldean_total} = {result.name_analysis.chaldean_reduced}</td>
                        <td className="px-3 py-2 text-center">{result.name_analysis.pythagorean_total} = {result.name_analysis.pythagorean_reduced}</td>
                        <td className="px-3 py-2"></td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>

            {/* Name Correction Suggestions */}
            {nameSuggestions.length > 0 && (
              <div className="bg-white rounded-xl shadow-lg overflow-hidden">
                <div className="bg-gradient-to-r from-amber-500 to-yellow-500 text-white p-4">
                  <h2 className="text-lg font-bold">Naam Sudhar / Name Correction Suggestions</h2>
                </div>
                <div className="p-4 space-y-3">
                  {nameSuggestions.map((suggestion, idx) => (
                    <div key={idx} className="bg-amber-50 rounded-lg p-3 border border-amber-200">
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-gray-600">{suggestion.original_name}</span>
                        <span className="text-gray-400">to</span>
                        <span className="font-bold text-amber-700">{suggestion.suggested_name}</span>
                      </div>
                      <div className="flex items-center gap-4 text-sm mb-2">
                        <span className="text-gray-500">Number: {suggestion.original_number} to {suggestion.new_number}</span>
                      </div>
                      <p className="text-sm text-gray-600">{suggestion.change_description}</p>
                      <p className="text-sm text-green-600 mt-1">{suggestion.benefit}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Reset Button */}
            <div className="flex justify-center gap-4">
              <button
                onClick={handleReset}
                className="px-6 py-3 bg-gray-500 hover:bg-gray-600 text-white font-semibold rounded-lg transition-colors"
              >
                Naya Vishleshan / New Analysis
              </button>
              <button
                onClick={() => window.print()}
                className="px-6 py-3 bg-purple-500 hover:bg-purple-600 text-white font-semibold rounded-lg transition-colors"
              >
                Print
              </button>
            </div>
          </div>
        )}

        {/* Compatibility Results */}
        {compatibilityResult && activeTab === 'compatibility' && (
          <div ref={resultsRef} className="space-y-6">
            {/* Score Header */}
            <div className="bg-white rounded-xl shadow-lg overflow-hidden">
              <div className={`p-6 text-center text-white ${
                compatibilityResult.compatibility_score >= 70 ? 'bg-gradient-to-r from-green-500 to-emerald-500' :
                compatibilityResult.compatibility_score >= 50 ? 'bg-gradient-to-r from-amber-500 to-orange-500' :
                'bg-gradient-to-r from-red-500 to-rose-500'
              }`}>
                <h2 className="text-2xl font-bold mb-4">Ank Anukoolata / Number Compatibility</h2>
                <div className="inline-block bg-white/20 rounded-full px-8 py-4">
                  <div className="text-5xl font-bold">{compatibilityResult.compatibility_score}%</div>
                  <div className="text-lg mt-1">{compatibilityResult.compatibility_level}</div>
                </div>
              </div>
            </div>

            {/* Person Details */}
            <div className="grid md:grid-cols-2 gap-6">
              <div className="bg-blue-50 rounded-xl p-4 border border-blue-200">
                <h3 className="font-bold text-blue-800 mb-3">{compatibilityResult.person1.name}</h3>
                <div className="flex gap-4">
                  <div>
                    <span className="text-xs text-gray-500">Moolank</span>
                    <NumberBadge number={compatibilityResult.person1.moolank} size="sm" />
                  </div>
                  <div>
                    <span className="text-xs text-gray-500">Bhagyank</span>
                    <NumberBadge number={compatibilityResult.person1.bhagyank} size="sm" />
                  </div>
                </div>
              </div>
              <div className="bg-pink-50 rounded-xl p-4 border border-pink-200">
                <h3 className="font-bold text-pink-800 mb-3">{compatibilityResult.person2.name}</h3>
                <div className="flex gap-4">
                  <div>
                    <span className="text-xs text-gray-500">Moolank</span>
                    <NumberBadge number={compatibilityResult.person2.moolank} size="sm" />
                  </div>
                  <div>
                    <span className="text-xs text-gray-500">Bhagyank</span>
                    <NumberBadge number={compatibilityResult.person2.bhagyank} size="sm" />
                  </div>
                </div>
              </div>
            </div>

            {/* Strengths & Challenges */}
            <div className="grid md:grid-cols-2 gap-6">
              <div className="bg-white rounded-xl shadow-lg overflow-hidden">
                <div className="bg-green-500 text-white p-3">
                  <h3 className="font-bold">Shakti / Strengths</h3>
                </div>
                <ul className="p-4 space-y-2">
                  {compatibilityResult.strengths.map((strength, idx) => (
                    <li key={idx} className="flex items-start gap-2 text-sm">
                      <span className="text-green-500">*</span>
                      <span>{strength}</span>
                    </li>
                  ))}
                </ul>
              </div>
              <div className="bg-white rounded-xl shadow-lg overflow-hidden">
                <div className="bg-orange-500 text-white p-3">
                  <h3 className="font-bold">Chunauti / Challenges</h3>
                </div>
                <ul className="p-4 space-y-2">
                  {compatibilityResult.challenges.map((challenge, idx) => (
                    <li key={idx} className="flex items-start gap-2 text-sm">
                      <span className="text-orange-500">!</span>
                      <span>{challenge}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>

            {/* Remedies */}
            {compatibilityResult.remedies.length > 0 && (
              <div className="bg-white rounded-xl shadow-lg overflow-hidden">
                <div className="bg-purple-500 text-white p-3">
                  <h3 className="font-bold">Upay / Remedies</h3>
                </div>
                <ul className="p-4 space-y-2">
                  {compatibilityResult.remedies.map((remedy, idx) => (
                    <li key={idx} className="flex items-start gap-2 text-sm">
                      <span className="text-purple-500">-</span>
                      <span>{remedy}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            <div className="flex justify-center">
              <button
                onClick={handleReset}
                className="px-6 py-3 bg-gray-500 hover:bg-gray-600 text-white font-semibold rounded-lg transition-colors"
              >
                Naya Milaan / New Comparison
              </button>
            </div>
          </div>
        )}

        {/* Business Analysis Results */}
        {businessResult && activeTab === 'business' && (
          <div ref={resultsRef} className="space-y-6">
            <div className="bg-white rounded-xl shadow-lg overflow-hidden">
              <div className={`p-6 text-center text-white ${
                businessResult.is_compatible && businessResult.is_auspicious ? 'bg-gradient-to-r from-green-500 to-emerald-500' :
                businessResult.is_compatible || businessResult.is_auspicious ? 'bg-gradient-to-r from-amber-500 to-orange-500' :
                'bg-gradient-to-r from-red-500 to-rose-500'
              }`}>
                <h2 className="text-2xl font-bold mb-2">{businessResult.business_name}</h2>
                <div className="text-lg">{businessResult.compatibility_level}</div>
              </div>
              <div className="p-6">
                <div className="grid md:grid-cols-3 gap-4 mb-6">
                  <div className="bg-blue-50 rounded-lg p-3 text-center">
                    <span className="text-xs text-gray-500 block">Namank (Chaldean)</span>
                    <NumberBadge number={businessResult.namank_chaldean} />
                    <p className="text-sm text-gray-600 mt-1">{businessResult.ruling_planet.hindi} ({businessResult.ruling_planet.planet})</p>
                  </div>
                  <div className="bg-green-50 rounded-lg p-3 text-center">
                    <span className="text-xs text-gray-500 block">Owner Moolank</span>
                    <NumberBadge number={businessResult.owner_moolank} />
                  </div>
                  <div className="bg-purple-50 rounded-lg p-3 text-center">
                    <span className="text-xs text-gray-500 block">Owner Bhagyank</span>
                    <NumberBadge number={businessResult.owner_bhagyank} />
                  </div>
                </div>

                <div className="flex gap-4 mb-4">
                  <span className={`px-3 py-1 rounded-full text-sm ${businessResult.is_compatible ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
                    {businessResult.is_compatible ? 'Compatible with Owner' : 'Not Fully Compatible'}
                  </span>
                  <span className={`px-3 py-1 rounded-full text-sm ${businessResult.is_auspicious ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700'}`}>
                    {businessResult.is_auspicious ? 'Auspicious Number' : 'Average Number'}
                  </span>
                </div>

                {businessResult.recommendations.length > 0 && (
                  <div className="bg-amber-50 rounded-lg p-4 border border-amber-200 mb-4">
                    <h4 className="font-semibold text-amber-800 mb-2">Sujhav / Recommendations</h4>
                    <ul className="space-y-1">
                      {businessResult.recommendations.map((rec, idx) => (
                        <li key={idx} className="text-sm text-gray-700">* {rec}</li>
                      ))}
                    </ul>
                  </div>
                )}

                <div className="grid md:grid-cols-2 gap-4">
                  <div className="bg-blue-50 rounded-lg p-3">
                    <h4 className="font-semibold text-blue-800 mb-2">Shubh Din / Lucky Days</h4>
                    <div className="flex flex-wrap gap-1">
                      {businessResult.lucky_days_for_business.map((day, idx) => (
                        <span key={idx} className="px-2 py-0.5 bg-white rounded text-sm">{day}</span>
                      ))}
                    </div>
                  </div>
                  <div className="bg-pink-50 rounded-lg p-3">
                    <h4 className="font-semibold text-pink-800 mb-2">Shubh Rang / Lucky Colors</h4>
                    <div className="flex flex-wrap gap-1">
                      {businessResult.lucky_colors_for_business.map((color, idx) => (
                        <span key={idx} className="px-2 py-0.5 bg-white rounded text-sm">{color}</span>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div className="flex justify-center">
              <button
                onClick={handleReset}
                className="px-6 py-3 bg-gray-500 hover:bg-gray-600 text-white font-semibold rounded-lg transition-colors"
              >
                Naya Vishleshan / New Analysis
              </button>
            </div>
          </div>
        )}

        {/* Info Section */}
        {!result && !compatibilityResult && !businessResult && (
          <div className="mt-6 p-4 bg-white rounded-lg shadow text-center">
            <h3 className="font-semibold text-gray-800 mb-2">Ank Jyotish kya hai? / What is Numerology?</h3>
            <p className="text-sm text-gray-600">
              Ank Jyotish mein har ank ka apna graha aur prabhav hota hai.
              Aapka janam tithi aur naam aapke jeevan path aur vyaktitva ko darshata hai.
              Is paddhati se shubh ank, rang, ratna aur anukool ank jaane ja sakte hain.
            </p>
            <div className="mt-4 grid grid-cols-3 md:grid-cols-9 gap-2">
              {[1, 2, 3, 4, 5, 6, 7, 8, 9].map((num) => (
                <div key={num} className="flex flex-col items-center">
                  <NumberBadge number={num} size="sm" />
                  <span className="text-xs text-gray-500 mt-1">
                    {num === 1 ? 'Surya' : num === 2 ? 'Chandra' : num === 3 ? 'Guru' :
                     num === 4 ? 'Rahu' : num === 5 ? 'Budh' : num === 6 ? 'Shukra' :
                     num === 7 ? 'Ketu' : num === 8 ? 'Shani' : 'Mangal'}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Disclaimer */}
        <div className="mt-6 p-4 bg-gray-100 rounded-lg text-center text-xs text-gray-500">
          <p>Vedic Ank Shastra aur Cheiro ke Numerology par aadharit</p>
          <p className="mt-1">Yah marg darshan ke liye hai. Mahatvpoorn nirnay mein vigyapta ki salah lein.</p>
        </div>
      </div>
    </main>
  );
}
