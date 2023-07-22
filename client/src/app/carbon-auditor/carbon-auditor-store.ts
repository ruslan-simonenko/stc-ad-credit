import {defineStore} from "pinia";
import {reactive} from "vue";
import {useApiClientAxios} from "../../api/api-client-axios.ts";

export interface CarbonAuditor {
    name: string,
    email: string,
    picture_url: string,
}

export interface CarbonAuditors {
    items: CarbonAuditor[]
}

export const useCarbonAuditorStore = defineStore("carbonAuditor", () => {
    const apiClient = useApiClientAxios()
    const all = reactive<CarbonAuditors>({
        items: []
    })

    const fetch = async () => {
        return apiClient.get('/domain/carbon-auditor').then((response) => {
            all.items = response.data
        })
    }

    return {
        all,
        fetch,
    }
})
