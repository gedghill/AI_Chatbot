import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [react()],
    server: {
        host: "0.0.0.0", // Bind to all interfaces
        port: 3000, // Default port for the Vite dev server
        proxy: {
            "/api": {
                target: "http://localhost:5000", // Point to the backend service in Docker Compose
                changeOrigin: true,
                secure: false,
                rewrite: (path) => path.replace(/^\/api/, ""), // Optional: Adjust the API path
            },
        },
    },
});
