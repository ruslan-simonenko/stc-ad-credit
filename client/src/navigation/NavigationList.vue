<template>
  <q-list padding class="menu-list">
    <q-item v-for="route in visibleRoutes" :active="route.name === currentRoute.name" v-ripple>
      <q-item-section avatar>
        <q-icon :name="route.meta.auth.navIcon"/>
      </q-item-section>

      <q-item-section>
        {{route.meta.auth.navLabel}}
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

const visibleRoutes = computed(() => router.options.routes.filter(
    route => route.meta?.auth?.allowedRoles.some(
        role => authStore.user?.roles.includes(role))))
</script>