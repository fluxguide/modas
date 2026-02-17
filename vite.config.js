import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

export default defineConfig({
  plugins: [vue()],
  server: { port: 5173 },
  base: "./",
  resolve: {
    alias: {
      "@src": path.resolve(__dirname, "src"),
      "@assets": path.resolve(__dirname, "assets"),
      "@components": path.resolve(__dirname, "src/components"),
      "@composables": path.resolve(__dirname, "src/composables"),
      "@img": path.resolve(__dirname, "assets/img"),
    },
  },
});