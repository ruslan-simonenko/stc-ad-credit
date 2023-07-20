import {defineStore} from "pinia";
import {computed, ref} from "vue";
import {useApiClientAxios} from "../api/api-client-axios.ts";
import {AxiosError} from "axios";

export interface User {
    name: string,
    email: string,
    picture_url: string,
}

export const useAuthStore = defineStore("auth", () => {
    const apiClient = useApiClientAxios()

    const user = ref<User | null>(null)
    const isAuthenticated = computed<boolean>(() => user.value != null)

    const loginWithGoogle = async (googleToken: string) => {
        user.value = null

        await apiClient.post('/auth/login', {
            credential: googleToken
        }).then(async (response) => {
            user.value = {
                name: response.data.name,
                email: response.data.email,
                picture_url: response.data.picture_url,
            }
            console.log("Login succeeded", user.value.name)
        }).catch((error: Error | AxiosError) => console.error("Login failed", error))
    }

    const logout = async () => user.value = null

    return {
        user,
        isAuthenticated,
        loginWithGoogle,
        logout,
    }
})
