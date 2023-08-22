import BusinessesPage from "./BusinessesPage.vue";
import {UserRole} from "../../user/user.ts";
import {RouteRecordRaw} from "vue-router";

const BUSINESS_ROUTES: RouteRecordRaw[] = [
    {
        name: 'Businesses', path: '/businesses', component: BusinessesPage, meta: {
            auth: {
                required: true,
                authorizedRoles: [UserRole.ADMIN, UserRole.BUSINESS_MANAGER],
            },
            navigationMenu: {type: 'entry', entry: {icon: 'storefront', label: 'Businesses'}}
        }
    },
];

export default BUSINESS_ROUTES