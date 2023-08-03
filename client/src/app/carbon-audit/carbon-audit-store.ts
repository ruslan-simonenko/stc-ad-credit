import {defineStore} from "pinia";
import {reactive} from "vue";
import {CarbonAuditAddFormDTO, CarbonAudits} from "./carbon-audit-types.ts";


export const useCarbonAuditStore = defineStore("carbonAudit", () => {
    const all = reactive<CarbonAudits>({
        items: [],
        fetching: false,
        error: false,
    })

    const fetch = async () => {
        all.fetching = true
        try {
            all.items = []
            all.error = false
        } catch (e) {
            all.error = true
        } finally {
            all.fetching = false
        }
    }

    const add = async (newCarbonAudit: CarbonAuditAddFormDTO) => {
        all.items.push({
            ...newCarbonAudit,
            id: all.items.reduce((id, audit) => Math.max(id, audit.id), 0) + 1
        })
    }

    return {
        all,
        fetch,
        add,
    }
})
