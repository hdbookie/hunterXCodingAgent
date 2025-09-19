/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./public/index.html"
  ],
  theme: {
    extend: {
      colors: {
        'surf-blue': '#0ea5e9',
        'surf-teal': '#14b8a6',
        'surf-sand': '#fbbf24'
      }
    },
  },
  plugins: [],
}