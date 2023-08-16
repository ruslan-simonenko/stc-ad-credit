import {defineStore} from "pinia";
import {reactive} from "vue";
import {useApiClientAxios} from "../../../api/api-client-axios.ts";
import {AdAllowance, AdAllowances, AdAllowanceSchema} from "./ad-allowance-types.ts";


export const useAdAllowanceStore = defineStore("adAllowance", () => {
    const apiClient = useApiClientAxios();

    const data = reactive<AdAllowances>({
        indexed: {},
        fetching: false,
    })

    const fetch = async () => {
        data.fetching = true
        try {
            const response = await apiClient.get('/ad-allowances/', {
                headers: {'Content-Type': 'application/json'}
            })
            data.indexed = response.data.items
                .map((record: any) => AdAllowanceSchema.parse(record))
                .reduce((accumulator: { [business_id: number]: AdAllowance }, adAllowance: AdAllowance) => {
                    accumulator[adAllowance.business_id] = adAllowance;
                    return accumulator;
                }, {})
        } finally {
            data.fetching = false
        }
    }

    return {
        data,
        fetch,
    }
})
