/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  darkMode: "class",
  theme: {
    extend: {
      fontFamily: {
        display: ["'Space Grotesk'", "'Inter'", "system-ui", "sans-serif"],
        sans: ["'Inter'", "system-ui", "sans-serif"],
        mono: ["'JetBrains Mono'", "'IBM Plex Mono'", "ui-monospace", "monospace"],
      },
      colors: {
        base: {
          950: "#06090d",
          900: "#0a0f16",
          850: "#0e141d",
          800: "#131a24",
          700: "#1b2430",
          600: "#26313f",
          500: "#3a4a5c",
          400: "#5c7086",
          300: "#8598ab",
          200: "#b3c1cf",
          100: "#dbe3ea",
          50: "#f2f5f8",
        },
        signal: {
          DEFAULT: "#ff5a3c",
          dim: "#c8432a",
          soft: "#ff7a5c",
        },
        gold: {
          DEFAULT: "#e8b84b",
          soft: "#f2cd76",
        },
        mint: {
          DEFAULT: "#3ddc97",
          soft: "#6ee6b4",
        },
        azure: {
          DEFAULT: "#3ba7e8",
          soft: "#6fc0f0",
        },
      },
      boxShadow: {
        panel: "0 1px 0 0 rgba(255,255,255,0.04) inset, 0 0 0 1px rgba(255,255,255,0.03) inset",
        glow: "0 0 24px -6px rgba(255,90,60,0.45)",
      },
      backgroundImage: {
        grid: "linear-gradient(rgba(255,255,255,0.025) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.025) 1px, transparent 1px)",
      },
      backgroundSize: {
        grid: "24px 24px",
      },
      keyframes: {
        "pop-in": {
          "0%": { transform: "scale(0.85)", opacity: "0" },
          "100%": { transform: "scale(1)", opacity: "1" },
        },
        "slide-up": {
          "0%": { transform: "translateY(8px)", opacity: "0" },
          "100%": { transform: "translateY(0)", opacity: "1" },
        },
        "pulse-ring": {
          "0%": { boxShadow: "0 0 0 0 rgba(255,90,60,0.45)" },
          "100%": { boxShadow: "0 0 0 10px rgba(255,90,60,0)" },
        },
      },
      animation: {
        "pop-in": "pop-in 0.22s cubic-bezier(0.34,1.56,0.64,1)",
        "slide-up": "slide-up 0.28s ease-out",
        "pulse-ring": "pulse-ring 1s cubic-bezier(0,0,0.2,1)",
      },
    },
  },
  plugins: [],
};
