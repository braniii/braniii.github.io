const colors = require('tailwindcss/colors')

module.exports = {
	purge: ["../templates/*.html"],
	darkMode: "media",
	theme: {
		extend: {
			spacing: {
				full: "100%",
			},
            animation: {
                'avatar-bounce': 'avatar 3s infinite',
            },
            keyframes: {
                avatar: {
                    '0%, 100%': { transform: 'translateY(0)', animationTimingFunction: 'ease-in' },
                    '50%': { transform: 'translateY(6px)', animationTimingFunction: 'ease-out' },
                }
            }
		},
		colors: {
			transparent: 'transparent',
           current: 'currentColor',
          'greenish': '#4d908e',
			black: colors.black,
      white: colors.white,
      gray: colors.blueGray,
      blue: colors.teal,
      red: colors.rose,
      yellow: colors.amber,
		},
  },
  variants: {
    extend: {},
  },
};
