'use client';

import React from 'react';
import Link from 'next/link';
import { SavedKundali, DEFAULT_CATEGORIES } from '@/lib/storage';

interface KundaliCardProps {
  kundali: SavedKundali;
  onEdit?: (kundali: SavedKundali) => void;
  onDelete?: (kundali: SavedKundali) => void;
  onSelect?: (kundali: SavedKundali) => void;
  isSelected?: boolean;
  showActions?: boolean;
  compact?: boolean;
}

export function KundaliCard({
  kundali,
  onEdit,
  onDelete,
  onSelect,
  isSelected = false,
  showActions = true,
  compact = false,
}: KundaliCardProps) {
  const category = DEFAULT_CATEGORIES.find(c => c.id === kundali.category);

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-IN', {
      day: '2-digit',
      month: 'short',
      year: 'numeric',
    });
  };

  const formatTime = (timeStr: string) => {
    const [hour, minute] = timeStr.split(':');
    const h = parseInt(hour);
    const ampm = h >= 12 ? 'PM' : 'AM';
    const displayHour = h % 12 || 12;
    return `${displayHour}:${minute} ${ampm}`;
  };

  const handleCardClick = () => {
    if (onSelect) {
      onSelect(kundali);
    }
  };

  if (compact) {
    return (
      <div
        className={`
          p-3 rounded-lg border transition-all cursor-pointer
          ${isSelected
            ? 'border-orange-500 bg-orange-50 ring-2 ring-orange-200'
            : 'border-gray-200 bg-white hover:border-orange-300 hover:shadow-md'
          }
        `}
        onClick={handleCardClick}
      >
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            {onSelect && (
              <div className={`
                w-5 h-5 rounded-full border-2 flex items-center justify-center
                ${isSelected ? 'border-orange-500 bg-orange-500' : 'border-gray-300'}
              `}>
                {isSelected && (
                  <svg className="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                  </svg>
                )}
              </div>
            )}
            <div>
              <div className="font-medium text-gray-800">{kundali.name}</div>
              <div className="text-xs text-gray-500">
                {formatDate(kundali.dob)} | {kundali.city}
              </div>
            </div>
          </div>
          {category && (
            <span
              className="text-xs px-2 py-0.5 rounded-full"
              style={{ backgroundColor: `${category.color}20`, color: category.color }}
            >
              {category.icon}
            </span>
          )}
        </div>
      </div>
    );
  }

  return (
    <div
      className={`
        bg-white rounded-xl shadow-md overflow-hidden border-2 transition-all
        ${isSelected
          ? 'border-orange-500 ring-2 ring-orange-200'
          : 'border-transparent hover:shadow-lg hover:border-orange-200'
        }
        ${onSelect ? 'cursor-pointer' : ''}
      `}
      onClick={onSelect ? handleCardClick : undefined}
    >
      {/* Header */}
      <div className="bg-gradient-to-r from-orange-100 to-yellow-100 p-4">
        <div className="flex items-start justify-between">
          <div className="flex items-center gap-3">
            {onSelect && (
              <div className={`
                w-6 h-6 rounded-full border-2 flex items-center justify-center shrink-0
                ${isSelected ? 'border-orange-500 bg-orange-500' : 'border-gray-400 bg-white'}
              `}>
                {isSelected && (
                  <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                  </svg>
                )}
              </div>
            )}
            <div>
              <h3 className="font-bold text-lg text-gray-800">{kundali.name}</h3>
              {category && (
                <span
                  className="inline-flex items-center gap-1 text-xs px-2 py-0.5 rounded-full mt-1"
                  style={{ backgroundColor: `${category.color}20`, color: category.color }}
                >
                  {category.icon} {category.nameHindi}
                </span>
              )}
            </div>
          </div>

          {/* Actions */}
          {showActions && !onSelect && (
            <div className="flex gap-1">
              {onEdit && (
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    onEdit(kundali);
                  }}
                  className="p-1.5 text-gray-500 hover:text-orange-500 hover:bg-orange-100 rounded transition-colors"
                  title="Edit"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                  </svg>
                </button>
              )}
              {onDelete && (
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    onDelete(kundali);
                  }}
                  className="p-1.5 text-gray-500 hover:text-red-500 hover:bg-red-100 rounded transition-colors"
                  title="Delete"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Body */}
      <div className="p-4">
        <div className="grid grid-cols-2 gap-3 text-sm">
          <div className="bg-gray-50 rounded-lg p-2">
            <div className="text-gray-500 text-xs">Birth Date / जन्म तिथि</div>
            <div className="font-semibold text-gray-800">{formatDate(kundali.dob)}</div>
          </div>
          <div className="bg-gray-50 rounded-lg p-2">
            <div className="text-gray-500 text-xs">Time / समय</div>
            <div className="font-semibold text-gray-800">{formatTime(kundali.tob)}</div>
          </div>
          <div className="col-span-2 bg-gray-50 rounded-lg p-2">
            <div className="text-gray-500 text-xs">Place / स्थान</div>
            <div className="font-semibold text-gray-800">{kundali.city}</div>
          </div>
        </div>

        {/* Cached Astrological Info */}
        {(kundali.moonRashi || kundali.lagnaRashi) && (
          <div className="mt-3 pt-3 border-t border-gray-100">
            <div className="grid grid-cols-2 gap-3 text-sm">
              {kundali.lagnaRashi && (
                <div>
                  <span className="text-gray-500 text-xs">लग्न / Lagna: </span>
                  <span className="font-medium text-orange-600">{kundali.lagnaRashi}</span>
                </div>
              )}
              {kundali.moonRashi && (
                <div>
                  <span className="text-gray-500 text-xs">चंद्र / Moon: </span>
                  <span className="font-medium text-blue-600">{kundali.moonRashi}</span>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Tags */}
        {kundali.tags && kundali.tags.length > 0 && (
          <div className="mt-3 flex flex-wrap gap-1">
            {kundali.tags.map((tag) => (
              <span
                key={tag}
                className="text-xs px-2 py-0.5 bg-gray-100 text-gray-600 rounded-full"
              >
                #{tag}
              </span>
            ))}
          </div>
        )}

        {/* Notes Preview */}
        {kundali.notes && (
          <div className="mt-3 text-xs text-gray-500 line-clamp-2">
            {kundali.notes}
          </div>
        )}
      </div>

      {/* Footer */}
      {showActions && !onSelect && (
        <div className="px-4 pb-4">
          <div className="flex gap-2">
            <Link
              href={`/?reload=${kundali.kundali_id}`}
              className="flex-1 text-center py-2 px-3 bg-orange-100 text-orange-700 rounded-lg hover:bg-orange-200 transition-colors text-sm font-medium"
              onClick={(e) => e.stopPropagation()}
            >
              कुंडली देखें / View
            </Link>
            <Link
              href={`/compare?k1=${kundali.id}`}
              className="py-2 px-3 bg-purple-100 text-purple-700 rounded-lg hover:bg-purple-200 transition-colors text-sm"
              onClick={(e) => e.stopPropagation()}
              title="तुलना / Compare"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" />
              </svg>
            </Link>
          </div>
        </div>
      )}

      {/* Saved Date */}
      <div className="px-4 pb-3 text-xs text-gray-400 text-right">
        सहेजा / Saved: {formatDate(kundali.savedAt)}
      </div>
    </div>
  );
}

// Mini card for inline display
export function KundaliMiniCard({ kundali }: { kundali: SavedKundali }) {
  const category = DEFAULT_CATEGORIES.find(c => c.id === kundali.category);

  return (
    <div className="inline-flex items-center gap-2 px-3 py-1.5 bg-orange-50 rounded-lg border border-orange-200">
      {category && <span>{category.icon}</span>}
      <span className="font-medium text-gray-800">{kundali.name}</span>
      <span className="text-xs text-gray-500">({kundali.city})</span>
    </div>
  );
}
