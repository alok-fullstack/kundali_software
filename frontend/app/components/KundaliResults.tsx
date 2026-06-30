'use client';

import React, { useState } from 'react';
import { Button } from './ui/Button';
import { downloadKundaliPDF } from '@/lib/api';

interface KundaliResultsProps {
  html: string;
  kundaliId?: string;
  onNewKundali: () => void;
  onPrint: () => void;
  onOpenMuhurta: () => void;
  onOpenHealth: () => void;
  onOpenVarga?: () => void;
  onOpenSave?: () => void;
}

export function KundaliResults({
  html,
  kundaliId,
  onNewKundali,
  onPrint,
  onOpenMuhurta,
  onOpenHealth,
  onOpenVarga,
  onOpenSave,
}: KundaliResultsProps) {
  const [isDownloadingPDF, setIsDownloadingPDF] = useState(false);

  const handleDownloadPDF = async () => {
    if (!kundaliId) {
      alert('Kundali ID not available. Please generate a new Kundali.');
      return;
    }

    setIsDownloadingPDF(true);
    try {
      await downloadKundaliPDF(kundaliId);
    } catch (error) {
      console.error('PDF download error:', error);
      alert('Failed to download PDF. Please try again.');
    } finally {
      setIsDownloadingPDF(false);
    }
  };

  return (
    <div className="bg-white rounded-2xl shadow-lg overflow-hidden mb-8">
      {/* Action Buttons */}
      <div className="bg-gradient-primary text-white p-4">
        <div className="flex flex-wrap justify-center gap-3">
          <Button
            variant="secondary"
            onClick={onPrint}
            className="flex items-center gap-2"
          >
            <span>🖨️</span> प्रिंट / Print
          </Button>
          {kundaliId && (
            <Button
              variant="secondary"
              onClick={handleDownloadPDF}
              disabled={isDownloadingPDF}
              className="flex items-center gap-2 bg-red-600 hover:bg-red-700"
            >
              {isDownloadingPDF ? (
                <>
                  <svg className="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  <span>बना रहे हैं... / Generating...</span>
                </>
              ) : (
                <>
                  <span>📄</span> PDF डाउनलोड / Download PDF
                </>
              )}
            </Button>
          )}
          <Button
            variant="success"
            onClick={onNewKundali}
            className="flex items-center gap-2"
          >
            <span>➕</span> नई कुंडली / New Kundali
          </Button>
          <Button
            variant="muhurta"
            onClick={onOpenMuhurta}
            className="flex items-center gap-2"
          >
            <span>🌟</span> शुभ मुहूर्त
          </Button>
          <Button
            variant="health"
            onClick={onOpenHealth}
            className="flex items-center gap-2"
          >
            <span>⚠️</span> स्वास्थ्य/दुर्घटना
          </Button>
          {onOpenVarga && (
            <Button
              variant="primary"
              onClick={onOpenVarga}
              className="flex items-center gap-2 bg-amber-600 hover:bg-amber-700"
            >
              <span>📊</span> वर्ग चार्ट
            </Button>
          )}
          {onOpenSave && (
            <Button
              variant="primary"
              onClick={onOpenSave}
              className="flex items-center gap-2 bg-purple-600 hover:bg-purple-700"
            >
              <span>💾</span> Save / सेव करें
            </Button>
          )}
        </div>
      </div>

      {/* Kundali Content - Rendered from server HTML */}
      <div
        className="kundali-content"
        dangerouslySetInnerHTML={{ __html: html }}
      />
    </div>
  );
}
