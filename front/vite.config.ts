import path from "node:path";
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";

// https://vitejs.dev/config/
export default defineConfig({
	root: "src/pages",
	plugins: [react()],
	publicDir: path.resolve(__dirname, "public"),
	resolve: {
		alias: {
			"@": path.resolve(__dirname, "./src"),
		},
	},
	build: {
		outDir: "../../../static",
		rollupOptions: {
			input: {
				"": path.resolve(__dirname, "src/pages/index.html"),
				telop: path.resolve(__dirname, "src/pages/telop/index.html"),
			},
		},
	},
});
