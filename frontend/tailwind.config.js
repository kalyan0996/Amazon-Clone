/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/context/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        "amazon-navy": "#131921",
        "amazon-navy-light": "#232F3E",
        "amazon-orange": "#FF9900",
        "amazon-yellow": "#FFD814",
        "amazon-yellow-dark": "#F7CA00",
        "amazon-teal": "#007185",
        "amazon-red": "#B12704",
        "amazon-bg": "#EAEDED",
      },
      fontFamily: {
        amazon: ['"Amazon Ember"', "Arial", "sans-serif"],
      },
    },
  },
  plugins: [],
};
