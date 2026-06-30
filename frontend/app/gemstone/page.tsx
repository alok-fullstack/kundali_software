'use client';

import React, { useState, useRef, useEffect } from 'react';
import Link from 'next/link';
import { CustomDatePicker, CustomTimePicker } from '../components/ui/DateTimePicker';
import { generateKundali, getGemstoneRecommendations } from '@/lib/api';
import { GemstoneResponse, GemstoneRecommendation, StoneToAvoid, GuidelineSection } from '@/lib/types';

const GOOGLE_MAPS_API_KEY = process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY || '';

// Simple response type for session-based analysis (matches backend /api/gemstone/recommend)
interface SimpleGemstoneRec {
  planet: string;
  planet_hindi: string;
  gemstone: string;
  gemstone_hindi: string;
  substitute: string[];
  weight: string;
  metal: string;
  finger: string;
  day_to_wear: string;
  mantra: string;
  benefits: string[];
  benefits_hindi: string[];
  precautions: string[];
  precautions_hindi: string[];
}

interface SimpleGemstoneResponse {
  success: boolean;
  recommendations: {
    primary_gemstones: SimpleGemstoneRec[];
    general_advice: string;
    general_advice_hindi: string;
  };
}

// Simple Results Component for session-based analysis
function SimpleGemstoneResults({ data, onReset }: { data: SimpleGemstoneResponse; onReset: () => void }) {
  const [expanded, setExpanded] = useState<number | null>(0);

  return (
    <div className="space-y-6">
      <div className="text-center">
        <button
          onClick={onReset}
          className="px-4 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600"
        >
          🔄 नई कुंडली / New Analysis
        </button>
      </div>

      {/* General Advice */}
      <div className="p-4 bg-amber-50 border border-amber-200 rounded-xl text-center">
        <p className="text-amber-800 font-medium">{data.recommendations.general_advice_hindi}</p>
        <p className="text-amber-600 text-sm mt-1">{data.recommendations.general_advice}</p>
      </div>

      {/* Gemstone Cards */}
      {data.recommendations.primary_gemstones.map((gem, idx) => (
        <div key={idx} className="bg-white rounded-xl shadow-lg overflow-hidden border-2 border-amber-300">
          <div
            className="p-4 bg-gradient-to-r from-amber-100 to-yellow-100 cursor-pointer"
            onClick={() => setExpanded(expanded === idx ? null : idx)}
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <span className="text-3xl">{PLANET_ICONS[gem.planet] || '💎'}</span>
                <div>
                  <h3 className="font-bold text-lg text-amber-800">{gem.gemstone_hindi}</h3>
                  <p className="text-amber-600">{gem.gemstone} • {gem.planet_hindi} ({gem.planet})</p>
                </div>
              </div>
              <span className="text-2xl">{expanded === idx ? '▲' : '▼'}</span>
            </div>
          </div>

          {expanded === idx && (
            <div className="p-4 space-y-4">
              {/* Wearing Details */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                <div className="p-3 bg-blue-50 rounded-lg text-center">
                  <p className="text-xs text-blue-600">वज़न / Weight</p>
                  <p className="font-semibold text-blue-800">{gem.weight}</p>
                </div>
                <div className="p-3 bg-green-50 rounded-lg text-center">
                  <p className="text-xs text-green-600">धातु / Metal</p>
                  <p className="font-semibold text-green-800">{gem.metal}</p>
                </div>
                <div className="p-3 bg-purple-50 rounded-lg text-center">
                  <p className="text-xs text-purple-600">उंगली / Finger</p>
                  <p className="font-semibold text-purple-800">{gem.finger}</p>
                </div>
                <div className="p-3 bg-orange-50 rounded-lg text-center">
                  <p className="text-xs text-orange-600">दिन / Day</p>
                  <p className="font-semibold text-orange-800">{gem.day_to_wear}</p>
                </div>
              </div>

              {/* Mantra */}
              {gem.mantra && (
                <div className="p-3 bg-yellow-50 rounded-lg">
                  <p className="text-xs text-yellow-600 mb-1">मंत्र / Mantra</p>
                  <p className="font-medium text-yellow-800">{gem.mantra}</p>
                </div>
              )}

              {/* Substitutes */}
              {gem.substitute && gem.substitute.length > 0 && (
                <div className="p-3 bg-indigo-50 rounded-lg">
                  <p className="text-xs text-indigo-600 mb-2">उपरत्न / Substitutes</p>
                  <div className="flex flex-wrap gap-2">
                    {gem.substitute.map((s, i) => (
                      <span key={i} className="px-2 py-1 bg-indigo-100 text-indigo-800 rounded text-sm">{s}</span>
                    ))}
                  </div>
                </div>
              )}

              {/* Benefits */}
              {gem.benefits_hindi && gem.benefits_hindi.length > 0 && (
                <div className="p-3 bg-green-50 rounded-lg">
                  <p className="text-xs text-green-600 mb-2">लाभ / Benefits</p>
                  <ul className="space-y-1">
                    {gem.benefits_hindi.map((b, i) => (
                      <li key={i} className="text-sm text-green-800">✓ {b}</li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Precautions */}
              {gem.precautions_hindi && gem.precautions_hindi.length > 0 && (
                <div className="p-3 bg-red-50 rounded-lg">
                  <p className="text-xs text-red-600 mb-2">सावधानियां / Precautions</p>
                  <ul className="space-y-1">
                    {gem.precautions_hindi.map((p, i) => (
                      <li key={i} className="text-sm text-red-800">⚠️ {p}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}
        </div>
      ))}
    </div>
  );
}

// Navigation component for all analysis pages
const AnalysisNav = () => (
  <div className="mb-6 flex flex-wrap justify-center gap-2">
    <Link href="/" className="px-3 py-1.5 bg-gradient-to-r from-orange-500 to-amber-500 text-white rounded-lg text-sm hover:shadow-lg transition-all">
      🏠 Home
    </Link>
    <Link href="/dosha" className="px-3 py-1.5 bg-gradient-to-r from-red-500 to-rose-500 text-white rounded-lg text-sm hover:shadow-lg transition-all">
      🔮 Dosha
    </Link>
    <Link href="/career" className="px-3 py-1.5 bg-gradient-to-r from-blue-500 to-indigo-500 text-white rounded-lg text-sm hover:shadow-lg transition-all">
      💼 Career
    </Link>
    <Link href="/remedies" className="px-3 py-1.5 bg-gradient-to-r from-green-500 to-teal-500 text-white rounded-lg text-sm hover:shadow-lg transition-all">
      🙏 Remedies
    </Link>
    <Link href="/gemstone" className="px-3 py-1.5 bg-gradient-to-r from-amber-500 to-yellow-500 text-white rounded-lg text-sm hover:shadow-lg transition-all">
      💎 Gemstone
    </Link>
    <Link href="/rashifal" className="px-3 py-1.5 bg-gradient-to-r from-indigo-500 to-purple-500 text-white rounded-lg text-sm hover:shadow-lg transition-all">
      ⭐ Rashifal
    </Link>
    <Link href="/prashna" className="px-3 py-1.5 bg-gradient-to-r from-violet-500 to-purple-500 text-white rounded-lg text-sm hover:shadow-lg transition-all">
      ❓ Prashna
    </Link>
    <Link href="/matching" className="px-3 py-1.5 bg-gradient-to-r from-pink-500 to-red-500 text-white rounded-lg text-sm hover:shadow-lg transition-all">
      💑 Matching
    </Link>
    <Link href="/panchang" className="px-3 py-1.5 bg-gradient-to-r from-orange-500 to-red-500 text-white rounded-lg text-sm hover:shadow-lg transition-all">
      📅 Panchang
    </Link>
    <Link href="/numerology" className="px-3 py-1.5 bg-gradient-to-r from-purple-600 to-violet-600 text-white rounded-lg text-sm hover:shadow-lg transition-all">
      🔢 Numerology
    </Link>
  </div>
);

// Planet to icon mapping
const PLANET_ICONS: Record<string, string> = {
  SUN: '☉',
  MOON: '☽',
  MARS: '♂',
  MERCURY: '☿',
  JUPITER: '♃',
  VENUS: '♀',
  SATURN: '♄',
  RAHU: '☊',
  KETU: '☋',
};

// Gemstone color mapping for UI
const GEMSTONE_COLORS: Record<string, { bg: string; border: string; text: string }> = {
  Ruby: { bg: 'bg-red-50', border: 'border-red-400', text: 'text-red-700' },
  Pearl: { bg: 'bg-blue-50', border: 'border-blue-300', text: 'text-blue-700' },
  'Red Coral': { bg: 'bg-orange-50', border: 'border-orange-400', text: 'text-orange-700' },
  Emerald: { bg: 'bg-green-50', border: 'border-green-500', text: 'text-green-700' },
  'Yellow Sapphire': { bg: 'bg-yellow-50', border: 'border-yellow-500', text: 'text-yellow-700' },
  Diamond: { bg: 'bg-gray-50', border: 'border-gray-400', text: 'text-gray-700' },
  'Blue Sapphire': { bg: 'bg-indigo-50', border: 'border-indigo-500', text: 'text-indigo-700' },
  'Hessonite Garnet': { bg: 'bg-amber-50', border: 'border-amber-600', text: 'text-amber-700' },
  "Cat's Eye": { bg: 'bg-lime-50', border: 'border-lime-600', text: 'text-lime-700' },
};

function getGemstoneColor(gemName: string) {
  return GEMSTONE_COLORS[gemName] || { bg: 'bg-purple-50', border: 'border-purple-400', text: 'text-purple-700' };
}

// Expandable Gemstone Card Component
function GemstoneCard({
  recommendation,
  isExpanded,
  onToggle,
}: {
  recommendation: GemstoneRecommendation;
  isExpanded: boolean;
  onToggle: () => void;
}) {
  const colors = getGemstoneColor(recommendation.gemstone.name_english);
  const isPrimary = recommendation.priority === 1;

  return (
    <div className={`rounded-xl border-2 overflow-hidden transition-all duration-300 shadow-md hover:shadow-lg ${colors.border} ${colors.bg}`}>
      {/* Header - Always visible */}
      <div
        onClick={onToggle}
        className="p-4 cursor-pointer hover:bg-opacity-80 transition-colors"
      >
        <div className="flex items-start justify-between">
          <div className="flex items-start gap-4">
            {/* Gemstone Icon */}
            <div className={`w-16 h-16 rounded-full flex items-center justify-center text-3xl ${colors.text} bg-white shadow-inner border-2 ${colors.border}`}>
              {PLANET_ICONS[recommendation.planet] || '💎'}
            </div>

            <div>
              {/* Gemstone Name */}
              <h3 className={`text-xl font-bold ${colors.text}`}>
                {recommendation.gemstone.name_hindi}
              </h3>
              <p className="text-sm text-gray-600">
                {recommendation.gemstone.name_english} ({recommendation.gemstone.name_sanskrit})
              </p>

              {/* Planet */}
              <div className="mt-2 flex items-center gap-2">
                <span className="text-sm font-medium text-gray-700">
                  {recommendation.planet_hindi} ({recommendation.planet})
                </span>
                {recommendation.current_dasha_relevant && (
                  <span className="px-2 py-0.5 bg-green-100 text-green-700 text-xs rounded-full border border-green-300">
                    Dasha Relevant
                  </span>
                )}
              </div>
            </div>
          </div>

          <div className="flex flex-col items-end gap-2">
            {/* Priority Badge */}
            <span className={`px-3 py-1 rounded-full text-sm font-medium ${
              isPrimary
                ? 'bg-green-100 text-green-800 border border-green-300'
                : 'bg-blue-100 text-blue-800 border border-blue-300'
            }`}>
              {recommendation.priority_label_hindi}
            </span>

            {/* Expand Icon */}
            <div className={`transform transition-transform duration-300 ${isExpanded ? 'rotate-180' : ''}`}>
              <svg className="w-6 h-6 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
              </svg>
            </div>
          </div>
        </div>

        {/* Reason */}
        <div className="mt-3 p-2 bg-white/50 rounded-lg">
          <p className="text-sm text-gray-700">{recommendation.reason_hindi}</p>
        </div>
      </div>

      {/* Expanded Content */}
      <div className={`overflow-hidden transition-all duration-300 ease-in-out ${
        isExpanded ? 'max-h-[2000px] opacity-100' : 'max-h-0 opacity-0'
      }`}>
        <div className="p-4 bg-white border-t border-gray-200">
          {/* Quick Info Grid */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-4">
            <div className="bg-gray-50 rounded-lg p-3 text-center">
              <div className="text-xs text-gray-500">रंग / Color</div>
              <div className="font-semibold text-gray-800 text-sm">{recommendation.gemstone.color}</div>
            </div>
            <div className="bg-gray-50 rounded-lg p-3 text-center">
              <div className="text-xs text-gray-500">उंगली / Finger</div>
              <div className="font-semibold text-gray-800 text-sm">{recommendation.gemstone.finger_hindi}</div>
            </div>
            <div className="bg-gray-50 rounded-lg p-3 text-center">
              <div className="text-xs text-gray-500">धातु / Metal</div>
              <div className="font-semibold text-gray-800 text-sm">{recommendation.gemstone.metal_hindi}</div>
            </div>
            <div className="bg-gray-50 rounded-lg p-3 text-center">
              <div className="text-xs text-gray-500">वजन / Weight</div>
              <div className="font-semibold text-gray-800 text-sm">
                {recommendation.gemstone.minimum_weight_ratti} रत्ती ({recommendation.gemstone.minimum_weight_carat} ct)
              </div>
            </div>
          </div>

          {/* Wearing Details */}
          <div className="grid md:grid-cols-2 gap-4 mb-4">
            <div className={`p-3 rounded-lg border ${colors.border} ${colors.bg}`}>
              <h4 className="font-semibold text-gray-800 mb-2 flex items-center gap-2">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                धारण दिवस / Wearing Day
              </h4>
              <p className="text-gray-700">{recommendation.gemstone.day_hindi}</p>
              <p className="text-sm text-gray-500">{recommendation.gemstone.day}</p>
            </div>
            <div className={`p-3 rounded-lg border ${colors.border} ${colors.bg}`}>
              <h4 className="font-semibold text-gray-800 mb-2 flex items-center gap-2">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                धारण समय / Wearing Time
              </h4>
              <p className="text-gray-700">{recommendation.gemstone.time_hindi}</p>
              <p className="text-sm text-gray-500">{recommendation.gemstone.time}</p>
            </div>
          </div>

          {/* Mantra Section */}
          <div className="p-4 bg-orange-50 rounded-lg border border-orange-200 mb-4">
            <h4 className="font-semibold text-orange-800 mb-2 flex items-center gap-2">
              <span className="text-lg">🙏</span>
              धारण मंत्र / Wearing Mantra
            </h4>
            <p className="text-lg font-medium text-orange-900 font-mono bg-white/50 p-3 rounded">
              {recommendation.gemstone.mantra}
            </p>
            <p className="text-sm text-orange-700 mt-2">
              जाप संख्या / Chant Count: <span className="font-bold">{recommendation.gemstone.mantra_count.toLocaleString()}</span> बार
            </p>
          </div>

          {/* Benefits */}
          <div className="mb-4">
            <h4 className="font-semibold text-green-800 mb-2 flex items-center gap-2">
              <svg className="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              लाभ / Benefits
            </h4>
            <ul className="space-y-2">
              {recommendation.gemstone.benefits.map((benefit, idx) => (
                <li key={idx} className="flex items-start gap-2 text-sm">
                  <span className="text-green-500 mt-0.5">+</span>
                  <span className="text-gray-700">{benefit}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Alternative Stones */}
          <div className="mb-4">
            <h4 className="font-semibold text-purple-800 mb-2 flex items-center gap-2">
              <svg className="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" />
              </svg>
              उपरत्न / Alternative Stones (Upratna)
            </h4>
            <div className="flex flex-wrap gap-2">
              {recommendation.gemstone.alternative_stones.map((stone, idx) => (
                <span key={idx} className="px-3 py-1 bg-purple-100 text-purple-800 text-sm rounded-full border border-purple-200">
                  {stone}
                </span>
              ))}
            </div>
          </div>

          {/* Favorable Nakshatras */}
          <div className="mb-4">
            <h4 className="font-semibold text-blue-800 mb-2 flex items-center gap-2">
              <span>*</span>
              शुभ नक्षत्र / Favorable Nakshatras
            </h4>
            <div className="flex flex-wrap gap-2">
              {recommendation.gemstone.nakshatra.map((nak, idx) => (
                <span key={idx} className="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full border border-blue-200">
                  {nak}
                </span>
              ))}
            </div>
          </div>

          {/* Precautions */}
          <div className="p-4 bg-red-50 rounded-lg border border-red-200 mb-4">
            <h4 className="font-semibold text-red-800 mb-2 flex items-center gap-2">
              <svg className="w-5 h-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
              सावधानियां / Precautions
            </h4>
            <ul className="space-y-2">
              {recommendation.gemstone.precautions.map((precaution, idx) => (
                <li key={idx} className="flex items-start gap-2 text-sm">
                  <span className="text-red-500 mt-0.5">!</span>
                  <span className="text-red-700">{precaution}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Special Instructions */}
          {recommendation.special_instructions.length > 0 && (
            <div className="p-3 bg-yellow-50 rounded-lg border border-yellow-200">
              <h4 className="font-semibold text-yellow-800 mb-2 text-sm">विशेष निर्देश / Special Instructions</h4>
              <ul className="space-y-1">
                {recommendation.special_instructions.map((inst, idx) => (
                  <li key={idx} className="text-sm text-yellow-700">* {inst}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// Stones to Avoid Section
function StonesToAvoidSection({ stones }: { stones: StoneToAvoid[] }) {
  if (stones.length === 0) return null;

  return (
    <div className="bg-white rounded-xl shadow-lg overflow-hidden mb-6">
      <div className="p-4 bg-red-100 border-b border-red-200">
        <h3 className="font-bold text-lg text-red-800 flex items-center gap-2">
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636" />
          </svg>
          वर्जित रत्न / Stones to Avoid
        </h3>
        <p className="text-sm text-red-600 mt-1">
          आपके लग्न के अनुसार ये रत्न हानिकारक हो सकते हैं
        </p>
      </div>
      <div className="p-4">
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-3">
          {stones.map((stone, idx) => (
            <div key={idx} className="p-3 bg-red-50 rounded-lg border border-red-200 flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-red-100 flex items-center justify-center text-red-600 text-lg">
                {PLANET_ICONS[stone.planet] || 'X'}
              </div>
              <div>
                <div className="font-semibold text-red-800">{stone.gemstone_hindi}</div>
                <div className="text-xs text-red-600">{stone.planet_hindi} - {stone.gemstone_english}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

// Guidelines Section
function GuidelinesSection({ guidelines }: { guidelines: GuidelineSection[] }) {
  return (
    <div className="bg-white rounded-xl shadow-lg overflow-hidden mb-6">
      <div className="p-4 bg-purple-100 border-b border-purple-200">
        <h3 className="font-bold text-lg text-purple-800 flex items-center gap-2">
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          रत्न धारण विधि / Gemstone Wearing Guidelines
        </h3>
      </div>
      <div className="p-4">
        <div className="grid md:grid-cols-2 gap-4">
          {guidelines.map((section, idx) => (
            <div key={idx} className="p-4 bg-purple-50 rounded-lg border border-purple-200">
              <h4 className="font-semibold text-purple-800 mb-3">{section.title}</h4>
              <ul className="space-y-2">
                {section.guidelines.map((guideline, gIdx) => (
                  <li key={gIdx} className="flex items-start gap-2 text-sm">
                    <span className="text-purple-500 mt-0.5">*</span>
                    <span className="text-gray-700">{guideline}</span>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

interface FormData {
  name: string;
  birthDate: Date | null;
  birthTime: { hour: number; minute: number } | null;
  city: string;
  latitude: number | null;
  longitude: number | null;
}

const initialFormData: FormData = {
  name: '',
  birthDate: null,
  birthTime: null,
  city: '',
  latitude: null,
  longitude: null,
};

export default function GemstonePage() {
  const [formData, setFormData] = useState<FormData>(initialFormData);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<GemstoneResponse | null>(null);
  const [simpleResult, setSimpleResult] = useState<SimpleGemstoneResponse | null>(null);
  const [googleLoaded, setGoogleLoaded] = useState(false);
  const [expandedIndex, setExpandedIndex] = useState<number | null>(0);
  const [hasSessionKundali, setHasSessionKundali] = useState(false);
  const [sessionKundaliName, setSessionKundaliName] = useState<string>('');

  const cityInputRef = useRef<HTMLInputElement>(null);
  const autocompleteRef = useRef<google.maps.places.Autocomplete | null>(null);
  const resultsRef = useRef<HTMLDivElement>(null);

  // Check for session kundali on mount
  useEffect(() => {
    const currentKundali = sessionStorage.getItem('current_kundali');
    if (currentKundali) {
      const parsed = JSON.parse(currentKundali);
      setHasSessionKundali(true);
      setSessionKundaliName(parsed.name || 'Current Kundali');
    }
  }, []);

  // Load Google Maps
  useEffect(() => {
    if (typeof window !== 'undefined' && !window.google && GOOGLE_MAPS_API_KEY) {
      const script = document.createElement('script');
      script.src = `https://maps.googleapis.com/maps/api/js?key=${GOOGLE_MAPS_API_KEY}&libraries=places`;
      script.async = true;
      script.defer = true;
      script.onload = () => setGoogleLoaded(true);
      document.head.appendChild(script);
    } else if (window.google) {
      setGoogleLoaded(true);
    }
  }, []);

  // Initialize autocomplete
  useEffect(() => {
    if (googleLoaded && cityInputRef.current && !autocompleteRef.current) {
      autocompleteRef.current = new google.maps.places.Autocomplete(cityInputRef.current, {
        types: ['(cities)'],
        fields: ['formatted_address', 'geometry', 'name'],
      });

      autocompleteRef.current.addListener('place_changed', () => {
        const place = autocompleteRef.current?.getPlace();
        if (place?.geometry?.location) {
          setFormData((prev) => ({
            ...prev,
            city: place.name || place.formatted_address || '',
            latitude: place.geometry!.location!.lat(),
            longitude: place.geometry!.location!.lng(),
          }));
        }
      });
    }
  }, [googleLoaded]);

  const validateForm = (): boolean => {
    if (!formData.name.trim()) {
      setError('कृपया नाम दर्ज करें / Please enter name');
      return false;
    }
    if (!formData.birthDate) {
      setError('कृपया जन्म तिथि चुनें / Please select birth date');
      return false;
    }
    if (!formData.birthTime) {
      setError('कृपया जन्म समय चुनें / Please select birth time');
      return false;
    }
    if (!formData.city.trim()) {
      setError('कृपया जन्म स्थान दर्ज करें / Please enter birth place');
      return false;
    }
    return true;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) return;

    setIsLoading(true);
    setError(null);

    try {
      // First generate the kundali
      const bd = formData.birthDate!;
      const year = bd.getFullYear();
      const month = (bd.getMonth() + 1).toString().padStart(2, '0');
      const day = bd.getDate().toString().padStart(2, '0');

      const kundaliResponse = await generateKundali({
        name: formData.name,
        dob: `${year}-${month}-${day}`,
        tob: `${formData.birthTime!.hour.toString().padStart(2, '0')}:${formData.birthTime!.minute.toString().padStart(2, '0')}`,
        city: formData.city,
        latitude: formData.latitude,
        longitude: formData.longitude,
      });

      if (!kundaliResponse.success || !kundaliResponse.kundali_id) {
        throw new Error(kundaliResponse.error || 'Failed to generate kundali');
      }

      // Then get gemstone recommendations
      const gemstoneResponse = await getGemstoneRecommendations(kundaliResponse.kundali_id);

      if (gemstoneResponse.success) {
        setResult(gemstoneResponse);
        setTimeout(() => {
          resultsRef.current?.scrollIntoView({ behavior: 'smooth' });
        }, 100);
      } else {
        setError(gemstoneResponse.error || 'Failed to get gemstone recommendations');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setFormData(initialFormData);
    setResult(null);
    setError(null);
    setExpandedIndex(0);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  // Analyze using session kundali (same as other pages)
  const handleAnalyzeFromSession = async () => {
    const currentKundali = sessionStorage.getItem('current_kundali');
    if (!currentKundali) {
      setError('कोई कुंडली नहीं मिली। पहले होम पेज पर कुंडली बनाएं।');
      return;
    }

    const kundaliParams = JSON.parse(currentKundali);
    setIsLoading(true);
    setError(null);

    try {
      // First generate kundali to get kundali_id
      const kundaliResponse = await generateKundali({
        name: kundaliParams.name,
        dob: kundaliParams.dob,
        tob: kundaliParams.tob,
        city: kundaliParams.city,
        latitude: kundaliParams.latitude,
        longitude: kundaliParams.longitude,
      });

      if (!kundaliResponse.success || !kundaliResponse.kundali_id) {
        throw new Error('Failed to generate kundali');
      }

      // Get gemstone recommendations using kundali_id
      const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000/api';
      const response = await fetch(`${API_BASE}/gemstone/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ kundali_id: kundaliResponse.kundali_id }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Failed to get gemstone recommendations');
      }

      const gemstoneResponse = await response.json();

      if (gemstoneResponse.success) {
        setSimpleResult(gemstoneResponse);
        setTimeout(() => {
          resultsRef.current?.scrollIntoView({ behavior: 'smooth' });
        }, 100);
      } else {
        setError(gemstoneResponse.error || 'Failed to get gemstone recommendations');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSimpleReset = () => {
    setSimpleResult(null);
    setError(null);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleToggleCard = (index: number) => {
    setExpandedIndex(expandedIndex === index ? null : index);
  };

  return (
    <main className="min-h-screen py-5 px-4 bg-gradient-to-br from-purple-50 via-orange-50 to-yellow-50">
      <div className="max-w-7xl mx-auto">
        <AnalysisNav />

        {/* Header */}
        <div className="text-center mb-6">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">
            <span className="text-purple-600">💎 रत्न परामर्श / Gemstone Recommendations</span>
          </h1>
          <p className="text-gray-600">वैदिक ज्योतिष के अनुसार अनुशंसित रत्न</p>
          <p className="text-sm text-gray-500 mt-1">गरुड़ पुराण, बृहत संहिता और मणिमाला के आधार पर</p>
        </div>

        {/* Quick Analyze from Session */}
        {!result && !simpleResult && hasSessionKundali && (
          <div className="bg-gradient-to-r from-amber-50 to-yellow-50 border border-amber-200 rounded-xl p-4 mb-6 text-center">
            <p className="text-amber-800 mb-3">
              <strong>{sessionKundaliName}</strong> की कुंडली उपलब्ध है
            </p>
            <button
              onClick={handleAnalyzeFromSession}
              disabled={isLoading}
              className="px-6 py-2 bg-gradient-to-r from-amber-500 to-yellow-500 text-white font-semibold rounded-lg hover:from-amber-600 hover:to-yellow-600 disabled:opacity-50"
            >
              {isLoading ? 'विश्लेषण हो रहा है...' : '💎 रत्न परामर्श देखें'}
            </button>
            <p className="text-sm text-amber-600 mt-2">या नीचे नई जानकारी भरें</p>
          </div>
        )}

        {/* Form Section */}
        {!result && !simpleResult && (
          <div className="bg-white rounded-xl shadow-lg mb-6">
            <div className="bg-gradient-to-r from-purple-500 to-indigo-500 text-white p-4">
              <div className="flex items-center gap-2">
                <span className="text-2xl">💎</span>
                <div>
                  <h2 className="font-bold">जन्म विवरण / Birth Details</h2>
                  <p className="text-sm text-white/80">रत्न सुझाव के लिए अपना विवरण दर्ज करें</p>
                </div>
              </div>
            </div>

            <form onSubmit={handleSubmit} className="p-6">
              {error && (
                <div className="mb-4 p-3 bg-red-50 border-l-4 border-red-500 rounded-r-lg text-red-700 flex items-center gap-2">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                  </svg>
                  <span>{error}</span>
                </div>
              )}

              <div className="grid md:grid-cols-2 gap-4 mb-6">
                {/* Name */}
                <div>
                  <label className="block mb-1.5 font-medium text-gray-700 text-sm">
                    <span className="text-purple-600">नाम</span>
                    <span className="text-gray-400 text-xs ml-1">/ Name *</span>
                  </label>
                  <input
                    type="text"
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    placeholder="अपना नाम लिखें..."
                    className="w-full px-3 py-2.5 border border-gray-200 rounded-lg focus:border-purple-500 focus:ring-1 focus:ring-purple-200 transition-all text-sm"
                    required
                  />
                </div>

                {/* City */}
                <div>
                  <label className="block mb-1.5 font-medium text-gray-700 text-sm">
                    <span className="text-purple-600">जन्म स्थान</span>
                    <span className="text-gray-400 text-xs ml-1">/ Birth Place *</span>
                  </label>
                  <input
                    ref={cityInputRef}
                    type="text"
                    value={formData.city}
                    onChange={(e) => setFormData({ ...formData, city: e.target.value })}
                    placeholder={googleLoaded ? "शहर का नाम टाइप करें..." : "Delhi, Mumbai..."}
                    className="w-full px-3 py-2.5 border border-gray-200 rounded-lg focus:border-purple-500 focus:ring-1 focus:ring-purple-200 transition-all text-sm"
                    required
                  />
                  {formData.latitude && formData.longitude && (
                    <p className="mt-1 text-xs text-green-600 bg-green-50 px-2 py-1 rounded w-fit">
                      {formData.latitude.toFixed(4)}N, {formData.longitude.toFixed(4)}E
                    </p>
                  )}
                </div>

                {/* Date */}
                <div>
                  <label className="block mb-1.5 font-medium text-gray-700 text-sm">
                    <span className="text-purple-600">जन्म तिथि</span>
                    <span className="text-gray-400 text-xs ml-1">/ Date of Birth *</span>
                  </label>
                  <CustomDatePicker
                    value={formData.birthDate}
                    onChange={(date) => setFormData({ ...formData, birthDate: date })}
                    placeholder="तारीख चुनें / Select date..."
                    minYear={1900}
                    maxYear={new Date().getFullYear()}
                  />
                </div>

                {/* Time */}
                <div>
                  <label className="block mb-1.5 font-medium text-gray-700 text-sm">
                    <span className="text-purple-600">जन्म समय</span>
                    <span className="text-gray-400 text-xs ml-1">/ Time of Birth *</span>
                  </label>
                  <CustomTimePicker
                    value={formData.birthTime}
                    onChange={(time) => setFormData({ ...formData, birthTime: time })}
                    placeholder="समय चुनें / Select time..."
                  />
                </div>
              </div>

              <div className="flex justify-center gap-4">
                <button
                  type="submit"
                  disabled={isLoading}
                  className="px-8 py-3 bg-gradient-to-r from-purple-500 to-indigo-600 hover:from-purple-600 hover:to-indigo-700 text-white font-semibold rounded-lg shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
                >
                  {isLoading ? (
                    <>
                      <svg className="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                      <span>गणना हो रही है...</span>
                    </>
                  ) : (
                    <>
                      <span>💎</span>
                      <span>रत्न सुझाव देखें / Get Recommendations</span>
                    </>
                  )}
                </button>
              </div>
            </form>

            {/* Info Box */}
            <div className="m-6 mt-0 p-4 bg-purple-50 rounded-lg border border-purple-200">
              <h3 className="font-semibold text-purple-800 mb-2">रत्न परामर्श क्या है? / What is Gemstone Consultation?</h3>
              <p className="text-sm text-gray-600">
                वैदिक ज्योतिष में नवग्रहों के लिए विशेष रत्न निर्धारित हैं। आपकी कुंडली के अनुसार शुभ ग्रहों के
                रत्न धारण करने से जीवन में सकारात्मक परिवर्तन आता है। हम गरुड़ पुराण, बृहत संहिता और
                मणिमाला जैसे प्राचीन ग्रंथों के आधार पर रत्न सुझाव देते हैं।
              </p>
              <div className="mt-3 flex flex-wrap gap-2 text-xs">
                <span className="px-2 py-1 bg-red-100 text-red-700 rounded">माणिक्य - Sun</span>
                <span className="px-2 py-1 bg-blue-100 text-blue-700 rounded">मोती - Moon</span>
                <span className="px-2 py-1 bg-orange-100 text-orange-700 rounded">मूंगा - Mars</span>
                <span className="px-2 py-1 bg-green-100 text-green-700 rounded">पन्ना - Mercury</span>
                <span className="px-2 py-1 bg-yellow-100 text-yellow-700 rounded">पुखराज - Jupiter</span>
                <span className="px-2 py-1 bg-gray-100 text-gray-700 rounded">हीरा - Venus</span>
                <span className="px-2 py-1 bg-indigo-100 text-indigo-700 rounded">नीलम - Saturn</span>
                <span className="px-2 py-1 bg-amber-100 text-amber-700 rounded">गोमेद - Rahu</span>
                <span className="px-2 py-1 bg-lime-100 text-lime-700 rounded">लहसुनिया - Ketu</span>
              </div>
            </div>
          </div>
        )}

        {/* Simple Results Section (from session kundali) */}
        {simpleResult && (
          <div ref={resultsRef} className="mb-8">
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h2 className="text-2xl font-bold mb-6 text-center text-purple-800">
                💎 रत्न परामर्श / Gemstone Recommendations
              </h2>
              <SimpleGemstoneResults data={simpleResult} onReset={handleSimpleReset} />
            </div>
          </div>
        )}

        {/* Results Section (from form) */}
        {result && !simpleResult && (
          <div ref={resultsRef}>
            {/* Summary Card */}
            <div className="bg-white rounded-xl shadow-lg overflow-hidden mb-6">
              <div className="p-6 bg-gradient-to-r from-purple-500 to-indigo-600 text-white">
                <h2 className="text-2xl font-bold mb-4 text-center">रत्न परामर्श / Gemstone Recommendations</h2>

                <div className="grid md:grid-cols-3 gap-4">
                  {/* Lagna Info */}
                  <div className="bg-white/20 rounded-lg p-4 text-center">
                    <div className="text-sm text-white/80">लग्न / Ascendant</div>
                    <div className="text-xl font-bold">{result.lagna.rashi}</div>
                    <div className="text-sm">{result.lagna.rashi_english}</div>
                    <div className="text-xs text-white/70 mt-1">Lord: {result.lagna.lord}</div>
                  </div>

                  {/* Moon Sign */}
                  <div className="bg-white/20 rounded-lg p-4 text-center">
                    <div className="text-sm text-white/80">चंद्र राशि / Moon Sign</div>
                    <div className="text-xl font-bold">{result.moon_sign.rashi}</div>
                    <div className="text-xs text-white/70 mt-1">Lord: {result.moon_sign.lord}</div>
                  </div>

                  {/* Current Dasha */}
                  <div className="bg-white/20 rounded-lg p-4 text-center">
                    <div className="text-sm text-white/80">वर्तमान दशा / Current Dasha</div>
                    <div className="text-xl font-bold">{result.current_dasha.full_dasha}</div>
                    <div className="text-xs text-white/70 mt-1">Mahadasha: {result.current_dasha.mahadasha}</div>
                  </div>
                </div>

                {result.yogakaraka && (
                  <div className="mt-4 text-center">
                    <span className="px-4 py-2 bg-yellow-400 text-yellow-900 rounded-full text-sm font-medium">
                      योगकारक / Yogakaraka: {result.yogakaraka}
                    </span>
                  </div>
                )}
              </div>
            </div>

            {/* Primary Recommendations */}
            {result.primary_recommendations.length > 0 && (
              <div className="mb-6">
                <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                  <span className="w-8 h-8 bg-green-500 text-white rounded-full flex items-center justify-center text-sm">1</span>
                  प्राथमिक अनुशंसा / Primary Recommendations
                </h3>
                <div className="space-y-4">
                  {result.primary_recommendations.map((rec, idx) => (
                    <GemstoneCard
                      key={idx}
                      recommendation={rec}
                      isExpanded={expandedIndex === idx}
                      onToggle={() => handleToggleCard(idx)}
                    />
                  ))}
                </div>
              </div>
            )}

            {/* Secondary Recommendations */}
            {result.secondary_recommendations.length > 0 && (
              <div className="mb-6">
                <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                  <span className="w-8 h-8 bg-blue-500 text-white rounded-full flex items-center justify-center text-sm">2</span>
                  द्वितीयक अनुशंसा / Secondary Recommendations
                </h3>
                <div className="space-y-4">
                  {result.secondary_recommendations.map((rec, idx) => (
                    <GemstoneCard
                      key={idx}
                      recommendation={rec}
                      isExpanded={expandedIndex === result.primary_recommendations.length + idx}
                      onToggle={() => handleToggleCard(result.primary_recommendations.length + idx)}
                    />
                  ))}
                </div>
              </div>
            )}

            {/* Stones to Avoid */}
            <StonesToAvoidSection stones={result.stones_to_avoid} />

            {/* Guidelines */}
            <GuidelinesSection guidelines={result.general_guidelines} />

            {/* Disclaimer */}
            <div className="bg-yellow-50 border border-yellow-200 rounded-xl p-4 mb-6">
              <h4 className="font-semibold text-yellow-800 mb-2 flex items-center gap-2">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                अस्वीकरण / Disclaimer
              </h4>
              <p className="text-sm text-yellow-700">{result.disclaimer.hindi}</p>
              <p className="text-xs text-yellow-600 mt-2">{result.disclaimer.english}</p>
            </div>

            {/* Actions */}
            <div className="flex justify-center gap-4 mb-6">
              <button
                onClick={handleReset}
                className="px-6 py-3 bg-gray-500 hover:bg-gray-600 text-white font-semibold rounded-lg transition-colors flex items-center gap-2"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                नया परामर्श / New Consultation
              </button>
              <button
                onClick={() => window.print()}
                className="px-6 py-3 bg-blue-500 hover:bg-blue-600 text-white font-semibold rounded-lg transition-colors flex items-center gap-2"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" />
                </svg>
                प्रिंट करें / Print
              </button>
            </div>

            {/* Footer */}
            <div className="text-center text-xs text-gray-500 pb-4">
              <p>गरुड़ पुराण (रत्न परीक्षा अध्याय), बृहत संहिता (वराहमिहिर), जातक पारिजात और मणिमाला पर आधारित</p>
              <p className="mt-1">Based on Garuda Purana, Brihat Samhita by Varahamihira, Jataka Parijata, and Mani Mala</p>
            </div>
          </div>
        )}
      </div>
    </main>
  );
}
