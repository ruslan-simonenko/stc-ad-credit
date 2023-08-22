import {defineStore} from "pinia";
import {reactive, watch} from "vue";
import {useApiClientAxios} from "../../../api/api-client-axios.ts";
import {AdAllowance, AdAllowances, AdAllowanceSchema} from "./ad-allowance-types.ts";
import {useAuthStore} from "../../../auth/auth-store.ts";


export const useAdAllowanceStore = defineStore("adAllowance", () => {
    const apiClient = useApiClientAxios();
    const authStore = useAuthStore();

    const data = reactive<AdAllowances>({
        indexed: {},
        fetching: false,
    })

    watch(() => authStore.user, () => data.indexed = {})

    const fetch = async () => {
        data.fetching = true
        try {
            const response = await apiClient.get('/ad-allowances/', {
                headers: {'Content-Type': 'application/json'}
            })
            data.indexed = response.data.objects
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
