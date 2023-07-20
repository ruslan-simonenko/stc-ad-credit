import {defineConfig} from 'vite'
import vue from '@vitejs/plugin-vue'
import {quasar, transformAssetUrls} from "@quasar/vite-plugin";

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [
        vue({
            template: {transformAssetUrls}
        }),
        quasar(),
    ],
    server: {
        proxy: {
            '/api': {
                target: "http://localhost:5000",
                changeOrigin: false,
                rewrite: path => path.replace(/^\/api/, '')
            }
        }
    }
})
