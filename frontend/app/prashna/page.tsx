'use client';

import React, { useState, useEffect, useRef } from 'react';
import Link from 'next/link';

const GOOGLE_MAPS_API_KEY = process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY || '';

interface PrashnaResult {
  question: string;
  question_type: string;
  query_time: string;
  location: string;
  primary_house: number;
  significators: string[];
  lagna_analysis: {
    sign: string;
    sign_hindi: string;
    lord: string;
    lord_house: number;
    strength: string;
    interpretation: string;
  };
  moon_analysis: {
    house: number;
    sign: string;
    sign_hindi: string;
    nakshatra: string;
    paksha: string;
    is_favorable: boolean;
    interpretation: string;
  };
  arudha: {
    house: number;
    sign: string;
    lord: string;
    lord_house: number;
    strength: string;
  };
  timing: {
    will_happen: boolean;
    timeframe: string;
    timeframe_hindi: string;
    timing_basis: string;
    confidence: string;
  };
  answer: string;
  answer_hindi: string;
  confidence_level: number;
  favorable_factors: string[];
  unfavorable_factors: string[];
  interpretation: string;
  interpretation_hindi: string;
}

const QUESTION_TYPES = [
  { value: 'general', label: 'सामान्य प्रश्न / General', icon: '❓' },
  { value: 'marriage', label: 'विवाह / Marriage', icon: '💍' },
  { value: 'career', label: 'करियर / Career', icon: '💼' },
  { value: 'health', label: 'स्वास्थ्य / Health', icon: '🏥' },
  { value: 'travel', label: 'यात्रा / Travel', icon: '✈️' },
  { value: 'lost_item', label: 'खोई वस्तु / Lost Item', icon: '🔍' },
  { value: 'litigation', label: 'मुकदमा / Litigation', icon: '⚖️' },
  { value: 'education', label: 'शिक्षा / Education', icon: '📚' },
  { value: 'finance', label: 'वित्त / Finance', icon: '💰' },
  { value: 'pregnancy', label: 'गर्भावस्था / Pregnancy', icon: '👶' },
];

export default function PrashnaPage() {
  const [question, setQuestion] = useState('');
  const [questionType, setQuestionType] = useState('general');
  const [city, setCity] = useState('');
  const [latitude, setLatitude] = useState<number | null>(null);
  const [longitude, setLongitude] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<PrashnaResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [googleLoaded, setGoogleLoaded] = useState(false);

  const autocompleteRef = useRef<google.maps.places.Autocomplete | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

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

  const analyzePrashna = async () => {
    if (!question.trim()) {
      setError('कृपया अपना प्रश्न लिखें / Please enter your question');
      return;
    }
    if (!city.trim()) {
      setError('कृपया स्थान चुनें / Please select a location');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await fetch('http://localhost:8000/api/prashna/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          question,
          question_type: questionType,
          city,
          latitude,
          longitude,
        }),
      });

      if (!response.ok) throw new Error('Failed to analyze prashna');

      const data = await response.json();
      if (data.success) {
        setResult(data.prashna);
      } else {
        setError(data.error || 'Analysis failed');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const getConfidenceColor = (level: number) => {
    if (level >= 70) return 'text-green-600 bg-green-100';
    if (level >= 40) return 'text-yellow-600 bg-yellow-100';
    return 'text-red-600 bg-red-100';
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-indigo-50">
      <div className="container mx-auto px-4 py-8 max-w-7xl">
        <Link href="/" className="inline-flex items-center gap-2 text-purple-600 hover:text-purple-700 mb-6">
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
          होम पर वापस जाएं / Back to Home
        </Link>

        <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
          <div className="bg-gradient-to-r from-purple-500 via-indigo-500 to-blue-500 text-white p-6 text-center">
            <div className="text-4xl mb-2">🔮</div>
            <h1 className="text-2xl font-bold mb-1">प्रश्न कुंडली</h1>
            <p className="text-white/90">Prashna Kundali (Horary Astrology)</p>
          </div>

          <div className="p-6">
            {!result && (
              <div className="space-y-6">
                <div className="bg-purple-50 p-4 rounded-xl">
                  <p className="text-gray-700 text-center">
                    प्रश्न कुंडली वैदिक ज्योतिष की एक विशेष शाखा है जो प्रश्न के समय के आधार पर उत्तर देती है।
                    <br />
                    <span className="text-sm text-gray-500">
                      Prashna Kundali is a branch of Vedic astrology that answers based on the time of asking.
                    </span>
                  </p>
                </div>

                <div>
                  <label className="block mb-2 font-medium text-gray-700">
                    <span className="text-purple-600">प्रश्न का प्रकार</span>
                    <span className="text-gray-400 text-sm ml-1">/ Question Type</span>
                  </label>
                  <div className="grid grid-cols-2 md:grid-cols-5 gap-2">
                    {QUESTION_TYPES.map((type) => (
                      <button
                        key={type.value}
                        onClick={() => setQuestionType(type.value)}
                        className={`p-3 rounded-lg text-center transition-all ${
                          questionType === type.value
                            ? 'bg-purple-100 border-2 border-purple-500 text-purple-700'
                            : 'bg-gray-50 border-2 border-gray-200 text-gray-600 hover:border-purple-300'
                        }`}
                      >
                        <span className="text-xl block mb-1">{type.icon}</span>
                        <span className="text-xs">{type.label.split('/')[0]}</span>
                      </button>
                    ))}
                  </div>
                </div>

                <div>
                  <label className="block mb-2 font-medium text-gray-700">
                    <span className="text-purple-600">आपका प्रश्न</span>
                    <span className="text-gray-400 text-sm ml-1">/ Your Question *</span>
                  </label>
                  <textarea
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    placeholder="अपना प्रश्न यहाँ लिखें... / Write your question here..."
                    className="w-full px-4 py-3 border border-gray-200 rounded-lg focus:border-purple-500 focus:ring-1 focus:ring-purple-200 min-h-[100px]"
                  />
                </div>

                <div>
                  <label className="block mb-2 font-medium text-gray-700">
                    <span className="text-purple-600">वर्तमान स्थान</span>
                    <span className="text-gray-400 text-sm ml-1">/ Current Location *</span>
                  </label>
                  <input
                    ref={inputRef}
                    type="text"
                    value={city}
                    onChange={(e) => setCity(e.target.value)}
                    placeholder={googleLoaded ? "शहर का नाम टाइप करें..." : "Delhi, Mumbai..."}
                    className="w-full px-4 py-3 border border-gray-200 rounded-lg focus:border-purple-500 focus:ring-1 focus:ring-purple-200"
                  />
                  {latitude && longitude && (
                    <p className="mt-2 text-xs text-green-600 flex items-center gap-1">
                      <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                      </svg>
                      {latitude.toFixed(4)}°N, {longitude.toFixed(4)}°E
                    </p>
                  )}
                </div>

                {error && (
                  <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded">
                    <p className="text-red-700">{error}</p>
                  </div>
                )}

                <button
                  onClick={analyzePrashna}
                  disabled={loading}
                  className="w-full py-4 bg-gradient-to-r from-purple-500 to-indigo-500 text-white font-semibold rounded-lg hover:from-purple-600 hover:to-indigo-600 disabled:opacity-50"
                >
                  {loading ? (
                    <span className="flex items-center justify-center gap-2">
                      <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                      </svg>
                      कुंडली बना रहे हैं...
                    </span>
                  ) : (
                    '🔮 प्रश्न कुंडली बनाएं / Generate Prashna Kundali'
                  )}
                </button>
              </div>
            )}

            {result && (
              <div className="space-y-6">
                <div className="bg-purple-50 p-4 rounded-xl">
                  <h3 className="font-semibold text-purple-800 mb-2">आपका प्रश्न / Your Question</h3>
                  <p className="text-gray-700">{result.question}</p>
                  <p className="text-sm text-gray-500 mt-2">
                    समय: {new Date(result.query_time).toLocaleString('hi-IN')} | स्थान: {result.location}
                  </p>
                </div>

                <div className={`p-6 rounded-xl text-center ${
                  result.timing.will_happen ? 'bg-green-50' : 'bg-red-50'
                }`}>
                  <div className="text-5xl mb-3">
                    {result.timing.will_happen ? '✅' : '⚠️'}
                  </div>
                  <h3 className={`text-xl font-bold mb-2 ${
                    result.timing.will_happen ? 'text-green-800' : 'text-red-800'
                  }`}>
                    {result.answer_hindi}
                  </h3>
                  <p className="text-gray-600">{result.answer}</p>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-gray-50 p-4 rounded-xl text-center">
                    <div className={`text-3xl font-bold ${getConfidenceColor(result.confidence_level).split(' ')[0]}`}>
                      {result.confidence_level}%
                    </div>
                    <div className="text-sm text-gray-600">विश्वास स्तर / Confidence</div>
                  </div>
                  <div className="bg-gray-50 p-4 rounded-xl text-center">
                    <div className="text-xl font-bold text-purple-700">
                      {result.timing.timeframe_hindi}
                    </div>
                    <div className="text-sm text-gray-600">समय सीमा / Timeframe</div>
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="bg-indigo-50 p-4 rounded-xl">
                    <h4 className="font-semibold text-indigo-800 mb-2">लग्न विश्लेषण / Lagna Analysis</h4>
                    <p className="text-sm text-gray-700">
                      <strong>लग्न:</strong> {result.lagna_analysis.sign_hindi} ({result.lagna_analysis.sign})
                    </p>
                    <p className="text-sm text-gray-700">
                      <strong>स्वामी:</strong> {result.lagna_analysis.lord} ({result.lagna_analysis.lord_house}वें भाव में)
                    </p>
                    <p className="text-sm text-gray-700">
                      <strong>शक्ति:</strong> {result.lagna_analysis.strength}
                    </p>
                  </div>

                  <div className="bg-blue-50 p-4 rounded-xl">
                    <h4 className="font-semibold text-blue-800 mb-2">चंद्र विश्लेषण / Moon Analysis</h4>
                    <p className="text-sm text-gray-700">
                      <strong>चंद्र:</strong> {result.moon_analysis.sign_hindi} ({result.moon_analysis.house}वें भाव में)
                    </p>
                    <p className="text-sm text-gray-700">
                      <strong>नक्षत्र:</strong> {result.moon_analysis.nakshatra}
                    </p>
                    <p className="text-sm text-gray-700">
                      <strong>पक्ष:</strong> {result.moon_analysis.paksha}
                    </p>
                  </div>
                </div>

                <div className="bg-purple-50 p-4 rounded-xl">
                  <h4 className="font-semibold text-purple-800 mb-2">आरूढ़ विश्लेषण / Arudha Analysis</h4>
                  <p className="text-gray-700">
                    आरूढ़ {result.arudha.house}वें भाव ({result.arudha.sign}) में है।
                    इसका स्वामी {result.arudha.lord} {result.arudha.lord_house}वें भाव में है।
                    शक्ति: {result.arudha.strength}
                  </p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {result.favorable_factors.length > 0 && (
                    <div className="bg-green-50 p-4 rounded-xl">
                      <h4 className="font-semibold text-green-800 mb-2">✅ अनुकूल कारक / Favorable</h4>
                      <ul className="space-y-1">
                        {result.favorable_factors.map((f, i) => (
                          <li key={i} className="text-sm text-gray-700">• {f}</li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {result.unfavorable_factors.length > 0 && (
                    <div className="bg-red-50 p-4 rounded-xl">
                      <h4 className="font-semibold text-red-800 mb-2">⚠️ प्रतिकूल कारक / Unfavorable</h4>
                      <ul className="space-y-1">
                        {result.unfavorable_factors.map((f, i) => (
                          <li key={i} className="text-sm text-gray-700">• {f}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>

                <div className="bg-yellow-50 p-4 rounded-xl">
                  <h4 className="font-semibold text-yellow-800 mb-2">विस्तृत व्याख्या / Detailed Interpretation</h4>
                  <p className="text-gray-700">{result.interpretation_hindi}</p>
                </div>

                <button
                  onClick={() => {
                    setResult(null);
                    setQuestion('');
                  }}
                  className="w-full py-3 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
                >
                  नया प्रश्न पूछें / Ask New Question
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </main>
  );
}
