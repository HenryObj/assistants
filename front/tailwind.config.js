/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {},
    fontFamily: {
      'DM_Sans': ['DM Sans', 'sans-serif'],
      'inter': ['Inter', 'sans-serif'],
    },
    colors: {
      'white': '#FFFFFF',
      'black' : '#111111',
      'sidebar-black': '#262626',
      'bg_sidebar-black': '#202123',
      'module-background-gray': '#F5F5F5',
      'chat-font': '#374151',
      'gray-100': '#666666',
      'borders-gray': '#A9ACB4',
      'attach-header-background-blue': '#DBDEE6',
      'file-background-blue': '#D8ECF0',
      'file-upload-background-gray': '#EEF1F7',
      'chat-icon-orange': '#FF6B00',
      'signup-orange': '#FF6B00',
      'button-selected-blue': '#00ACCB',
      'button-hover-green': '#46BC96',
    },
  },
  plugins: [],
};
