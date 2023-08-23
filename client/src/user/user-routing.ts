import {RouteRecordRaw} from "vue-router";
import DisabledUserPage from "./DisabledUserPage.vue";
import AdminPage from "../app/admin/AdminPage.vue";
import {UserRole} from "./user.ts";
import {useAuthStore} from "../auth/auth-store.ts";
import UserAddPage from "./management/UserAddPage.vue";
import UserEditPage from "./management/UserEditPage.vue";


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
    {
        name: 'UserAdd', path: '/users/add', component: UserAddPage, meta: {
            auth: {
                required: true,
                authorizedRoles: [UserRole.ADMIN]
            },
            navigationMenu: {type: 'linked', routeName: 'Admin'}
        }
    },
    {
        name: 'UserEdit', path: '/users/:id/edit', component: UserEditPage, meta: {
            auth: {
                required: true,
                authorizedRoles: [UserRole.ADMIN]
            },
            navigationMenu: {type: 'linked', routeName: 'Admin'}
        }
    }
];

export default USER_ROUTES