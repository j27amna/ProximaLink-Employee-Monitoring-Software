/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.{html,js}", "./static/**/*.{html,js,css}"],
  theme: {
    extend: {
      colors: {
        primary: "#191c24",
        secondary: "#00C7FD",
        tertiary: "#0071c5",
        accent: {
          white: "#FFFFFF",
          green: "#198754",
          cyan: "#0dcaf0",
          red: "#ab2e3c",
          yellow: "#ffc107",
        },
      },
    },
  },
  plugins: [],
};
