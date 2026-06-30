'use client';

import React, { useState, useEffect, useRef } from 'react';
import Link from 'next/link';
import { getDailyPanchang } from '@/lib/api';
import { PanchangData, ChoghadiyaItem } from '@/lib/types';

const GOOGLE_MAPS_API_KEY = process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY || '';

// Helper function to format date for API
function formatDateForAPI(date: Date): string {
  const year = date.getFullYear();
  const month = (date.getMonth() + 1).toString().padStart(2, '0');
  const day = date.getDate().toString().padStart(2, '0');
  return `${year}-${month}-${day}`;
}

// Helper to get quality color
function getQualityColor(quality: string, isAuspicious: boolean): string {
  if (isAuspicious) {
    if (quality === 'Most Auspicious') return 'bg-green-500';
    if (quality === 'Auspicious') return 'bg-green-400';
    if (quality === 'Good for travel') return 'bg-blue-400';
    return 'bg-green-300';
  }
  return 'bg-red-400';
}

// Choghadiya Card Component
function ChoghadiyaCard({ chog, isCurrent }: { chog: ChoghadiyaItem; isCurrent: boolean }) {
  const bgColor = chog.is_auspicious ? 'bg-green-50 border-green-200' : 'bg-red-50 border-red-200';
  const textColor = chog.is_auspicious ? 'text-green-700' : 'text-red-700';

  return (
    <div className={`p-3 rounded-lg border ${bgColor} ${isCurrent ? 'ring-2 ring-orange-500 shadow-lg' : ''}`}>
      <div className="flex justify-between items-center">
        <div>
          <div className={`font-semibold ${textColor}`}>{chog.name}</div>
          <div className="text-xs text-gray-500">{chog.hindi}</div>
        </div>
        <div className="text-right">
          <div className="text-sm font-medium">{chog.start} - {chog.end}</div>
          <div className={`text-xs ${chog.is_auspicious ? 'text-green-600' : 'text-red-600'}`}>
            {chog.quality}
          </div>
        </div>
      </div>
      {isCurrent && (
        <div className="mt-2 text-xs bg-orange-100 text-orange-700 px-2 py-1 rounded text-center">
          Current / वर्तमान
        </div>
      )}
    </div>
  );
}

// Inauspicious Period Card
function InauspiciousPeriodCard({
  name,
  hindi,
  start,
  end,
  severity
}: {
  name: string;
  hindi: string;
  start: string;
  end: string;
  severity: 'high' | 'medium' | 'low';
}) {
  const bgColors = {
    high: 'bg-red-100 border-red-300',
    medium: 'bg-orange-100 border-orange-300',
    low: 'bg-yellow-100 border-yellow-300'
  };

  return (
    <div className={`p-3 rounded-lg border ${bgColors[severity]}`}>
      <div className="flex justify-between items-center">
        <div>
          <div className="font-semibold text-gray-800">{name}</div>
          <div className="text-xs text-gray-500">{hindi}</div>
        </div>
        <div className="text-right">
          <div className="text-sm font-medium">{start} - {end}</div>
          <div className={`text-xs ${severity === 'high' ? 'text-red-600' : 'text-orange-600'}`}>
            {severity === 'high' ? 'Avoid / टालें' : 'Caution / सावधान'}
          </div>
        </div>
      </div>
    </div>
  );
}

// Five Limb Card Component
function PanchAngCard({
  title,
  titleHindi,
  value,
  valueHindi,
  subtitle,
  isAuspicious,
  extra
}: {
  title: string;
  titleHindi: string;
  value: string;
  valueHindi: string;
  subtitle?: string;
  isAuspicious?: boolean;
  extra?: React.ReactNode;
}) {
  return (
    <div className={`bg-white rounded-xl shadow-lg p-4 border-l-4 ${isAuspicious === false ? 'border-red-500' : isAuspicious === true ? 'border-green-500' : 'border-orange-500'}`}>
      <div className="text-xs text-gray-500 uppercase tracking-wide">{title}</div>
      <div className="text-xs text-orange-500">{titleHindi}</div>
      <div className="mt-2 text-xl font-bold text-gray-800">{value}</div>
      <div className="text-lg text-orange-600">{valueHindi}</div>
      {subtitle && <div className="mt-1 text-sm text-gray-500">{subtitle}</div>}
      {extra && <div className="mt-2">{extra}</div>}
    </div>
  );
}

export default function PanchangPage() {
  const [selectedDate, setSelectedDate] = useState<Date>(new Date());
  const [panchang, setPanchang] = useState<PanchangData | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [location, setLocation] = useState({
    name: 'Delhi',
    latitude: 28.6139,
    longitude: 77.2090
  });
  const [googleLoaded, setGoogleLoaded] = useState(false);
  const locationInputRef = useRef<HTMLInputElement>(null);
  const autocompleteRef = useRef<google.maps.places.Autocomplete | null>(null);

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

  // Initialize autocomplete
  useEffect(() => {
    if (googleLoaded && locationInputRef.current && !autocompleteRef.current) {
      autocompleteRef.current = new google.maps.places.Autocomplete(locationInputRef.current, {
        types: ['(cities)'],
        fields: ['formatted_address', 'geometry', 'name'],
      });

      autocompleteRef.current.addListener('place_changed', () => {
        const place = autocompleteRef.current?.getPlace();
        if (place?.geometry?.location) {
          setLocation({
            name: place.name || place.formatted_address || '',
            latitude: place.geometry.location.lat(),
            longitude: place.geometry.location.lng(),
          });
        }
      });
    }
  }, [googleLoaded]);

  // Fetch panchang data
  const fetchPanchang = async () => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await getDailyPanchang({
        date: formatDateForAPI(selectedDate),
        latitude: location.latitude,
        longitude: location.longitude,
        timezone: 'Asia/Kolkata',
        location: location.name
      });

      if (response.success && response.data) {
        setPanchang(response.data);
      } else {
        setError(response.error || 'Failed to fetch Panchang');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  // Fetch on initial load and when date/location changes
  useEffect(() => {
    fetchPanchang();
  }, [selectedDate, location]);

  // Date navigation
  const goToPreviousDay = () => {
    const newDate = new Date(selectedDate);
    newDate.setDate(newDate.getDate() - 1);
    setSelectedDate(newDate);
  };

  const goToNextDay = () => {
    const newDate = new Date(selectedDate);
    newDate.setDate(newDate.getDate() + 1);
    setSelectedDate(newDate);
  };

  const goToToday = () => {
    setSelectedDate(new Date());
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
            Back to Kundali / वापस जाएं
          </Link>
          <h1 className="text-3xl font-bold text-gray-800 mb-2">
            <span className="text-orange-500">Daily Panchang / दैनिक पंचांग</span>
          </h1>
          <p className="text-gray-600">Vedic Almanac based on Surya Siddhanta</p>
          <p className="text-sm text-gray-500 mt-1">सूर्य सिद्धांत और मुहूर्त चिंतामणि पर आधारित</p>
        </div>

        {/* Controls */}
        <div className="bg-white rounded-xl shadow-lg p-4 mb-6">
          <div className="flex flex-wrap items-center justify-between gap-4">
            {/* Date Navigation */}
            <div className="flex items-center gap-2">
              <button
                onClick={goToPreviousDay}
                className="p-2 rounded-lg bg-gray-100 hover:bg-gray-200 transition-colors"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                </svg>
              </button>

              <input
                type="date"
                value={formatDateForAPI(selectedDate)}
                onChange={(e) => setSelectedDate(new Date(e.target.value))}
                className="px-4 py-2 border border-gray-200 rounded-lg focus:border-orange-500 focus:ring-1 focus:ring-orange-200"
              />

              <button
                onClick={goToNextDay}
                className="p-2 rounded-lg bg-gray-100 hover:bg-gray-200 transition-colors"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </button>

              <button
                onClick={goToToday}
                className="px-3 py-2 text-sm bg-orange-500 text-white rounded-lg hover:bg-orange-600 transition-colors"
              >
                Today / आज
              </button>
            </div>

            {/* Location */}
            <div className="flex items-center gap-2">
              <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
              <input
                ref={locationInputRef}
                type="text"
                value={location.name}
                onChange={(e) => setLocation({ ...location, name: e.target.value })}
                placeholder="Enter city..."
                className="px-3 py-2 border border-gray-200 rounded-lg focus:border-orange-500 focus:ring-1 focus:ring-orange-200 w-48"
              />
            </div>
          </div>
        </div>

        {/* Loading State */}
        {isLoading && (
          <div className="flex justify-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-4 border-orange-500 border-t-transparent"></div>
          </div>
        )}

        {/* Error State */}
        {error && (
          <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded-lg mb-6">
            <p className="text-red-700">{error}</p>
          </div>
        )}

        {/* Panchang Data */}
        {panchang && !isLoading && (
          <>
            {/* Date Header */}
            <div className="bg-gradient-to-r from-orange-500 to-yellow-500 rounded-xl p-6 text-white mb-6 shadow-lg">
              <div className="flex justify-between items-center">
                <div>
                  <h2 className="text-2xl font-bold">{panchang.vara.name} / {panchang.vara.hindi}</h2>
                  <p className="text-orange-100">{panchang.date_hindi}</p>
                  <p className="text-sm text-orange-200">{panchang.location}</p>
                </div>
                <div className="text-right">
                  <div className={`px-4 py-2 rounded-full ${panchang.auspiciousness.is_shubh_din ? 'bg-green-500' : 'bg-red-500'}`}>
                    <span className="font-bold">{panchang.auspiciousness.score}/100</span>
                  </div>
                  <p className="text-sm mt-1">
                    {panchang.auspiciousness.is_shubh_din ? 'Shubh Din / शुभ दिन' : 'Saadharan Din / साधारण दिन'}
                  </p>
                </div>
              </div>
            </div>

            {/* Sun/Moon Timings */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
              <div className="bg-white rounded-xl shadow p-4 text-center">
                <div className="text-3xl mb-2">🌅</div>
                <div className="text-sm text-gray-500">Sunrise / सूर्योदय</div>
                <div className="text-xl font-bold text-orange-600">{panchang.timings.sunrise}</div>
              </div>
              <div className="bg-white rounded-xl shadow p-4 text-center">
                <div className="text-3xl mb-2">🌇</div>
                <div className="text-sm text-gray-500">Sunset / सूर्यास्त</div>
                <div className="text-xl font-bold text-orange-600">{panchang.timings.sunset}</div>
              </div>
              <div className="bg-white rounded-xl shadow p-4 text-center">
                <div className="text-3xl mb-2">🌙</div>
                <div className="text-sm text-gray-500">Moonrise / चंद्रोदय</div>
                <div className="text-xl font-bold text-orange-600">{panchang.timings.moonrise || 'N/A'}</div>
              </div>
              <div className="bg-white rounded-xl shadow p-4 text-center">
                <div className="text-3xl mb-2">🌑</div>
                <div className="text-sm text-gray-500">Moonset / चंद्रास्त</div>
                <div className="text-xl font-bold text-orange-600">{panchang.timings.moonset || 'N/A'}</div>
              </div>
            </div>

            {/* Five Limbs (Panch Ang) */}
            <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
              <span className="text-orange-500">Panch Ang</span>
              <span className="text-gray-400">/</span>
              <span className="text-orange-400">पंच अंग</span>
              <span className="text-sm font-normal text-gray-500 ml-2">(Five Limbs)</span>
            </h3>

            <div className="grid md:grid-cols-3 lg:grid-cols-5 gap-4 mb-6">
              {/* Tithi */}
              <PanchAngCard
                title="Tithi"
                titleHindi="तिथि"
                value={panchang.tithi.name}
                valueHindi={panchang.tithi.hindi}
                subtitle={`${panchang.tithi.paksha} Paksha | Lord: ${panchang.tithi.lord}`}
                isAuspicious={!panchang.tithi.is_rikta}
                extra={
                  <div className="flex items-center gap-2">
                    <div className="flex-1 bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-orange-500 h-2 rounded-full"
                        style={{ width: `${panchang.tithi.percentage_elapsed}%` }}
                      ></div>
                    </div>
                    <span className="text-xs text-gray-500">{panchang.tithi.percentage_elapsed}%</span>
                  </div>
                }
              />

              {/* Nakshatra */}
              <PanchAngCard
                title="Nakshatra"
                titleHindi="नक्षत्र"
                value={panchang.nakshatra.name}
                valueHindi={panchang.nakshatra.hindi}
                subtitle={`Pada ${panchang.nakshatra.pada} | Lord: ${panchang.nakshatra.lord}`}
                extra={
                  <div className="text-xs text-gray-500">Deity: {panchang.nakshatra.deity}</div>
                }
              />

              {/* Yoga */}
              <PanchAngCard
                title="Yoga"
                titleHindi="योग"
                value={panchang.yoga.name}
                valueHindi={panchang.yoga.hindi}
                isAuspicious={!panchang.yoga.is_inauspicious}
                extra={
                  <div className="text-xs text-gray-500">{panchang.yoga.description}</div>
                }
              />

              {/* Karana */}
              <PanchAngCard
                title="Karana"
                titleHindi="करण"
                value={panchang.karana.name}
                valueHindi={panchang.karana.hindi}
                subtitle={`Type: ${panchang.karana.type}`}
                isAuspicious={panchang.karana.is_auspicious && !panchang.karana.is_vishti}
                extra={
                  panchang.karana.is_vishti && (
                    <div className="text-xs bg-red-100 text-red-700 px-2 py-1 rounded">
                      Bhadra / भद्रा - Avoid important works
                    </div>
                  )
                }
              />

              {/* Moon Rashi */}
              <PanchAngCard
                title="Moon Sign"
                titleHindi="चंद्र राशि"
                value={panchang.moon_rashi.name}
                valueHindi={panchang.moon_rashi.hindi}
                subtitle={`Lord: ${panchang.vara.lord}`}
              />
            </div>

            {/* Inauspicious Periods */}
            <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
              <span className="text-red-500">Avoid These Times</span>
              <span className="text-gray-400">/</span>
              <span className="text-red-400">इन समय से बचें</span>
            </h3>

            <div className="grid md:grid-cols-3 gap-4 mb-6">
              <InauspiciousPeriodCard
                name="Rahu Kaal"
                hindi={panchang.rahu_kaal.hindi}
                start={panchang.rahu_kaal.start}
                end={panchang.rahu_kaal.end}
                severity="high"
              />
              <InauspiciousPeriodCard
                name="Yamaghantaka"
                hindi={panchang.yamaghantaka.hindi}
                start={panchang.yamaghantaka.start}
                end={panchang.yamaghantaka.end}
                severity="medium"
              />
              <InauspiciousPeriodCard
                name="Gulika Kaal"
                hindi={panchang.gulika_kaal.hindi}
                start={panchang.gulika_kaal.start}
                end={panchang.gulika_kaal.end}
                severity="medium"
              />
            </div>

            {/* Abhijit Muhurta */}
            {panchang.abhijit_muhurta && (
              <div className="bg-green-50 border border-green-200 rounded-xl p-4 mb-6">
                <div className="flex items-center gap-3">
                  <div className="text-3xl">🌟</div>
                  <div>
                    <h4 className="font-bold text-green-800">Abhijit Muhurta / अभिजित मुहूर्त</h4>
                    <p className="text-green-700">
                      {panchang.abhijit_muhurta.start} - {panchang.abhijit_muhurta.end}
                    </p>
                    <p className="text-sm text-green-600">Most auspicious time of the day / दिन का सबसे शुभ समय</p>
                  </div>
                </div>
              </div>
            )}

            {/* Choghadiya */}
            <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
              <span className="text-orange-500">Choghadiya</span>
              <span className="text-gray-400">/</span>
              <span className="text-orange-400">चौघड़िया</span>
            </h3>

            <div className="grid md:grid-cols-2 gap-6 mb-6">
              {/* Day Choghadiya */}
              <div className="bg-white rounded-xl shadow-lg overflow-hidden">
                <div className="bg-yellow-100 p-3 border-b">
                  <h4 className="font-bold text-yellow-800 flex items-center gap-2">
                    <span>🌞</span>
                    <span>Day Choghadiya / दिन का चौघड़िया</span>
                  </h4>
                  <p className="text-xs text-yellow-600">
                    {panchang.timings.sunrise} - {panchang.timings.sunset}
                  </p>
                </div>
                <div className="p-3 space-y-2">
                  {panchang.day_choghadiya.map((chog, idx) => (
                    <ChoghadiyaCard
                      key={idx}
                      chog={chog}
                      isCurrent={panchang.current_choghadiya?.name === chog.name && panchang.current_choghadiya?.start === chog.start}
                    />
                  ))}
                </div>
              </div>

              {/* Night Choghadiya */}
              <div className="bg-white rounded-xl shadow-lg overflow-hidden">
                <div className="bg-indigo-100 p-3 border-b">
                  <h4 className="font-bold text-indigo-800 flex items-center gap-2">
                    <span>🌙</span>
                    <span>Night Choghadiya / रात का चौघड़िया</span>
                  </h4>
                  <p className="text-xs text-indigo-600">
                    {panchang.timings.sunset} onwards
                  </p>
                </div>
                <div className="p-3 space-y-2">
                  {panchang.night_choghadiya.map((chog, idx) => (
                    <ChoghadiyaCard
                      key={idx}
                      chog={chog}
                      isCurrent={panchang.current_choghadiya?.name === chog.name && panchang.current_choghadiya?.start === chog.start}
                    />
                  ))}
                </div>
              </div>
            </div>

            {/* Auspiciousness Assessment */}
            <div className="bg-white rounded-xl shadow-lg overflow-hidden mb-6">
              <div className={`p-4 ${panchang.auspiciousness.is_shubh_din ? 'bg-green-100' : 'bg-orange-100'}`}>
                <h3 className="font-bold text-lg">
                  {panchang.auspiciousness.is_shubh_din ? 'Auspicious Day / शुभ दिन' : 'Ordinary Day / साधारण दिन'}
                </h3>
              </div>
              <div className="p-4">
                <div className="grid md:grid-cols-2 gap-6">
                  {/* Positive Factors */}
                  {panchang.auspiciousness.positive_factors.length > 0 && (
                    <div>
                      <h4 className="font-semibold text-green-700 mb-2 flex items-center gap-2">
                        <span className="text-green-500">+</span>
                        Positive Factors / शुभ कारक
                      </h4>
                      <ul className="space-y-1">
                        {panchang.auspiciousness.positive_factors.map((factor, idx) => (
                          <li key={idx} className="text-sm text-gray-700 flex items-start gap-2">
                            <span className="text-green-500 mt-0.5">+</span>
                            <span>{factor}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Negative Factors */}
                  {panchang.auspiciousness.negative_factors.length > 0 && (
                    <div>
                      <h4 className="font-semibold text-red-700 mb-2 flex items-center gap-2">
                        <span className="text-red-500">!</span>
                        Caution / सावधानी
                      </h4>
                      <ul className="space-y-1">
                        {panchang.auspiciousness.negative_factors.map((factor, idx) => (
                          <li key={idx} className="text-sm text-gray-700 flex items-start gap-2">
                            <span className="text-red-500 mt-0.5">!</span>
                            <span>{factor}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>

                {/* Recommendations */}
                {panchang.auspiciousness.recommendations.length > 0 && (
                  <div className="mt-4 pt-4 border-t">
                    <h4 className="font-semibold text-gray-700 mb-2">Recommendations / सुझाव</h4>
                    <ul className="space-y-1">
                      {panchang.auspiciousness.recommendations.map((rec, idx) => (
                        <li key={idx} className="text-sm text-gray-600 flex items-start gap-2">
                          <span className="text-orange-500 mt-0.5">*</span>
                          <span>{rec}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </div>

            {/* Legend */}
            <div className="bg-gray-50 rounded-xl p-4 mb-6">
              <h4 className="font-semibold text-gray-700 mb-3">Choghadiya Legend / चौघड़िया प्रकार</h4>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-sm">
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 bg-green-500 rounded"></div>
                  <span>Amrit (अमृत) - Most Auspicious</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 bg-green-400 rounded"></div>
                  <span>Shubh (शुभ) - Auspicious</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 bg-green-300 rounded"></div>
                  <span>Labh (लाभ) - Gain</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 bg-blue-400 rounded"></div>
                  <span>Char (चर) - Good for Travel</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 bg-red-400 rounded"></div>
                  <span>Udveg (उद्वेग) - Anxiety</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 bg-red-500 rounded"></div>
                  <span>Kaal (काल) - Inauspicious</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 bg-red-300 rounded"></div>
                  <span>Rog (रोग) - Disease</span>
                </div>
              </div>
            </div>

            {/* Disclaimer */}
            <div className="text-center text-xs text-gray-500 mt-6 p-4 bg-gray-50 rounded-lg">
              <p>Based on Surya Siddhanta, Muhurta Chintamani, and Dharmasindhu</p>
              <p className="mt-1">सूर्य सिद्धांत, मुहूर्त चिंतामणि और धर्मसिंधु पर आधारित</p>
              <p className="mt-2 text-gray-400">
                Swiss Ephemeris accuracy | Lahiri Ayanamsa: {panchang.ayanamsa.toFixed(4)} degrees
              </p>
            </div>
          </>
        )}
      </div>
    </main>
  );
}
