import {defineStore} from "pinia";
import {computed} from "vue";
import {useApiClientAxios} from "../api/api-client-axios.ts";
import {StorageSerializers, useLocalStorage} from "@vueuse/core";
import {User, UserRole} from "../user/user.ts";


export const useAuthStore = defineStore("auth", () => {
    const apiClient = useApiClientAxios()

    const user = useLocalStorage<User | null>('auth.user', null, {
        serializer: StorageSerializers.object
    })
    const accessToken = useLocalStorage<string | null>('auth.accessToken', null)
    const isAuthenticated = computed<boolean>(() => user.value != null)
    const hasRole = (role: UserRole): boolean => user.value?.roles.includes(role) ?? false

    const loginWithGoogle = async (googleToken: string) => {
        const response = await apiClient.post('/auth/login', {
            credential: googleToken
        })
        updateAuthenticatedUser(response.data.access_token, response.data.user)
    }

    const logout = async () => {
        accessToken.value = null
        user.value = null
    }

    const loginAs = async (user: User) => {
        const response = await apiClient.post('/auth/login-as', {
            user_id: user.id,
        })
        // TODO: save current user somewhere and restore on logout
        updateAuthenticatedUser(response.data.access_token, response.data.user)
    }

    const updateAuthenticatedUser = (newAccessToken: string, newUser: User) => {
        accessToken.value = newAccessToken
        user.value = newUser
    }

    const devFeatures = {
        loginAs
    }

    return {
        user,
        isAuthenticated,
        hasRole,
        accessToken,
        loginWithGoogle,
        logout,
        ...devFeatures
    }
})
