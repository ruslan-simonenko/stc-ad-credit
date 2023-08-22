<template>
  <q-list padding class="menu-list">
    <q-item v-for="route in visibleRoutes" :active="currentRouteName == route.name" v-ripple
            clickable @click="router.push({name: route.name})">
      <q-item-section avatar>
        <q-icon :name="getNavMenuEntry(route).icon"/>
      </q-item-section>
      <q-item-section>
        {{ getNavMenuEntry(route).label }}
      </q-item-section>
    </q-item>
  </q-list>
</template>
<script setup lang="ts">
import {
  _RouteLocationBase,
  RouteLocationNormalizedLoaded,
  RouteRecordName,
  RouteRecordRaw,
  useRoute,
  useRouter
} from "vue-router";
import {computed} from "vue";
import {useRoutingStore} from "./routing-store.ts";

const router = useRouter()
const currentRoute = useRoute()
const routingStore = useRoutingStore();

const visibleRoutes = computed(() =>
    router.options.routes
        .filter(route => {
          const supportsNavigation = route.meta?.navigationMenu?.type === 'entry'
          return supportsNavigation && routingStore.passesAuthGuards(route)
        }));

const currentRouteName = computed<RouteRecordName | null>(() => {
  const currentRouteNavigationMenu = currentRoute.meta.navigationMenu;
  if (currentRouteNavigationMenu?.type === 'entry') {
    return currentRoute.name ?? null
  } else if (currentRouteNavigationMenu?.type === 'linked') {
    return currentRouteNavigationMenu.routeName
  }
  return null;
});

const getNavMenuEntry = (route: RouteRecordRaw) => {
  const navMenu = route.meta!.navigationMenu!;
  if (navMenu.type !== 'entry') {
    throw new Error('Visible routes were filtered incorrectly')
  }
  return navMenu.entry
}
</script>