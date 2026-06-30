'use client';

import React, { useState, useRef, useEffect } from 'react';
import Link from 'next/link';
import { CustomDatePicker, CustomTimePicker } from '../components/ui/DateTimePicker';
import { GunaRadarChart } from '../components/GunaRadarChart';
import { matchKundalis, downloadMatchingPDF } from '@/lib/api';
import { MatchResponse, PersonDetails, KootaInterpretation } from '@/lib/types';

const GOOGLE_MAPS_API_KEY = process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY || '';

interface PersonFormData {
  name: string;
  birthDate: Date | null;
  birthTime: { hour: number; minute: number } | null;
  city: string;
  latitude: number | null;
  longitude: number | null;
}

const initialPersonData: PersonFormData = {
  name: '',
  birthDate: null,
  birthTime: null,
  city: '',
  latitude: null,
  longitude: null,
};

// Expandable Koota Card Component
function ExpandableKootaCard({
  koota,
  interpretation,
  isExpanded,
  onToggle,
}: {
  koota: { name: string; name_hindi: string; max_points: number; obtained_points: number; boy_value: string; girl_value: string; is_auspicious: boolean; dosha?: string | null };
  interpretation?: KootaInterpretation;
  isExpanded: boolean;
  onToggle: () => void;
}) {
  const isFavorable = koota.is_auspicious;
  const hasRemedies = interpretation?.remedies && interpretation.remedies.length > 0;

  return (
    <div
      className={`rounded-lg border overflow-hidden transition-all duration-300 ${
        isFavorable ? 'border-green-200 bg-green-50' : 'border-red-200 bg-red-50'
      }`}
    >
      {/* Collapsed Header - Clickable */}
      <div
        onClick={onToggle}
        className={`p-4 cursor-pointer hover:bg-opacity-80 transition-colors flex items-center justify-between ${
          isFavorable ? 'hover:bg-green-100' : 'hover:bg-red-100'
        }`}
      >
        <div className="flex items-center gap-4 flex-1">
          {/* Koota Name */}
          <div className="min-w-[120px]">
            <div className="font-semibold text-gray-800">{koota.name}</div>
            <div className="text-xs text-gray-500">{koota.name_hindi}</div>
          </div>

          {/* Score */}
          <div className={`text-center min-w-[60px] font-bold ${isFavorable ? 'text-green-600' : 'text-red-600'}`}>
            {koota.obtained_points}/{koota.max_points}
          </div>

          {/* Boy & Girl Values */}
          <div className="flex-1 flex items-center gap-2 text-sm">
            <span className="text-gray-600">{koota.boy_value}</span>
            <span className="text-gray-400">vs</span>
            <span className="text-gray-600">{koota.girl_value}</span>
          </div>

          {/* Status */}
          <div className="flex items-center gap-2">
            <span className={`font-bold ${isFavorable ? 'text-green-600' : 'text-red-600'}`}>
              {isFavorable ? 'शुभ / Good' : 'ध्यान दें / Attention'}
            </span>
            {koota.dosha && (
              <span className="text-xs bg-red-100 text-red-700 px-2 py-0.5 rounded">
                {koota.dosha}
              </span>
            )}
          </div>
        </div>

        {/* Expand/Collapse Icon */}
        <div className={`ml-4 transform transition-transform duration-300 ${isExpanded ? 'rotate-180' : ''}`}>
          <svg className="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
          </svg>
        </div>
      </div>

      {/* Expanded Content */}
      <div
        className={`overflow-hidden transition-all duration-300 ease-in-out ${
          isExpanded ? 'max-h-[800px] opacity-100' : 'max-h-0 opacity-0'
        }`}
      >
        <div className={`p-4 border-t ${isFavorable ? 'border-green-200 bg-white' : 'border-red-200 bg-white'}`}>
          {interpretation ? (
            <>
              {/* Title - Hindi */}
              {interpretation.title_hindi && (
                <h4 className={`font-bold text-lg mb-1 ${isFavorable ? 'text-green-700' : 'text-red-700'}`}>
                  {interpretation.title_hindi}
                </h4>
              )}
              {/* Title - English (smaller) */}
              {interpretation.title && (
                <p className="text-xs text-gray-500 mb-3">
                  ({interpretation.title})
                </p>
              )}

              {/* Detailed Interpretation - Hindi First */}
              {interpretation.detailed_interpretation_hindi && (
                <div className="mb-4 p-3 bg-orange-50 rounded-lg border border-orange-200">
                  <p className="text-sm text-gray-800 leading-relaxed">
                    {interpretation.detailed_interpretation_hindi}
                  </p>
                </div>
              )}

              {/* Effects - Hindi */}
              {interpretation.effects_hindi && interpretation.effects_hindi.length > 0 && (
                <div className="mb-4">
                  <h5 className="font-medium text-gray-800 mb-2 text-sm">प्रभाव / Effects:</h5>
                  <ul className="space-y-2">
                    {interpretation.effects_hindi.map((effect, idx) => (
                      <li key={idx} className="flex items-start gap-2 text-sm">
                        <span className={`mt-1 ${isFavorable ? 'text-green-500' : 'text-orange-500'}`}>
                          ➤
                        </span>
                        <span className="text-gray-700">{effect}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Remedies (only shown for low-scoring/unfavorable) */}
              {hasRemedies && !isFavorable && (
                <div className="mt-4 p-3 bg-purple-50 rounded-lg border border-purple-200">
                  <h5 className="font-medium text-purple-800 mb-2 text-sm flex items-center gap-1">
                    <span>उपाय / Suggested Remedies:</span>
                  </h5>
                  <ul className="space-y-1">
                    {interpretation.remedies.slice(0, 4).map((remedy, idx) => (
                      <li key={idx} className="flex items-start gap-2 text-sm text-purple-700">
                        <span className="text-purple-500 mt-0.5">🙏</span>
                        <span>{remedy}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </>
          ) : (
            <p className="text-sm text-gray-500 italic">
              विस्तृत व्याख्या उपलब्ध नहीं है / Detailed interpretation not available.
            </p>
          )}
        </div>
      </div>
    </div>
  );
}

// Expandable Koota Section Component
function ExpandableKootaSection({
  kootaScores,
  kootaInterpretations,
  totalPoints,
}: {
  kootaScores: Array<{ name: string; name_hindi: string; max_points: number; obtained_points: number; boy_value: string; girl_value: string; description: string; is_auspicious: boolean; dosha?: string | null }>;
  kootaInterpretations: KootaInterpretation[];
  totalPoints: number;
}) {
  const [expandedIndex, setExpandedIndex] = useState<number | null>(null);
  const [expandAll, setExpandAll] = useState(false);

  // Create a map of interpretations by name for easy lookup
  const interpretationMap = new Map<string, KootaInterpretation>();
  kootaInterpretations.forEach(ki => {
    interpretationMap.set(ki.name, ki);
  });

  const handleToggle = (index: number) => {
    if (expandAll) {
      setExpandAll(false);
      setExpandedIndex(index);
    } else {
      setExpandedIndex(expandedIndex === index ? null : index);
    }
  };

  const handleExpandAll = () => {
    setExpandAll(!expandAll);
    setExpandedIndex(null);
  };

  return (
    <div className="bg-white rounded-xl shadow-lg overflow-hidden mb-6">
      <div className="p-4 bg-gray-100 border-b flex items-center justify-between">
        <div>
          <h3 className="font-bold text-lg">अष्टकूट मिलान / Ashtakoot Milan - 8 Kootas</h3>
          <p className="text-xs text-gray-500 mt-1">किसी भी कूट पर क्लिक करें विस्तार से जानने के लिए / Click to see details</p>
        </div>
        <div className="flex items-center gap-4">
          <button
            onClick={handleExpandAll}
            className="text-sm text-orange-600 hover:text-orange-700 font-medium flex items-center gap-1"
          >
            {expandAll ? 'सब बंद करें / Collapse All' : 'सब खोलें / Expand All'}
            <svg className={`w-4 h-4 transform transition-transform ${expandAll ? 'rotate-180' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
            </svg>
          </button>
          <div className="text-right">
            <div className="font-bold text-lg">{totalPoints}/36</div>
            <div className="text-xs text-gray-500">कुल गुण / Total Gunas</div>
          </div>
        </div>
      </div>

      <div className="p-4 space-y-3">
        {kootaScores.map((koota, index) => (
          <ExpandableKootaCard
            key={index}
            koota={koota}
            interpretation={interpretationMap.get(koota.name)}
            isExpanded={expandAll || expandedIndex === index}
            onToggle={() => handleToggle(index)}
          />
        ))}
      </div>
    </div>
  );
}

function PersonForm({
  title,
  titleHindi,
  icon,
  data,
  onChange,
  inputRef,
  googleLoaded,
}: {
  title: string;
  titleHindi: string;
  icon: string;
  data: PersonFormData;
  onChange: (data: PersonFormData) => void;
  inputRef: React.RefObject<HTMLInputElement>;
  googleLoaded: boolean;
}) {
  return (
    <div className="bg-white rounded-xl shadow-lg">
      <div className="bg-gradient-to-r from-orange-500 to-yellow-400 text-white p-4 rounded-t-xl">
        <div className="flex items-center gap-2">
          <span className="text-2xl">{icon}</span>
          <div>
            <h2 className="font-bold">{titleHindi}</h2>
            <p className="text-sm text-white/80">{title}&apos;s Details</p>
          </div>
        </div>
      </div>

      <div className="p-4 space-y-4 relative">
        {/* Name */}
        <div>
          <label className="block mb-1.5 font-medium text-gray-700 text-sm">
            <span className="text-orange-500">नाम</span>
            <span className="text-gray-400 text-xs ml-1">/ Name *</span>
          </label>
          <input
            type="text"
            value={data.name}
            onChange={(e) => onChange({ ...data, name: e.target.value })}
            placeholder={title === 'Boy' ? 'वर का नाम लिखें...' : 'कन्या का नाम लिखें...'}
            className="w-full px-3 py-2.5 border border-gray-200 rounded-lg focus:border-orange-500 focus:ring-1 focus:ring-orange-200 transition-all text-sm"
            required
          />
        </div>

        {/* Date */}
        <div>
          <label className="block mb-1.5 font-medium text-gray-700 text-sm">
            <span className="text-orange-500">जन्म तिथि</span>
            <span className="text-gray-400 text-xs ml-1">/ DOB *</span>
          </label>
          <CustomDatePicker
            value={data.birthDate}
            onChange={(date) => onChange({ ...data, birthDate: date })}
            placeholder="तारीख चुनें / Select date..."
            minYear={1900}
            maxYear={new Date().getFullYear()}
          />
        </div>

        {/* Time */}
        <div>
          <label className="block mb-1.5 font-medium text-gray-700 text-sm">
            <span className="text-orange-500">जन्म समय</span>
            <span className="text-gray-400 text-xs ml-1">/ Time *</span>
          </label>
          <CustomTimePicker
            value={data.birthTime}
            onChange={(time) => onChange({ ...data, birthTime: time })}
            placeholder="समय चुनें / Select time..."
          />
        </div>

        {/* City */}
        <div>
          <label className="block mb-1.5 font-medium text-gray-700 text-sm">
            <span className="text-orange-500">जन्म स्थान</span>
            <span className="text-gray-400 text-xs ml-1">/ Place *</span>
          </label>
          <div className="relative">
            <input
              ref={inputRef}
              type="text"
              value={data.city}
              onChange={(e) => onChange({ ...data, city: e.target.value })}
              placeholder={googleLoaded ? "शहर का नाम टाइप करें..." : "Delhi, Mumbai..."}
              className="w-full px-3 py-2.5 border border-gray-200 rounded-lg focus:border-orange-500 focus:ring-1 focus:ring-orange-200 transition-all text-sm"
              required
            />
            {data.latitude && data.longitude && (
              <p className="mt-1 text-xs text-green-600 bg-green-50 px-2 py-1 rounded w-fit">
                {data.latitude.toFixed(4)}°N, {data.longitude.toFixed(4)}°E
              </p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

// Helper functions for localStorage
const STORAGE_KEY = 'kundali_milan_form_data';

const saveToLocalStorage = (boyData: PersonFormData, girlData: PersonFormData) => {
  if (typeof window === 'undefined') return;
  try {
    const data = {
      boy: {
        ...boyData,
        birthDate: boyData.birthDate?.toISOString() || null,
      },
      girl: {
        ...girlData,
        birthDate: girlData.birthDate?.toISOString() || null,
      },
      savedAt: new Date().toISOString(),
    };
    localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
  } catch (e) {
    console.error('Failed to save to localStorage:', e);
  }
};

const loadFromLocalStorage = (): { boy: PersonFormData; girl: PersonFormData } | null => {
  if (typeof window === 'undefined') return null;
  try {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (!saved) return null;

    const data = JSON.parse(saved);
    return {
      boy: {
        ...data.boy,
        birthDate: data.boy.birthDate ? new Date(data.boy.birthDate) : null,
      },
      girl: {
        ...data.girl,
        birthDate: data.girl.birthDate ? new Date(data.girl.birthDate) : null,
      },
    };
  } catch (e) {
    console.error('Failed to load from localStorage:', e);
    return null;
  }
};

const clearLocalStorage = () => {
  if (typeof window === 'undefined') return;
  try {
    localStorage.removeItem(STORAGE_KEY);
  } catch (e) {
    console.error('Failed to clear localStorage:', e);
  }
};

export default function MatchingPage() {
  const [boyData, setBoyData] = useState<PersonFormData>(initialPersonData);
  const [girlData, setGirlData] = useState<PersonFormData>(initialPersonData);
  const [isLoading, setIsLoading] = useState(false);
  const [isDownloadingPDF, setIsDownloadingPDF] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<MatchResponse | null>(null);
  const [googleLoaded, setGoogleLoaded] = useState(false);
  const [isDataLoaded, setIsDataLoaded] = useState(false);

  const boyInputRef = useRef<HTMLInputElement>(null);
  const girlInputRef = useRef<HTMLInputElement>(null);
  const resultsRef = useRef<HTMLDivElement>(null);

  const boyAutocompleteRef = useRef<google.maps.places.Autocomplete | null>(null);
  const girlAutocompleteRef = useRef<google.maps.places.Autocomplete | null>(null);

  // Load saved form data from localStorage on mount
  useEffect(() => {
    const savedData = loadFromLocalStorage();
    if (savedData) {
      setBoyData(savedData.boy);
      setGirlData(savedData.girl);
    }
    setIsDataLoaded(true);
  }, []);

  // Save form data to localStorage whenever it changes
  useEffect(() => {
    if (isDataLoaded) {
      saveToLocalStorage(boyData, girlData);
    }
  }, [boyData, girlData, isDataLoaded]);

  // Load Google Maps
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

  // Initialize autocomplete for boy
  useEffect(() => {
    if (googleLoaded && boyInputRef.current && !boyAutocompleteRef.current) {
      boyAutocompleteRef.current = new google.maps.places.Autocomplete(boyInputRef.current, {
        types: ['(cities)'],
        fields: ['formatted_address', 'geometry', 'name'],
      });

      boyAutocompleteRef.current.addListener('place_changed', () => {
        const place = boyAutocompleteRef.current?.getPlace();
        if (place?.geometry?.location) {
          setBoyData((prev) => ({
            ...prev,
            city: place.name || place.formatted_address || '',
            latitude: place.geometry!.location!.lat(),
            longitude: place.geometry!.location!.lng(),
          }));
        }
      });
    }
  }, [googleLoaded]);

  // Initialize autocomplete for girl
  useEffect(() => {
    if (googleLoaded && girlInputRef.current && !girlAutocompleteRef.current) {
      girlAutocompleteRef.current = new google.maps.places.Autocomplete(girlInputRef.current, {
        types: ['(cities)'],
        fields: ['formatted_address', 'geometry', 'name'],
      });

      girlAutocompleteRef.current.addListener('place_changed', () => {
        const place = girlAutocompleteRef.current?.getPlace();
        if (place?.geometry?.location) {
          setGirlData((prev) => ({
            ...prev,
            city: place.name || place.formatted_address || '',
            latitude: place.geometry!.location!.lat(),
            longitude: place.geometry!.location!.lng(),
          }));
        }
      });
    }
  }, [googleLoaded]);

  const validateForm = (): boolean => {
    if (!boyData.name || !boyData.birthDate || !boyData.birthTime || !boyData.city) {
      setError('Please fill all fields for the boy');
      return false;
    }
    if (!girlData.name || !girlData.birthDate || !girlData.birthTime || !girlData.city) {
      setError('Please fill all fields for the girl');
      return false;
    }
    return true;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) return;

    setIsLoading(true);
    setError(null);

    const formatPerson = (data: PersonFormData): PersonDetails => {
      // Format date using LOCAL date parts (not UTC) to avoid timezone shift
      const bd = data.birthDate!;
      const year = bd.getFullYear();
      const month = (bd.getMonth() + 1).toString().padStart(2, '0');
      const day = bd.getDate().toString().padStart(2, '0');

      return {
        name: data.name,
        dob: `${year}-${month}-${day}`,
        tob: `${data.birthTime!.hour.toString().padStart(2, '0')}:${data.birthTime!.minute.toString().padStart(2, '0')}`,
        city: data.city,
        latitude: data.latitude,
        longitude: data.longitude,
        timezone: 'Asia/Kolkata',
      };
    };

    try {
      const response = await matchKundalis({
        boy: formatPerson(boyData),
        girl: formatPerson(girlData),
      });

      if (response.success) {
        setResult(response);
        setTimeout(() => {
          resultsRef.current?.scrollIntoView({ behavior: 'smooth' });
        }, 100);
      } else {
        setError(response.error || 'Failed to match kundalis');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setBoyData(initialPersonData);
    setGirlData(initialPersonData);
    setResult(null);
    setError(null);
    clearLocalStorage(); // Clear saved form data
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleDownloadPDF = async () => {
    if (!boyData.birthDate || !boyData.birthTime || !girlData.birthDate || !girlData.birthTime) {
      alert('Please complete all form fields to download PDF.');
      return;
    }

    setIsDownloadingPDF(true);
    try {
      // Format date using LOCAL date parts (not UTC) to avoid timezone shift
      const formatPerson = (data: PersonFormData) => {
        const bd = data.birthDate!;
        const year = bd.getFullYear();
        const month = (bd.getMonth() + 1).toString().padStart(2, '0');
        const day = bd.getDate().toString().padStart(2, '0');

        return {
          name: data.name,
          dob: `${year}-${month}-${day}`,
          tob: `${data.birthTime!.hour.toString().padStart(2, '0')}:${data.birthTime!.minute.toString().padStart(2, '0')}`,
          city: data.city,
          latitude: data.latitude,
          longitude: data.longitude,
          timezone: 'Asia/Kolkata',
        };
      };

      await downloadMatchingPDF({
        boy: formatPerson(boyData),
        girl: formatPerson(girlData),
      });
    } catch (error) {
      console.error('PDF download error:', error);
      alert('Failed to download PDF. Please try again.');
    } finally {
      setIsDownloadingPDF(false);
    }
  };

  return (
    <main className="min-h-screen py-5 px-4 bg-gradient-to-br from-orange-50 to-yellow-50">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-6">
          <Link href="/" className="inline-flex items-center text-orange-600 hover:text-orange-700 mb-4">
            <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            वापस जाएं / Back to Kundali
          </Link>
          <h1 className="text-3xl font-bold text-gray-800 mb-2">
            <span className="text-orange-500">कुंडली मिलान / Kundali Milan</span>
          </h1>
          <p className="text-gray-600">विवाह अनुकूलता विश्लेषण - अष्टकूट मिलान</p>
          <p className="text-sm text-gray-500 mt-1">बृहत पाराशर होरा शास्त्र के आधार पर</p>
        </div>

        {/* Form Section */}
        {!result && (
          <form onSubmit={handleSubmit}>
            {error && (
              <div className="mb-4 p-3 bg-red-50 border-l-4 border-red-500 rounded-r-lg text-red-700 flex items-center gap-2">
                <span>Warning</span>
                <span>{error}</span>
              </div>
            )}

            <div className="grid md:grid-cols-2 gap-6 mb-6">
              <PersonForm
                title="Boy"
                titleHindi="वर (Var)"
                icon="🤵"
                data={boyData}
                onChange={setBoyData}
                inputRef={boyInputRef}
                googleLoaded={googleLoaded}
              />
              <PersonForm
                title="Girl"
                titleHindi="कन्या (Kanya)"
                icon="👰"
                data={girlData}
                onChange={setGirlData}
                inputRef={girlInputRef}
                googleLoaded={googleLoaded}
              />
            </div>

            <div className="flex justify-center gap-4">
              <button
                type="submit"
                disabled={isLoading}
                className="px-8 py-3 bg-gradient-to-r from-orange-500 to-yellow-500 hover:from-orange-600 hover:to-yellow-600 text-white font-semibold rounded-lg shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isLoading ? (
                  <span className="flex items-center justify-center gap-2">
                    <svg className="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Matching...
                  </span>
                ) : (
                  <span className="flex items-center justify-center gap-2">
                    <span>मिलान देखें / Check Compatibility</span>
                  </span>
                )}
              </button>
              <button
                type="button"
                onClick={handleReset}
                disabled={isLoading}
                className="px-6 py-3 bg-gray-100 hover:bg-gray-200 text-gray-600 font-semibold rounded-lg border border-gray-300 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                रीसेट / Reset
              </button>
            </div>

            {/* Info Box */}
            <div className="mt-6 p-4 bg-white rounded-lg shadow text-center">
              <h3 className="font-semibold text-gray-800 mb-2">अष्टकूट मिलान क्या है? / What is Ashtakoot Milan?</h3>
              <p className="text-sm text-gray-600">
                अष्टकूट मिलान वैदिक ज्योतिष में विवाह के लिए वर-वधू की कुंडली मिलाने की पारंपरिक 8-कूट प्रणाली है।
                इसमें कुल 36 गुणों का मिलान होता है - वर्ण, वश्य, तारा, योनि, ग्रह मैत्री, गण, भकूट और नाड़ी।
              </p>
              <div className="mt-3 flex justify-center gap-4 text-xs text-gray-500">
                <span>18+ गुण: ठीक है</span>
                <span>|</span>
                <span>25+ गुण: अच्छा</span>
                <span>|</span>
                <span>30+ गुण: उत्तम</span>
              </div>
            </div>
          </form>
        )}

        {/* Results Section */}
        {result && (
          <div ref={resultsRef}>
            {/* Score Summary */}
            <div className="bg-white rounded-xl shadow-lg overflow-hidden mb-6">
              <div className={`p-6 text-center text-white ${
                result.percentage >= 70 ? 'bg-gradient-to-r from-green-500 to-emerald-500' :
                result.percentage >= 50 ? 'bg-gradient-to-r from-amber-500 to-orange-500' :
                'bg-gradient-to-r from-red-500 to-rose-500'
              }`}>
                <h2 className="text-2xl font-bold mb-4">मिलान परिणाम / Matching Result</h2>
                <div className="inline-block bg-white/20 rounded-full px-8 py-4">
                  <div className="text-5xl font-bold">{result.total_points}/36</div>
                  <div className="text-lg mt-1">{result.percentage}% मिलान / Match</div>
                </div>
                <div className="mt-4">
                  <span className={`px-4 py-2 rounded-full text-sm font-medium ${
                    result.percentage >= 70 ? 'bg-green-700' :
                    result.percentage >= 50 ? 'bg-amber-700' :
                    'bg-red-700'
                  }`}>
                    {result.compatibility_level === 'Excellent' ? 'उत्तम / Excellent' :
                     result.compatibility_level === 'Good' ? 'अच्छा / Good' :
                     result.compatibility_level === 'Average' ? 'औसत / Average' :
                     result.compatibility_level === 'Below Average' ? 'कम / Below Average' :
                     result.compatibility_level} अनुकूलता
                  </span>
                </div>
              </div>

            </div>

            {/* Detailed Profile Cards */}
            <div className="grid md:grid-cols-2 gap-6 mb-6">
              {/* Boy's Profile Card */}
              <div className="bg-white rounded-xl shadow-lg overflow-hidden border-t-4 border-blue-500">
                <div className="bg-gradient-to-r from-blue-500 to-blue-600 text-white p-4">
                  <div className="flex items-center gap-3">
                    <div className="w-12 h-12 bg-white/20 rounded-full flex items-center justify-center text-2xl">
                      🤵
                    </div>
                    <div>
                      <h3 className="text-xl font-bold">{result.boy_name}</h3>
                      <p className="text-blue-100 text-sm">वर (Var)</p>
                    </div>
                  </div>
                </div>
                <div className="p-4 space-y-3">
                  <div className="grid grid-cols-2 gap-3 text-sm">
                    <div className="bg-gray-50 rounded-lg p-3">
                      <div className="text-gray-500 text-xs">जन्म तिथि / DOB</div>
                      <div className="font-semibold text-gray-800">{result.boy_details.dob}</div>
                    </div>
                    <div className="bg-gray-50 rounded-lg p-3">
                      <div className="text-gray-500 text-xs">जन्म समय / Time</div>
                      <div className="font-semibold text-gray-800">{result.boy_details.birth_time || '-'}</div>
                    </div>
                    <div className="bg-gray-50 rounded-lg p-3">
                      <div className="text-gray-500 text-xs">जन्म स्थान / Place</div>
                      <div className="font-semibold text-gray-800">{result.boy_details.city}</div>
                    </div>
                    <div className="bg-gray-50 rounded-lg p-3">
                      <div className="text-gray-500 text-xs">लग्न / Lagna</div>
                      <div className="font-semibold text-gray-800">{result.boy_details.lagna_rashi}</div>
                    </div>
                  </div>
                  <div className="border-t pt-3">
                    <h4 className="text-sm font-semibold text-gray-700 mb-2">चंद्र विवरण / Moon Details</h4>
                    <div className="grid grid-cols-2 gap-3 text-sm">
                      <div className="bg-blue-50 rounded-lg p-3 border border-blue-100">
                        <div className="text-blue-600 text-xs">राशि / Rashi</div>
                        <div className="font-semibold text-blue-800">{result.boy_details.moon_rashi}</div>
                      </div>
                      <div className="bg-blue-50 rounded-lg p-3 border border-blue-100">
                        <div className="text-blue-600 text-xs">नक्षत्र / Nakshatra</div>
                        <div className="font-semibold text-blue-800">{result.boy_details.moon_nakshatra}</div>
                      </div>
                    </div>
                  </div>
                  <div className="border-t pt-3">
                    <h4 className="text-sm font-semibold text-gray-700 mb-2">गुण विवरण / Matching Attributes</h4>
                    <div className="grid grid-cols-2 gap-2 text-sm">
                      <div className="flex justify-between items-center bg-orange-50 rounded p-2">
                        <span className="text-orange-700 text-xs">वर्ण / Varna</span>
                        <span className="font-medium text-orange-900">{result.boy_details.varna || '-'}</span>
                      </div>
                      <div className="flex justify-between items-center bg-purple-50 rounded p-2">
                        <span className="text-purple-700 text-xs">गण / Gana</span>
                        <span className="font-medium text-purple-900">{result.boy_details.gana || '-'}</span>
                      </div>
                      <div className="flex justify-between items-center bg-green-50 rounded p-2">
                        <span className="text-green-700 text-xs">नाड़ी / Nadi</span>
                        <span className="font-medium text-green-900">{result.boy_details.nadi || '-'}</span>
                      </div>
                      <div className="flex justify-between items-center bg-pink-50 rounded p-2">
                        <span className="text-pink-700 text-xs">योनि / Yoni</span>
                        <span className="font-medium text-pink-900">{result.boy_details.yoni || '-'}</span>
                      </div>
                      <div className="col-span-2 flex justify-between items-center bg-yellow-50 rounded p-2">
                        <span className="text-yellow-700 text-xs">नक्षत्र स्वामी / Nakshatra Lord</span>
                        <span className="font-medium text-yellow-900">{result.boy_details.nakshatra_lord || '-'}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Girl's Profile Card */}
              <div className="bg-white rounded-xl shadow-lg overflow-hidden border-t-4 border-pink-500">
                <div className="bg-gradient-to-r from-pink-500 to-pink-600 text-white p-4">
                  <div className="flex items-center gap-3">
                    <div className="w-12 h-12 bg-white/20 rounded-full flex items-center justify-center text-2xl">
                      👰
                    </div>
                    <div>
                      <h3 className="text-xl font-bold">{result.girl_name}</h3>
                      <p className="text-pink-100 text-sm">कन्या (Kanya)</p>
                    </div>
                  </div>
                </div>
                <div className="p-4 space-y-3">
                  <div className="grid grid-cols-2 gap-3 text-sm">
                    <div className="bg-gray-50 rounded-lg p-3">
                      <div className="text-gray-500 text-xs">जन्म तिथि / DOB</div>
                      <div className="font-semibold text-gray-800">{result.girl_details.dob}</div>
                    </div>
                    <div className="bg-gray-50 rounded-lg p-3">
                      <div className="text-gray-500 text-xs">जन्म समय / Time</div>
                      <div className="font-semibold text-gray-800">{result.girl_details.birth_time || '-'}</div>
                    </div>
                    <div className="bg-gray-50 rounded-lg p-3">
                      <div className="text-gray-500 text-xs">जन्म स्थान / Place</div>
                      <div className="font-semibold text-gray-800">{result.girl_details.city}</div>
                    </div>
                    <div className="bg-gray-50 rounded-lg p-3">
                      <div className="text-gray-500 text-xs">लग्न / Lagna</div>
                      <div className="font-semibold text-gray-800">{result.girl_details.lagna_rashi}</div>
                    </div>
                  </div>
                  <div className="border-t pt-3">
                    <h4 className="text-sm font-semibold text-gray-700 mb-2">चंद्र विवरण / Moon Details</h4>
                    <div className="grid grid-cols-2 gap-3 text-sm">
                      <div className="bg-pink-50 rounded-lg p-3 border border-pink-100">
                        <div className="text-pink-600 text-xs">राशि / Rashi</div>
                        <div className="font-semibold text-pink-800">{result.girl_details.moon_rashi}</div>
                      </div>
                      <div className="bg-pink-50 rounded-lg p-3 border border-pink-100">
                        <div className="text-pink-600 text-xs">नक्षत्र / Nakshatra</div>
                        <div className="font-semibold text-pink-800">{result.girl_details.moon_nakshatra}</div>
                      </div>
                    </div>
                  </div>
                  <div className="border-t pt-3">
                    <h4 className="text-sm font-semibold text-gray-700 mb-2">गुण विवरण / Matching Attributes</h4>
                    <div className="grid grid-cols-2 gap-2 text-sm">
                      <div className="flex justify-between items-center bg-orange-50 rounded p-2">
                        <span className="text-orange-700 text-xs">वर्ण / Varna</span>
                        <span className="font-medium text-orange-900">{result.girl_details.varna || '-'}</span>
                      </div>
                      <div className="flex justify-between items-center bg-purple-50 rounded p-2">
                        <span className="text-purple-700 text-xs">गण / Gana</span>
                        <span className="font-medium text-purple-900">{result.girl_details.gana || '-'}</span>
                      </div>
                      <div className="flex justify-between items-center bg-green-50 rounded p-2">
                        <span className="text-green-700 text-xs">नाड़ी / Nadi</span>
                        <span className="font-medium text-green-900">{result.girl_details.nadi || '-'}</span>
                      </div>
                      <div className="flex justify-between items-center bg-pink-50 rounded p-2">
                        <span className="text-pink-700 text-xs">योनि / Yoni</span>
                        <span className="font-medium text-pink-900">{result.girl_details.yoni || '-'}</span>
                      </div>
                      <div className="col-span-2 flex justify-between items-center bg-yellow-50 rounded p-2">
                        <span className="text-yellow-700 text-xs">नक्षत्र स्वामी / Nakshatra Lord</span>
                        <span className="font-medium text-yellow-900">{result.girl_details.nakshatra_lord || '-'}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Guna Radar Chart - Visual representation */}
            {result.koota_scores && result.koota_scores.length > 0 && (
              <GunaRadarChart kootaScores={result.koota_scores} />
            )}

            {/* Koota Scores - Expandable Cards */}
            <ExpandableKootaSection
              kootaScores={result.koota_scores}
              kootaInterpretations={result.koota_interpretations || []}
              totalPoints={result.total_points}
            />

            {/* Doshas */}
            {result.doshas.length > 0 && (
              <div className="bg-white rounded-xl shadow-lg overflow-hidden mb-6">
                <div className="p-4 bg-red-100 border-b">
                  <h3 className="font-bold text-lg text-red-800">दोष पाए गए / Doshas Detected</h3>
                </div>
                <div className="p-4 space-y-4">
                  {result.doshas.map((dosha, index) => (
                    <div
                      key={index}
                      className={`p-4 rounded-lg border ${
                        dosha.is_cancelled ? 'bg-green-50 border-green-200' : 'bg-red-50 border-red-200'
                      }`}
                    >
                      <div className="flex items-center justify-between mb-2">
                        <span className="font-bold">{dosha.name}</span>
                        <span className={`px-2 py-1 rounded text-xs text-white ${
                          dosha.is_cancelled ? 'bg-green-500' :
                          dosha.severity === 'Critical' ? 'bg-red-600' :
                          dosha.severity === 'High' ? 'bg-orange-500' :
                          'bg-yellow-500'
                        }`}>
                          {dosha.is_cancelled ? 'निरस्त / Cancelled' :
                           dosha.severity === 'Critical' ? 'गंभीर / Critical' :
                           dosha.severity === 'High' ? 'उच्च / High' :
                           dosha.severity === 'Medium' ? 'मध्यम / Medium' :
                           'सामान्य / Low'}
                        </span>
                      </div>
                      <p className="text-sm text-gray-700">{dosha.description}</p>
                      {dosha.remedies.length > 0 && !dosha.is_cancelled && (
                        <div className="mt-3">
                          <p className="text-xs font-medium text-gray-600 mb-1">उपाय / Remedies:</p>
                          <ul className="text-xs text-gray-600 list-disc list-inside">
                            {dosha.remedies.slice(0, 3).map((remedy, i) => (
                              <li key={i}>{remedy}</li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Marriage Muhurta Suggestions */}
            {result.marriage_timing && (
              <div className="bg-white rounded-xl shadow-lg overflow-hidden mb-6">
                <div className="p-4 bg-gradient-to-r from-pink-100 to-purple-100 border-b">
                  <h3 className="font-bold text-lg text-purple-800 flex items-center gap-2">
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                    Auspicious Marriage Timing / Shubh Vivah Muhurta
                  </h3>
                </div>
                <div className="p-4 space-y-5">
                  {/* Favorable Days */}
                  {result.marriage_timing.favorable_days.length > 0 && (
                    <div>
                      <h4 className="font-semibold text-gray-700 mb-2 flex items-center gap-2">
                        <svg className="w-4 h-4 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
                        </svg>
                        Favorable Days / Shubh Din
                      </h4>
                      <div className="flex flex-wrap gap-2">
                        {result.marriage_timing.favorable_days.map((day, i) => (
                          <span key={i} className="px-3 py-1 bg-green-100 text-green-800 text-sm rounded-full border border-green-200">
                            {day}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Favorable Months */}
                  {result.marriage_timing.favorable_months.length > 0 && (
                    <div>
                      <h4 className="font-semibold text-gray-700 mb-2 flex items-center gap-2">
                        <svg className="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                        </svg>
                        Favorable Months / Shubh Maas
                      </h4>
                      <div className="flex flex-wrap gap-2">
                        {result.marriage_timing.favorable_months.map((month, i) => (
                          <span key={i} className="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full border border-blue-200">
                            {month}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Times to Avoid */}
                  {result.marriage_timing.avoid.length > 0 && (
                    <div>
                      <h4 className="font-semibold text-gray-700 mb-2 flex items-center gap-2">
                        <svg className="w-4 h-4 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                        </svg>
                        Times to Avoid / Tyajya Kaal
                      </h4>
                      <div className="flex flex-wrap gap-2">
                        {result.marriage_timing.avoid.map((item, i) => (
                          <span key={i} className="px-3 py-1 bg-red-100 text-red-800 text-sm rounded-full border border-red-200">
                            {item}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* General Advice */}
                  {result.marriage_timing.general_advice.length > 0 && (
                    <div>
                      <h4 className="font-semibold text-gray-700 mb-2 flex items-center gap-2">
                        <svg className="w-4 h-4 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                        </svg>
                        General Advice / Salah
                      </h4>
                      <ul className="space-y-2">
                        {result.marriage_timing.general_advice.map((advice, i) => (
                          <li key={i} className="flex items-start gap-2 text-sm text-gray-700">
                            <span className="text-amber-500 mt-0.5">*</span>
                            <span>{advice}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* Recommendation */}
            <div className="bg-white rounded-xl shadow-lg overflow-hidden mb-6">
              <div className="p-4 bg-orange-100 border-b">
                <h3 className="font-bold text-lg text-orange-800">सिफारिश / Recommendation</h3>
              </div>
              <div className="p-4">
                <pre className="whitespace-pre-wrap text-sm text-gray-700 font-sans">
                  {result.recommendation}
                </pre>
              </div>
            </div>

            {/* Areas of Strength & Concern */}
            <div className="grid md:grid-cols-2 gap-6 mb-6">
              {result.areas_of_strength.length > 0 && (
                <div className="bg-white rounded-xl shadow-lg overflow-hidden">
                  <div className="p-4 bg-green-100 border-b">
                    <h3 className="font-bold text-green-800">मजबूत पक्ष / Strengths</h3>
                  </div>
                  <ul className="p-4 space-y-2">
                    {result.areas_of_strength.map((item, i) => (
                      <li key={i} className="flex items-start gap-2 text-sm">
                        <span className="text-green-500 mt-0.5">✓</span>
                        <span>{item}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
              {result.areas_of_concern.length > 0 && (
                <div className="bg-white rounded-xl shadow-lg overflow-hidden">
                  <div className="p-4 bg-red-100 border-b">
                    <h3 className="font-bold text-red-800">चिंता के क्षेत्र / Areas of Concern</h3>
                  </div>
                  <ul className="p-4 space-y-2">
                    {result.areas_of_concern.map((item, i) => (
                      <li key={i} className="flex items-start gap-2 text-sm">
                        <span className="text-red-500 mt-0.5">⚠</span>
                        <span>{item}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>

            {/* Remedies */}
            {result.remedies.length > 0 && (
              <div className="bg-white rounded-xl shadow-lg overflow-hidden mb-6">
                <div className="p-4 bg-purple-100 border-b">
                  <h3 className="font-bold text-purple-800">सुझाए गए उपाय / Recommended Remedies</h3>
                </div>
                <ul className="p-4 space-y-2">
                  {result.remedies.slice(0, 10).map((remedy, i) => (
                    <li key={i} className="flex items-start gap-2 text-sm">
                      <span className="text-purple-500">🙏</span>
                      <span>{remedy}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Actions */}
            <div className="flex justify-center gap-4 flex-wrap">
              <button
                onClick={handleReset}
                className="px-6 py-3 bg-gray-500 hover:bg-gray-600 text-white font-semibold rounded-lg transition-colors"
              >
                नया मिलान / New Matching
              </button>
              <button
                onClick={handleDownloadPDF}
                disabled={isDownloadingPDF}
                className="px-6 py-3 bg-red-600 hover:bg-red-700 text-white font-semibold rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
              >
                {isDownloadingPDF ? (
                  <>
                    <svg className="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    <span>Generating PDF...</span>
                  </>
                ) : (
                  <>
                    <span>PDF डाउनलोड / Download PDF</span>
                  </>
                )}
              </button>
              <button
                onClick={() => window.print()}
                className="px-6 py-3 bg-blue-500 hover:bg-blue-600 text-white font-semibold rounded-lg transition-colors"
              >
                प्रिंट करें / Print
              </button>
            </div>

            {/* Disclaimer */}
            <div className="mt-6 p-4 bg-gray-100 rounded-lg text-center text-xs text-gray-500">
              <p>बृहत पाराशर होरा शास्त्र, मुहूर्त चिंतामणि और जातक पारिजात पर आधारित</p>
              <p className="mt-1">यह रिपोर्ट केवल मार्गदर्शन के लिए है। महत्वपूर्ण निर्णयों के लिए कृपया किसी योग्य ज्योतिषी से परामर्श करें।</p>
            </div>
          </div>
        )}
      </div>
    </main>
  );
}

