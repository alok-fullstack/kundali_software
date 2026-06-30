'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { getKundaliDataForAnalysis } from '@/lib/api';

// Navigation component for all analysis pages
const AnalysisNav = () => (
  <div className="mb-6 flex flex-wrap justify-center gap-2">
    <Link href="/" className="px-3 py-1.5 bg-gradient-to-r from-orange-500 to-amber-500 text-white rounded-lg text-sm hover:shadow-lg transition-all">
      🏠 होम / Home
    </Link>
    <Link href="/dosha" className="px-3 py-1.5 bg-gradient-to-r from-red-500 to-rose-500 text-white rounded-lg text-sm hover:shadow-lg transition-all">
      🔮 दोष / Dosha
    </Link>
    <Link href="/career" className="px-3 py-1.5 bg-gradient-to-r from-blue-500 to-indigo-500 text-white rounded-lg text-sm hover:shadow-lg transition-all">
      💼 करियर / Career
    </Link>
    <Link href="/remedies" className="px-3 py-1.5 bg-gradient-to-r from-green-500 to-teal-500 text-white rounded-lg text-sm hover:shadow-lg transition-all">
      🙏 उपाय / Remedies
    </Link>
    <Link href="/gemstone" className="px-3 py-1.5 bg-gradient-to-r from-amber-500 to-yellow-500 text-white rounded-lg text-sm hover:shadow-lg transition-all">
      💎 रत्न / Gemstone
    </Link>
    <Link href="/rashifal" className="px-3 py-1.5 bg-gradient-to-r from-indigo-500 to-purple-500 text-white rounded-lg text-sm hover:shadow-lg transition-all">
      ⭐ राशिफल / Rashifal
    </Link>
    <Link href="/prashna" className="px-3 py-1.5 bg-gradient-to-r from-violet-500 to-purple-500 text-white rounded-lg text-sm hover:shadow-lg transition-all">
      ❓ प्रश्न / Prashna
    </Link>
    <Link href="/matching" className="px-3 py-1.5 bg-gradient-to-r from-pink-500 to-red-500 text-white rounded-lg text-sm hover:shadow-lg transition-all">
      💑 मिलान / Matching
    </Link>
    <Link href="/panchang" className="px-3 py-1.5 bg-gradient-to-r from-orange-500 to-red-500 text-white rounded-lg text-sm hover:shadow-lg transition-all">
      📅 पंचांग / Panchang
    </Link>
    <Link href="/numerology" className="px-3 py-1.5 bg-gradient-to-r from-purple-600 to-violet-600 text-white rounded-lg text-sm hover:shadow-lg transition-all">
      🔢 अंक / Numerology
    </Link>
  </div>
);

interface DoshaResult {
  is_present: boolean;
  severity?: string;
  type?: string;
  type_hindi?: string;
  effects?: string[];
  remedies?: string[];
  causes?: string[];
  phase?: string;
  phase_hindi?: string;
  mars_house?: number;
  cancellation?: string[];
}

interface DoshaAnalysis {
  kaal_sarp: DoshaResult | null;
  pitra_dosha: DoshaResult | null;
  sade_sati: DoshaResult | null;
  guru_chandal: DoshaResult | null;
  grahan_dosha: DoshaResult | null;
  manglik: DoshaResult | null;
  summary: string;
  summary_hindi: string;
  total_doshas: number;
  severity_score: number;
}

export default function DoshaPage() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<DoshaAnalysis | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [expandedDosha, setExpandedDosha] = useState<string | null>(null);

  const analyzeDoshas = async () => {
    setLoading(true);
    setError(null);

    // Get current kundali from sessionStorage
    const currentKundali = sessionStorage.getItem('current_kundali');
    if (!currentKundali) {
      setError('कोई कुंडली नहीं मिली। पहले होम पेज पर कुंडली बनाएं।');
      setLoading(false);
      return;
    }

    const kundaliParams = JSON.parse(currentKundali);

    try {
      // Regenerate kundali and get analysis data
      const kundaliData = await getKundaliDataForAnalysis({
        name: kundaliParams.name,
        dob: kundaliParams.dob,
        tob: kundaliParams.tob,
        city: kundaliParams.city,
        latitude: kundaliParams.latitude,
        longitude: kundaliParams.longitude,
      });

      // Analyze doshas
      const response = await fetch('http://localhost:8000/api/dosha/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ kundali_data: kundaliData }),
      });

      if (!response.ok) throw new Error('Failed to analyze doshas');

      const data = await response.json();
      if (data.success) {
        setResult(data.dosha_analysis);
      } else {
        setError(data.error || 'Analysis failed');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const getSeverityColor = (severity?: string) => {
    switch (severity?.toLowerCase()) {
      case 'severe': return 'text-red-600 bg-red-50';
      case 'moderate': return 'text-yellow-600 bg-yellow-50';
      case 'mild': return 'text-green-600 bg-green-50';
      default: return 'text-gray-600 bg-gray-50';
    }
  };

  const DoshaCard = ({
    title,
    titleHindi,
    dosha,
    icon,
    id
  }: {
    title: string;
    titleHindi: string;
    dosha: DoshaResult | null;
    icon: string;
    id: string;
  }) => {
    const isExpanded = expandedDosha === id;

    if (!dosha) return null;

    return (
      <div className={`rounded-xl border-2 transition-all ${
        dosha.is_present
          ? 'border-red-200 bg-red-50/50'
          : 'border-green-200 bg-green-50/50'
      }`}>
        <div
          className="p-4 cursor-pointer"
          onClick={() => setExpandedDosha(isExpanded ? null : id)}
        >
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <span className="text-2xl">{icon}</span>
              <div>
                <h3 className="font-bold text-gray-800">{titleHindi}</h3>
                <p className="text-sm text-gray-500">{title}</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                dosha.is_present
                  ? 'bg-red-100 text-red-700'
                  : 'bg-green-100 text-green-700'
              }`}>
                {dosha.is_present ? 'उपस्थित / Present' : 'अनुपस्थित / Absent'}
              </span>
              <svg
                className={`w-5 h-5 transition-transform ${isExpanded ? 'rotate-180' : ''}`}
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
              </svg>
            </div>
          </div>

          {dosha.is_present && dosha.severity && (
            <div className={`mt-2 inline-block px-2 py-1 rounded text-xs font-medium ${getSeverityColor(dosha.severity)}`}>
              गंभीरता / Severity: {dosha.severity}
            </div>
          )}
        </div>

        {isExpanded && dosha.is_present && (
          <div className="border-t border-gray-200 p-4 space-y-4">
            {dosha.type_hindi && (
              <div>
                <h4 className="font-semibold text-gray-700 mb-1">प्रकार / Type</h4>
                <p className="text-gray-600">{dosha.type_hindi}</p>
              </div>
            )}

            {dosha.phase_hindi && (
              <div>
                <h4 className="font-semibold text-gray-700 mb-1">वर्तमान चरण / Current Phase</h4>
                <p className="text-gray-600">{dosha.phase_hindi}</p>
              </div>
            )}

            {dosha.mars_house && (
              <div>
                <h4 className="font-semibold text-gray-700 mb-1">मंगल का भाव / Mars House</h4>
                <p className="text-gray-600">{dosha.mars_house}वां भाव / {dosha.mars_house}th House</p>
              </div>
            )}

            {dosha.causes && dosha.causes.length > 0 && (
              <div>
                <h4 className="font-semibold text-gray-700 mb-2">कारण / Causes</h4>
                <ul className="space-y-1">
                  {dosha.causes.map((cause, i) => (
                    <li key={i} className="flex items-start gap-2 text-gray-600 text-sm">
                      <span className="text-orange-500 mt-1">•</span>
                      {cause}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {dosha.effects && dosha.effects.length > 0 && (
              <div>
                <h4 className="font-semibold text-gray-700 mb-2">प्रभाव / Effects</h4>
                <ul className="space-y-1">
                  {dosha.effects.map((effect, i) => (
                    <li key={i} className="flex items-start gap-2 text-gray-600 text-sm">
                      <span className="text-red-500 mt-1">⚠</span>
                      {effect}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {dosha.remedies && dosha.remedies.length > 0 && (
              <div>
                <h4 className="font-semibold text-green-700 mb-2">उपाय / Remedies</h4>
                <ul className="space-y-1">
                  {dosha.remedies.map((remedy, i) => (
                    <li key={i} className="flex items-start gap-2 text-gray-600 text-sm">
                      <span className="text-green-500 mt-1">✓</span>
                      {remedy}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {dosha.cancellation && dosha.cancellation.length > 0 && (
              <div className="bg-blue-50 p-3 rounded-lg">
                <h4 className="font-semibold text-blue-700 mb-2">दोष निवारण कारक / Cancellation Factors</h4>
                <ul className="space-y-1">
                  {dosha.cancellation.map((factor, i) => (
                    <li key={i} className="flex items-start gap-2 text-blue-600 text-sm">
                      <span className="mt-1">💡</span>
                      {factor}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}
      </div>
    );
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-orange-50 via-white to-yellow-50">
      <div className="container mx-auto px-4 py-8 max-w-7xl">
        <AnalysisNav />

        <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
          <div className="bg-gradient-to-r from-red-500 via-orange-500 to-yellow-500 text-white p-6 text-center">
            <div className="text-4xl mb-2">🔮</div>
            <h1 className="text-2xl font-bold mb-1">दोष विश्लेषण / Dosha Analysis</h1>
            <p className="text-white/90">पूर्ण दोष विश्लेषण / Complete Dosha Analysis</p>
          </div>

          <div className="p-6">
            {!result && (
              <div className="text-center py-8">
                <p className="text-gray-600 mb-6">
                  अपनी कुंडली में सभी दोषों का विश्लेषण करें<br />
                  <span className="text-sm text-gray-500">Analyze all doshas in your Kundali</span>
                </p>
                <button
                  onClick={analyzeDoshas}
                  disabled={loading}
                  className="px-8 py-3 bg-gradient-to-r from-orange-500 to-yellow-500 text-white font-semibold rounded-lg hover:from-orange-600 hover:to-yellow-600 disabled:opacity-50"
                >
                  {loading ? (
                    <span className="flex items-center gap-2">
                      <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                      </svg>
                      विश्लेषण हो रहा है... / Analyzing...
                    </span>
                  ) : (
                    'दोष विश्लेषण करें / Analyze Doshas'
                  )}
                </button>
              </div>
            )}

            {error && (
              <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded mb-6">
                <p className="text-red-700">{error}</p>
              </div>
            )}

            {result && (
              <div className="space-y-6">
                <div className="grid grid-cols-2 gap-4 mb-6">
                  <div className="bg-orange-50 p-4 rounded-xl text-center">
                    <div className="text-3xl font-bold text-orange-600">{result.total_doshas}</div>
                    <div className="text-sm text-gray-600">दोष पाए गए / Doshas Found</div>
                  </div>
                  <div className="bg-blue-50 p-4 rounded-xl text-center">
                    <div className="text-3xl font-bold text-blue-600">{result.severity_score}%</div>
                    <div className="text-sm text-gray-600">गंभीरता स्कोर / Severity Score</div>
                  </div>
                </div>

                <div className="bg-yellow-50 p-4 rounded-xl">
                  <h3 className="font-semibold text-gray-800 mb-2">सारांश / Summary</h3>
                  <p className="text-gray-700">{result.summary_hindi}</p>
                </div>

                <div className="space-y-4">
                  <h3 className="font-bold text-lg text-gray-800">विस्तृत दोष विश्लेषण / Detailed Dosha Analysis</h3>

                  <DoshaCard
                    id="kaal_sarp"
                    title="Kaal Sarp Dosha"
                    titleHindi="काल सर्प दोष"
                    dosha={result.kaal_sarp}
                    icon="🐍"
                  />

                  <DoshaCard
                    id="manglik"
                    title="Manglik Dosha"
                    titleHindi="मांगलिक दोष"
                    dosha={result.manglik}
                    icon="♂"
                  />

                  <DoshaCard
                    id="pitra"
                    title="Pitra Dosha"
                    titleHindi="पितृ दोष"
                    dosha={result.pitra_dosha}
                    icon="👥"
                  />

                  <DoshaCard
                    id="sade_sati"
                    title="Sade Sati"
                    titleHindi="साढ़े साती"
                    dosha={result.sade_sati}
                    icon="🪐"
                  />

                  <DoshaCard
                    id="guru_chandal"
                    title="Guru Chandal Yoga"
                    titleHindi="गुरु चांडाल योग"
                    dosha={result.guru_chandal}
                    icon="♃"
                  />

                  <DoshaCard
                    id="grahan"
                    title="Grahan Dosha"
                    titleHindi="ग्रहण दोष"
                    dosha={result.grahan_dosha}
                    icon="🌑"
                  />
                </div>

                <button
                  onClick={() => setResult(null)}
                  className="w-full py-3 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
                >
                  नया विश्लेषण / New Analysis
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </main>
  );
}
