# Kundali Software - Next.js Frontend

A modern React/Next.js frontend for the Vedic astrology Kundali generation system.

## Features

- **KundaliForm**: Birth details input with date/time pickers
- **KundaliResults**: Display kundali chart, planets, houses, and predictions
- **ChatAssistant**: AI-powered chat interface for kundali questions
- **MuhurtaModal**: Find auspicious timing for events
- **HealthModal**: Health and accident predictions

## Tech Stack

- Next.js 14 (App Router)
- React 18
- TypeScript
- Tailwind CSS
- Hindi/Devanagari font support

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn
- Backend server running on `http://localhost:5000`

### Installation

```bash
cd frontend
npm install
```

### Development

```bash
npm run dev
```

The app will be available at `http://localhost:3000`

### Production Build

```bash
npm run build
npm start
```

## Backend API Endpoints

The frontend connects to the Flask backend at `http://localhost:5000`:

- `POST /generate` - Generate new kundali
- `POST /chat` - Chat with AI assistant
- `POST /muhurta` - Find auspicious timing
- `POST /health` - Get health predictions

## Project Structure

```
frontend/
├── app/
│   ├── components/
│   │   ├── ui/          # Reusable UI components
│   │   │   ├── Button.tsx
│   │   │   ├── Input.tsx
│   │   │   ├── Select.tsx
│   │   │   └── Modal.tsx
│   │   ├── KundaliForm.tsx
│   │   ├── KundaliResults.tsx
│   │   ├── ChatAssistant.tsx
│   │   ├── MuhurtaModal.tsx
│   │   ├── HealthModal.tsx
│   │   ├── PlanetTable.tsx
│   │   └── DashaDisplay.tsx
│   ├── globals.css
│   ├── layout.tsx
│   └── page.tsx
├── lib/
│   ├── api.ts           # API client functions
│   └── types.ts         # TypeScript interfaces
├── public/
│   └── favicon.ico
├── package.json
├── next.config.js
├── tailwind.config.js
├── tsconfig.json
└── postcss.config.js
```

## Styling

- Uses Tailwind CSS with custom theme colors matching the original UI
- Primary: #ff6b35 (orange/saffron)
- Accent: #f7931e (golden)
- Secondary: #8b4513 (brown)
- Supports Hindi/Devanagari text via Noto Sans Devanagari font

## Environment Variables

Create a `.env.local` file for custom configuration:

```env
NEXT_PUBLIC_API_BASE=http://localhost:5000
```

## Running with Backend

1. Start the Flask backend:
   ```bash
   cd ..
   python kundali_web.py
   ```

2. Start the Next.js frontend:
   ```bash
   cd frontend
   npm run dev
   ```

3. Open http://localhost:3000 in your browser
