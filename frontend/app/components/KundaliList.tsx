'use client';

import React, { useState, useEffect, useMemo } from 'react';
import { KundaliCard } from './KundaliCard';
import {
  SavedKundali,
  DEFAULT_CATEGORIES,
  getSavedKundalis,
  deleteKundali,
  getAllTags,
  exportKundalis,
  importKundalis,
} from '@/lib/storage';
import { Modal } from './ui/Modal';
import { Button } from './ui/Button';
import { SaveKundaliModal } from './SaveKundaliModal';

interface KundaliListProps {
  onSelect?: (kundali: SavedKundali) => void;
  selectedIds?: string[];
  maxSelection?: number;
  compact?: boolean;
  showFilters?: boolean;
  showImportExport?: boolean;
}

export function KundaliList({
  onSelect,
  selectedIds = [],
  maxSelection = 0,
  compact = false,
  showFilters = true,
  showImportExport = true,
}: KundaliListProps) {
  const [kundalis, setKundalis] = useState<SavedKundali[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('');
  const [selectedTag, setSelectedTag] = useState<string>('');
  const [sortBy, setSortBy] = useState<'newest' | 'oldest' | 'name'>('newest');
  const [allTags, setAllTags] = useState<string[]>([]);

  // Edit modal state
  const [editingKundali, setEditingKundali] = useState<SavedKundali | null>(null);

  // Delete confirmation state
  const [deleteConfirm, setDeleteConfirm] = useState<SavedKundali | null>(null);

  // Import modal state
  const [showImportModal, setShowImportModal] = useState(false);
  const [importFile, setImportFile] = useState<File | null>(null);
  const [importResult, setImportResult] = useState<{ imported: number; skipped: number; errors: string[] } | null>(null);

  // Load data
  const loadData = () => {
    setKundalis(getSavedKundalis());
    setAllTags(getAllTags());
  };

  useEffect(() => {
    loadData();
  }, []);

  // Filter and sort
  const filteredKundalis = useMemo(() => {
    let result = [...kundalis];

    // Search filter
    if (searchQuery) {
      const query = searchQuery.toLowerCase();
      result = result.filter(k =>
        k.name.toLowerCase().includes(query) ||
        k.city.toLowerCase().includes(query) ||
        k.tags?.some(t => t.toLowerCase().includes(query))
      );
    }

    // Category filter
    if (selectedCategory) {
      result = result.filter(k => k.category === selectedCategory);
    }

    // Tag filter
    if (selectedTag) {
      result = result.filter(k => k.tags?.includes(selectedTag));
    }

    // Sort
    switch (sortBy) {
      case 'oldest':
        result.sort((a, b) => new Date(a.savedAt).getTime() - new Date(b.savedAt).getTime());
        break;
      case 'name':
        result.sort((a, b) => a.name.localeCompare(b.name));
        break;
      default: // newest
        result.sort((a, b) => new Date(b.savedAt).getTime() - new Date(a.savedAt).getTime());
    }

    return result;
  }, [kundalis, searchQuery, selectedCategory, selectedTag, sortBy]);

  // Handle selection
  const handleSelect = (kundali: SavedKundali) => {
    if (!onSelect) return;

    if (maxSelection === 1) {
      // Single selection mode
      onSelect(kundali);
    } else {
      // Multi selection mode
      const isSelected = selectedIds.includes(kundali.id);
      if (isSelected || maxSelection === 0 || selectedIds.length < maxSelection) {
        onSelect(kundali);
      }
    }
  };

  // Handle delete
  const handleDelete = () => {
    if (!deleteConfirm) return;

    deleteKundali(deleteConfirm.id);
    setDeleteConfirm(null);
    loadData();
  };

  // Handle export
  const handleExport = () => {
    const data = exportKundalis();
    const blob = new Blob([data], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `kundalis_${new Date().toISOString().split('T')[0]}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  // Handle import
  const handleImport = async () => {
    if (!importFile) return;

    try {
      const text = await importFile.text();
      const result = importKundalis(text, false);
      setImportResult(result);
      if (result.imported > 0) {
        loadData();
      }
    } catch (error) {
      setImportResult({
        imported: 0,
        skipped: 0,
        errors: [error instanceof Error ? error.message : 'Failed to read file'],
      });
    }
  };

  // Clear all filters
  const clearFilters = () => {
    setSearchQuery('');
    setSelectedCategory('');
    setSelectedTag('');
    setSortBy('newest');
  };

  const hasActiveFilters = searchQuery || selectedCategory || selectedTag;

  return (
    <div className="space-y-4">
      {/* Search and Filters */}
      {showFilters && (
        <div className="bg-white rounded-xl shadow-md p-4 space-y-4">
          {/* Search */}
          <div className="relative">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="नाम, शहर, या टैग से खोजें... / Search by name, city, or tag..."
              className="w-full pl-10 pr-4 py-2.5 border border-gray-200 rounded-lg focus:border-orange-500 focus:ring-1 focus:ring-orange-200 transition-all"
            />
            <svg
              className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>

          {/* Filters Row */}
          <div className="flex flex-wrap gap-3 items-center">
            {/* Category Filter */}
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="px-3 py-2 border border-gray-200 rounded-lg focus:border-orange-500 focus:ring-1 focus:ring-orange-200 text-sm bg-white"
            >
              <option value="">सभी श्रेणियां / All Categories</option>
              {DEFAULT_CATEGORIES.map((cat) => (
                <option key={cat.id} value={cat.id}>
                  {cat.icon} {cat.name}
                </option>
              ))}
            </select>

            {/* Tag Filter */}
            {allTags.length > 0 && (
              <select
                value={selectedTag}
                onChange={(e) => setSelectedTag(e.target.value)}
                className="px-3 py-2 border border-gray-200 rounded-lg focus:border-orange-500 focus:ring-1 focus:ring-orange-200 text-sm bg-white"
              >
                <option value="">सभी टैग / All Tags</option>
                {allTags.map((tag) => (
                  <option key={tag} value={tag}>
                    #{tag}
                  </option>
                ))}
              </select>
            )}

            {/* Sort */}
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value as 'newest' | 'oldest' | 'name')}
              className="px-3 py-2 border border-gray-200 rounded-lg focus:border-orange-500 focus:ring-1 focus:ring-orange-200 text-sm bg-white"
            >
              <option value="newest">नवीनतम / Newest First</option>
              <option value="oldest">सबसे पुराना / Oldest First</option>
              <option value="name">नाम A-Z / Name A-Z</option>
            </select>

            {/* Clear Filters */}
            {hasActiveFilters && (
              <button
                onClick={clearFilters}
                className="px-3 py-2 text-orange-600 hover:text-orange-700 text-sm font-medium"
              >
                फ़िल्टर साफ़ करें / Clear Filters
              </button>
            )}

            {/* Spacer */}
            <div className="flex-1" />

            {/* Import/Export */}
            {showImportExport && (
              <div className="flex gap-2">
                <button
                  onClick={() => setShowImportModal(true)}
                  className="px-3 py-2 text-sm text-gray-600 hover:text-gray-800 border border-gray-200 rounded-lg hover:bg-gray-50 flex items-center gap-1"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
                  </svg>
                  आयात / Import
                </button>
                <button
                  onClick={handleExport}
                  disabled={kundalis.length === 0}
                  className="px-3 py-2 text-sm text-gray-600 hover:text-gray-800 border border-gray-200 rounded-lg hover:bg-gray-50 flex items-center gap-1 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                  </svg>
                  निर्यात / Export
                </button>
              </div>
            )}
          </div>

          {/* Results count */}
          <div className="text-sm text-gray-500">
            {filteredKundalis.length} of {kundalis.length} Kundalis
            {maxSelection > 0 && selectedIds.length > 0 && (
              <span className="ml-2 text-orange-600">
                ({selectedIds.length}/{maxSelection} selected)
              </span>
            )}
          </div>
        </div>
      )}

      {/* Empty State */}
      {kundalis.length === 0 ? (
        <div className="bg-white rounded-xl shadow-md p-8 text-center">
          <div className="text-6xl mb-4">📋</div>
          <h3 className="text-lg font-semibold text-gray-800 mb-2">कोई कुंडली सहेजी नहीं / No Saved Kundalis</h3>
          <p className="text-gray-600 mb-4">
            कुंडली बनाएं और यहां देखने के लिए सेव करें / Generate a Kundali and save it to see it here.
          </p>
          <a
            href="/"
            className="inline-flex items-center gap-2 px-4 py-2 bg-orange-500 text-white rounded-lg hover:bg-orange-600 transition-colors"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
            कुंडली बनाएं / Generate Kundali
          </a>
        </div>
      ) : filteredKundalis.length === 0 ? (
        <div className="bg-white rounded-xl shadow-md p-8 text-center">
          <div className="text-5xl mb-4">🔍</div>
          <h3 className="text-lg font-semibold text-gray-800 mb-2">कोई परिणाम नहीं / No Results Found</h3>
          <p className="text-gray-600 mb-4">
            अपनी खोज या फ़िल्टर बदलें / Try adjusting your search or filters.
          </p>
          <button
            onClick={clearFilters}
            className="text-orange-600 hover:text-orange-700 font-medium"
          >
            सभी फ़िल्टर साफ़ करें / Clear All Filters
          </button>
        </div>
      ) : (
        /* Kundali Grid */
        <div className={compact
          ? 'space-y-2'
          : 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4'
        }>
          {filteredKundalis.map((kundali) => (
            <KundaliCard
              key={kundali.id}
              kundali={kundali}
              onEdit={() => setEditingKundali(kundali)}
              onDelete={() => setDeleteConfirm(kundali)}
              onSelect={onSelect ? () => handleSelect(kundali) : undefined}
              isSelected={selectedIds.includes(kundali.id)}
              showActions={!onSelect}
              compact={compact}
            />
          ))}
        </div>
      )}

      {/* Edit Modal */}
      {editingKundali && (
        <SaveKundaliModal
          isOpen={!!editingKundali}
          onClose={() => setEditingKundali(null)}
          kundaliData={{
            name: editingKundali.name,
            dob: editingKundali.dob,
            tob: editingKundali.tob,
            city: editingKundali.city,
            latitude: editingKundali.latitude,
            longitude: editingKundali.longitude,
            kundali_id: editingKundali.kundali_id,
          }}
          editingKundali={editingKundali}
          onSaved={() => {
            loadData();
            setEditingKundali(null);
          }}
        />
      )}

      {/* Delete Confirmation Modal */}
      {deleteConfirm && (
        <Modal
          isOpen={!!deleteConfirm}
          onClose={() => setDeleteConfirm(null)}
          title="कुंडली मिटाएं / Delete Kundali"
          titleIcon="Warning"
          variant="health"
        >
          <div className="space-y-4">
            <p className="text-gray-700">
              क्या आप{' '}
              <span className="font-semibold">{deleteConfirm.name}</span>{' '}
              की कुंडली मिटाना चाहते हैं? / Are you sure you want to delete?
            </p>
            <p className="text-sm text-gray-500">
              यह क्रिया पूर्ववत नहीं की जा सकती / This action cannot be undone.
            </p>
            <div className="flex justify-end gap-3 pt-4 border-t">
              <Button variant="outline" onClick={() => setDeleteConfirm(null)}>
                रद्द करें / Cancel
              </Button>
              <Button
                variant="health"
                onClick={handleDelete}
              >
                मिटाएं / Delete
              </Button>
            </div>
          </div>
        </Modal>
      )}

      {/* Import Modal */}
      <Modal
        isOpen={showImportModal}
        onClose={() => {
          setShowImportModal(false);
          setImportFile(null);
          setImportResult(null);
        }}
        title="कुंडली आयात करें / Import Kundalis"
        titleIcon="Upload"
      >
        <div className="space-y-4">
          {!importResult ? (
            <>
              <p className="text-gray-600 text-sm">
                कुंडली आयात करने के लिए JSON फ़ाइल चुनें / Select a JSON file to import Kundalis.
              </p>

              <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
                <input
                  type="file"
                  accept=".json"
                  onChange={(e) => setImportFile(e.target.files?.[0] || null)}
                  className="hidden"
                  id="import-file"
                />
                <label
                  htmlFor="import-file"
                  className="cursor-pointer block"
                >
                  <svg className="w-12 h-12 text-gray-400 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                  </svg>
                  <p className="text-gray-600">फ़ाइल चुनें / Click to select file</p>
                  <p className="text-xs text-gray-400 mt-1">केवल .json फ़ाइलें / Only .json files</p>
                </label>
              </div>

              {importFile && (
                <div className="flex items-center gap-2 p-3 bg-orange-50 rounded-lg">
                  <svg className="w-5 h-5 text-orange-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  <span className="flex-1 truncate">{importFile.name}</span>
                  <button
                    onClick={() => setImportFile(null)}
                    className="text-gray-400 hover:text-gray-600"
                  >
                    x
                  </button>
                </div>
              )}

              <div className="flex justify-end gap-3 pt-4 border-t">
                <Button
                  variant="outline"
                  onClick={() => {
                    setShowImportModal(false);
                    setImportFile(null);
                  }}
                >
                  रद्द करें / Cancel
                </Button>
                <Button
                  variant="primary"
                  onClick={handleImport}
                  disabled={!importFile}
                >
                  आयात करें / Import
                </Button>
              </div>
            </>
          ) : (
            <>
              <div className={`p-4 rounded-lg ${importResult.errors.length > 0 ? 'bg-yellow-50' : 'bg-green-50'}`}>
                <h3 className="font-semibold mb-2">आयात परिणाम / Import Results</h3>
                <ul className="text-sm space-y-1">
                  <li className="text-green-700">आयातित / Imported: {importResult.imported}</li>
                  <li className="text-gray-600">छोड़े गए (डुप्लीकेट) / Skipped: {importResult.skipped}</li>
                  {importResult.errors.length > 0 && (
                    <li className="text-red-600">त्रुटियां / Errors: {importResult.errors.length}</li>
                  )}
                </ul>

                {importResult.errors.length > 0 && (
                  <div className="mt-3 p-2 bg-red-50 rounded text-xs text-red-700">
                    {importResult.errors.map((err, i) => (
                      <div key={i}>{err}</div>
                    ))}
                  </div>
                )}
              </div>

              <div className="flex justify-end pt-4 border-t">
                <Button
                  variant="primary"
                  onClick={() => {
                    setShowImportModal(false);
                    setImportFile(null);
                    setImportResult(null);
                  }}
                >
                  हो गया / Done
                </Button>
              </div>
            </>
          )}
        </div>
      </Modal>
    </div>
  );
}
