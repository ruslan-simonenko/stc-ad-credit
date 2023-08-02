import {defineStore} from "pinia";
import {reactive} from "vue";
import {BusinessAddFormDTO, Businesses} from "./business-types.ts";


export const useBusinessStore = defineStore("business", () => {
    const all = reactive<Businesses>({
        items: [],
    })

    const add = async (newBusiness: BusinessAddFormDTO) => {
        all.items.push(newBusiness)
    }

    return {
        all,
        add,
    }
})
