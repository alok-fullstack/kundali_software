'use client';

import React from 'react';
import { DashaInfo, CurrentDasha } from '@/lib/types';

interface DashaDisplayProps {
  currentDasha: CurrentDasha;
  mahadashas: DashaInfo[];
}

// This component can be used for structured data display
// Currently the server returns HTML, but this is available for future use
export function DashaDisplay({ currentDasha, mahadashas }: DashaDisplayProps) {
  const planetHindi: Record<string, string> = {
    Ketu: 'केतु',
    Venus: 'शुक्र',
    Sun: 'सूर्य',
    Moon: 'चंद्र',
    Mars: 'मंगल',
    Rahu: 'राहु',
    Jupiter: 'गुरु',
    Saturn: 'शनि',
    Mercury: 'बुध',
  };

  return (
    <div className="space-y-6">
      {/* Current Dasha Card */}
      <div className="bg-gradient-to-br from-saffron-50 to-saffron-100 rounded-xl p-5 border-l-4 border-primary-500">
        <h3 className="text-lg font-bold text-secondary mb-3">
          वर्तमान दशा / Current Dasha: {currentDasha.full_dasha}
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <span className="font-semibold">महादशा / Mahadasha:</span>{' '}
            {planetHindi[currentDasha.mahadasha.planet] || currentDasha.mahadasha.planet}
            <br />
            <span className="text-sm text-gray-600">
              ({currentDasha.mahadasha.start} - {currentDasha.mahadasha.end})
            </span>
          </div>
          <div>
            <span className="font-semibold">अंतर्दशा / Antardasha:</span>{' '}
            {planetHindi[currentDasha.antardasha.planet] || currentDasha.antardasha.planet}
          </div>
        </div>
      </div>

      {/* Mahadasha Timeline */}
      <div className="overflow-x-auto">
        <table className="w-full border-collapse">
          <thead>
            <tr className="bg-gradient-primary text-white">
              <th className="px-4 py-3 text-left">महादशा / Mahadasha</th>
              <th className="px-4 py-3 text-left">आरंभ / Start</th>
              <th className="px-4 py-3 text-left">समाप्ति / End</th>
              <th className="px-4 py-3 text-left">अवधि / Duration</th>
            </tr>
          </thead>
          <tbody>
            {mahadashas.map((dasha, index) => {
              const isCurrent = dasha.planet === currentDasha.mahadasha.planet;
              return (
                <tr
                  key={`${dasha.planet}-${index}`}
                  className={
                    isCurrent
                      ? 'bg-yellow-100 font-semibold'
                      : index % 2 === 0
                      ? 'bg-saffron-50'
                      : 'bg-white'
                  }
                >
                  <td className="px-4 py-3 border-b border-gray-200">
                    <strong>{planetHindi[dasha.planet] || dasha.planet}</strong>
                    {isCurrent && (
                      <span className="ml-2 text-primary-500">← वर्तमान / Current</span>
                    )}
                  </td>
                  <td className="px-4 py-3 border-b border-gray-200">{dasha.start}</td>
                  <td className="px-4 py-3 border-b border-gray-200">{dasha.end}</td>
                  <td className="px-4 py-3 border-b border-gray-200">
                    {dasha.duration_years.toFixed(1)} वर्ष / Years
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
