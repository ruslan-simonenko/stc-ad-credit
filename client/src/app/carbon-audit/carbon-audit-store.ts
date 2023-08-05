import {defineStore} from "pinia";
import {reactive} from "vue";
import {CarbonAudit, CarbonAuditAddFormDTO, CarbonAudits} from "./carbon-audit-types.ts";
import {useApiClientAxios} from "../../api/api-client-axios.ts";


export const useCarbonAuditStore = defineStore("carbonAudit", () => {
    const apiClient = useApiClientAxios();

    const all = reactive<CarbonAudits>({
        items: [],
        fetching: false,
        error: false,
    })

    const fetch = async () => {
        all.fetching = true
        try {
            const response = await apiClient.get('/carbon_audits/', {
                headers: {'Content-Type': 'application/json'}
            })
            all.items = response.data.audits.sort((a: CarbonAudit, b: CarbonAudit) => b.id - a.id)
            all.error = false
        } catch (e) {
            all.error = true
        } finally {
            all.fetching = false
        }
    }

    const add = async (newCarbonAudit: CarbonAuditAddFormDTO) => {
        await apiClient.post('/carbon_audits/', newCarbonAudit,{
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
