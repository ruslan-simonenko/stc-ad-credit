import {RouteRecordRaw} from "vue-router";
import AdRecordsPage from "./AdRecordsPage.vue";
import {UserRole} from "../../../user/user.ts";
import AdRecordAddPage from "./add/AdRecordAddPage.vue";

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
    {
        name: 'AdRecordAdd', path: '/ad-records/add', component: AdRecordAddPage, meta: {
            auth: {
                required: true,
                authorizedRoles: [UserRole.AD_MANAGER]
            },
            navigationMenu: {type: 'linked', routeName: 'AdRecords'}
        }
    }
];

export default AD_RECORD_ROUTES