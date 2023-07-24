import {defineStore} from "pinia";
import {reactive} from "vue";
import {useApiClientAxios} from "../../api/api-client-axios.ts";

export interface CarbonAuditor {
    name: string,
    email: string,
    picture_url: string,
}

export interface CarbonAuditorForm {
    email: string,
}

export interface CarbonAuditors {
    items: CarbonAuditor[],
    fetching: boolean,
    error: boolean,
}

export const useCarbonAuditorStore = defineStore("carbonAuditor", () => {
    const apiClient = useApiClientAxios()
    const all = reactive<CarbonAuditors>({
        items: [],
        fetching: false,
        error: false,
    })

    const fetch = async () => {
        all.fetching = true
        return apiClient.get('/domain/carbon-auditor/', {
            headers:{
                'Content-Type': 'application/json'
            }
        }).then((response) => {
            all.items = response.data
            all.fetching = false
            all.error = false
        }).catch(() => {
            all.fetching = false
            all.error = true
        })
    }

    const add = async (newAuditor: CarbonAuditorForm) => {
        return apiClient.post('/domain/carbon-auditor/', newAuditor).finally(() => fetch())
    }

    return {
        all,
        fetch,
        add,
    }
})
