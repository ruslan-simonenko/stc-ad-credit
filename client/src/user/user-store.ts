import {defineStore} from "pinia";
import {reactive} from "vue";
import {User, UserAddFormDTO, Users} from "./user.ts";
import {useApiClientAxios} from "../api/api-client-axios.ts";


export const useUserStore = defineStore("user", () => {
    const apiClient = useApiClientAxios()
    const all = reactive<Users>({
        items: [],
        fetching: false,
        error: false,
    })

    const fetch = async () => {
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


    return {
        all,
        fetch,
        add,
    }
})
