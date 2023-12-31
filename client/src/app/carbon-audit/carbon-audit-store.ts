import {defineStore} from "pinia";
import {reactive, watch} from "vue";
import {CarbonAudit, CarbonAuditAddFormDTO, CarbonAudits} from "./carbon-audit-types.ts";
import {useApiClientAxios} from "../../api/api-client-axios.ts";
import {useAuthStore} from "../../auth/auth-store.ts";


export const useCarbonAuditStore = defineStore("carbonAudit", () => {
    const apiClient = useApiClientAxios();
    const authStore = useAuthStore();

    const all = reactive<CarbonAudits>({
        items: [],
        fetching: false,
        error: false,
    })

    watch(() => authStore.user, () => all.items = [])

    const fetch = async () => {
        all.fetching = true
        try {
            const response = await apiClient.get('/carbon_audits/', {
                headers: {'Content-Type': 'application/json'}
            })
            all.items = response.data.objects.sort((a: CarbonAudit, b: CarbonAudit) => b.id - a.id)
            all.error = false
        } catch (e) {
            all.error = true
        } finally {
            all.fetching = false
        }
    }

    const add = async (newCarbonAudit: CarbonAuditAddFormDTO) => {
        await apiClient.post('/carbon_audits/', newCarbonAudit, {
            headers: {'Content-Type': 'application/json'}
        })
        await fetch();
    }

    return {
        all,
        fetch,
        add,
    }
})
