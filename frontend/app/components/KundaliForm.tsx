'use client';

import React, { useState, useRef, useEffect } from 'react';
import { CustomDatePicker, CustomTimePicker } from './ui/DateTimePicker';
import { KundaliInput } from '@/lib/types';
import { generateKundali } from '@/lib/api';

const GOOGLE_MAPS_API_KEY = process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY || '';

// LocalStorage helpers for form persistence
const STORAGE_KEY = 'kundali_form_data';

interface FormData {
  name: string;
  birthDate: string | null;
  birthTime: { hour: number; minute: number } | null;
  city: string;
  latitude: number | null;
  longitude: number | null;
}

const saveFormToStorage = (data: FormData) => {
  if (typeof window === 'undefined') return;
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify({
      ...data,
      savedAt: new Date().toISOString(),
    }));
  } catch (e) {
    console.error('Failed to save form data:', e);
  }
};

const loadFormFromStorage = (): FormData | null => {
  if (typeof window === 'undefined') return null;
  try {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (!saved) return null;
    const data = JSON.parse(saved);
    return {
      name: data.name || '',
      birthDate: data.birthDate || null,
      birthTime: data.birthTime || null,
      city: data.city || '',
      latitude: data.latitude || null,
      longitude: data.longitude || null,
    };
  } catch (e) {
    console.error('Failed to load form data:', e);
    return null;
  }
};

const clearFormStorage = () => {
  if (typeof window === 'undefined') return;
  try {
    localStorage.removeItem(STORAGE_KEY);
  } catch (e) {
    console.error('Failed to clear form data:', e);
  }
};

interface KundaliFormProps {
  onKundaliGenerated: (
    kundaliId: string,
    html: string,
    name: string,
    formData?: { dob: string; tob: string; city: string; latitude: number | null; longitude: number | null }
  ) => void;
}

export function KundaliForm({ onKundaliGenerated }: KundaliFormProps) {
  const [name, setName] = useState('');
  const [birthDate, setBirthDate] = useState<Date | null>(null);
  const [birthTime, setBirthTime] = useState<{ hour: number; minute: number } | null>(null);
  const [city, setCity] = useState('');
  const [latitude, setLatitude] = useState<number | null>(null);
  const [longitude, setLongitude] = useState<number | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [googleLoaded, setGoogleLoaded] = useState(false);
  const [isDataLoaded, setIsDataLoaded] = useState(false);

  const autocompleteRef = useRef<google.maps.places.Autocomplete | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Load saved form data from localStorage on mount
  useEffect(() => {
    const savedData = loadFormFromStorage();
    if (savedData) {
      setName(savedData.name);
      setBirthDate(savedData.birthDate ? new Date(savedData.birthDate) : null);
      setBirthTime(savedData.birthTime);
      setCity(savedData.city);
      setLatitude(savedData.latitude);
      setLongitude(savedData.longitude);
    }
    setIsDataLoaded(true);
  }, []);

  // Save form data to localStorage whenever it changes
  useEffect(() => {
    if (isDataLoaded) {
      saveFormToStorage({
        name,
        birthDate: birthDate?.toISOString() || null,
        birthTime,
        city,
        latitude,
        longitude,
      });
    }
  }, [name, birthDate, birthTime, city, latitude, longitude, isDataLoaded]);

  // Load Google Maps Script
  useEffect(() => {
    if (typeof window !== 'undefined' && !window.google && GOOGLE_MAPS_API_KEY) {
      const script = document.createElement('script');
      script.src = `https://maps.googleapis.com/maps/api/js?key=${GOOGLE_MAPS_API_KEY}&libraries=places`;
      script.async = true;
      script.defer = true;
      script.onload = () => setGoogleLoaded(true);
      document.head.appendChild(script);
    } else if (window.google) {
      setGoogleLoaded(true);
    }
  }, []);

  // Initialize Google Places Autocomplete
  useEffect(() => {
    if (googleLoaded && inputRef.current && !autocompleteRef.current) {
      autocompleteRef.current = new google.maps.places.Autocomplete(inputRef.current, {
        types: ['(cities)'],
        fields: ['formatted_address', 'geometry', 'name'],
      });

      autocompleteRef.current.addListener('place_changed', () => {
        const place = autocompleteRef.current?.getPlace();
        if (place?.geometry?.location) {
          setCity(place.name || place.formatted_address || '');
          setLatitude(place.geometry.location.lat());
          setLongitude(place.geometry.location.lng());
        }
      });
    }
  }, [googleLoaded]);

  const handleReset = () => {
    setName('');
    setBirthDate(null);
    setBirthTime(null);
    setCity('');
    setLatitude(null);
    setLongitude(null);
    setError(null);
    clearFormStorage();
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!name || !birthDate || !birthTime || !city) {
      setError('कृपया सभी आवश्यक फ़ील्ड भरें / Please fill all required fields');
      return;
    }

    setIsLoading(true);
    setError(null);

    // Format date using LOCAL date parts (not UTC) to avoid timezone shift
    const year = birthDate.getFullYear();
    const month = (birthDate.getMonth() + 1).toString().padStart(2, '0');
    const day = birthDate.getDate().toString().padStart(2, '0');

    const formData: KundaliInput = {
      name,
      dob: `${year}-${month}-${day}`,
      tob: `${birthTime.hour.toString().padStart(2, '0')}:${birthTime.minute.toString().padStart(2, '0')}`,
      city,
      latitude,
      longitude,
    };

    try {
      const result = await generateKundali(formData);
      if (result.success && result.kundali_id && result.html) {
        onKundaliGenerated(result.kundali_id, result.html, name, {
          dob: formData.dob,
          tob: formData.tob,
          city: formData.city,
          latitude: formData.latitude ?? null,
          longitude: formData.longitude ?? null,
        });
      } else {
        setError(result.error || 'Failed to generate kundali');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-2xl shadow-2xl">
      {/* Header */}
      <div className="bg-gradient-to-r from-orange-500 via-orange-400 to-yellow-400 text-white p-5 text-center relative overflow-hidden rounded-t-2xl">
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-0 left-0 w-32 h-32 bg-white rounded-full -translate-x-1/2 -translate-y-1/2" />
          <div className="absolute bottom-0 right-0 w-40 h-40 bg-white rounded-full translate-x-1/3 translate-y-1/3" />
        </div>
        <div className="relative z-10">
          <div className="text-4xl mb-2 drop-shadow-lg">ॐ</div>
          <h1 className="text-xl font-bold mb-1">विस्तृत कुंडली जनरेटर</h1>
          <p className="text-white/90 text-sm">Complete Kundali with Full Predictions</p>
        </div>
      </div>

      {/* Form */}
      <form onSubmit={handleSubmit} className="p-4 md:p-6 pb-6">
        {error && (
          <div className="mb-4 p-3 bg-red-50 border-l-4 border-red-500 rounded-r-lg text-red-700 flex items-center gap-2 animate-in text-sm">
            <span>⚠️</span>
            <span>{error}</span>
          </div>
        )}

        <div className="space-y-4">
          {/* Name Input */}
          <div>
            <label className="block mb-1.5 font-medium text-gray-700 text-sm">
              <span className="text-orange-500">नाम</span>
              <span className="text-gray-400 text-xs ml-1">/ Name *</span>
            </label>
            <div className="relative">
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="अपना नाम लिखें / Enter your name"
                className="w-full px-3 py-2.5 pl-10 border border-gray-200 rounded-lg focus:border-orange-500 focus:ring-1 focus:ring-orange-200 transition-all text-sm"
                required
              />
              <div className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              </div>
            </div>
          </div>

          {/* Date and Time Row */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Date Picker */}
            <div className="relative">
              <label className="block mb-1.5 font-medium text-gray-700 text-sm">
                <span className="text-orange-500">जन्म तिथि</span>
                <span className="text-gray-400 text-xs ml-1">/ DOB *</span>
              </label>
              <CustomDatePicker
                value={birthDate}
                onChange={setBirthDate}
                placeholder="तिथि चुनें / Select date..."
                minYear={1900}
                maxYear={new Date().getFullYear()}
              />
            </div>

            {/* Time Picker */}
            <div className="relative">
              <label className="block mb-1.5 font-medium text-gray-700 text-sm">
                <span className="text-orange-500">जन्म समय</span>
                <span className="text-gray-400 text-xs ml-1">/ Time *</span>
              </label>
              <CustomTimePicker
                value={birthTime}
                onChange={setBirthTime}
                placeholder="समय चुनें / Select time..."
              />
            </div>
          </div>

          {/* Location Picker */}
          <div>
            <label className="block mb-1.5 font-medium text-gray-700 text-sm">
              <span className="text-orange-500">जन्म स्थान</span>
              <span className="text-gray-400 text-xs ml-1">/ Place *</span>
            </label>
            <div className="relative">
              <input
                ref={inputRef}
                type="text"
                value={city}
                onChange={(e) => setCity(e.target.value)}
                placeholder={googleLoaded ? "शहर का नाम टाइप करें..." : "Delhi, Mumbai..."}
                className="w-full px-3 py-2.5 pl-10 border border-gray-200 rounded-lg focus:border-orange-500 focus:ring-1 focus:ring-orange-200 transition-all text-sm"
                required
              />
              <div className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
              </div>
              {googleLoaded && (
                <div className="absolute right-3 top-1/2 -translate-y-1/2">
                  <img src="https://developers.google.com/static/maps/documentation/images/powered_by_google_on_white.png" alt="Google" className="h-3 opacity-50" />
                </div>
              )}
            </div>
            {latitude && longitude && (
              <p className="mt-1.5 text-xs text-green-600 flex items-center gap-1 bg-green-50 px-2 py-1 rounded w-fit">
                <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                {latitude.toFixed(4)}°N, {longitude.toFixed(4)}°E
              </p>
            )}
          </div>

          {/* Manual Coordinates (Advanced) */}
          <details className="bg-gray-50 rounded-lg p-3 border border-gray-200">
            <summary className="cursor-pointer font-medium text-gray-600 hover:text-orange-500 flex items-center gap-1.5 text-xs">
              <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
              मैनुअल निर्देशांक / Manual Coordinates (Optional)
            </summary>
            <div className="grid grid-cols-2 gap-3 mt-3">
              <div>
                <label className="block mb-1 text-xs text-gray-600">अक्षांश / Latitude</label>
                <input
                  type="number"
                  step="0.0001"
                  value={latitude || ''}
                  onChange={(e) => setLatitude(e.target.value ? parseFloat(e.target.value) : null)}
                  placeholder="28.6139"
                  className="w-full px-2.5 py-2 border border-gray-300 rounded text-xs focus:border-orange-500 focus:ring-1 focus:ring-orange-200"
                />
              </div>
              <div>
                <label className="block mb-1 text-xs text-gray-600">देशांतर / Longitude</label>
                <input
                  type="number"
                  step="0.0001"
                  value={longitude || ''}
                  onChange={(e) => setLongitude(e.target.value ? parseFloat(e.target.value) : null)}
                  placeholder="77.2090"
                  className="w-full px-2.5 py-2 border border-gray-300 rounded text-xs focus:border-orange-500 focus:ring-1 focus:ring-orange-200"
                />
              </div>
            </div>
          </details>
        </div>

        {/* Submit and Reset Buttons */}
        <div className="mt-5 flex gap-3">
          <button
            type="submit"
            disabled={isLoading}
            className="flex-1 py-3 px-4 bg-gradient-to-r from-orange-500 to-yellow-500 hover:from-orange-600 hover:to-yellow-600 text-white font-semibold text-sm rounded-lg shadow-md hover:shadow-lg transform hover:-translate-y-0.5 transition-all disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none disabled:hover:shadow-md"
          >
            {isLoading ? (
              <span className="flex items-center justify-center gap-2">
                <svg className="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                कुंडली बना रहे हैं...
              </span>
            ) : (
              <span className="flex items-center justify-center gap-2">
                <span className="text-lg">🔮</span>
                कुंडली बनाएं / Generate Kundali
              </span>
            )}
          </button>
          <button
            type="button"
            onClick={handleReset}
            disabled={isLoading}
            className="py-3 px-4 bg-gray-100 hover:bg-gray-200 text-gray-600 font-medium text-sm rounded-lg border border-gray-300 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            title="फॉर्म साफ़ करें / Clear form"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
          </button>
        </div>

        {/* Info Box */}
        <div className="mt-4 p-2.5 bg-gradient-to-r from-orange-50 to-yellow-50 rounded-lg border border-orange-100">
          <div className="flex items-center justify-center gap-3 text-xs">
            <div className="flex items-center gap-1 text-orange-600">
              <span>🌟</span>
              <span className="font-medium">Swiss Ephemeris</span>
            </div>
            <div className="w-1 h-1 bg-orange-200 rounded-full" />
            <div className="text-gray-500">NASA JPL</div>
            <div className="w-1 h-1 bg-orange-200 rounded-full" />
            <div className="text-green-600 font-medium">Sub-Arc-Second Precision</div>
          </div>
        </div>
      </form>
    </div>
  );
}
