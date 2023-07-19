/// <reference types="vite/client" />

/**
 * Type definitions for Vite's .env files, see https://vitejs.dev/guide/env-and-mode.html#intellisense-for-typescript
 */
interface ImportMetaEnv {
    /**
     * Google Sign In - Client ID, see https://developers.google.com/identity/gsi/web/guides/get-google-api-clientid
     * Current configuration: https://console.cloud.google.com/apis/credentials?project=stc-ad-credit-test
     */
    readonly VITE_GOOGLE_LOGIN_CLIENT_ID: string
}

interface ImportMeta {
    readonly env: ImportMetaEnv
}