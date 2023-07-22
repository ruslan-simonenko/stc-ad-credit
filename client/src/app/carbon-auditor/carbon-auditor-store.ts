import {defineStore} from "pinia";
import {ref} from "vue";

export interface CarbonAuditor {
    name: string,
    email: string,
    picture_url: string,
}

export const useCarbonAuditorStore = defineStore("carbonAuditor", () => {
    const all = ref<CarbonAuditor[]>([
        {name: 'John Doe', email: 'john.doe@gmail.com', picture_url: 'https://cdn.quasar.dev/img/avatar4.jpg'},
        {name: 'Jane Doe', email: 'jane.doe@gmail.com', picture_url: 'https://cdn.quasar.dev/img/avatar2.jpg'}
    ])

    return {
        all,
    }
})
