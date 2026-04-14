import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  base: "/magic/",
  plugins: [react()],
  build: {
    outDir: "../../boutique_ai_saas/magic_studio/spa_dist",
    emptyOutDir: true,
  },
});
