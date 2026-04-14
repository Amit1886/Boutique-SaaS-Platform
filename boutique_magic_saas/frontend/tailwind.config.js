/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      boxShadow: {
        neon: "0 0 30px rgba(219,39,119,0.45)",
        glass: "0 12px 40px rgba(0,0,0,0.18)"
      }
    }
  },
  plugins: [require("daisyui")],
  daisyui: {
    themes: [
      {
        magic_light: {
          primary: "#db2777",
          secondary: "#7c3aed",
          accent: "#0ea5e9",
          neutral: "#0f172a",
          "base-100": "#ffffff",
          "base-200": "#f1f5f9",
          "base-300": "#e2e8f0",
          info: "#0ea5e9",
          success: "#10b981",
          warning: "#f59e0b",
          error: "#ef4444"
        }
      },
      "dark"
    ]
  }
};

