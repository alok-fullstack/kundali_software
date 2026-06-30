'use client';

import React, { useState, useRef, useEffect } from 'react';

interface DatePickerProps {
  value: Date | null;
  onChange: (date: Date | null) => void;
  placeholder?: string;
  minYear?: number;
  maxYear?: number;
}

interface TimePickerProps {
  value: { hour: number; minute: number } | null;
  onChange: (time: { hour: number; minute: number } | null) => void;
  placeholder?: string;
}

// Custom Date Picker
export function CustomDatePicker({
  value,
  onChange,
  placeholder = 'Select date...',
  minYear = 1900,
  maxYear = new Date().getFullYear(),
}: DatePickerProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [viewDate, setViewDate] = useState(value || new Date());
  const containerRef = useRef<HTMLDivElement>(null);

  const months = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
  ];

  const monthsHindi = [
    'जनवरी', 'फरवरी', 'मार्च', 'अप्रैल', 'मई', 'जून',
    'जुलाई', 'अगस्त', 'सितंबर', 'अक्टूबर', 'नवंबर', 'दिसंबर'
  ];

  const daysOfWeek = ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa'];

  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (containerRef.current && !containerRef.current.contains(e.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const getDaysInMonth = (year: number, month: number) => {
    return new Date(year, month + 1, 0).getDate();
  };

  const getFirstDayOfMonth = (year: number, month: number) => {
    return new Date(year, month, 1).getDay();
  };

  const generateCalendarDays = () => {
    const year = viewDate.getFullYear();
    const month = viewDate.getMonth();
    const daysInMonth = getDaysInMonth(year, month);
    const firstDay = getFirstDayOfMonth(year, month);
    const days: (number | null)[] = [];

    for (let i = 0; i < firstDay; i++) {
      days.push(null);
    }
    for (let i = 1; i <= daysInMonth; i++) {
      days.push(i);
    }
    return days;
  };

  const handleDateSelect = (day: number) => {
    const newDate = new Date(viewDate.getFullYear(), viewDate.getMonth(), day);
    onChange(newDate);
    setIsOpen(false);
  };

  const handleMonthChange = (delta: number) => {
    setViewDate(new Date(viewDate.getFullYear(), viewDate.getMonth() + delta, 1));
  };

  const handleYearChange = (year: number) => {
    setViewDate(new Date(year, viewDate.getMonth(), 1));
  };

  const handleMonthSelect = (month: number) => {
    setViewDate(new Date(viewDate.getFullYear(), month, 1));
  };

  const formatDate = (date: Date) => {
    return `${date.getDate()} ${months[date.getMonth()]} ${date.getFullYear()}`;
  };

  const isToday = (day: number) => {
    const today = new Date();
    return (
      day === today.getDate() &&
      viewDate.getMonth() === today.getMonth() &&
      viewDate.getFullYear() === today.getFullYear()
    );
  };

  const isSelected = (day: number) => {
    if (!value) return false;
    return (
      day === value.getDate() &&
      viewDate.getMonth() === value.getMonth() &&
      viewDate.getFullYear() === value.getFullYear()
    );
  };

  const years = Array.from({ length: maxYear - minYear + 1 }, (_, i) => maxYear - i);

  return (
    <div ref={containerRef} className="relative w-full">
      <button
        type="button"
        onClick={() => setIsOpen(!isOpen)}
        className="w-full px-3 py-2.5 text-left bg-white border border-gray-200 rounded-lg hover:border-orange-300 focus:border-orange-500 focus:ring-1 focus:ring-orange-200 transition-all flex items-center justify-between text-sm"
      >
        <span className={value ? 'text-gray-900' : 'text-gray-400'}>
          {value ? formatDate(value) : placeholder}
        </span>
        <svg className="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
      </button>

      {isOpen && (
        <div className="absolute z-[100] mt-1 left-0 right-0 w-full bg-white rounded-lg shadow-xl border border-orange-200 animate-in">
          {/* Header */}
          <div className="bg-gradient-to-r from-orange-500 to-yellow-500 p-2 text-white rounded-t-lg">
            <div className="flex items-center justify-between mb-1">
              <button
                type="button"
                onClick={() => handleMonthChange(-1)}
                className="p-1.5 hover:bg-white/20 rounded-full transition-colors"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                </svg>
              </button>
              <div className="text-center">
                <div className="font-semibold text-sm">{months[viewDate.getMonth()]}</div>
                <div className="text-xs opacity-80">{monthsHindi[viewDate.getMonth()]}</div>
              </div>
              <button
                type="button"
                onClick={() => handleMonthChange(1)}
                className="p-1.5 hover:bg-white/20 rounded-full transition-colors"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </button>
            </div>

            {/* Month & Year Selectors */}
            <div className="flex gap-2">
              <select
                value={viewDate.getMonth()}
                onChange={(e) => handleMonthSelect(parseInt(e.target.value))}
                className="flex-1 px-2 py-1.5 bg-white/20 rounded text-white text-xs focus:outline-none focus:ring-1 focus:ring-white/50"
              >
                {months.map((month, i) => (
                  <option key={month} value={i} className="text-gray-900">{month}</option>
                ))}
              </select>
              <select
                value={viewDate.getFullYear()}
                onChange={(e) => handleYearChange(parseInt(e.target.value))}
                className="flex-1 px-2 py-1.5 bg-white/20 rounded text-white text-xs focus:outline-none focus:ring-1 focus:ring-white/50"
              >
                {years.map((year) => (
                  <option key={year} value={year} className="text-gray-900">{year}</option>
                ))}
              </select>
            </div>
          </div>

          {/* Calendar Grid */}
          <div className="p-2">
            <div className="grid grid-cols-7 gap-0.5 mb-1">
              {daysOfWeek.map((day) => (
                <div key={day} className="text-center text-xs font-medium text-gray-500 py-1">
                  {day}
                </div>
              ))}
            </div>
            <div className="grid grid-cols-7 gap-0.5">
              {generateCalendarDays().map((day, index) => (
                <button
                  key={index}
                  type="button"
                  disabled={day === null}
                  onClick={() => day && handleDateSelect(day)}
                  className={`
                    w-7 h-7 flex items-center justify-center rounded text-xs font-medium transition-all
                    ${day === null ? 'invisible' : 'hover:bg-orange-100'}
                    ${isSelected(day!) ? 'bg-orange-500 text-white hover:bg-orange-600' : ''}
                    ${isToday(day!) && !isSelected(day!) ? 'border border-orange-500 text-orange-600' : ''}
                    ${!isSelected(day!) && !isToday(day!) ? 'text-gray-700' : ''}
                  `}
                >
                  {day}
                </button>
              ))}
            </div>
          </div>

          {/* Quick Actions */}
          <div className="px-2 pb-2 flex gap-1">
            <button
              type="button"
              onClick={() => {
                onChange(new Date());
                setIsOpen(false);
              }}
              className="flex-1 py-1.5 text-xs bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors font-medium"
            >
              आज / Today
            </button>
            <button
              type="button"
              onClick={() => {
                onChange(null);
                setIsOpen(false);
              }}
              className="flex-1 py-1.5 text-xs bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors font-medium"
            >
              साफ़ / Clear
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

// Standard Time Picker with Dropdowns
export function CustomTimePicker({
  value,
  onChange,
  placeholder = 'Select time...',
}: TimePickerProps) {
  const [isOpen, setIsOpen] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  // Convert 24-hour to 12-hour format for display
  const getDisplayValues = () => {
    if (!value) return { hour: 6, minute: 0, period: 'AM' as const };
    const hour12 = value.hour % 12 || 12;
    const period = value.hour >= 12 ? 'PM' as const : 'AM' as const;
    return { hour: hour12, minute: value.minute, period };
  };

  const displayValues = getDisplayValues();

  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (containerRef.current && !containerRef.current.contains(e.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleTimeChange = (hour12: number, minute: number, period: 'AM' | 'PM') => {
    let hour24 = hour12;
    if (period === 'PM' && hour12 !== 12) hour24 = hour12 + 12;
    if (period === 'AM' && hour12 === 12) hour24 = 0;
    onChange({ hour: hour24, minute });
  };

  const formatTime = () => {
    if (!value) return placeholder;
    const h = value.hour % 12 || 12;
    const m = value.minute.toString().padStart(2, '0');
    const p = value.hour >= 12 ? 'PM' : 'AM';
    return `${h}:${m} ${p}`;
  };

  const hours = Array.from({ length: 12 }, (_, i) => i + 1);
  const minutes = Array.from({ length: 60 }, (_, i) => i);

  return (
    <div ref={containerRef} className="relative w-full">
      <button
        type="button"
        onClick={() => setIsOpen(!isOpen)}
        className="w-full px-3 py-2.5 text-left bg-white border border-gray-200 rounded-lg hover:border-orange-300 focus:border-orange-500 focus:ring-1 focus:ring-orange-200 transition-all flex items-center justify-between text-sm"
      >
        <span className={value ? 'text-gray-900' : 'text-gray-400'}>
          {formatTime()}
        </span>
        <svg className="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      </button>

      {isOpen && (
        <div className="absolute z-[100] mt-1 left-0 w-full min-w-[280px] bg-white rounded-lg shadow-xl border border-orange-200 animate-in">
          {/* Header */}
          <div className="bg-gradient-to-r from-orange-500 to-yellow-500 p-3 text-white text-center rounded-t-lg">
            <div className="text-lg font-semibold">
              {displayValues.hour}:{displayValues.minute.toString().padStart(2, '0')} {displayValues.period}
            </div>
            <div className="text-xs opacity-80">समय चुनें / Select Time</div>
          </div>

          {/* Time Selectors */}
          <div className="p-4">
            <div className="flex items-center justify-center gap-2">
              {/* Hour Select */}
              <div className="flex-1">
                <label className="block text-xs text-gray-500 mb-1 text-center">घंटा / Hour</label>
                <select
                  value={displayValues.hour}
                  onChange={(e) => handleTimeChange(parseInt(e.target.value), displayValues.minute, displayValues.period)}
                  className="w-full px-3 py-2.5 border border-gray-300 rounded-lg text-center text-base font-semibold focus:border-orange-500 focus:ring-1 focus:ring-orange-200 bg-white"
                >
                  {hours.map((h) => (
                    <option key={h} value={h}>{h}</option>
                  ))}
                </select>
              </div>

              <div className="text-2xl font-bold text-gray-400 pt-5">:</div>

              {/* Minute Select */}
              <div className="flex-1">
                <label className="block text-xs text-gray-500 mb-1 text-center">मिनट / Minute</label>
                <select
                  value={displayValues.minute}
                  onChange={(e) => handleTimeChange(displayValues.hour, parseInt(e.target.value), displayValues.period)}
                  className="w-full px-3 py-2.5 border border-gray-300 rounded-lg text-center text-base font-semibold focus:border-orange-500 focus:ring-1 focus:ring-orange-200 bg-white"
                >
                  {minutes.map((m) => (
                    <option key={m} value={m}>{m.toString().padStart(2, '0')}</option>
                  ))}
                </select>
              </div>

              {/* AM/PM Select */}
              <div className="flex-1">
                <label className="block text-xs text-gray-500 mb-1 text-center">AM/PM</label>
                <select
                  value={displayValues.period}
                  onChange={(e) => handleTimeChange(displayValues.hour, displayValues.minute, e.target.value as 'AM' | 'PM')}
                  className="w-full px-3 py-2.5 border border-gray-300 rounded-lg text-center text-base font-semibold focus:border-orange-500 focus:ring-1 focus:ring-orange-200 bg-white"
                >
                  <option value="AM">AM</option>
                  <option value="PM">PM</option>
                </select>
              </div>
            </div>

            {/* Quick Time Buttons */}
            <div className="mt-4 grid grid-cols-4 gap-2">
              {[
                { label: '6 AM', hour: 6, minute: 0 },
                { label: '12 PM', hour: 12, minute: 0 },
                { label: '6 PM', hour: 18, minute: 0 },
                { label: '12 AM', hour: 0, minute: 0 },
              ].map((preset) => (
                <button
                  key={preset.label}
                  type="button"
                  onClick={() => {
                    onChange({ hour: preset.hour, minute: preset.minute });
                  }}
                  className="py-1.5 text-xs bg-gray-100 hover:bg-orange-100 hover:text-orange-600 rounded-lg transition-colors font-medium"
                >
                  {preset.label}
                </button>
              ))}
            </div>
          </div>

          {/* Actions */}
          <div className="px-4 pb-4 flex gap-2">
            <button
              type="button"
              onClick={() => {
                onChange(null);
                setIsOpen(false);
              }}
              className="flex-1 py-2 text-sm bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors font-medium"
            >
              साफ़ / Clear
            </button>
            <button
              type="button"
              onClick={() => setIsOpen(false)}
              className="flex-1 py-2 text-sm bg-orange-500 hover:bg-orange-600 text-white rounded-lg transition-colors font-medium"
            >
              हो गया / Done
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
