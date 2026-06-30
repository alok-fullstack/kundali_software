'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { getKundaliDataForAnalysis } from '@/lib/api';

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

interface PlanetRemedy {
  planet: string;
  planet_hindi: string;
  is_weak: boolean;
  is_afflicted: boolean;
  mantras: Array<{
    type: string;
    text: string;
    transliteration: string;
    jaap_count: number;
    best_day: string;
  }>;
  gemstone: {
    primary: string;
    substitute: string[];
    weight: string;
    metal: string;
    finger: string;
    day_to_wear: string;
  };
  charity: {
    items: string[];
    recipient: string;
    day: string;
    time: string;
  };
  lal_kitab: string[];
  general_tips: string[];
}

interface DoshaRemedy {
  dosha_name: string;
  dosha_name_hindi: string;
  severity: string;
  mantras: string[];
  temples: string[];
  rituals: string[];
  charity: string[];
  lifestyle: string[];
  timeline: string;
}

interface RemediesResult {
  planet_remedies: PlanetRemedy[];
  dosha_remedies: DoshaRemedy[];
  house_remedies: any[];
  priority_remedies: string[];
  priority_remedies_hindi: string[];
  daily_routine: string[];
  weekly_routine: string[];
  monthly_routine: string[];
  yearly_routine: string[];
}

export default function RemediesPage() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<RemediesResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'planet' | 'dosha' | 'routine'>('planet');
  const [expandedPlanet, setExpandedPlanet] = useState<string | null>(null);

  const analyzeRemedies = async () => {
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

      // Analyze remedies
      const response = await fetch('http://localhost:8000/api/remedies/comprehensive', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ kundali_data: kundaliData }),
      });

      if (!response.ok) throw new Error('Failed to get remedies');

      const data = await response.json();
      if (data.success) {
        setResult(data.remedies);
      } else {
        setError(data.error || 'Failed to load remedies');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const PlanetIcon = ({ planet }: { planet: string }) => {
    const icons: Record<string, string> = {
      SUN: '☀️', MOON: '🌙', MARS: '♂️', MERCURY: '☿️',
      JUPITER: '♃', VENUS: '♀️', SATURN: '🪐', RAHU: '☊', KETU: '☋'
    };
    return <span className="text-2xl">{icons[planet] || '⭐'}</span>;
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-orange-50 via-white to-yellow-50">
      <div className="container mx-auto px-4 py-8 max-w-7xl">
        <AnalysisNav />

        <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
          <div className="bg-gradient-to-r from-green-500 via-teal-500 to-cyan-500 text-white p-6 text-center">
            <div className="text-4xl mb-2">🙏</div>
            <h1 className="text-2xl font-bold mb-1">वैदिक उपाय</h1>
            <p className="text-white/90">Comprehensive Vedic Remedies</p>
          </div>

          <div className="p-6">
            {!result && (
              <div className="text-center py-8">
                <p className="text-gray-600 mb-6">
                  अपनी कुंडली के अनुसार व्यापक उपाय प्राप्त करें<br />
                  <span className="text-sm text-gray-500">Get personalized remedies based on your Kundali</span>
                </p>
                <button
                  onClick={analyzeRemedies}
                  disabled={loading}
                  className="px-8 py-3 bg-gradient-to-r from-green-500 to-teal-500 text-white font-semibold rounded-lg hover:from-green-600 hover:to-teal-600 disabled:opacity-50"
                >
                  {loading ? (
                    <span className="flex items-center gap-2">
                      <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                      </svg>
                      उपाय खोज रहे हैं...
                    </span>
                  ) : (
                    'उपाय प्राप्त करें / Get Remedies'
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
                {result.priority_remedies_hindi.length > 0 && (
                  <div className="bg-yellow-50 border-l-4 border-yellow-500 p-4 rounded-r-xl">
                    <h3 className="font-bold text-yellow-800 mb-2">⭐ प्राथमिकता उपाय / Priority Remedies</h3>
                    <ul className="space-y-1">
                      {result.priority_remedies_hindi.map((rem, i) => (
                        <li key={i} className="text-yellow-700">{i + 1}. {rem}</li>
                      ))}
                    </ul>
                  </div>
                )}

                <div className="flex border-b overflow-x-auto">
                  <button
                    onClick={() => setActiveTab('planet')}
                    className={`flex-1 py-3 px-4 font-medium whitespace-nowrap ${
                      activeTab === 'planet'
                        ? 'text-green-600 border-b-2 border-green-600'
                        : 'text-gray-500 hover:text-gray-700'
                    }`}
                  >
                    🌟 ग्रह उपाय
                  </button>
                  <button
                    onClick={() => setActiveTab('dosha')}
                    className={`flex-1 py-3 px-4 font-medium whitespace-nowrap ${
                      activeTab === 'dosha'
                        ? 'text-red-600 border-b-2 border-red-600'
                        : 'text-gray-500 hover:text-gray-700'
                    }`}
                  >
                    🔮 दोष उपाय
                  </button>
                  <button
                    onClick={() => setActiveTab('routine')}
                    className={`flex-1 py-3 px-4 font-medium whitespace-nowrap ${
                      activeTab === 'routine'
                        ? 'text-blue-600 border-b-2 border-blue-600'
                        : 'text-gray-500 hover:text-gray-700'
                    }`}
                  >
                    📅 दिनचर्या
                  </button>
                </div>

                {activeTab === 'planet' && (
                  <div className="space-y-4">
                    {result.planet_remedies.length > 0 ? (
                      result.planet_remedies.map((remedy, i) => (
                        <div key={i} className="border rounded-xl overflow-hidden">
                          <div
                            className={`p-4 cursor-pointer flex items-center justify-between ${
                              remedy.is_weak || remedy.is_afflicted
                                ? 'bg-orange-50'
                                : 'bg-green-50'
                            }`}
                            onClick={() => setExpandedPlanet(
                              expandedPlanet === remedy.planet ? null : remedy.planet
                            )}
                          >
                            <div className="flex items-center gap-3">
                              <PlanetIcon planet={remedy.planet} />
                              <div>
                                <h4 className="font-bold text-gray-800">{remedy.planet_hindi}</h4>
                                <div className="flex gap-2 mt-1">
                                  {remedy.is_weak && (
                                    <span className="px-2 py-0.5 bg-orange-200 text-orange-800 rounded text-xs">
                                      कमजोर / Weak
                                    </span>
                                  )}
                                  {remedy.is_afflicted && (
                                    <span className="px-2 py-0.5 bg-red-200 text-red-800 rounded text-xs">
                                      पीड़ित / Afflicted
                                    </span>
                                  )}
                                </div>
                              </div>
                            </div>
                            <svg
                              className={`w-5 h-5 transition-transform ${
                                expandedPlanet === remedy.planet ? 'rotate-180' : ''
                              }`}
                              fill="none"
                              stroke="currentColor"
                              viewBox="0 0 24 24"
                            >
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                            </svg>
                          </div>

                          {expandedPlanet === remedy.planet && (
                            <div className="p-4 space-y-4 border-t">
                              {remedy.mantras.length > 0 && (
                                <div>
                                  <h5 className="font-semibold text-purple-700 mb-2">🕉️ मंत्र / Mantras</h5>
                                  {remedy.mantras.map((mantra, j) => (
                                    <div key={j} className="bg-purple-50 p-3 rounded-lg mb-2">
                                      <p className="font-medium text-purple-800">{mantra.text}</p>
                                      <p className="text-sm text-purple-600 italic">{mantra.transliteration}</p>
                                      <p className="text-xs text-gray-500 mt-1">
                                        जाप: {mantra.jaap_count} बार | दिन: {mantra.best_day}
                                      </p>
                                    </div>
                                  ))}
                                </div>
                              )}

                              {remedy.gemstone && (
                                <div>
                                  <h5 className="font-semibold text-blue-700 mb-2">💎 रत्न / Gemstone</h5>
                                  <div className="bg-blue-50 p-3 rounded-lg">
                                    <p className="font-medium text-blue-800">{remedy.gemstone.primary}</p>
                                    <div className="text-sm text-gray-600 mt-2 grid grid-cols-2 gap-2">
                                      <span>वजन: {remedy.gemstone.weight}</span>
                                      <span>धातु: {remedy.gemstone.metal}</span>
                                      <span>उंगली: {remedy.gemstone.finger}</span>
                                      <span>दिन: {remedy.gemstone.day_to_wear}</span>
                                    </div>
                                  </div>
                                </div>
                              )}

                              {remedy.charity && remedy.charity.items?.length > 0 && (
                                <div>
                                  <h5 className="font-semibold text-green-700 mb-2">🎁 दान / Charity</h5>
                                  <div className="bg-green-50 p-3 rounded-lg">
                                    <ul className="text-sm text-gray-700">
                                      {remedy.charity.items.map((item, j) => (
                                        <li key={j}>• {item}</li>
                                      ))}
                                    </ul>
                                    <p className="text-xs text-gray-500 mt-2">
                                      किसे: {remedy.charity.recipient} | दिन: {remedy.charity.day}
                                    </p>
                                  </div>
                                </div>
                              )}

                              {remedy.lal_kitab.length > 0 && (
                                <div>
                                  <h5 className="font-semibold text-red-700 mb-2">📕 लाल किताब उपाय</h5>
                                  <ul className="bg-red-50 p-3 rounded-lg space-y-1">
                                    {remedy.lal_kitab.map((tip, j) => (
                                      <li key={j} className="text-sm text-gray-700">• {tip}</li>
                                    ))}
                                  </ul>
                                </div>
                              )}
                            </div>
                          )}
                        </div>
                      ))
                    ) : (
                      <p className="text-center text-gray-500 py-8">
                        कोई कमजोर ग्रह नहीं मिला। आपकी कुंडली अच्छी है!
                      </p>
                    )}
                  </div>
                )}

                {activeTab === 'dosha' && (
                  <div className="space-y-4">
                    {result.dosha_remedies.length > 0 ? (
                      result.dosha_remedies.map((dosha, i) => (
                        <div key={i} className="bg-red-50 rounded-xl p-4 space-y-3">
                          <div className="flex items-center justify-between">
                            <h4 className="font-bold text-red-800">{dosha.dosha_name_hindi}</h4>
                            <span className={`px-2 py-1 rounded text-xs font-medium ${
                              dosha.severity === 'Severe'
                                ? 'bg-red-200 text-red-800'
                                : dosha.severity === 'Moderate'
                                ? 'bg-yellow-200 text-yellow-800'
                                : 'bg-green-200 text-green-800'
                            }`}>
                              {dosha.severity}
                            </span>
                          </div>

                          {dosha.mantras.length > 0 && (
                            <div>
                              <h5 className="text-sm font-semibold text-gray-700">मंत्र:</h5>
                              <ul className="text-sm text-gray-600">
                                {dosha.mantras.map((m, j) => <li key={j}>• {m}</li>)}
                              </ul>
                            </div>
                          )}

                          {dosha.temples.length > 0 && (
                            <div>
                              <h5 className="text-sm font-semibold text-gray-700">मंदिर:</h5>
                              <ul className="text-sm text-gray-600">
                                {dosha.temples.map((t, j) => <li key={j}>• {t}</li>)}
                              </ul>
                            </div>
                          )}

                          {dosha.rituals.length > 0 && (
                            <div>
                              <h5 className="text-sm font-semibold text-gray-700">पूजा:</h5>
                              <ul className="text-sm text-gray-600">
                                {dosha.rituals.map((r, j) => <li key={j}>• {r}</li>)}
                              </ul>
                            </div>
                          )}

                          <p className="text-xs text-gray-500">
                            समयावधि: {dosha.timeline}
                          </p>
                        </div>
                      ))
                    ) : (
                      <p className="text-center text-gray-500 py-8">
                        कोई दोष नहीं मिला। बधाई हो!
                      </p>
                    )}
                  </div>
                )}

                {activeTab === 'routine' && (
                  <div className="space-y-6">
                    <div>
                      <h4 className="font-bold text-gray-800 mb-3 flex items-center gap-2">
                        ☀️ दैनिक दिनचर्या / Daily Routine
                      </h4>
                      <ul className="bg-yellow-50 p-4 rounded-xl space-y-2">
                        {result.daily_routine.map((item, i) => (
                          <li key={i} className="flex items-start gap-2 text-gray-700">
                            <span className="text-yellow-600">•</span>
                            {item}
                          </li>
                        ))}
                      </ul>
                    </div>

                    <div>
                      <h4 className="font-bold text-gray-800 mb-3 flex items-center gap-2">
                        📅 साप्ताहिक दिनचर्या / Weekly Routine
                      </h4>
                      <ul className="bg-blue-50 p-4 rounded-xl space-y-2">
                        {result.weekly_routine.map((item, i) => (
                          <li key={i} className="flex items-start gap-2 text-gray-700">
                            <span className="text-blue-600">•</span>
                            {item}
                          </li>
                        ))}
                      </ul>
                    </div>

                    <div>
                      <h4 className="font-bold text-gray-800 mb-3 flex items-center gap-2">
                        🌙 मासिक दिनचर्या / Monthly Routine
                      </h4>
                      <ul className="bg-purple-50 p-4 rounded-xl space-y-2">
                        {result.monthly_routine.map((item, i) => (
                          <li key={i} className="flex items-start gap-2 text-gray-700">
                            <span className="text-purple-600">•</span>
                            {item}
                          </li>
                        ))}
                      </ul>
                    </div>

                    <div>
                      <h4 className="font-bold text-gray-800 mb-3 flex items-center gap-2">
                        🎊 वार्षिक दिनचर्या / Yearly Routine
                      </h4>
                      <ul className="bg-green-50 p-4 rounded-xl space-y-2">
                        {result.yearly_routine.map((item, i) => (
                          <li key={i} className="flex items-start gap-2 text-gray-700">
                            <span className="text-green-600">•</span>
                            {item}
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>
                )}

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
