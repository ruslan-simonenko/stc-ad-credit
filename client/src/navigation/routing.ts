import {createRouter, createWebHashHistory, RouteRecordRaw} from "vue-router";
import LoginPage from "../auth/LoginPage.vue";
import AdminPage from "../app/admin/AdminPage.vue";
import {useAuthStore} from "../auth/auth-store.ts";
import CarbonAuditPage from "../app/carbon-audit/CarbonAuditPage.vue";
import {UserRole} from "../user/user.ts";
import DisabledUserPage from "../user/DisabledUserPage.vue";
import BusinessesPage from "../app/business/BusinessesPage.vue";

const navigateToHomeIfAuthenticated = () => {
    const authStore = useAuthStore();
    if (authStore.isAuthenticated) {
        return {name: 'Admin'}
    }
    return true
}

const redirectFromHome = () => {
    const authStore = useAuthStore()
    if (authStore.isAuthenticated) {
        if (authStore.user!.roles.includes(UserRole.ADMIN)) {
            return {name: 'Admin'}
        } else if (authStore.user!.roles.includes(UserRole.CARBON_AUDITOR)) {
            return {name: 'CarbonAudit'}
        } else if (authStore.user!.roles.length === 0) {
            return {name: 'DisabledUser'}
        }
        throw new Error('Unsupported role: ' + authStore.user!.roles)
    } else {
        return {name: 'Login'}
    }
}

const routes: RouteRecordRaw[] = [
    {name: 'Home', path: '/', redirect: redirectFromHome},
    {name: "Login", path: '/login', beforeEnter: navigateToHomeIfAuthenticated, component: LoginPage},
    {name: 'DisabledUser', path: '/disabled', component: DisabledUserPage},
    {
        name: 'Admin', path: '/admin', component: AdminPage, meta: {
            auth: {
                allowedRoles: [UserRole.ADMIN, UserRole.CARBON_AUDITOR],
                navIcon: 'manage_accounts',
                navLabel: 'Users'
            }
        }
    },
    {
        name: 'CarbonAudit', path: '/carbon-audit', component: CarbonAuditPage, meta: {
            auth: {
                allowedRoles: [UserRole.CARBON_AUDITOR],
                navIcon: 'co2',
                navLabel: 'Carbon Audit'
            }
        }
    },
    {
        name: 'Businesses', path: '/businesses', component: BusinessesPage, meta: {
            auth: {
                allowedRoles: [UserRole.ADMIN, UserRole.CARBON_AUDITOR],
                navIcon: 'storefront',
                navLabel: 'Businesses'
            }
        }
    },
]

export const appRouter = createRouter({
    history: createWebHashHistory(),
    routes
})
appRouter.beforeEach((to) => {
    const authStore = useAuthStore()
    if (to.meta.requiresAuth !== true || authStore.isAuthenticated) {
        return true;
    }
    return {
        name: 'Login',
        query: {next: to.fullPath}
    }
})
