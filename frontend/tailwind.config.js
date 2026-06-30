/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#ff6b35',
          50: '#fff5f0',
          100: '#ffe8dc',
          200: '#ffd1b8',
          300: '#ffb088',
          400: '#ff8c58',
          500: '#ff6b35',
          600: '#f54d15',
          700: '#cc3a0c',
          800: '#a13110',
          900: '#832c12',
        },
        secondary: {
          DEFAULT: '#8b4513',
          light: '#a0522d',
          dark: '#6b3410',
        },
        accent: {
          DEFAULT: '#f7931e',
          light: '#ffa94d',
          dark: '#d47c00',
        },
        saffron: {
          50: '#fff8f0',
          100: '#fff5e6',
          200: '#ffe4c4',
          300: '#ffd39b',
          400: '#f7931e',
          500: '#ff6b35',
        },
      },
      fontFamily: {
        hindi: ['Noto Sans Devanagari', 'sans-serif'],
      },
      backgroundImage: {
        'gradient-primary': 'linear-gradient(135deg, #ff6b35 0%, #f7931e 100%)',
        'gradient-saffron': 'linear-gradient(135deg, #fff5e6 0%, #ffe4c4 100%)',
        'gradient-chat': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'gradient-muhurta': 'linear-gradient(135deg, #9c27b0 0%, #673ab7 100%)',
        'gradient-health': 'linear-gradient(135deg, #dc3545 0%, #c82333 100%)',
      },
    },
  },
  plugins: [],
};
