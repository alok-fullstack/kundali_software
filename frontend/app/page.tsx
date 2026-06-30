'use client';

import React, { useState, useRef } from 'react';
import Link from 'next/link';
import { KundaliForm } from './components/KundaliForm';
import { KundaliResults } from './components/KundaliResults';
import { ChatAssistant } from './components/ChatAssistant';
import { MuhurtaModal } from './components/MuhurtaModal';
import { HealthModal } from './components/HealthModal';
import { DivisionalChartModal } from './components/DivisionalChartModal';

// Store form data for saving
interface FormData {
  dob: string;
  tob: string;
  city: string;
  latitude: number | null;
  longitude: number | null;
}

export default function Home() {
  const [kundaliId, setKundaliId] = useState<string | null>(null);
  const [kundaliHtml, setKundaliHtml] = useState<string | null>(null);
  const [personName, setPersonName] = useState<string>('');
  const [formData, setFormData] = useState<FormData | null>(null);
  const [isMuhurtaOpen, setIsMuhurtaOpen] = useState(false);
  const [isHealthOpen, setIsHealthOpen] = useState(false);
  const [isVargaOpen, setIsVargaOpen] = useState(false);
  const resultsRef = useRef<HTMLDivElement>(null);

  const handleKundaliGenerated = (id: string, html: string, name: string, data?: FormData) => {
    setKundaliId(id);
    setKundaliHtml(html);
    setPersonName(name);
    if (data) {
      setFormData(data);
      // Store in sessionStorage for other pages to use (no permanent save needed)
      sessionStorage.setItem('current_kundali', JSON.stringify({
        name,
        dob: data.dob,
        tob: data.tob,
        city: data.city,
        latitude: data.latitude,
        longitude: data.longitude,
        kundali_id: id,
      }));
    }

    // Scroll to results after a short delay
    setTimeout(() => {
      resultsRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, 100);
  };

  const handleNewKundali = () => {
    setKundaliId(null);
    setKundaliHtml(null);
    setPersonName('');
    setFormData(null);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handlePrint = () => {
    window.print();
  };

  const handleOpenMuhurta = () => {
    if (kundaliId) {
      setIsMuhurtaOpen(true);
    }
  };

  const handleOpenHealth = () => {
    if (kundaliId) {
      setIsHealthOpen(true);
    }
  };

  const handleOpenVarga = () => {
    if (kundaliId) {
      setIsVargaOpen(true);
    }
  };

  return (
    <main className="min-h-screen py-5 px-4">
      <div className="max-w-7xl mx-auto">
        {/* Quick Links */}
        {!kundaliId && (
          <div className="mb-6 flex justify-center gap-4 flex-wrap">
            <Link
              href="/matching"
              className="px-4 py-2 bg-gradient-to-r from-pink-500 to-red-500 text-white rounded-lg shadow hover:shadow-lg transition-all flex items-center gap-2"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
              </svg>
              <span>कुंडली मिलान / Kundali Matching</span>
            </Link>
            <Link
              href="/saved"
              className="px-4 py-2 bg-gradient-to-r from-purple-500 to-indigo-500 text-white rounded-lg shadow hover:shadow-lg transition-all flex items-center gap-2"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4" />
              </svg>
              <span>सहेजी कुंडली / Saved Kundalis</span>
            </Link>
            <Link
              href="/compare"
              className="px-4 py-2 bg-gradient-to-r from-teal-500 to-cyan-500 text-white rounded-lg shadow hover:shadow-lg transition-all flex items-center gap-2"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" />
              </svg>
              <span>तुलना / Compare</span>
            </Link>
            <Link
              href="/gemstone"
              className="px-4 py-2 bg-gradient-to-r from-amber-500 to-yellow-500 text-white rounded-lg shadow hover:shadow-lg transition-all flex items-center gap-2"
            >
              <span className="text-lg">💎</span>
              <span>Ratna / Gemstone</span>
            </Link>
            <Link
              href="/panchang"
              className="px-4 py-2 bg-gradient-to-r from-orange-500 to-red-500 text-white rounded-lg shadow hover:shadow-lg transition-all flex items-center gap-2"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              <span>दैनिक पंचांग / Daily Panchang</span>
            </Link>
            <Link
              href="/rashifal"
              className="px-4 py-2 bg-gradient-to-r from-indigo-500 to-purple-500 text-white rounded-lg shadow hover:shadow-lg transition-all flex items-center gap-2"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
              </svg>
              <span>राशिफल / Rashifal</span>
            </Link>
            <Link
              href="/numerology"
              className="px-4 py-2 bg-gradient-to-r from-purple-600 to-violet-600 text-white rounded-lg shadow hover:shadow-lg transition-all flex items-center gap-2"
            >
              <span className="text-lg font-bold">123</span>
              <span>Ank Jyotish</span>
            </Link>
            <Link
              href="/dosha"
              className="px-4 py-2 bg-gradient-to-r from-red-500 to-rose-500 text-white rounded-lg shadow hover:shadow-lg transition-all flex items-center gap-2"
            >
              <span className="text-lg">🔮</span>
              <span>दोष विश्लेषण / Dosha Analysis</span>
            </Link>
            <Link
              href="/career"
              className="px-4 py-2 bg-gradient-to-r from-blue-500 to-indigo-500 text-white rounded-lg shadow hover:shadow-lg transition-all flex items-center gap-2"
            >
              <span className="text-lg">💼</span>
              <span>करियर / Career & Finance</span>
            </Link>
            <Link
              href="/remedies"
              className="px-4 py-2 bg-gradient-to-r from-green-500 to-teal-500 text-white rounded-lg shadow hover:shadow-lg transition-all flex items-center gap-2"
            >
              <span className="text-lg">🙏</span>
              <span>वैदिक उपाय / Vedic Remedies</span>
            </Link>
            <Link
              href="/prashna"
              className="px-4 py-2 bg-gradient-to-r from-violet-500 to-purple-500 text-white rounded-lg shadow hover:shadow-lg transition-all flex items-center gap-2"
            >
              <span className="text-lg">❓</span>
              <span>प्रश्न कुंडली / Prashna Kundali</span>
            </Link>
          </div>
        )}

        {/* Form Section - Always visible when no kundali */}
        {!kundaliId && (
          <div className="no-print relative">
            <KundaliForm onKundaliGenerated={handleKundaliGenerated} />
          </div>
        )}

        {/* Navigation Bar - After Kundali Generation */}
        {kundaliId && (
          <div className="mb-6 flex flex-wrap justify-center gap-2 no-print">
            <Link href="/" className="px-3 py-1.5 bg-gradient-to-r from-orange-500 to-amber-500 text-white rounded-lg text-sm hover:shadow-lg transition-all">
              🏠 होम / Home
            </Link>
            <Link href="/dosha" className="px-3 py-1.5 bg-gradient-to-r from-red-500 to-rose-500 text-white rounded-lg text-sm hover:shadow-lg transition-all">
              🔮 दोष / Dosha
            </Link>
            <Link href="/career" className="px-3 py-1.5 bg-gradient-to-r from-blue-500 to-indigo-500 text-white rounded-lg text-sm hover:shadow-lg transition-all">
              💼 करियर / Career
            </Link>
            <Link href="/remedies" className="px-3 py-1.5 bg-gradient-to-r from-green-500 to-teal-500 text-white rounded-lg text-sm hover:shadow-lg transition-all">
              🙏 उपाय / Remedies
            </Link>
            <Link href="/gemstone" className="px-3 py-1.5 bg-gradient-to-r from-amber-500 to-yellow-500 text-white rounded-lg text-sm hover:shadow-lg transition-all">
              💎 रत्न / Gemstone
            </Link>
            <Link href="/rashifal" className="px-3 py-1.5 bg-gradient-to-r from-indigo-500 to-purple-500 text-white rounded-lg text-sm hover:shadow-lg transition-all">
              ⭐ राशिफल / Rashifal
            </Link>
            <Link href="/prashna" className="px-3 py-1.5 bg-gradient-to-r from-violet-500 to-purple-500 text-white rounded-lg text-sm hover:shadow-lg transition-all">
              ❓ प्रश्न / Prashna
            </Link>
            <Link href="/matching" className="px-3 py-1.5 bg-gradient-to-r from-pink-500 to-red-500 text-white rounded-lg text-sm hover:shadow-lg transition-all">
              💑 मिलान / Matching
            </Link>
            <Link href="/panchang" className="px-3 py-1.5 bg-gradient-to-r from-orange-500 to-red-500 text-white rounded-lg text-sm hover:shadow-lg transition-all">
              📅 पंचांग / Panchang
            </Link>
            <Link href="/numerology" className="px-3 py-1.5 bg-gradient-to-r from-purple-600 to-violet-600 text-white rounded-lg text-sm hover:shadow-lg transition-all">
              🔢 अंक ज्योतिष / Numerology
            </Link>
          </div>
        )}

        {/* Results Section */}
        {kundaliId && kundaliHtml && (
          <div ref={resultsRef}>
            <KundaliResults
              html={kundaliHtml}
              kundaliId={kundaliId}
              onNewKundali={handleNewKundali}
              onPrint={handlePrint}
              onOpenMuhurta={handleOpenMuhurta}
              onOpenHealth={handleOpenHealth}
              onOpenVarga={handleOpenVarga}
            />
          </div>
        )}

        {/* Chat Assistant - Only visible after kundali is generated */}
        {kundaliId && (
          <div className="mt-8 no-print">
            <ChatAssistant kundaliId={kundaliId} personName={personName} />
          </div>
        )}

        {/* Modals */}
        {kundaliId && (
          <>
            <MuhurtaModal
              isOpen={isMuhurtaOpen}
              onClose={() => setIsMuhurtaOpen(false)}
              kundaliId={kundaliId}
            />
            <HealthModal
              isOpen={isHealthOpen}
              onClose={() => setIsHealthOpen(false)}
              kundaliId={kundaliId}
            />
            <DivisionalChartModal
              isOpen={isVargaOpen}
              onClose={() => setIsVargaOpen(false)}
              kundaliId={kundaliId}
            />
          </>
        )}
      </div>
    </main>
  );
}
