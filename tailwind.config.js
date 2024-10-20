/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          light: '#4a90e2',
          DEFAULT: '#3498db',
          dark: '#2980b9',
        },
        secondary: '#10B981',
        accent: '#EF4444',
        background: '#F3F4F6',
        text: '#1F2937',
        'primary-dark': '#2563EB',
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        heading: ['Poppins', 'sans-serif'],
      },
      fontWeight: {
        normal: 400,
        medium: 500,
        semibold: 600,
        bold: 700,
      },
    },
  },
  plugins: [],
}
