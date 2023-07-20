import {defineStore} from "pinia";
import {computed, ref} from "vue";
import {useApiClientAxios} from "../api/api-client-axios.ts";

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

        return apiClient.post('/auth/login', {
            credential: googleToken
        }).then(async (response) => {
            user.value = {
                name: response.data.name,
                email: response.data.email,
                picture_url: response.data.picture_url,
            }
            console.log("Login succeeded", user.value.name)
        })
    }

    const logout = async () => user.value = null

    return {
        user,
        isAuthenticated,
        loginWithGoogle,
        logout,
    }
})
