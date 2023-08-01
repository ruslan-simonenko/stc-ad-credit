<template>
  <q-list padding class="menu-list">
    <q-item v-for="route in visibleRoutes" :active="route.name === currentRoute.name" v-ripple>
      <q-item-section avatar>
        <q-icon :name="route.meta.navigation!.icon"/>
      </q-item-section>
      <q-item-section>
        {{ route.meta.navigation!.label }}
      </q-item-section>
    </q-item>
  </q-list>
</template>
<script setup lang="ts">
import {useRoute, useRouter} from "vue-router";
import {computed} from "vue";
import {useAuthStore} from "../auth/auth-store.ts";

const router = useRouter()
const currentRoute = useRoute()
const authStore = useAuthStore();

const visibleRoutes = computed(() =>
    router.options.routes
        .filter(route => {
          // noinspection JSIncompatibleTypesComparison
          const supportsNavigation = route.meta?.navigation !== undefined
          const passesAuthenticationGuard = !(route.meta?.auth?.required) || authStore.isAuthenticated
          const passesAuthorizationGuard = !(route.meta?.auth?.authorizedRoles) ||
              route.meta?.auth?.authorizedRoles.some(role => authStore.user?.roles.includes(role))
          return supportsNavigation && passesAuthenticationGuard && passesAuthorizationGuard
        }))
</script>