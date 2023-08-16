<template>
  <q-list padding class="menu-list">
    <q-item v-for="route in visibleRoutes" :active="route.name === currentRoute.name" v-ripple
            clickable @click="router.push({name: route.name})">
      <q-item-section avatar>
        <q-icon :name="route.meta!.navigation!.icon"/>
      </q-item-section>
      <q-item-section>
        {{ route.meta!.navigation!.label }}
      </q-item-section>
    </q-item>
  </q-list>
</template>
<script setup lang="ts">
import {useRoute, useRouter} from "vue-router";
import {computed} from "vue";
import {useRoutingStore} from "./routing-store.ts";

const router = useRouter()
const currentRoute = useRoute()
const routingStore = useRoutingStore();

const visibleRoutes = computed(() =>
    router.options.routes
        .filter(route => {
          // noinspection JSIncompatibleTypesComparison
          const supportsNavigation = route.meta?.navigation !== undefined
          return supportsNavigation && routingStore.passesAuthGuards(route)
        }))
</script>