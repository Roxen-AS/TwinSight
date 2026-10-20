/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'ts-bg':      '#020C1B',
        'ts-card':    'rgba(4,18,42,0.92)',
        'ts-accent':  '#1E90FF',
        'ts-success': '#00D97E',
        'ts-warning': '#F59E0B',
        'ts-danger':  '#FF3860',
        'ts-cyan':    '#00E5FF',
        'ts-purple':  '#9B59B6',
      },
      fontFamily: {
        sans:  ['Space Grotesk', 'system-ui', 'sans-serif'],
        mono:  ['JetBrains Mono', 'monospace'],
        brand: ['Rajdhani', 'sans-serif'],
      },
      animation: {
        'pulse-slow': 'ts-pulse 1.8s ease-in-out infinite',
        'glow':       'ts-glow 2s ease-in-out infinite',
        'slide-in':   'ts-slide-in 0.2s ease-out',
      },
      backdropBlur: {
        'ts': '20px',
      },
    },
  },
  plugins: [],
}
