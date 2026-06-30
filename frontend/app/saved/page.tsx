'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { KundaliList } from '../components/KundaliList';
import { getStorageStats, DEFAULT_CATEGORIES } from '@/lib/storage';

export default function SavedKundalisPage() {
  const [stats, setStats] = useState<{
    totalKundalis: number;
    categoryBreakdown: Record<string, number>;
    oldestEntry: string | null;
    newestEntry: string | null;
    storageUsed: number;
  } | null>(null);

  useEffect(() => {
    setStats(getStorageStats());
  }, []);

  const formatStorageSize = (bytes: number) => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
  };

  const getCategoryName = (catId: string) => {
    const cat = DEFAULT_CATEGORIES.find(c => c.id === catId);
    return cat ? `${cat.icon} ${cat.name}` : catId;
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
            होम पर वापस / Back to Home
          </Link>
          <h1 className="text-3xl font-bold text-gray-800 mb-2">
            <span className="text-orange-500">सहेजी हुई कुंडली / Saved Kundalis</span>
          </h1>
          <p className="text-gray-600">अपनी संग्रहीत जन्मपत्री प्रबंधित करें / Manage your stored birth charts</p>
        </div>

        {/* Quick Stats */}
        {stats && stats.totalKundalis > 0 && (
          <div className="bg-white rounded-xl shadow-lg p-4 mb-6">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="text-center p-3 bg-orange-50 rounded-lg">
                <div className="text-3xl font-bold text-orange-600">{stats.totalKundalis}</div>
                <div className="text-sm text-gray-600">कुल कुंडली / Total</div>
              </div>

              <div className="text-center p-3 bg-blue-50 rounded-lg">
                <div className="text-3xl font-bold text-blue-600">
                  {Object.keys(stats.categoryBreakdown).length}
                </div>
                <div className="text-sm text-gray-600">श्रेणियां / Categories</div>
              </div>

              <div className="text-center p-3 bg-green-50 rounded-lg">
                <div className="text-xl font-bold text-green-600">
                  {stats.newestEntry
                    ? new Date(stats.newestEntry).toLocaleDateString('en-IN', { day: '2-digit', month: 'short' })
                    : '-'
                  }
                </div>
                <div className="text-sm text-gray-600">नवीनतम / Latest</div>
              </div>

              <div className="text-center p-3 bg-purple-50 rounded-lg">
                <div className="text-xl font-bold text-purple-600">{formatStorageSize(stats.storageUsed)}</div>
                <div className="text-sm text-gray-600">संग्रहण / Storage</div>
              </div>
            </div>

            {/* Category Breakdown */}
            {Object.keys(stats.categoryBreakdown).length > 0 && (
              <div className="mt-4 pt-4 border-t">
                <h3 className="text-sm font-medium text-gray-600 mb-2">श्रेणी विवरण / Category Breakdown</h3>
                <div className="flex flex-wrap gap-2">
                  {Object.entries(stats.categoryBreakdown).map(([catId, count]) => (
                    <span
                      key={catId}
                      className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm"
                    >
                      {getCategoryName(catId)}: {count}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Quick Actions */}
        <div className="flex flex-wrap gap-3 mb-6 justify-center">
          <Link
            href="/"
            className="inline-flex items-center gap-2 px-4 py-2 bg-orange-500 text-white rounded-lg hover:bg-orange-600 transition-colors shadow-md"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
            नई कुंडली / New Kundali
          </Link>
          <Link
            href="/compare"
            className="inline-flex items-center gap-2 px-4 py-2 bg-purple-500 text-white rounded-lg hover:bg-purple-600 transition-colors shadow-md"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" />
            </svg>
            तुलना करें / Compare
          </Link>
          <Link
            href="/matching"
            className="inline-flex items-center gap-2 px-4 py-2 bg-pink-500 text-white rounded-lg hover:bg-pink-600 transition-colors shadow-md"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
            </svg>
            कुंडली मिलान / Matching
          </Link>
        </div>

        {/* Kundali List */}
        <KundaliList
          showFilters={true}
          showImportExport={true}
        />

        {/* Help Text */}
        <div className="mt-8 p-4 bg-white rounded-lg shadow text-center text-sm text-gray-600">
          <h3 className="font-semibold text-gray-800 mb-2">सुझाव / Tips</h3>
          <ul className="space-y-1">
            <li>परिवार, मित्रों को श्रेणियों में व्यवस्थित करें / Use categories to organize family & friends</li>
            <li>जल्दी खोजने के लिए टैग जोड़ें / Add tags for quick filtering (#manglik, #marriage)</li>
            <li>बैकअप के लिए JSON में निर्यात करें / Export as JSON to backup</li>
            <li>देखने या तुलना के लिए किसी भी कार्ड पर क्लिक करें / Click any card to view or compare</li>
          </ul>
        </div>
      </div>
    </main>
  );
}
