import {useAuthStore} from "./auth-store.ts";
import {App, Plugin} from "vue";
import {InternalAxiosRequestConfig} from "axios";

export const jwtAuth: Plugin = {
    install: (app: App) => {
        const apiClient = app.config.globalProperties.$apiClientAxios;
        const router = app.config.globalProperties.$router;
        apiClient.interceptors.request.use((config: InternalAxiosRequestConfig) => {
            const authStore = useAuthStore()
            if (authStore.accessToken) {
                config.headers.Authorization = `Bearer ${authStore.accessToken}`;
            } else {
                delete config.headers.Authorization
            }
            return config;
        })
        apiClient.interceptors.response.use(null, async (error: any) => {
            if (error.response.status === 401) {
                const authStore = useAuthStore()
                await authStore.logout()
                await router.push({name: 'Home'})
            }
            return Promise.reject(error)
        })
    }
}