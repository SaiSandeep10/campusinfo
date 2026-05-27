/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Space Grotesk', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      colors: {
        accent: '#3B82F6',
        cyan: '#06B6D4',
      },
      animation: {
        'bounce-dot': 'bounce-dot 1s infinite',
        'fade-in-up': 'fadeInUp 0.3s ease forwards',
      }
    },
  },
  plugins: [],
}