import {defineStore} from "pinia";
import {reactive} from "vue";
import {
    Business,
    BusinessAddFormDTO,
    BusinessDTOPublicSchema,
    BusinessDTOSchema,
    Businesses,
} from "./business-types.ts";
import {useApiClientAxios} from "../../api/api-client-axios.ts";
import {useAuthStore} from "../../auth/auth-store.ts";
import {UserRole} from "../../user/user.ts";


export const useBusinessStore = defineStore("business", () => {
    const apiClient = useApiClientAxios();
    const authStore = useAuthStore();

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
            const parser = authStore.hasRole(UserRole.BUSINESS_MANAGER) ? _parseDTO : _parseDTOPublic;
            all.items = response.data.objects
                .map((business: any) => parser(business))
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

const _parseDTO = (business: any): Business => {
    const {
        email,
        facebook_url,
        id,
        name,
        registration_number,
        registration_type
    } = BusinessDTOSchema.parse(business)
    return {id, name, facebook_url, sensitive: {registration_type, registration_number, email}}
}

const _parseDTOPublic = (business: any): Business => {
    const {facebook_url, id, name} = BusinessDTOPublicSchema.parse(business)
    return {id, name, facebook_url}
}
