import {defineStore} from "pinia";
import {reactive} from "vue";
import {User, UserAddFormDTO, UserRole, Users} from "./user.ts";
import {useApiClientAxios} from "../api/api-client-axios.ts";
import {useAuthStore} from "../auth/auth-store.ts";


export const useUserStore = defineStore("user", () => {
    const authStore = useAuthStore();

    const apiClient = useApiClientAxios()
    const all = reactive<Users>({
        items: [],
        fetching: false,
        error: false,
    })

    const fetch = async () => {
        if (!authStore.user.roles.includes(UserRole.ADMIN)) {
            return;
        }
        all.fetching = true
        return apiClient.get('/users/manageable/', {
            headers: {'Content-Type': 'application/json'}
        }).then((response) => {
            all.items = response.data.users.sort((a: User, b: User) => b.id - a.id)
            all.fetching = false
            all.error = false
        }).catch(() => {
            all.fetching = false
            all.error = true
        })
    }

    const add = async (newUser: UserAddFormDTO) => {
        return apiClient.post('/users/', newUser).finally(() => fetch())
    }

    const setEnabled = async (userID: number, enabled: boolean) => {
        const response = await apiClient.put(`/users/${userID}`, {
            roles: enabled ? [UserRole.CARBON_AUDITOR] : []
        })
        const updatedUser = response.data.user;
        const itemIndex = all.items.findIndex((user) => user.id === userID)
        all.items[itemIndex] = updatedUser
    }

    return {
        all,
        fetch,
        add,
        setEnabled,
    }
})
