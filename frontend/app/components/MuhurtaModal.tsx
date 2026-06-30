'use client';

import React, { useState } from 'react';
import { Modal } from './ui/Modal';
import { Button } from './ui/Button';
import { Select } from './ui/Select';
import { findMuhurta } from '@/lib/api';
import { EventType, EVENT_TYPE_OPTIONS, MUHURTA_YEARS } from '@/lib/types';

interface MuhurtaModalProps {
  isOpen: boolean;
  onClose: () => void;
  kundaliId: string;
}

export function MuhurtaModal({ isOpen, onClose, kundaliId }: MuhurtaModalProps) {
  const [eventType, setEventType] = useState<EventType>('marriage');
  const [year, setYear] = useState(2027);
  const [isLoading, setIsLoading] = useState(false);
  const [resultHtml, setResultHtml] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async () => {
    setIsLoading(true);
    setError(null);
    setResultHtml(null);

    try {
      const response = await findMuhurta(kundaliId, eventType, year);
      if (response.success && response.html) {
        setResultHtml(response.html);
      } else {
        setError(response.error || 'Failed to find muhurta');
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

  const eventOptions = EVENT_TYPE_OPTIONS.map((opt) => ({
    value: opt.value,
    label: `${opt.labelHindi} (${opt.label})`,
  }));

  const yearOptions = MUHURTA_YEARS.map((y) => ({
    value: y,
    label: y.toString(),
  }));

  return (
    <Modal
      isOpen={isOpen}
      onClose={handleClose}
      title="शुभ मुहूर्त खोजें / Find Auspicious Muhurta"
      titleIcon="🌟"
      variant="muhurta"
    >
      <div className="space-y-5">
        {/* Search Form */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Select
            label="Event Type"
            labelHindi="कार्य का प्रकार"
            options={eventOptions}
            value={eventType}
            onChange={(e) => setEventType(e.target.value as EventType)}
          />
          <Select
            label="Year"
            labelHindi="वर्ष"
            options={yearOptions}
            value={year}
            onChange={(e) => setYear(parseInt(e.target.value))}
          />
        </div>

        <Button
          variant="muhurta"
          fullWidth
          size="lg"
          onClick={handleSearch}
          isLoading={isLoading}
        >
          <span className="flex items-center justify-center gap-2">
            <span>🔍</span> मुहूर्त खोजें / Find Muhurta
          </span>
        </Button>

        {/* Loading */}
        {isLoading && (
          <div className="text-center py-8">
            <div className="inline-block animate-spin rounded-full h-10 w-10 border-4 border-purple-200 border-t-purple-500" />
            <p className="mt-3 text-gray-600">मुहूर्त खोज रहे हैं... / Searching Muhurta...</p>
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
            className="muhurta-results border-t border-gray-200 pt-5 mt-5"
            dangerouslySetInnerHTML={{ __html: resultHtml }}
          />
        )}
      </div>
    </Modal>
  );
}
