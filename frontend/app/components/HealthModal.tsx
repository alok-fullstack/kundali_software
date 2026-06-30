'use client';

import React, { useState } from 'react';
import { Modal } from './ui/Modal';
import { Button } from './ui/Button';
import { Select } from './ui/Select';
import { getHealthPredictions } from '@/lib/api';
import { HEALTH_START_YEARS, HEALTH_END_YEARS } from '@/lib/types';

interface HealthModalProps {
  isOpen: boolean;
  onClose: () => void;
  kundaliId: string;
}

export function HealthModal({ isOpen, onClose, kundaliId }: HealthModalProps) {
  const [startYear, setStartYear] = useState(2026);
  const [endYear, setEndYear] = useState(2030);
  const [isLoading, setIsLoading] = useState(false);
  const [resultHtml, setResultHtml] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async () => {
    setIsLoading(true);
    setError(null);
    setResultHtml(null);

    try {
      const response = await getHealthPredictions(kundaliId, startYear, endYear);
      if (response.success && response.html) {
        setResultHtml(response.html);
      } else {
        setError(response.error || 'Failed to get health predictions');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  const handleClose = () => {
    setResultHtml(null);
    setError(null);
    onClose();
  };

  const startYearOptions = HEALTH_START_YEARS.map((y) => ({
    value: y,
    label: y.toString(),
  }));

  const endYearOptions = HEALTH_END_YEARS.map((y) => ({
    value: y,
    label: y.toString(),
  }));

  return (
    <Modal
      isOpen={isOpen}
      onClose={handleClose}
      title="स्वास्थ्य एवं दुर्घटना विश्लेषण / Health &amp; Accident Analysis"
      titleIcon="⚠️"
      variant="health"
    >
      <div className="space-y-5">
        {/* Search Form */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Select
            label="Start Year"
            labelHindi="प्रारंभ वर्ष"
            options={startYearOptions}
            value={startYear}
            onChange={(e) => setStartYear(parseInt(e.target.value))}
          />
          <Select
            label="End Year"
            labelHindi="अंत वर्ष"
            options={endYearOptions}
            value={endYear}
            onChange={(e) => setEndYear(parseInt(e.target.value))}
          />
        </div>

        <Button
          variant="health"
          fullWidth
          size="lg"
          onClick={handleSearch}
          isLoading={isLoading}
        >
          <span className="flex items-center justify-center gap-2">
            <span>🔍</span> विश्लेषण करें / Analyze
          </span>
        </Button>

        {/* Loading */}
        {isLoading && (
          <div className="text-center py-8">
            <div className="inline-block animate-spin rounded-full h-10 w-10 border-4 border-red-200 border-t-red-500" />
            <p className="mt-3 text-gray-600">विश्लेषण कर रहे हैं... / Analyzing...</p>
          </div>
        )}

        {/* Error */}
        {error && (
          <div className="p-4 bg-red-50 border border-red-200 rounded-lg text-red-700 text-center">
            {error}
          </div>
        )}

        {/* Results */}
        {resultHtml && (
          <div
            className="health-results border-t border-gray-200 pt-5 mt-5"
            dangerouslySetInnerHTML={{ __html: resultHtml }}
          />
        )}
      </div>
    </Modal>
  );
}
