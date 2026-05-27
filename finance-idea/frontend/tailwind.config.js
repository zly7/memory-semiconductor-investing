/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{vue,ts,tsx,js,jsx}',
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        bg: {
          0: 'var(--bg-0)',
          1: 'var(--bg-1)',
          2: 'var(--bg-2)',
        },
        ink: {
          1: 'var(--text-1)',
          2: 'var(--text-2)',
          3: 'var(--text-3)',
        },
        line: 'var(--border)',
        accent: 'var(--accent)',
        up: 'var(--up)',
        down: 'var(--down)',
        warn: 'var(--warn)',
        nu: 'var(--neutral)',
      },
      fontFamily: {
        mono: ['"JetBrains Mono"', '"SF Mono"', 'Menlo', 'monospace'],
        sans: ['"PingFang SC"', '"Helvetica Neue"', '"Microsoft YaHei"', 'Arial', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
