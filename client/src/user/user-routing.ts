import {RouteRecordRaw} from "vue-router";
import DisabledUserPage from "./DisabledUserPage.vue";
import AdminPage from "../app/admin/AdminPage.vue";
import {UserRole} from "./user.ts";
import {useAuthStore} from "../auth/auth-store.ts";


const doNotNavigateIfNotDisabled = () => {
    const authStore = useAuthStore();
    return authStore.user?.roles.length === 0;
}

const USER_ROUTES: RouteRecordRaw[] = [
    {
        name: 'DisabledUser',
        path: '/disabled',
        beforeEnter: doNotNavigateIfNotDisabled,
        component: DisabledUserPage,
        meta: {
            auth: {required: true}
        }
    },
    {
        name: 'Admin', path: '/admin', component: AdminPage, meta: {
            auth: {
                required: true,
                authorizedRoles: [UserRole.ADMIN],
            },
            navigationMenu: {type: 'entry', entry: {icon: 'manage_accounts', label: 'Users'}}
        }
    },
];

export default USER_ROUTES