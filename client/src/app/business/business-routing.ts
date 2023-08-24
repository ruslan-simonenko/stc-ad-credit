import BusinessesPage from "./BusinessesPage.vue";
import {UserRole} from "../../user/user.ts";
import {RouteRecordRaw} from "vue-router";
import BusinessFormPage from "./form/BusinessFormPage.vue";

const BUSINESS_ROUTES: RouteRecordRaw[] = [
    {
        name: 'Businesses', path: '/businesses', component: BusinessesPage, meta: {
            auth: {
                required: true,
                authorizedRoles: [UserRole.ADMIN, UserRole.BUSINESS_MANAGER],
            },
            navigationMenu: {type:'entry', entry: {icon: 'storefront', label: 'Businesses'}}
        }
    },
    {
        name: 'BusinessAdd', path: '/businesses/add', component: BusinessFormPage, meta: {
            auth: {
                required: true,
                authorizedRoles: [UserRole.BUSINESS_MANAGER]
            },
            navigationMenu: {type: 'linked', routeName: 'Businesses'}
        }
    }
];

export default BUSINESS_ROUTES