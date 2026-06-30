'use client';

import React, { useState, useMemo } from 'react';
import { KootaScore } from '@/lib/types';

interface GunaRadarChartProps {
  kootaScores: KootaScore[];
}

interface TooltipData {
  visible: boolean;
  x: number;
  y: number;
  koota: KootaScore | null;
  percentage: number;
}

// SVG dimensions (constants outside component to avoid useMemo dependency issues)
const SIZE = 400;
const CENTER = SIZE / 2;
const MAX_RADIUS = 150;
const LABEL_RADIUS = MAX_RADIUS + 40;
const NUM_AXES = 8;
const ANGLE_STEP = (2 * Math.PI) / NUM_AXES;
const START_ANGLE = -Math.PI / 2; // Start from top

export function GunaRadarChart({ kootaScores }: GunaRadarChartProps) {
  const [tooltip, setTooltip] = useState<TooltipData>({
    visible: false,
    x: 0,
    y: 0,
    koota: null,
    percentage: 0,
  });

  // Calculate percentage for each koota
  const kootaData = useMemo(() => {
    return kootaScores.map((koota, index) => {
      const percentage = (koota.obtained_points / koota.max_points) * 100;
      const angle = START_ANGLE + index * ANGLE_STEP;
      return {
        ...koota,
        percentage,
        angle,
        // Point on the chart based on percentage
        x: CENTER + (MAX_RADIUS * percentage / 100) * Math.cos(angle),
        y: CENTER + (MAX_RADIUS * percentage / 100) * Math.sin(angle),
        // Label position (outside the chart)
        labelX: CENTER + LABEL_RADIUS * Math.cos(angle),
        labelY: CENTER + LABEL_RADIUS * Math.sin(angle),
        // Axis endpoint
        axisX: CENTER + MAX_RADIUS * Math.cos(angle),
        axisY: CENTER + MAX_RADIUS * Math.sin(angle),
      };
    });
  }, [kootaScores]);

  // Create the polygon path for the data
  const dataPath = useMemo(() => {
    if (kootaData.length === 0) return '';
    return kootaData
      .map((d, i) => `${i === 0 ? 'M' : 'L'} ${d.x} ${d.y}`)
      .join(' ') + ' Z';
  }, [kootaData]);

  // Create concentric circles for reference (25%, 50%, 75%, 100%)
  const referenceCircles = [25, 50, 75, 100];

  // Handle mouse events for tooltip
  const handleMouseEnter = (koota: typeof kootaData[0], event: React.MouseEvent) => {
    const rect = (event.currentTarget as SVGElement).ownerSVGElement?.getBoundingClientRect();
    if (rect) {
      setTooltip({
        visible: true,
        x: event.clientX - rect.left,
        y: event.clientY - rect.top - 10,
        koota,
        percentage: koota.percentage,
      });
    }
  };

  const handleMouseLeave = () => {
    setTooltip({ ...tooltip, visible: false });
  };

  // Determine color based on percentage
  const getAreaColor = (percentage: number) => {
    if (percentage >= 70) return { fill: 'url(#greenGradient)', stroke: '#059669' };
    if (percentage >= 50) return { fill: 'url(#orangeGradient)', stroke: '#ea580c' };
    return { fill: 'url(#redGradient)', stroke: '#dc2626' };
  };

  // Calculate average percentage for overall color
  const averagePercentage = useMemo(() => {
    if (kootaData.length === 0) return 0;
    return kootaData.reduce((sum, d) => sum + d.percentage, 0) / kootaData.length;
  }, [kootaData]);

  const areaColors = getAreaColor(averagePercentage);

  return (
    <div className="bg-white rounded-xl shadow-lg overflow-hidden mb-6">
      <div className="p-4 bg-gradient-to-r from-orange-500 to-yellow-400 border-b">
        <h3 className="font-bold text-lg text-white text-center">
          गुण मिलान चार्ट / Guna Milan Chart
        </h3>
        <p className="text-sm text-white/90 text-center mt-1">
          अनुकूलता रडार / Compatibility Radar
        </p>
      </div>

      <div className="p-4">
        <div className="flex flex-col lg:flex-row items-center justify-center gap-6">
          {/* Radar Chart */}
          <div className="relative">
            <svg
              width={SIZE}
              height={SIZE}
              viewBox={`0 0 ${SIZE} ${SIZE}`}
              className="overflow-visible"
            >
              {/* Gradient Definitions */}
              <defs>
                <radialGradient id="greenGradient" cx="50%" cy="50%" r="50%">
                  <stop offset="0%" stopColor="#10b981" stopOpacity="0.8" />
                  <stop offset="100%" stopColor="#059669" stopOpacity="0.4" />
                </radialGradient>
                <radialGradient id="orangeGradient" cx="50%" cy="50%" r="50%">
                  <stop offset="0%" stopColor="#f59e0b" stopOpacity="0.8" />
                  <stop offset="100%" stopColor="#ea580c" stopOpacity="0.4" />
                </radialGradient>
                <radialGradient id="redGradient" cx="50%" cy="50%" r="50%">
                  <stop offset="0%" stopColor="#ef4444" stopOpacity="0.8" />
                  <stop offset="100%" stopColor="#dc2626" stopOpacity="0.4" />
                </radialGradient>
                {/* Drop shadow filter */}
                <filter id="dropShadow" x="-20%" y="-20%" width="140%" height="140%">
                  <feDropShadow dx="0" dy="2" stdDeviation="3" floodOpacity="0.3"/>
                </filter>
              </defs>

              {/* Reference circles */}
              {referenceCircles.map((pct) => (
                <circle
                  key={pct}
                  cx={CENTER}
                  cy={CENTER}
                  r={(MAX_RADIUS * pct) / 100}
                  fill="none"
                  stroke="#e5e7eb"
                  strokeWidth="1"
                  strokeDasharray={pct === 100 ? 'none' : '4,4'}
                />
              ))}

              {/* Reference circle labels */}
              {referenceCircles.map((pct) => (
                <text
                  key={`label-${pct}`}
                  x={CENTER + 5}
                  y={CENTER - (MAX_RADIUS * pct) / 100 + 4}
                  fontSize="10"
                  fill="#9ca3af"
                >
                  {pct}%
                </text>
              ))}

              {/* Axis lines */}
              {kootaData.map((d, i) => (
                <line
                  key={`axis-${i}`}
                  x1={CENTER}
                  y1={CENTER}
                  x2={d.axisX}
                  y2={d.axisY}
                  stroke="#d1d5db"
                  strokeWidth="1"
                />
              ))}

              {/* Data polygon with gradient fill */}
              {kootaData.length > 0 && (
                <path
                  d={dataPath}
                  fill={areaColors.fill}
                  stroke={areaColors.stroke}
                  strokeWidth="2"
                  filter="url(#dropShadow)"
                />
              )}

              {/* Data points */}
              {kootaData.map((d, i) => (
                <g key={`point-${i}`}>
                  <circle
                    cx={d.x}
                    cy={d.y}
                    r="8"
                    fill={d.is_auspicious ? '#10b981' : '#ef4444'}
                    stroke="white"
                    strokeWidth="2"
                    className="cursor-pointer transition-all hover:r-10"
                    onMouseEnter={(e) => handleMouseEnter(d, e)}
                    onMouseLeave={handleMouseLeave}
                  />
                  {/* Percentage inside the point */}
                  <text
                    x={d.x}
                    y={d.y + 1}
                    fontSize="8"
                    fill="white"
                    textAnchor="middle"
                    dominantBaseline="middle"
                    className="pointer-events-none font-bold"
                  >
                    {Math.round(d.percentage)}
                  </text>
                </g>
              ))}

              {/* Axis labels */}
              {kootaData.map((d, i) => {
                // Determine text anchor based on position
                let textAnchor: 'start' | 'middle' | 'end' = 'middle';
                if (d.labelX < CENTER - 20) textAnchor = 'end';
                else if (d.labelX > CENTER + 20) textAnchor = 'start';

                return (
                  <g key={`label-${i}`}>
                    <text
                      x={d.labelX}
                      y={d.labelY - 6}
                      fontSize="11"
                      fontWeight="600"
                      fill="#374151"
                      textAnchor={textAnchor}
                    >
                      {d.name}
                    </text>
                    <text
                      x={d.labelX}
                      y={d.labelY + 8}
                      fontSize="10"
                      fill="#6b7280"
                      textAnchor={textAnchor}
                    >
                      {d.name_hindi}
                    </text>
                    <text
                      x={d.labelX}
                      y={d.labelY + 20}
                      fontSize="9"
                      fill="#9ca3af"
                      textAnchor={textAnchor}
                    >
                      ({d.obtained_points}/{d.max_points})
                    </text>
                  </g>
                );
              })}

              {/* Center label */}
              <text
                x={CENTER}
                y={CENTER - 12}
                fontSize="14"
                fontWeight="bold"
                fill="#374151"
                textAnchor="middle"
              >
                {Math.round(averagePercentage)}%
              </text>
              <text
                x={CENTER}
                y={CENTER + 4}
                fontSize="10"
                fill="#6b7280"
                textAnchor="middle"
              >
                औसत
              </text>
              <text
                x={CENTER}
                y={CENTER + 16}
                fontSize="9"
                fill="#9ca3af"
                textAnchor="middle"
              >
                Average
              </text>
            </svg>

            {/* Tooltip */}
            {tooltip.visible && tooltip.koota && (
              <div
                className="absolute bg-gray-900 text-white text-xs rounded-lg px-3 py-2 pointer-events-none z-10 shadow-lg"
                style={{
                  left: tooltip.x,
                  top: tooltip.y,
                  transform: 'translate(-50%, -100%)',
                }}
              >
                <div className="font-bold">{tooltip.koota.name_hindi} / {tooltip.koota.name}</div>
                <div className="mt-1">
                  अंक / Score: {tooltip.koota.obtained_points}/{tooltip.koota.max_points}
                </div>
                <div>मेल / Match: {Math.round(tooltip.percentage)}%</div>
                <div className={tooltip.koota.is_auspicious ? 'text-green-400' : 'text-red-400'}>
                  {tooltip.koota.is_auspicious ? 'शुभ / Auspicious' : 'ध्यान दें / Needs Attention'}
                </div>
                {tooltip.koota.dosha && (
                  <div className="text-yellow-400 mt-1">{tooltip.koota.dosha}</div>
                )}
                {/* Arrow */}
                <div className="absolute left-1/2 bottom-0 transform -translate-x-1/2 translate-y-full">
                  <div className="border-8 border-transparent border-t-gray-900" />
                </div>
              </div>
            )}
          </div>

          {/* Legend */}
          <div className="bg-gray-50 rounded-lg p-4 min-w-[280px]">
            <h4 className="font-semibold text-gray-800 mb-1 text-center">विवरण / Legend</h4>
            <p className="text-xs text-gray-500 text-center mb-3">रंग संकेत / Color Guide</p>

            {/* Color coding */}
            <div className="space-y-2 mb-4">
              <div className="flex items-center gap-2">
                <div className="w-4 h-4 rounded-full bg-green-500"></div>
                <span className="text-sm text-gray-600">70%+ : उत्तम मेल / Excellent</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-4 h-4 rounded-full bg-orange-500"></div>
                <span className="text-sm text-gray-600">50-70% : अच्छा मेल / Good</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-4 h-4 rounded-full bg-red-500"></div>
                <span className="text-sm text-gray-600">&lt;50% : उपाय आवश्यक / Remedies</span>
              </div>
            </div>

            <hr className="my-3 border-gray-200" />

            {/* Koota meanings */}
            <h5 className="font-medium text-gray-700 mb-2 text-sm">अष्टकूट / 8 Kootas</h5>
            <div className="space-y-1.5 text-xs text-gray-600">
              <div><span className="font-medium">वर्ण / Varna:</span> आध्यात्मिक मेल / Spiritual</div>
              <div><span className="font-medium">वश्य / Vashya:</span> आकर्षण / Attraction</div>
              <div><span className="font-medium">तारा / Tara:</span> जन्म नक्षत्र / Birth Star</div>
              <div><span className="font-medium">योनि / Yoni:</span> शारीरिक मेल / Physical</div>
              <div><span className="font-medium">ग्रह मैत्री / Graha Maitri:</span> मानसिक मेल / Mental</div>
              <div><span className="font-medium">गण / Gana:</span> स्वभाव / Temperament</div>
              <div><span className="font-medium">भकूट / Bhakoot:</span> परिवार कल्याण / Family</div>
              <div><span className="font-medium">नाड़ी / Nadi:</span> स्वास्थ्य व संतान / Health</div>
            </div>

            <hr className="my-3 border-gray-200" />

            {/* Summary stats */}
            <div className="text-center">
              <p className="text-xs text-gray-500 mb-1">सारांश / Summary</p>
              <div className="text-sm text-gray-600">
                <span className="text-green-600 font-semibold">
                  {kootaData.filter(k => k.is_auspicious).length}
                </span>
                {' '}शुभ / Auspicious
                <span className="mx-2">|</span>
                <span className="text-red-600 font-semibold">
                  {kootaData.filter(k => !k.is_auspicious).length}
                </span>
                {' '}ध्यान दें / Attention
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
