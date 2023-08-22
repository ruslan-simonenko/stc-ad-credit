import {defineStore} from "pinia";
import {reactive, watch} from "vue";
import {useApiClientAxios} from "../../../api/api-client-axios.ts";
import {AdStrategy, AdStrategySchema} from "./ad-strategy-types.ts";
import {useAuthStore} from "../../../auth/auth-store.ts";


export const useAdStrategyStore = defineStore("adStrategy", () => {
    const apiClient = useApiClientAxios();
    const authStore = useAuthStore();

    const data = reactive<{ strategy: AdStrategy | null, fetching: boolean }>({
        strategy: null,
        fetching: false,
    })

    watch(() => authStore.user, () => data.strategy = null)

    const fetch = async () => {
        data.fetching = true
        try {
            const response = await apiClient.get('/ad-strategy/', {
                headers: {'Content-Type': 'application/json'}
            })
            data.strategy = AdStrategySchema.parse(response.data)
        } finally {
            data.fetching = false
        }
    }

    return {
        data,
        fetch,
    }
})
