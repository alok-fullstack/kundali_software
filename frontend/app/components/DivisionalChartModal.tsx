'use client';

import React, { useState, useEffect } from 'react';
import { Modal } from './ui/Modal';
import { Button } from './ui/Button';
import {
  VargaType,
  DivisionalChart,
  NavamsaAnalysis,
  DasamsaAnalysis,
  VARGA_CHART_INFO,
  VargaPredictionItem,
} from '../../lib/types';

interface DivisionalChartModalProps {
  isOpen: boolean;
  onClose: () => void;
  kundaliId: string;
}

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export function DivisionalChartModal({
  isOpen,
  onClose,
  kundaliId,
}: DivisionalChartModalProps) {
  const [activeTab, setActiveTab] = useState<'charts' | 'navamsa' | 'dasamsa'>('charts');
  const [selectedVarga, setSelectedVarga] = useState<VargaType>('D9_NAVAMSA');
  const [chartData, setChartData] = useState<DivisionalChart | null>(null);
  const [navamsaAnalysis, setNavamsaAnalysis] = useState<NavamsaAnalysis | null>(null);
  const [dasamsaAnalysis, setDasamsaAnalysis] = useState<DasamsaAnalysis | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Fetch chart when selection changes
  useEffect(() => {
    if (isOpen && activeTab === 'charts') {
      fetchChart(selectedVarga);
    }
  }, [isOpen, selectedVarga, activeTab]);

  // Fetch analysis when tab changes
  useEffect(() => {
    if (isOpen && activeTab === 'navamsa' && !navamsaAnalysis) {
      fetchNavamsaAnalysis();
    }
    if (isOpen && activeTab === 'dasamsa' && !dasamsaAnalysis) {
      fetchDasamsaAnalysis();
    }
  }, [isOpen, activeTab]);

  const fetchChart = async (vargaType: VargaType) => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(
        `${API_BASE}/api/varga/chart/${kundaliId}/${vargaType}`
      );
      const data = await response.json();
      if (data.success) {
        setChartData(data.chart);
      } else {
        setError(data.detail || 'Failed to fetch chart');
      }
    } catch (err) {
      setError('Error fetching chart');
    } finally {
      setLoading(false);
    }
  };

  const fetchNavamsaAnalysis = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(
        `${API_BASE}/api/varga/analysis/navamsa/${kundaliId}`
      );
      const data = await response.json();
      if (data.success) {
        setNavamsaAnalysis(data);
      } else {
        setError(data.detail || 'Failed to fetch analysis');
      }
    } catch (err) {
      setError('Error fetching analysis');
    } finally {
      setLoading(false);
    }
  };

  const fetchDasamsaAnalysis = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(
        `${API_BASE}/api/varga/analysis/dasamsa/${kundaliId}`
      );
      const data = await response.json();
      if (data.success) {
        setDasamsaAnalysis(data);
      } else {
        setError(data.detail || 'Failed to fetch analysis');
      }
    } catch (err) {
      setError('Error fetching analysis');
    } finally {
      setLoading(false);
    }
  };

  const getVargaInfo = (type: VargaType) => {
    return VARGA_CHART_INFO.find((v) => v.type === type);
  };

  const renderChartGrid = () => {
    if (!chartData) return null;

    // Create 12-house grid
    const houses: Record<string, string[]> = {};
    for (let i = 1; i <= 12; i++) {
      houses[i.toString()] = chartData.planets_in_houses[i.toString()] || [];
    }

    return (
      <div className="grid grid-cols-4 gap-1 bg-amber-100 p-2 rounded-lg">
        {/* Traditional North Indian Chart Layout */}
        {/* Row 1 */}
        <div className="border border-amber-600 p-2 text-center bg-white min-h-[60px]">
          <div className="text-xs text-amber-800 font-bold">12</div>
          <div className="text-xs">{houses['12'].join(', ')}</div>
        </div>
        <div className="border border-amber-600 p-2 text-center bg-white min-h-[60px]">
          <div className="text-xs text-amber-800 font-bold">1</div>
          <div className="text-xs font-bold text-red-600">लग्न / Asc</div>
          <div className="text-xs">{houses['1'].join(', ')}</div>
        </div>
        <div className="border border-amber-600 p-2 text-center bg-white min-h-[60px]">
          <div className="text-xs text-amber-800 font-bold">2</div>
          <div className="text-xs">{houses['2'].join(', ')}</div>
        </div>
        <div className="border border-amber-600 p-2 text-center bg-white min-h-[60px]">
          <div className="text-xs text-amber-800 font-bold">3</div>
          <div className="text-xs">{houses['3'].join(', ')}</div>
        </div>

        {/* Row 2 */}
        <div className="border border-amber-600 p-2 text-center bg-white min-h-[60px]">
          <div className="text-xs text-amber-800 font-bold">11</div>
          <div className="text-xs">{houses['11'].join(', ')}</div>
        </div>
        <div className="col-span-2 border border-amber-600 p-2 bg-amber-50 flex flex-col justify-center items-center">
          <div className="text-sm font-bold text-amber-800">
            {chartData.varga_name}
          </div>
          <div className="text-xs text-amber-600">
            Lagna: {chartData.lagna.varga_rashi}
          </div>
        </div>
        <div className="border border-amber-600 p-2 text-center bg-white min-h-[60px]">
          <div className="text-xs text-amber-800 font-bold">4</div>
          <div className="text-xs">{houses['4'].join(', ')}</div>
        </div>

        {/* Row 3 */}
        <div className="border border-amber-600 p-2 text-center bg-white min-h-[60px]">
          <div className="text-xs text-amber-800 font-bold">10</div>
          <div className="text-xs">{houses['10'].join(', ')}</div>
        </div>
        <div className="col-span-2 row-span-1 border border-amber-600 p-2 bg-amber-50 text-center">
          <div className="text-xs text-gray-600">{chartData.varga_description}</div>
        </div>
        <div className="border border-amber-600 p-2 text-center bg-white min-h-[60px]">
          <div className="text-xs text-amber-800 font-bold">5</div>
          <div className="text-xs">{houses['5'].join(', ')}</div>
        </div>

        {/* Row 4 */}
        <div className="border border-amber-600 p-2 text-center bg-white min-h-[60px]">
          <div className="text-xs text-amber-800 font-bold">9</div>
          <div className="text-xs">{houses['9'].join(', ')}</div>
        </div>
        <div className="border border-amber-600 p-2 text-center bg-white min-h-[60px]">
          <div className="text-xs text-amber-800 font-bold">8</div>
          <div className="text-xs">{houses['8'].join(', ')}</div>
        </div>
        <div className="border border-amber-600 p-2 text-center bg-white min-h-[60px]">
          <div className="text-xs text-amber-800 font-bold">7</div>
          <div className="text-xs">{houses['7'].join(', ')}</div>
        </div>
        <div className="border border-amber-600 p-2 text-center bg-white min-h-[60px]">
          <div className="text-xs text-amber-800 font-bold">6</div>
          <div className="text-xs">{houses['6'].join(', ')}</div>
        </div>
      </div>
    );
  };

  const renderPlanetTable = () => {
    if (!chartData) return null;

    return (
      <div className="mt-4 overflow-x-auto">
        <table className="min-w-full text-sm">
          <thead className="bg-amber-100">
            <tr>
              <th className="px-2 py-1 text-left">ग्रह / Planet</th>
              <th className="px-2 py-1 text-left">D-1 राशि / Rashi</th>
              <th className="px-2 py-1 text-left">{chartData.varga_name}</th>
              <th className="px-2 py-1 text-left">विभाग / Division</th>
              <th className="px-2 py-1 text-left">स्थिति / Status</th>
            </tr>
          </thead>
          <tbody>
            {Object.entries(chartData.planets).map(([name, pos]) => (
              <tr key={name} className="border-b">
                <td className="px-2 py-1 font-medium">{name}</td>
                <td className="px-2 py-1">{pos.original_rashi}</td>
                <td className="px-2 py-1">{pos.varga_rashi}</td>
                <td className="px-2 py-1">{pos.division_number}</td>
                <td className="px-2 py-1">
                  {pos.is_exalted && (
                    <span className="text-green-600 font-bold">उच्च / Exalted</span>
                  )}
                  {pos.is_debilitated && (
                    <span className="text-red-600 font-bold">नीच / Debilitated</span>
                  )}
                  {pos.is_own_sign && (
                    <span className="text-blue-600 font-bold">स्वराशि / Own Sign</span>
                  )}
                  {!pos.is_exalted && !pos.is_debilitated && !pos.is_own_sign && (
                    <span className="text-gray-500">-</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  };

  const renderNavamsaAnalysis = () => {
    if (!navamsaAnalysis) return null;

    return (
      <div className="space-y-4">
        {/* Spouse Characteristics */}
        <div className="bg-pink-50 rounded-lg p-4">
          <h3 className="font-bold text-pink-800 mb-2">
            जीवनसाथी विशेषताएं / Spouse Characteristics (7th House)
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm">
            <div>
              <span className="font-medium">सप्तम भाव / 7th House:</span>{' '}
              {navamsaAnalysis.spouse_characteristics.seventh_house_rashi_english}
            </div>
            <div>
              <span className="font-medium">सप्तमेश / 7th Lord:</span>{' '}
              {navamsaAnalysis.spouse_characteristics.seventh_lord}
            </div>
            <div className="md:col-span-2">
              <span className="font-medium">रूप-रंग / Appearance:</span>{' '}
              {navamsaAnalysis.spouse_characteristics.appearance}
            </div>
            <div className="md:col-span-2">
              <span className="font-medium">स्वभाव / Nature:</span>{' '}
              {navamsaAnalysis.spouse_characteristics.nature}
            </div>
            <div className="md:col-span-2">
              <span className="font-medium">मुख्य गुण / Key Traits:</span>{' '}
              {navamsaAnalysis.spouse_characteristics.key_traits}
            </div>
          </div>
        </div>

        {/* Marriage Quality */}
        <div className="bg-purple-50 rounded-lg p-4">
          <h3 className="font-bold text-purple-800 mb-2">विवाह गुणवत्ता / Marriage Quality</h3>
          <div className="flex items-center gap-4 mb-2">
            <div className="text-2xl font-bold text-purple-700">
              {navamsaAnalysis.marriage_quality.quality_score}/100
            </div>
            <div
              className={`px-3 py-1 rounded-full text-sm font-medium ${
                navamsaAnalysis.marriage_quality.quality_level === 'Excellent'
                  ? 'bg-green-100 text-green-800'
                  : navamsaAnalysis.marriage_quality.quality_level === 'Good'
                  ? 'bg-blue-100 text-blue-800'
                  : navamsaAnalysis.marriage_quality.quality_level === 'Moderate'
                  ? 'bg-yellow-100 text-yellow-800'
                  : 'bg-red-100 text-red-800'
              }`}
            >
              {navamsaAnalysis.marriage_quality.quality_level}
            </div>
          </div>
          {navamsaAnalysis.marriage_quality.positive_factors.length > 0 && (
            <div className="mb-2">
              <span className="text-green-600 font-medium">सकारात्मक / Positives: </span>
              {navamsaAnalysis.marriage_quality.positive_factors.join(', ')}
            </div>
          )}
          {navamsaAnalysis.marriage_quality.negative_factors.length > 0 && (
            <div>
              <span className="text-red-600 font-medium">चुनौतियां / Challenges: </span>
              {navamsaAnalysis.marriage_quality.negative_factors.join(', ')}
            </div>
          )}
        </div>

        {/* Marriage Timing */}
        <div className="bg-blue-50 rounded-lg p-4">
          <h3 className="font-bold text-blue-800 mb-2">विवाह समय / Marriage Timing</h3>
          <div className="text-lg font-medium mb-2">
            Indication: {navamsaAnalysis.marriage_timing_factors.overall_indication}
          </div>
          <ul className="list-disc list-inside text-sm">
            {navamsaAnalysis.marriage_timing_factors.factors.map((factor, i) => (
              <li key={i}>{factor}</li>
            ))}
          </ul>
        </div>

        {/* Spiritual Path */}
        <div className="bg-indigo-50 rounded-lg p-4">
          <h3 className="font-bold text-indigo-800 mb-2">आध्यात्मिक प्रकृति / Spiritual Nature</h3>
          <div className="text-lg font-medium mb-2">
            {navamsaAnalysis.spiritual_aspects.spiritual_path}
          </div>
          {navamsaAnalysis.spiritual_aspects.dharmic_strengths.length > 0 && (
            <ul className="list-disc list-inside text-sm">
              {navamsaAnalysis.spiritual_aspects.dharmic_strengths.map((s, i) => (
                <li key={i}>{s}</li>
              ))}
            </ul>
          )}
        </div>

        {/* Predictions */}
        {navamsaAnalysis.predictions.length > 0 && (
          <div className="bg-gray-50 rounded-lg p-4">
            <h3 className="font-bold text-gray-800 mb-2">भविष्यवाणी / Predictions</h3>
            {navamsaAnalysis.predictions.map((pred, i) => (
              <div
                key={i}
                className={`p-3 rounded-lg mb-2 ${
                  pred.is_favorable ? 'bg-green-50' : 'bg-yellow-50'
                }`}
              >
                <div className="font-medium">
                  {pred.category}: {pred.aspect}
                </div>
                <div className="text-sm mt-1">{pred.prediction}</div>
                {pred.remedies.length > 0 && (
                  <div className="text-sm mt-2 text-orange-700">
                    उपाय / Remedies: {pred.remedies.join(', ')}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    );
  };

  const renderDasamsaAnalysis = () => {
    if (!dasamsaAnalysis) return null;

    return (
      <div className="space-y-4">
        {/* Career Direction */}
        <div className="bg-blue-50 rounded-lg p-4">
          <h3 className="font-bold text-blue-800 mb-2">करियर दिशा / Career Direction</h3>
          <div className="text-sm mb-2">
            <span className="font-medium">दशमांश लग्न / Dasamsa Lagna:</span>{' '}
            {dasamsaAnalysis.career_lagna.rashi_english}
          </div>
          <div className="text-sm mb-2">
            <span className="font-medium">पेशेवर दृष्टिकोण / Professional Approach:</span>{' '}
            {dasamsaAnalysis.career_lagna.professional_approach}
          </div>
          <div className="mt-3">
            <span className="font-medium">उपयुक्त करियर / Suitable Careers:</span>
            <div className="flex flex-wrap gap-2 mt-1">
              {dasamsaAnalysis.career_lagna.suitable_careers.map((career, i) => (
                <span
                  key={i}
                  className="px-2 py-1 bg-blue-100 text-blue-800 rounded-full text-xs"
                >
                  {career}
                </span>
              ))}
            </div>
          </div>
        </div>

        {/* 10th House Analysis */}
        <div className="bg-green-50 rounded-lg p-4">
          <h3 className="font-bold text-green-800 mb-2">दशम भाव विश्लेषण / 10th House Analysis</h3>
          <div className="grid grid-cols-2 gap-2 text-sm">
            <div>
              <span className="font-medium">दशम भाव / 10th House:</span>{' '}
              {dasamsaAnalysis.tenth_house_analysis.rashi_english}
            </div>
            <div>
              <span className="font-medium">दशमेश / 10th Lord:</span>{' '}
              {dasamsaAnalysis.tenth_house_analysis.tenth_lord}
            </div>
            {dasamsaAnalysis.tenth_house_analysis.planets_in_10th.length > 0 && (
              <div className="col-span-2">
                <span className="font-medium">दशम में ग्रह / Planets in 10th:</span>{' '}
                {dasamsaAnalysis.tenth_house_analysis.planets_in_10th.join(', ')}
              </div>
            )}
          </div>
          {dasamsaAnalysis.tenth_house_analysis.indicated_domains.length > 0 && (
            <div className="mt-3">
              <span className="font-medium">संकेतित क्षेत्र / Indicated Domains:</span>
              <div className="flex flex-wrap gap-2 mt-1">
                {dasamsaAnalysis.tenth_house_analysis.indicated_domains.map(
                  (domain, i) => (
                    <span
                      key={i}
                      className="px-2 py-1 bg-green-100 text-green-800 rounded-full text-xs"
                    >
                      {domain}
                    </span>
                  )
                )}
              </div>
            </div>
          )}
        </div>

        {/* Career Indicators */}
        {dasamsaAnalysis.career_indicators.length > 0 && (
          <div className="bg-yellow-50 rounded-lg p-4">
            <h3 className="font-bold text-yellow-800 mb-2">करियर संकेतक / Career Indicators</h3>
            {dasamsaAnalysis.career_indicators.map((indicator, i) => (
              <div
                key={i}
                className={`p-2 rounded mb-2 ${
                  indicator.favorable ? 'bg-green-100' : 'bg-red-100'
                }`}
              >
                <span className="font-medium">{indicator.planet}:</span>{' '}
                {indicator.indication}
              </div>
            ))}
          </div>
        )}

        {/* Professional Strengths */}
        <div className="bg-purple-50 rounded-lg p-4">
          <h3 className="font-bold text-purple-800 mb-2">
            पेशेवर शक्ति और कमजोरी / Professional Strengths & Weaknesses
          </h3>
          {dasamsaAnalysis.professional_strengths.strengths.length > 0 && (
            <div className="mb-2">
              <span className="text-green-600 font-medium">शक्तियां / Strengths:</span>
              <ul className="list-disc list-inside text-sm">
                {dasamsaAnalysis.professional_strengths.strengths.map((s, i) => (
                  <li key={i}>{s}</li>
                ))}
              </ul>
            </div>
          )}
          {dasamsaAnalysis.professional_strengths.weaknesses.length > 0 && (
            <div>
              <span className="text-red-600 font-medium">चुनौतियां / Challenges:</span>
              <ul className="list-disc list-inside text-sm">
                {dasamsaAnalysis.professional_strengths.weaknesses.map((w, i) => (
                  <li key={i}>{w}</li>
                ))}
              </ul>
            </div>
          )}
        </div>

        {/* Career Timing */}
        <div className="bg-indigo-50 rounded-lg p-4">
          <h3 className="font-bold text-indigo-800 mb-2">करियर वृद्धि / Career Growth</h3>
          <div className="text-lg font-medium mb-2">
            Pattern: {dasamsaAnalysis.career_timing.growth_pattern}
          </div>
          {dasamsaAnalysis.career_timing.factors.length > 0 && (
            <ul className="list-disc list-inside text-sm">
              {dasamsaAnalysis.career_timing.factors.map((f, i) => (
                <li key={i}>{f}</li>
              ))}
            </ul>
          )}
        </div>
      </div>
    );
  };

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title="षोडशवर्ग चार्ट / Divisional Charts (Varga)"
      size="xl"
    >
      {/* Tabs */}
      <div className="flex border-b border-gray-200 mb-4">
        <button
          className={`px-4 py-2 font-medium ${
            activeTab === 'charts'
              ? 'text-amber-600 border-b-2 border-amber-600'
              : 'text-gray-500 hover:text-gray-700'
          }`}
          onClick={() => setActiveTab('charts')}
        >
          चार्ट / Charts
        </button>
        <button
          className={`px-4 py-2 font-medium ${
            activeTab === 'navamsa'
              ? 'text-pink-600 border-b-2 border-pink-600'
              : 'text-gray-500 hover:text-gray-700'
          }`}
          onClick={() => setActiveTab('navamsa')}
        >
          विवाह (D-9) / Marriage
        </button>
        <button
          className={`px-4 py-2 font-medium ${
            activeTab === 'dasamsa'
              ? 'text-blue-600 border-b-2 border-blue-600'
              : 'text-gray-500 hover:text-gray-700'
          }`}
          onClick={() => setActiveTab('dasamsa')}
        >
          करियर (D-10) / Career
        </button>
      </div>

      {/* Loading and Error States */}
      {loading && (
        <div className="flex justify-center items-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-amber-600"></div>
        </div>
      )}

      {error && (
        <div className="bg-red-100 text-red-700 p-3 rounded-lg mb-4">{error}</div>
      )}

      {/* Tab Content */}
      {!loading && !error && (
        <>
          {activeTab === 'charts' && (
            <div>
              {/* Chart Selector */}
              <div className="mb-4">
                <label className="block text-sm font-medium mb-2">
                  Select Divisional Chart:
                </label>
                <div className="grid grid-cols-4 gap-2">
                  {VARGA_CHART_INFO.slice(0, 8).map((varga) => (
                    <button
                      key={varga.type}
                      className={`p-2 text-xs rounded border ${
                        selectedVarga === varga.type
                          ? 'bg-amber-100 border-amber-500 text-amber-800'
                          : 'bg-white border-gray-300 hover:bg-gray-50'
                      } ${
                        varga.importance === 'high' ? 'font-bold' : ''
                      }`}
                      onClick={() => setSelectedVarga(varga.type)}
                    >
                      <div>{varga.name}</div>
                      <div className="text-gray-500">{varga.nameHindi}</div>
                    </button>
                  ))}
                </div>
                <div className="grid grid-cols-4 gap-2 mt-2">
                  {VARGA_CHART_INFO.slice(8).map((varga) => (
                    <button
                      key={varga.type}
                      className={`p-2 text-xs rounded border ${
                        selectedVarga === varga.type
                          ? 'bg-amber-100 border-amber-500 text-amber-800'
                          : 'bg-white border-gray-300 hover:bg-gray-50'
                      } ${
                        varga.importance === 'high' ? 'font-bold' : ''
                      }`}
                      onClick={() => setSelectedVarga(varga.type)}
                    >
                      <div>{varga.name}</div>
                      <div className="text-gray-500">{varga.nameHindi}</div>
                    </button>
                  ))}
                </div>
              </div>

              {/* Chart Display */}
              {chartData && (
                <>
                  {renderChartGrid()}
                  {renderPlanetTable()}
                </>
              )}
            </div>
          )}

          {activeTab === 'navamsa' && (
            <div>
              <div className="text-center mb-4">
                <h2 className="text-xl font-bold text-pink-800">
                  Navamsa Analysis (D-9)
                </h2>
                <p className="text-sm text-gray-600">
                  Marriage, Spouse Characteristics, and Dharma
                </p>
              </div>
              {navamsaAnalysis ? (
                renderNavamsaAnalysis()
              ) : (
                <div className="text-center py-8 text-gray-500">
                  Loading analysis...
                </div>
              )}
            </div>
          )}

          {activeTab === 'dasamsa' && (
            <div>
              <div className="text-center mb-4">
                <h2 className="text-xl font-bold text-blue-800">
                  Dasamsa Analysis (D-10)
                </h2>
                <p className="text-sm text-gray-600">
                  Career, Profession, and Professional Success
                </p>
              </div>
              {dasamsaAnalysis ? (
                renderDasamsaAnalysis()
              ) : (
                <div className="text-center py-8 text-gray-500">
                  Loading analysis...
                </div>
              )}
            </div>
          )}
        </>
      )}
    </Modal>
  );
}
