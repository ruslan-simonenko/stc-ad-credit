import {createRouter, createWebHashHistory, RouteRecordRaw} from "vue-router";
import LoginPage from "../auth/LoginPage.vue";
import AdminPage from "../app/admin/AdminPage.vue";
import {useAuthStore} from "../auth/auth-store.ts";
import CarbonAuditPage from "../app/carbon-audit/CarbonAuditPage.vue";
import {UserRole} from "../user/user.ts";
import DisabledUserPage from "../user/DisabledUserPage.vue";
import {useRoutingStore} from "./routing-store.ts";
import AdRecordsPage from "../app/ad/records/AdRecordsPage.vue";
import AdStrategyPage from "../app/ad/strategy/AdStrategyPage.vue";
import BUSINESS_ROUTES from "../app/business/business-routing.ts";

const navigateToHomeIfAuthenticated = () => {
    const authStore = useAuthStore();
    if (authStore.isAuthenticated) {
        return {name: 'Home'}
    }
    return true
}

const doNotNavigateIfNotDisabled = () => {
    const authStore = useAuthStore();
    return authStore.user?.roles.length === 0;
}

const redirectFromHome = () => {
    const authStore = useAuthStore()
    if (authStore.isAuthenticated) {
        const roles = authStore.user!.roles;
        if (roles.includes(UserRole.ADMIN)) {
            return {name: 'Admin'}
        } else if (roles.includes(UserRole.BUSINESS_MANAGER)) {
            return {name: 'Businesses'}
        } else if (roles.includes(UserRole.CARBON_AUDITOR)) {
            return {name: 'CarbonAudit'}
        } else if (roles.includes(UserRole.AD_MANAGER)) {
            return {name: 'AdRecords'}
        } else if (roles.length === 0) {
            return {name: 'DisabledUser'}
        }
        throw new Error('Unsupported role: ' + roles)
    } else {
        return {name: 'Login'}
    }
}

const routes: RouteRecordRaw[] = [
    {name: 'Home', path: '/', redirect: redirectFromHome},
    {name: "Login", path: '/login', beforeEnter: navigateToHomeIfAuthenticated, component: LoginPage},
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
            navigationMenu: {
                icon: 'manage_accounts',
                label: 'Users'
            }
        }
    },
    {
        name: 'CarbonAudit', path: '/carbon-audit', component: CarbonAuditPage, meta: {
            auth: {
                required: true,
                authorizedRoles: [UserRole.CARBON_AUDITOR],
            },
            navigationMenu: {
                icon: 'co2',
                label: 'Carbon Audit'
            }
        }
    },
    {
        name: 'AdRecords', path: '/ad-records', component: AdRecordsPage, meta: {
            auth: {
                required: true,
                authorizedRoles: [UserRole.ADMIN, UserRole.AD_MANAGER],
            },
            navigationMenu: {
                icon: 'list_alt',
                label: 'Ad Records'
            }
        }
    },
    {
        name: 'AdStrategy', path: '/ad-strategy', component: AdStrategyPage, meta: {
            auth: {
                required: true,
                authorizedRoles: [UserRole.ADMIN, UserRole.AD_MANAGER],
            },
            navigationMenu: {
                icon: 'tune',
                label: 'Ad Strategy'
            }
        }
    },
    ...BUSINESS_ROUTES
]

export const appRouter = createRouter({
    history: createWebHashHistory(),
    routes
})
appRouter.beforeEach((to) => {
    const routingStore = useRoutingStore();
    if (!routingStore.passesAuthenticationGuard(to)) {
        return {
            name: 'Login',
            query: {next: to.fullPath}
        }
    }
    if (!routingStore.passesAuthorizationGuard(to)) {
        return {name: 'Home'}
    }
    return true;
})
