import {defineStore} from "pinia";
import {reactive} from "vue";
import {Users} from "./user.ts";
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
            all.items = response.data.users
            all.fetching = false
            all.error = false
        }).catch(() => {
            all.fetching = false
            all.error = true
        })
    }

    return {
        all,
        fetch,
    }
})
