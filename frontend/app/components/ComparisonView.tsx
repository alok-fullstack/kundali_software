'use client';

import React, { useState, useEffect } from 'react';
import { SavedKundali, DEFAULT_CATEGORIES } from '@/lib/storage';
import { matchKundalis } from '@/lib/api';
import { MatchResponse } from '@/lib/types';
import { Button } from './ui/Button';
import { GunaRadarChart } from './GunaRadarChart';

interface ComparisonViewProps {
  kundali1: SavedKundali;
  kundali2: SavedKundali;
  onBack?: () => void;
}

export function ComparisonView({ kundali1, kundali2, onBack }: ComparisonViewProps) {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [matchResult, setMatchResult] = useState<MatchResponse | null>(null);
  const [activeTab, setActiveTab] = useState<'overview' | 'gunas' | 'details'>('overview');

  // Auto-fetch match result on mount
  useEffect(() => {
    fetchMatchResult();
  }, [kundali1.id, kundali2.id]);

  const fetchMatchResult = async () => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await matchKundalis({
        boy: {
          name: kundali1.name,
          dob: kundali1.dob,
          tob: kundali1.tob,
          city: kundali1.city,
          latitude: kundali1.latitude,
          longitude: kundali1.longitude,
          timezone: 'Asia/Kolkata',
        },
        girl: {
          name: kundali2.name,
          dob: kundali2.dob,
          tob: kundali2.tob,
          city: kundali2.city,
          latitude: kundali2.latitude,
          longitude: kundali2.longitude,
          timezone: 'Asia/Kolkata',
        },
      });

      if (response.success) {
        setMatchResult(response);
      } else {
        setError(response.error || 'Failed to compare Kundalis');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-IN', {
      day: '2-digit',
      month: 'short',
      year: 'numeric',
    });
  };

  const formatTime = (timeStr: string) => {
    const [hour, minute] = timeStr.split(':');
    const h = parseInt(hour);
    const ampm = h >= 12 ? 'PM' : 'AM';
    const displayHour = h % 12 || 12;
    return `${displayHour}:${minute} ${ampm}`;
  };

  const getCategory = (categoryId?: string) => {
    return DEFAULT_CATEGORIES.find(c => c.id === categoryId);
  };

  // Loading State
  if (isLoading) {
    return (
      <div className="bg-white rounded-xl shadow-lg p-8 text-center">
        <div className="animate-spin w-16 h-16 border-4 border-orange-500 border-t-transparent rounded-full mx-auto mb-4" />
        <h3 className="text-lg font-semibold text-gray-800 mb-2">कुंडली तुलना हो रही है... / Comparing Kundalis...</h3>
        <p className="text-gray-600">ज्योतिषीय अनुकूलता विश्लेषण / Analyzing compatibility</p>
      </div>
    );
  }

  // Error State
  if (error) {
    return (
      <div className="bg-white rounded-xl shadow-lg p-8">
        <div className="text-center mb-6">
          <div className="text-5xl mb-4">⚠️</div>
          <h3 className="text-lg font-semibold text-red-800 mb-2">तुलना विफल / Comparison Failed</h3>
          <p className="text-gray-600">{error}</p>
        </div>
        <div className="flex justify-center gap-3">
          <Button variant="outline" onClick={onBack}>
            वापस जाएं / Go Back
          </Button>
          <Button variant="primary" onClick={fetchMatchResult}>
            पुनः प्रयास / Retry
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header with Back Button */}
      {onBack && (
        <button
          onClick={onBack}
          className="inline-flex items-center text-orange-600 hover:text-orange-700"
        >
          <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
          चयन पर वापस / Back to Selection
        </button>
      )}

      {/* Comparison Header Cards */}
      <div className="grid md:grid-cols-2 gap-4">
        {/* Kundali 1 */}
        <div className="bg-white rounded-xl shadow-lg overflow-hidden border-t-4 border-blue-500">
          <div className="bg-gradient-to-r from-blue-500 to-blue-600 text-white p-4">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 bg-white/20 rounded-full flex items-center justify-center text-2xl">
                {getCategory(kundali1.category)?.icon || 'Person 1'}
              </div>
              <div>
                <h3 className="text-xl font-bold">{kundali1.name}</h3>
                {kundali1.category && (
                  <p className="text-blue-100 text-sm">{getCategory(kundali1.category)?.nameHindi}</p>
                )}
              </div>
            </div>
          </div>
          <div className="p-4">
            <div className="grid grid-cols-2 gap-3 text-sm">
              <div className="bg-gray-50 rounded-lg p-2">
                <div className="text-gray-500 text-xs">जन्म तिथि / DOB</div>
                <div className="font-semibold">{formatDate(kundali1.dob)}</div>
              </div>
              <div className="bg-gray-50 rounded-lg p-2">
                <div className="text-gray-500 text-xs">समय / Time</div>
                <div className="font-semibold">{formatTime(kundali1.tob)}</div>
              </div>
              <div className="col-span-2 bg-gray-50 rounded-lg p-2">
                <div className="text-gray-500 text-xs">स्थान / Place</div>
                <div className="font-semibold">{kundali1.city}</div>
              </div>
            </div>
            {matchResult && (
              <div className="mt-3 pt-3 border-t border-gray-100">
                <div className="grid grid-cols-2 gap-2 text-sm">
                  <div>
                    <span className="text-gray-500 text-xs">चंद्र राशि / Moon:</span>
                    <span className="ml-1 font-medium text-blue-600">{matchResult.boy_details.moon_rashi}</span>
                  </div>
                  <div>
                    <span className="text-gray-500 text-xs">नक्षत्र / Nakshatra:</span>
                    <span className="ml-1 font-medium text-blue-600">{matchResult.boy_details.moon_nakshatra}</span>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Kundali 2 */}
        <div className="bg-white rounded-xl shadow-lg overflow-hidden border-t-4 border-pink-500">
          <div className="bg-gradient-to-r from-pink-500 to-pink-600 text-white p-4">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 bg-white/20 rounded-full flex items-center justify-center text-2xl">
                {getCategory(kundali2.category)?.icon || 'Person 2'}
              </div>
              <div>
                <h3 className="text-xl font-bold">{kundali2.name}</h3>
                {kundali2.category && (
                  <p className="text-pink-100 text-sm">{getCategory(kundali2.category)?.nameHindi}</p>
                )}
              </div>
            </div>
          </div>
          <div className="p-4">
            <div className="grid grid-cols-2 gap-3 text-sm">
              <div className="bg-gray-50 rounded-lg p-2">
                <div className="text-gray-500 text-xs">जन्म तिथि / DOB</div>
                <div className="font-semibold">{formatDate(kundali2.dob)}</div>
              </div>
              <div className="bg-gray-50 rounded-lg p-2">
                <div className="text-gray-500 text-xs">समय / Time</div>
                <div className="font-semibold">{formatTime(kundali2.tob)}</div>
              </div>
              <div className="col-span-2 bg-gray-50 rounded-lg p-2">
                <div className="text-gray-500 text-xs">स्थान / Place</div>
                <div className="font-semibold">{kundali2.city}</div>
              </div>
            </div>
            {matchResult && (
              <div className="mt-3 pt-3 border-t border-gray-100">
                <div className="grid grid-cols-2 gap-2 text-sm">
                  <div>
                    <span className="text-gray-500 text-xs">चंद्र राशि / Moon:</span>
                    <span className="ml-1 font-medium text-pink-600">{matchResult.girl_details.moon_rashi}</span>
                  </div>
                  <div>
                    <span className="text-gray-500 text-xs">नक्षत्र / Nakshatra:</span>
                    <span className="ml-1 font-medium text-pink-600">{matchResult.girl_details.moon_nakshatra}</span>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Match Score Card */}
      {matchResult && (
        <>
          <div className={`rounded-xl shadow-lg overflow-hidden text-white ${
            matchResult.percentage >= 70 ? 'bg-gradient-to-r from-green-500 to-emerald-500' :
            matchResult.percentage >= 50 ? 'bg-gradient-to-r from-amber-500 to-orange-500' :
            'bg-gradient-to-r from-red-500 to-rose-500'
          }`}>
            <div className="p-6 text-center">
              <h2 className="text-2xl font-bold mb-4">Compatibility Score / मिलान स्कोर</h2>
              <div className="inline-block bg-white/20 rounded-full px-8 py-4">
                <div className="text-5xl font-bold">{matchResult.total_points}/36</div>
                <div className="text-lg mt-1">{matchResult.percentage}% Match</div>
              </div>
              <div className="mt-4">
                <span className={`px-4 py-2 rounded-full text-sm font-medium ${
                  matchResult.percentage >= 70 ? 'bg-green-700' :
                  matchResult.percentage >= 50 ? 'bg-amber-700' :
                  'bg-red-700'
                }`}>
                  {matchResult.compatibility_level === 'Excellent' ? 'Excellent / Excellent' :
                   matchResult.compatibility_level === 'Good' ? 'Good / Good' :
                   matchResult.compatibility_level === 'Average' ? 'Average / Average' :
                   matchResult.compatibility_level}
                </span>
              </div>
            </div>
          </div>

          {/* Tabs */}
          <div className="bg-white rounded-xl shadow-lg overflow-hidden">
            <div className="flex border-b">
              {[
                { id: 'overview', label: 'Overview', labelHindi: 'सारांश' },
                { id: 'gunas', label: '8 Gunas', labelHindi: 'अष्टकूट' },
                { id: 'details', label: 'Details', labelHindi: 'विवरण' },
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id as 'overview' | 'gunas' | 'details')}
                  className={`flex-1 py-3 px-4 text-center font-medium transition-colors ${
                    activeTab === tab.id
                      ? 'text-orange-600 border-b-2 border-orange-500 bg-orange-50'
                      : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'
                  }`}
                >
                  <span className="hidden sm:inline">{tab.labelHindi} / </span>
                  {tab.label}
                </button>
              ))}
            </div>

            <div className="p-4">
              {/* Overview Tab */}
              {activeTab === 'overview' && (
                <div className="space-y-6">
                  {/* Strengths & Concerns */}
                  <div className="grid md:grid-cols-2 gap-4">
                    {matchResult.areas_of_strength.length > 0 && (
                      <div className="bg-green-50 rounded-lg p-4 border border-green-200">
                        <h3 className="font-bold text-green-800 mb-3 flex items-center gap-2">
                          <span>✓</span>
                          शक्तियां / Strengths
                        </h3>
                        <ul className="space-y-2">
                          {matchResult.areas_of_strength.map((item, i) => (
                            <li key={i} className="flex items-start gap-2 text-sm">
                              <span className="text-green-500 mt-0.5">Check</span>
                              <span className="text-gray-700">{item}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                    {matchResult.areas_of_concern.length > 0 && (
                      <div className="bg-red-50 rounded-lg p-4 border border-red-200">
                        <h3 className="font-bold text-red-800 mb-3 flex items-center gap-2">
                          <span>⚠️</span>
                          चिंताएं / Concerns
                        </h3>
                        <ul className="space-y-2">
                          {matchResult.areas_of_concern.map((item, i) => (
                            <li key={i} className="flex items-start gap-2 text-sm">
                              <span className="text-red-500 mt-0.5">Warning</span>
                              <span className="text-gray-700">{item}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>

                  {/* Recommendation */}
                  <div className="bg-orange-50 rounded-lg p-4 border border-orange-200">
                    <h3 className="font-bold text-orange-800 mb-2">सुझाव / Recommendation</h3>
                    <pre className="whitespace-pre-wrap text-sm text-gray-700 font-sans">
                      {matchResult.recommendation}
                    </pre>
                  </div>

                  {/* Doshas */}
                  {matchResult.doshas.length > 0 && (
                    <div className="bg-white rounded-lg border border-gray-200">
                      <div className="p-4 border-b bg-red-50">
                        <h3 className="font-bold text-red-800">दोष पाए गए / Doshas Detected</h3>
                      </div>
                      <div className="p-4 space-y-3">
                        {matchResult.doshas.map((dosha, i) => (
                          <div
                            key={i}
                            className={`p-3 rounded-lg border ${
                              dosha.is_cancelled ? 'bg-green-50 border-green-200' : 'bg-red-50 border-red-200'
                            }`}
                          >
                            <div className="flex items-center justify-between mb-1">
                              <span className="font-bold">{dosha.name}</span>
                              <span className={`px-2 py-0.5 rounded text-xs text-white ${
                                dosha.is_cancelled ? 'bg-green-500' : 'bg-red-500'
                              }`}>
                                {dosha.is_cancelled ? 'निरस्त / Cancelled' : dosha.severity}
                              </span>
                            </div>
                            <p className="text-sm text-gray-700">{dosha.description}</p>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}

              {/* Gunas Tab */}
              {activeTab === 'gunas' && (
                <div className="space-y-6">
                  {/* Radar Chart */}
                  {matchResult.koota_scores && matchResult.koota_scores.length > 0 && (
                    <GunaRadarChart kootaScores={matchResult.koota_scores} />
                  )}

                  {/* Koota Scores Table */}
                  <div className="overflow-x-auto">
                    <table className="w-full text-sm">
                      <thead>
                        <tr className="bg-orange-500 text-white">
                          <th className="px-4 py-3 text-left">कूट / Koota</th>
                          <th className="px-4 py-3 text-center">{kundali1.name}</th>
                          <th className="px-4 py-3 text-center">{kundali2.name}</th>
                          <th className="px-4 py-3 text-center">अंक / Score</th>
                          <th className="px-4 py-3 text-center">स्थिति / Status</th>
                        </tr>
                      </thead>
                      <tbody>
                        {matchResult.koota_scores.map((koota, i) => (
                          <tr
                            key={i}
                            className={`border-b ${koota.is_auspicious ? 'bg-green-50' : 'bg-red-50'}`}
                          >
                            <td className="px-4 py-3">
                              <div className="font-medium">{koota.name}</div>
                              <div className="text-xs text-gray-500">{koota.name_hindi}</div>
                            </td>
                            <td className="px-4 py-3 text-center text-blue-600">{koota.boy_value}</td>
                            <td className="px-4 py-3 text-center text-pink-600">{koota.girl_value}</td>
                            <td className="px-4 py-3 text-center font-bold">
                              {koota.obtained_points}/{koota.max_points}
                            </td>
                            <td className="px-4 py-3 text-center">
                              <span className={`px-2 py-1 rounded text-xs font-medium ${
                                koota.is_auspicious
                                  ? 'bg-green-200 text-green-800'
                                  : 'bg-red-200 text-red-800'
                              }`}>
                                {koota.is_auspicious ? 'Good' : 'Attention'}
                              </span>
                            </td>
                          </tr>
                        ))}
                        <tr className="bg-orange-100 font-bold">
                          <td className="px-4 py-3" colSpan={3}>Total / Total</td>
                          <td className="px-4 py-3 text-center">
                            {matchResult.total_points}/36
                          </td>
                          <td className="px-4 py-3 text-center">
                            {matchResult.percentage}%
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              )}

              {/* Details Tab */}
              {activeTab === 'details' && (
                <div className="space-y-6">
                  {/* Side by Side Comparison */}
                  <div className="grid md:grid-cols-2 gap-4">
                    {/* Person 1 Details */}
                    <div className="border border-blue-200 rounded-lg overflow-hidden">
                      <div className="bg-blue-100 p-3 font-bold text-blue-800">
                        {kundali1.name}
                      </div>
                      <div className="p-4 space-y-2 text-sm">
                        <div className="flex justify-between">
                          <span className="text-gray-500">Lagna / Lagna</span>
                          <span className="font-medium">{matchResult.boy_details.lagna_rashi}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-500">Moon Rashi / Rashi</span>
                          <span className="font-medium">{matchResult.boy_details.moon_rashi}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-500">Nakshatra / Nakshatra</span>
                          <span className="font-medium">{matchResult.boy_details.moon_nakshatra}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-500">Varna / Varna</span>
                          <span className="font-medium">{matchResult.boy_details.varna || '-'}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-500">Gana / Gana</span>
                          <span className="font-medium">{matchResult.boy_details.gana || '-'}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-500">Nadi / Nadi</span>
                          <span className="font-medium">{matchResult.boy_details.nadi || '-'}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-500">Yoni / Yoni</span>
                          <span className="font-medium">{matchResult.boy_details.yoni || '-'}</span>
                        </div>
                      </div>
                    </div>

                    {/* Person 2 Details */}
                    <div className="border border-pink-200 rounded-lg overflow-hidden">
                      <div className="bg-pink-100 p-3 font-bold text-pink-800">
                        {kundali2.name}
                      </div>
                      <div className="p-4 space-y-2 text-sm">
                        <div className="flex justify-between">
                          <span className="text-gray-500">Lagna / Lagna</span>
                          <span className="font-medium">{matchResult.girl_details.lagna_rashi}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-500">Moon Rashi / Rashi</span>
                          <span className="font-medium">{matchResult.girl_details.moon_rashi}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-500">Nakshatra / Nakshatra</span>
                          <span className="font-medium">{matchResult.girl_details.moon_nakshatra}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-500">Varna / Varna</span>
                          <span className="font-medium">{matchResult.girl_details.varna || '-'}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-500">Gana / Gana</span>
                          <span className="font-medium">{matchResult.girl_details.gana || '-'}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-500">Nadi / Nadi</span>
                          <span className="font-medium">{matchResult.girl_details.nadi || '-'}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-500">Yoni / Yoni</span>
                          <span className="font-medium">{matchResult.girl_details.yoni || '-'}</span>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Remedies */}
                  {matchResult.remedies.length > 0 && (
                    <div className="bg-purple-50 rounded-lg p-4 border border-purple-200">
                      <h3 className="font-bold text-purple-800 mb-3">Recommended Remedies / Remedies</h3>
                      <ul className="space-y-2">
                        {matchResult.remedies.slice(0, 10).map((remedy, i) => (
                          <li key={i} className="flex items-start gap-2 text-sm">
                            <span className="text-purple-500">Prayer</span>
                            <span className="text-gray-700">{remedy}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Marriage Timing */}
                  {matchResult.marriage_timing && (
                    <div className="bg-white rounded-lg border border-gray-200">
                      <div className="p-4 border-b bg-gradient-to-r from-pink-100 to-purple-100">
                        <h3 className="font-bold text-purple-800">Auspicious Marriage Timing / Auspicious Timing</h3>
                      </div>
                      <div className="p-4 space-y-4">
                        {matchResult.marriage_timing.favorable_days.length > 0 && (
                          <div>
                            <h4 className="font-medium text-gray-700 mb-2">Favorable Days</h4>
                            <div className="flex flex-wrap gap-2">
                              {matchResult.marriage_timing.favorable_days.map((day, i) => (
                                <span key={i} className="px-3 py-1 bg-green-100 text-green-800 text-sm rounded-full">
                                  {day}
                                </span>
                              ))}
                            </div>
                          </div>
                        )}
                        {matchResult.marriage_timing.favorable_months.length > 0 && (
                          <div>
                            <h4 className="font-medium text-gray-700 mb-2">Favorable Months</h4>
                            <div className="flex flex-wrap gap-2">
                              {matchResult.marriage_timing.favorable_months.map((month, i) => (
                                <span key={i} className="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full">
                                  {month}
                                </span>
                              ))}
                            </div>
                          </div>
                        )}
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>

          {/* Actions */}
          <div className="flex justify-center gap-4">
            <Button
              variant="outline"
              onClick={() => window.print()}
              className="flex items-center gap-2"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" />
              </svg>
              Print
            </Button>
          </div>

          {/* Disclaimer */}
          <div className="text-center text-xs text-gray-500 p-4 bg-gray-50 rounded-lg">
            <p>Based on Brihat Parashar Hora Shastra and Muhurta Chintamani</p>
            <p className="mt-1">This report is for guidance only. Please consult a qualified astrologer for important decisions.</p>
          </div>
        </>
      )}
    </div>
  );
}
