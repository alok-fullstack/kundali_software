'use client';

import React, { useState, useEffect, Suspense } from 'react';
import Link from 'next/link';
import { useSearchParams } from 'next/navigation';
import { KundaliList } from '../components/KundaliList';
import { ComparisonView } from '../components/ComparisonView';
import { KundaliMiniCard } from '../components/KundaliCard';
import { Button } from '../components/ui/Button';
import {
  SavedKundali,
  getSavedKundalis,
  getSavedKundaliById,
  saveComparison,
  getComparisonHistory,
} from '@/lib/storage';

type ViewMode = 'select' | 'compare';

function ComparePageContent() {
  const searchParams = useSearchParams();
  const [viewMode, setViewMode] = useState<ViewMode>('select');
  const [selectedKundalis, setSelectedKundalis] = useState<SavedKundali[]>([]);
  const [recentComparisons, setRecentComparisons] = useState<Array<{
    kundali1: SavedKundali | null;
    kundali2: SavedKundali | null;
    comparedAt: string;
  }>>([]);

  // Load pre-selected Kundali from URL params
  useEffect(() => {
    const k1 = searchParams.get('k1');
    const k2 = searchParams.get('k2');

    if (k1) {
      const kundali1 = getSavedKundaliById(k1);
      if (kundali1) {
        setSelectedKundalis(prev => {
          if (!prev.find(k => k.id === kundali1.id)) {
            return [...prev, kundali1];
          }
          return prev;
        });
      }
    }

    if (k2) {
      const kundali2 = getSavedKundaliById(k2);
      if (kundali2) {
        setSelectedKundalis(prev => {
          if (!prev.find(k => k.id === kundali2.id)) {
            return [...prev, kundali2];
          }
          return prev;
        });
      }
    }
  }, [searchParams]);

  // Load recent comparisons
  useEffect(() => {
    const history = getComparisonHistory();
    const withKundalis = history.map(h => ({
      kundali1: getSavedKundaliById(h.kundali1Id),
      kundali2: getSavedKundaliById(h.kundali2Id),
      comparedAt: h.comparedAt,
    })).filter(h => h.kundali1 && h.kundali2);
    setRecentComparisons(withKundalis);
  }, []);

  const handleSelect = (kundali: SavedKundali) => {
    setSelectedKundalis(prev => {
      const isSelected = prev.find(k => k.id === kundali.id);
      if (isSelected) {
        return prev.filter(k => k.id !== kundali.id);
      }
      if (prev.length < 2) {
        return [...prev, kundali];
      }
      return prev;
    });
  };

  const handleCompare = () => {
    if (selectedKundalis.length === 2) {
      // Save to history
      saveComparison(selectedKundalis[0].id, selectedKundalis[1].id);
      setViewMode('compare');
    }
  };

  const handleBack = () => {
    setViewMode('select');
    setSelectedKundalis([]);
  };

  const handleQuickCompare = (k1: SavedKundali, k2: SavedKundali) => {
    setSelectedKundalis([k1, k2]);
    saveComparison(k1.id, k2.id);
    setViewMode('compare');
  };

  const allKundalis = getSavedKundalis();

  // Compare View
  if (viewMode === 'compare' && selectedKundalis.length === 2) {
    return (
      <main className="min-h-screen py-5 px-4 bg-gradient-to-br from-orange-50 to-yellow-50">
        <div className="max-w-7xl mx-auto">
          <ComparisonView
            kundali1={selectedKundalis[0]}
            kundali2={selectedKundalis[1]}
            onBack={handleBack}
          />
        </div>
      </main>
    );
  }

  // Selection View
  return (
    <main className="min-h-screen py-5 px-4 bg-gradient-to-br from-orange-50 to-yellow-50">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-6">
          <Link href="/saved" className="inline-flex items-center text-orange-600 hover:text-orange-700 mb-4">
            <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            सहेजी कुंडली पर वापस / Back to Saved Kundalis
          </Link>
          <h1 className="text-3xl font-bold text-gray-800 mb-2">
            <span className="text-orange-500">कुंडली तुलना / Compare Kundalis</span>
          </h1>
          <p className="text-gray-600">तुलना के लिए दो कुंडली चुनें / Select two Kundalis to compare</p>
        </div>

        {/* Empty State */}
        {allKundalis.length < 2 && (
          <div className="bg-white rounded-xl shadow-lg p-8 text-center mb-6">
            <div className="text-6xl mb-4">📊</div>
            <h3 className="text-lg font-semibold text-gray-800 mb-2">
              तुलना के लिए कम से कम 2 कुंडली चाहिए / Need at least 2 saved Kundalis
            </h3>
            <p className="text-gray-600 mb-4">
              आपके पास {allKundalis.length} कुंडली है / You have {allKundalis.length} saved Kundali{allKundalis.length !== 1 ? 's' : ''}.
            </p>
            <Link
              href="/"
              className="inline-flex items-center gap-2 px-4 py-2 bg-orange-500 text-white rounded-lg hover:bg-orange-600 transition-colors"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
              </svg>
              कुंडली बनाएं / Generate Kundali
            </Link>
          </div>
        )}

        {allKundalis.length >= 2 && (
          <>
            {/* Selection Summary */}
            <div className="bg-white rounded-xl shadow-lg p-4 mb-6">
              <div className="flex flex-wrap items-center justify-between gap-4">
                <div>
                  <h3 className="font-medium text-gray-800 mb-2">तुलना के लिए चयनित / Selected for Comparison</h3>
                  <div className="flex flex-wrap gap-3">
                    {selectedKundalis.length === 0 ? (
                      <span className="text-gray-400 text-sm">नीचे से 2 कुंडली चुनें / Select 2 Kundalis below</span>
                    ) : (
                      <>
                        {selectedKundalis.map((k, i) => (
                          <React.Fragment key={k.id}>
                            <div className="flex items-center gap-2">
                              <KundaliMiniCard kundali={k} />
                              <button
                                onClick={() => handleSelect(k)}
                                className="text-gray-400 hover:text-red-500"
                              >
                                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                                </svg>
                              </button>
                            </div>
                            {i === 0 && selectedKundalis.length === 2 && (
                              <div className="flex items-center text-gray-400">
                                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" />
                                </svg>
                              </div>
                            )}
                          </React.Fragment>
                        ))}
                      </>
                    )}
                  </div>
                </div>

                <Button
                  variant="primary"
                  onClick={handleCompare}
                  disabled={selectedKundalis.length !== 2}
                  className="flex items-center gap-2"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                  अभी तुलना करें / Compare Now
                </Button>
              </div>
            </div>

            {/* Recent Comparisons */}
            {recentComparisons.length > 0 && (
              <div className="bg-white rounded-xl shadow-lg p-4 mb-6">
                <h3 className="font-medium text-gray-800 mb-3 flex items-center gap-2">
                  <svg className="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  हाल की तुलनाएं / Recent Comparisons
                </h3>
                <div className="space-y-2">
                  {recentComparisons.slice(0, 5).map((comparison, i) => (
                    comparison.kundali1 && comparison.kundali2 && (
                      <div
                        key={i}
                        className="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-orange-50 cursor-pointer transition-colors"
                        onClick={() => handleQuickCompare(comparison.kundali1!, comparison.kundali2!)}
                      >
                        <div className="flex items-center gap-3">
                          <span className="font-medium text-gray-800">{comparison.kundali1.name}</span>
                          <svg className="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" />
                          </svg>
                          <span className="font-medium text-gray-800">{comparison.kundali2.name}</span>
                        </div>
                        <span className="text-xs text-gray-400">
                          {new Date(comparison.comparedAt).toLocaleDateString('en-IN')}
                        </span>
                      </div>
                    )
                  ))}
                </div>
              </div>
            )}

            {/* Kundali Selection List */}
            <div className="bg-white rounded-xl shadow-lg p-4">
              <h3 className="font-medium text-gray-800 mb-4 flex items-center gap-2">
                <svg className="w-5 h-5 text-orange-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 10h16M4 14h16M4 18h16" />
                </svg>
                तुलना के लिए कुंडली चुनें / Select Kundalis to Compare
              </h3>
              <KundaliList
                onSelect={handleSelect}
                selectedIds={selectedKundalis.map(k => k.id)}
                maxSelection={2}
                compact={false}
                showFilters={true}
                showImportExport={false}
              />
            </div>
          </>
        )}

        {/* Info Box */}
        <div className="mt-6 p-4 bg-white rounded-lg shadow text-center text-sm text-gray-600">
          <h3 className="font-semibold text-gray-800 mb-2">तुलना के बारे में / About Comparison</h3>
          <p>
            तुलना में अष्टकूट गुण मिलान प्रणाली का उपयोग होता है। इसमें सभी 8 कूट शामिल हैं: वर्ण, वश्य, तारा, योनि, ग्रह मैत्री, गण, भकूट, और नाड़ी। /
            The comparison uses Ashtakoot Guna Milan system including all 8 Kootas for marriage or general compatibility analysis.
          </p>
        </div>
      </div>
    </main>
  );
}

// Wrap in Suspense for useSearchParams
export default function ComparePage() {
  return (
    <Suspense fallback={
      <main className="min-h-screen py-5 px-4 bg-gradient-to-br from-orange-50 to-yellow-50">
        <div className="max-w-7xl mx-auto text-center py-20">
          <div className="animate-spin w-12 h-12 border-4 border-orange-500 border-t-transparent rounded-full mx-auto mb-4" />
          <p className="text-gray-600">लोड हो रहा है... / Loading...</p>
        </div>
      </main>
    }>
      <ComparePageContent />
    </Suspense>
  );
}
