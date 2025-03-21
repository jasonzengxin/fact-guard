module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./public/index.html"
  ],
  theme: {
    extend: {
      colors: {
        yellow: {
          500: '#fbbf24',
          600: '#d97706',
        },
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}; 