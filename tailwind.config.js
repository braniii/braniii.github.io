module.exports = {
  purge: ["src/index.html"],
  darkMode: "media",
  theme: {
    extend: {
      spacing: {
        full: "100%",
      },
    },
  },
  variants: {
    extend: {},
  },
  plugins: [require("tailwindcss"), require("autoprefixer")],
};
