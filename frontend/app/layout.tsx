import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'विस्तृत कुंडली जनरेटर - Kundali Generator',
  description: 'Generate detailed Vedic birth charts (Kundali) with full predictions, AI chat assistant, Muhurta timing, and health analysis.',
  keywords: 'kundali, horoscope, vedic astrology, birth chart, jyotish, muhurta',
  icons: {
    icon: '/favicon.ico',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="hi">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
      </head>
      <body className="min-h-screen bg-gradient-saffron">
        {children}
      </body>
    </html>
  );
}
