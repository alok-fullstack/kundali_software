'use client';

import React from 'react';
import { PlanetPosition } from '@/lib/types';

interface PlanetTableProps {
  planets: PlanetPosition[];
}

// This component can be used for structured data display
// Currently the server returns HTML, but this is available for future use
export function PlanetTable({ planets }: PlanetTableProps) {
  const planetSymbols: Record<string, string> = {
    SUN: '☉',
    MOON: '☽',
    MARS: '♂',
    MERCURY: '☿',
    JUPITER: '♃',
    VENUS: '♀',
    SATURN: '♄',
    RAHU: '☊',
    KETU: '☋',
  };

  const planetHindi: Record<string, string> = {
    SUN: 'सूर्य',
    MOON: 'चंद्र',
    MARS: 'मंगल',
    MERCURY: 'बुध',
    JUPITER: 'गुरु',
    VENUS: 'शुक्र',
    SATURN: 'शनि',
    RAHU: 'राहु',
    KETU: 'केतु',
  };

  return (
    <div className="overflow-x-auto">
      <table className="w-full border-collapse">
        <thead>
          <tr className="bg-gradient-primary text-white">
            <th className="px-4 py-3 text-left">ग्रह / Planet</th>
            <th className="px-4 py-3 text-left">राशि / Sign</th>
            <th className="px-4 py-3 text-left">अंश / Degree</th>
            <th className="px-4 py-3 text-left">नक्षत्र / Nakshatra</th>
            <th className="px-4 py-3 text-left">भाव / House</th>
            <th className="px-4 py-3 text-left">स्थिति / Status</th>
          </tr>
        </thead>
        <tbody>
          {planets.map((planet, index) => (
            <tr
              key={planet.planet}
              className={index % 2 === 0 ? 'bg-saffron-50' : 'bg-white'}
            >
              <td className="px-4 py-3 border-b border-gray-200">
                <span className="mr-2">{planetSymbols[planet.planet] || ''}</span>
                {planetHindi[planet.planet] || planet.planet}
              </td>
              <td className="px-4 py-3 border-b border-gray-200">{planet.rashi}</td>
              <td className="px-4 py-3 border-b border-gray-200">
                {planet.rashi_degree.toFixed(2)}°
              </td>
              <td className="px-4 py-3 border-b border-gray-200">
                {planet.nakshatra} पाद {planet.pada}
              </td>
              <td className="px-4 py-3 border-b border-gray-200">{planet.house}</td>
              <td className="px-4 py-3 border-b border-gray-200">
                <span
                  className={
                    planet.is_retrograde
                      ? 'text-red-600 font-semibold'
                      : 'text-green-600 font-semibold'
                  }
                >
                  {planet.is_retrograde ? 'वक्री / Retro' : 'मार्गी / Direct'}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
