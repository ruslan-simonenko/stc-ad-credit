import {defineStore} from "pinia";
import {reactive} from "vue";
import {useApiClientAxios} from "../../../api/api-client-axios.ts";
import {AdStrategy, AdStrategySchema} from "./ad-strategy-types.ts";


export const useAdStrategyStore = defineStore("adStrategy", () => {
    const apiClient = useApiClientAxios();

    const data = reactive<{ strategy: AdStrategy | null, fetching: boolean }>({
        strategy: null,
        fetching: false,
    })

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
