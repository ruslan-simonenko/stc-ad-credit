import {_RouteRecordBase} from "vue-router";
import {defineStore} from "pinia";
import {useAuthStore} from "../auth/auth-store.ts";

export const useRoutingStore = defineStore("routing", () => {
    const authStore = useAuthStore();

    const passesAuthGuards = (route: _RouteRecordBase): boolean => {
        return passesAuthenticationGuard(route) && passesAuthorizationGuard(route)
    }

    const passesAuthenticationGuard = (route: _RouteRecordBase): boolean => {
        return route.meta.auth?.required !== true || authStore.isAuthenticated;
    }
    const passesAuthorizationGuard = (route: _RouteRecordBase): boolean => {
        if (route.meta.auth?.authorizedRoles == null) {
            return true;
        }
        return authStore.user?.roles.some(role => route.meta.auth?.authorizedRoles?.includes(role))
    }

    return {
        passesAuthGuards,
        passesAuthenticationGuard,
        passesAuthorizationGuard
    }
})
