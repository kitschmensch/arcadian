import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'
import liveReload from 'vite-plugin-live-reload'

// https://vitejs.dev/config/
export default defineConfig({
  input: 'src/main.js',

  build: {
    manifest: true,
    base: process.env.mode === "production" ? "/static/" : "/"
  },
  plugins: [
    svelte(),
    liveReload('../server/home/static')
  ],

})
