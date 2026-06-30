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

interface YogaResult {
  name: string;
  name_hindi: string;
  strength: string;
  description: string;
  description_hindi: string;
  effects: string[];
  effects_hindi: string[];
  planets_involved: string[];
}

interface CareerAnalysis {
  tenth_house_sign: string;
  tenth_house_lord: string;
  tenth_lord_house: number;
  planets_in_tenth: string[];
  recommended_careers: string[];
  career_traits: string;
  career_timing: string;
  career_timing_hindi: string;
  government_job_yoga: boolean;
  business_yoga: boolean;
  foreign_career_yoga: boolean;
}

interface DhanaYogaAnalysis {
  yogas_present: YogaResult[];
  wealth_potential: string;
  wealth_potential_hindi: string;
  best_wealth_periods: string[];
  wealth_sources: string[];
  wealth_sources_hindi: string[];
  poverty_yogas: YogaResult[];
}

interface CareerFinanceResult {
  career_analysis: CareerAnalysis;
  dhana_yoga_analysis: DhanaYogaAnalysis;
  overall_career_score: number;
  overall_wealth_score: number;
  summary: string;
  summary_hindi: string;
  recommendations: string[];
  recommendations_hindi: string[];
}

export default function CareerPage() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<CareerFinanceResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'career' | 'finance'>('career');

  const analyzeCareer = async () => {
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

      // Analyze career
      const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000/api';
      const response = await fetch(`${API_BASE}/career/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ kundali_data: kundaliData }),
      });

      if (!response.ok) throw new Error('Failed to analyze career');

      const data = await response.json();
      if (data.success) {
        setResult(data.career_finance);
      } else {
        setError(data.error || 'Analysis failed');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const ScoreGauge = ({ score, label }: { score: number; label: string }) => (
    <div className="text-center">
      <div className="relative w-32 h-32 mx-auto">
        <svg className="w-full h-full" viewBox="0 0 100 100">
          <circle
            className="text-gray-200"
            strokeWidth="10"
            stroke="currentColor"
            fill="transparent"
            r="40"
            cx="50"
            cy="50"
          />
          <circle
            className={score >= 70 ? 'text-green-500' : score >= 40 ? 'text-yellow-500' : 'text-red-500'}
            strokeWidth="10"
            strokeDasharray={`${score * 2.51} 251.2`}
            strokeLinecap="round"
            stroke="currentColor"
            fill="transparent"
            r="40"
            cx="50"
            cy="50"
            transform="rotate(-90 50 50)"
          />
          <text x="50" y="50" textAnchor="middle" dy="0.3em" className="text-2xl font-bold fill-gray-800">
            {score}%
          </text>
        </svg>
      </div>
      <p className="mt-2 text-sm font-medium text-gray-600">{label}</p>
    </div>
  );

  return (
    <main className="min-h-screen bg-gradient-to-br from-orange-50 via-white to-yellow-50">
      <div className="container mx-auto px-4 py-8 max-w-7xl">
        <AnalysisNav />

        <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
          <div className="bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 text-white p-6 text-center">
            <div className="text-4xl mb-2">💼</div>
            <h1 className="text-2xl font-bold mb-1">करियर और वित्त विश्लेषण</h1>
            <p className="text-white/90">Career & Finance Analysis</p>
          </div>

          <div className="p-6">
            {!result && (
              <div className="text-center py-8">
                <p className="text-gray-600 mb-6">
                  अपनी कुंडली से करियर और धन योग जानें<br />
                  <span className="text-sm text-gray-500">Discover career paths and wealth yogas from your Kundali</span>
                </p>
                <button
                  onClick={analyzeCareer}
                  disabled={loading}
                  className="px-8 py-3 bg-gradient-to-r from-blue-500 to-purple-500 text-white font-semibold rounded-lg hover:from-blue-600 hover:to-purple-600 disabled:opacity-50"
                >
                  {loading ? (
                    <span className="flex items-center gap-2">
                      <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                      </svg>
                      विश्लेषण हो रहा है...
                    </span>
                  ) : (
                    'विश्लेषण करें / Analyze'
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
                <div className="flex justify-center gap-8 py-4">
                  <ScoreGauge score={result.overall_career_score} label="करियर स्कोर / Career Score" />
                  <ScoreGauge score={result.overall_wealth_score} label="धन स्कोर / Wealth Score" />
                </div>

                <div className="bg-gradient-to-r from-blue-50 to-purple-50 p-4 rounded-xl">
                  <p className="text-gray-700">{result.summary_hindi}</p>
                </div>

                <div className="flex border-b">
                  <button
                    onClick={() => setActiveTab('career')}
                    className={`flex-1 py-3 font-medium ${
                      activeTab === 'career'
                        ? 'text-blue-600 border-b-2 border-blue-600'
                        : 'text-gray-500 hover:text-gray-700'
                    }`}
                  >
                    💼 करियर / Career
                  </button>
                  <button
                    onClick={() => setActiveTab('finance')}
                    className={`flex-1 py-3 font-medium ${
                      activeTab === 'finance'
                        ? 'text-green-600 border-b-2 border-green-600'
                        : 'text-gray-500 hover:text-gray-700'
                    }`}
                  >
                    💰 धन योग / Finance
                  </button>
                </div>

                {activeTab === 'career' && (
                  <div className="space-y-6">
                    <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                      <div className="bg-blue-50 p-4 rounded-xl">
                        <div className="text-xs text-gray-500 mb-1">10वां भाव / 10th House</div>
                        <div className="font-bold text-blue-700">{result.career_analysis.tenth_house_sign}</div>
                      </div>
                      <div className="bg-purple-50 p-4 rounded-xl">
                        <div className="text-xs text-gray-500 mb-1">10वें भाव का स्वामी / 10th Lord</div>
                        <div className="font-bold text-purple-700">{result.career_analysis.tenth_house_lord}</div>
                      </div>
                      <div className="bg-pink-50 p-4 rounded-xl">
                        <div className="text-xs text-gray-500 mb-1">स्वामी का भाव / Lord in House</div>
                        <div className="font-bold text-pink-700">{result.career_analysis.tenth_lord_house}</div>
                      </div>
                    </div>

                    <div className="flex flex-wrap gap-2">
                      {result.career_analysis.government_job_yoga && (
                        <span className="px-3 py-1 bg-yellow-100 text-yellow-800 rounded-full text-sm font-medium">
                          🏛️ सरकारी नौकरी योग / Govt Job Yoga
                        </span>
                      )}
                      {result.career_analysis.business_yoga && (
                        <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-medium">
                          🏪 व्यापार योग / Business Yoga
                        </span>
                      )}
                      {result.career_analysis.foreign_career_yoga && (
                        <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium">
                          ✈️ विदेश करियर योग / Foreign Career Yoga
                        </span>
                      )}
                    </div>

                    {result.career_analysis.career_traits && (
                      <div className="bg-gray-50 p-4 rounded-xl">
                        <h4 className="font-semibold text-gray-700 mb-2">करियर गुण / Career Traits</h4>
                        <p className="text-gray-600">{result.career_analysis.career_traits}</p>
                      </div>
                    )}

                    <div>
                      <h4 className="font-semibold text-gray-700 mb-3">अनुशंसित करियर / Recommended Careers</h4>
                      <div className="flex flex-wrap gap-2">
                        {result.career_analysis.recommended_careers.map((career, i) => (
                          <span key={i} className="px-3 py-2 bg-gradient-to-r from-blue-100 to-purple-100 text-gray-700 rounded-lg text-sm">
                            {career}
                          </span>
                        ))}
                      </div>
                    </div>

                    <div className="bg-blue-50 p-4 rounded-xl">
                      <h4 className="font-semibold text-blue-700 mb-2">⏰ करियर समय / Career Timing</h4>
                      <p className="text-gray-600">{result.career_analysis.career_timing_hindi}</p>
                    </div>
                  </div>
                )}

                {activeTab === 'finance' && (
                  <div className="space-y-6">
                    <div className="bg-green-50 p-4 rounded-xl text-center">
                      <div className="text-sm text-gray-500 mb-1">धन क्षमता / Wealth Potential</div>
                      <div className="text-2xl font-bold text-green-700">
                        {result.dhana_yoga_analysis.wealth_potential_hindi}
                      </div>
                    </div>

                    <div>
                      <h4 className="font-semibold text-gray-700 mb-3">✨ धन योग / Wealth Yogas</h4>
                      {result.dhana_yoga_analysis.yogas_present.length > 0 ? (
                        <div className="space-y-3">
                          {result.dhana_yoga_analysis.yogas_present.map((yoga, i) => (
                            <div key={i} className="bg-gradient-to-r from-green-50 to-emerald-50 p-4 rounded-xl border border-green-200">
                              <div className="flex items-center justify-between mb-2">
                                <h5 className="font-bold text-green-800">{yoga.name_hindi}</h5>
                                <span className={`px-2 py-1 rounded text-xs font-medium ${
                                  yoga.strength === 'Strong'
                                    ? 'bg-green-200 text-green-800'
                                    : 'bg-yellow-200 text-yellow-800'
                                }`}>
                                  {yoga.strength}
                                </span>
                              </div>
                              <p className="text-sm text-gray-600 mb-2">{yoga.description_hindi}</p>
                              <div className="flex flex-wrap gap-1">
                                {yoga.planets_involved.map((p, j) => (
                                  <span key={j} className="px-2 py-0.5 bg-white rounded text-xs text-gray-600">
                                    {p}
                                  </span>
                                ))}
                              </div>
                            </div>
                          ))}
                        </div>
                      ) : (
                        <p className="text-gray-500 text-center py-4">कोई प्रमुख धन योग नहीं मिला</p>
                      )}
                    </div>

                    {result.dhana_yoga_analysis.wealth_sources_hindi.length > 0 && (
                      <div>
                        <h4 className="font-semibold text-gray-700 mb-3">💵 धन के स्रोत / Wealth Sources</h4>
                        <div className="flex flex-wrap gap-2">
                          {result.dhana_yoga_analysis.wealth_sources_hindi.map((source, i) => (
                            <span key={i} className="px-3 py-2 bg-green-100 text-green-700 rounded-lg text-sm">
                              {source}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}

                    <div>
                      <h4 className="font-semibold text-gray-700 mb-3">📅 श्रेष्ठ धन काल / Best Wealth Periods</h4>
                      <div className="flex flex-wrap gap-2">
                        {result.dhana_yoga_analysis.best_wealth_periods.map((period, i) => (
                          <span key={i} className="px-3 py-2 bg-yellow-100 text-yellow-800 rounded-lg text-sm">
                            {period}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                )}

                {result.recommendations_hindi.length > 0 && (
                  <div className="bg-orange-50 p-4 rounded-xl">
                    <h4 className="font-semibold text-orange-700 mb-3">💡 सुझाव / Recommendations</h4>
                    <ul className="space-y-2">
                      {result.recommendations_hindi.map((rec, i) => (
                        <li key={i} className="flex items-start gap-2 text-gray-700">
                          <span className="text-orange-500 mt-1">•</span>
                          {rec}
                        </li>
                      ))}
                    </ul>
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
