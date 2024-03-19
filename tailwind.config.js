const colors = require('tailwindcss/colors')

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.html"],
  // corePlugins: [
  //   "fontSmoothing",
  //   "fontFamily",
  //   "fontSize",
  //   "accessibility",
  //   "flex",
  //   "verticalAlign",
  //   "gap",
  //   "margin",
  //   "padding",
  //   "justifyContent",
  //   "alignContent",
  // ],
  theme: {
    // colors: {
    //   transparent: 'transparent',
    //   current: 'currentColor',
    //   black: colors.black,
    //   white: colors.white,
    //   gray: colors.gray,
    //   emerald: colors.emerald,
    //   indigo: colors.indigo,
    //   yellow: colors.yellow,
    // },
    extend: {},
  },
  plugins: [],
}

