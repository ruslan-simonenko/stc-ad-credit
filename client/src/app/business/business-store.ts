import {defineStore} from "pinia";
import {reactive} from "vue";
import {Business, BusinessAddFormDTO, Businesses, BusinessSchema} from "./business-types.ts";
import {useApiClientAxios} from "../../api/api-client-axios.ts";


export const useBusinessStore = defineStore("business", () => {
    const apiClient = useApiClientAxios();

    const all = reactive<Businesses>({
        items: [],
        fetching: false,
        error: false,
    })

    const fetch = async () => {
        all.fetching = true
        try {
            const response = await apiClient.get('/businesses/', {
                headers: {'Content-Type': 'application/json'}
            })
            all.items = response.data.businesses.map((business: any) => BusinessSchema.parse(business))
                .sort((a: Business, b: Business) => b.id - a.id)
            all.error = false
        } catch (e) {
            all.error = true
        } finally {
            all.fetching = false
        }
    }

    const add = async (newBusiness: BusinessAddFormDTO) => {
        try {
            await apiClient.post('/businesses/', newBusiness)
        } finally {
            await fetch()
        }
    }

    return {
        all,
        fetch,
        add,
    }
})
