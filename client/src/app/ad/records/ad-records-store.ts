import {defineStore} from "pinia";
import {reactive} from "vue";
import {useApiClientAxios} from "../../../api/api-client-axios.ts";
import {AdRecord, AdRecordAddFormDTO, AdRecords, AdRecordSchema} from "./ad-records-types.ts";
import {useAdAllowanceStore} from "../allowance/ad-allowance-store.ts";


export const useAdRecordsStore = defineStore("adRecords", () => {
    const apiClient = useApiClientAxios();

    const adAllowanceStore = useAdAllowanceStore();

    const all = reactive<AdRecords>({
        items: [],
        fetching: false,
    })

    const fetch = async () => {
        all.fetching = true
        try {
            const response = await apiClient.get('/ad-records/', {
                headers: {'Content-Type': 'application/json'}
            })
            all.items = response.data.records
                .map((record: any) => AdRecordSchema.parse(record))
                .sort((a: AdRecord, b: AdRecord) => b.created_at.getTime() - a.created_at.getTime())
        } finally {
            all.fetching = false
        }
    }

    const add = async (newRecord: AdRecordAddFormDTO) => {
        try {
            const response = await apiClient.post('/ad-records/', newRecord, {
                headers: {'Content-Type': 'application/json'}
            })
            const createdRecord = AdRecordSchema.parse(response.data);
            all.items.unshift(createdRecord)
        } catch (e) {
            await fetch()
            throw e
        } finally {
            // noinspection ES6MissingAwait
            adAllowanceStore.fetch()
        }
    }

    return {
        all,
        fetch,
        add,
    }
})
