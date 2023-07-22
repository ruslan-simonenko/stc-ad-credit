import {defineStore} from "pinia";
import {computed} from "vue";
import {useApiClientAxios} from "../api/api-client-axios.ts";
import {StorageSerializers, useLocalStorage} from "@vueuse/core";

export interface User {
    name: string,
    email: string,
    picture_url: string,
}

export const useAuthStore = defineStore("auth", () => {
    const apiClient = useApiClientAxios()

    const user = useLocalStorage<User>('auth.user', null, {
        serializer: StorageSerializers.object
    })
    const accessToken = useLocalStorage('auth.accessToken', null)
    const isAuthenticated = computed<boolean>(() => user.value != null)

    const loginWithGoogle = async (googleToken: string) => {
        user.value = null

        return apiClient.post('/auth/login', {
            credential: googleToken
        }).then(async (response) => {
            accessToken.value = response.data.access_token
            user.value = {
                name: response.data.name,
                email: response.data.email,
                picture_url: response.data.picture_url,
            }
            console.log("Login succeeded", user.value.name)
        })
    }

    const logout = async () => {
        accessToken.value = null
        user.value = null
    }

    return {
        user,
        isAuthenticated,
        accessToken,
        loginWithGoogle,
        logout,
    }
})
