import {_RouteLocationBase, _RouteRecordBase} from "vue-router";
import {defineStore} from "pinia";
import {useAuthStore} from "../auth/auth-store.ts";

export const useRoutingStore = defineStore("routing", () => {
    const authStore = useAuthStore();

    const passesAuthGuards = (route: _RouteRecordBase| _RouteLocationBase): boolean => {
        return passesAuthenticationGuard(route) && passesAuthorizationGuard(route)
    }

    const passesAuthenticationGuard = (route: _RouteRecordBase | _RouteLocationBase): boolean => {
        return route.meta?.auth?.required !== true || authStore.isAuthenticated;
    }
    const passesAuthorizationGuard = (route: _RouteRecordBase | _RouteLocationBase): boolean => {
        const routeAllowedRoles = route.meta?.auth?.authorizedRoles;
        if (routeAllowedRoles == null) {
            return true;
        }
        return (authStore.user?.roles ?? []).some(role => routeAllowedRoles.includes(role))
    }

    return {
        passesAuthGuards,
        passesAuthenticationGuard,
        passesAuthorizationGuard
    }
})
