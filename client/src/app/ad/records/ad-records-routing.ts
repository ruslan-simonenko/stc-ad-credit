import {RouteRecordRaw} from "vue-router";
import AdRecordsPage from "./AdRecordsPage.vue";
import {UserRole} from "../../../user/user.ts";

const AD_RECORD_ROUTES: RouteRecordRaw[] = [
    {
        name: 'AdRecords', path: '/ad-records', component: AdRecordsPage, meta: {
            auth: {
                required: true,
                authorizedRoles: [UserRole.ADMIN, UserRole.AD_MANAGER],
            },
            navigationMenu: {type: 'entry', entry: {icon: 'list_alt', label: 'Ad Records'}}
        }
    },
];

export default AD_RECORD_ROUTES