<template>
  <q-layout>
    <Header></Header>
    <q-page-container>
      <router-view v-slot="{ Component }">
        <keep-alive max="20" :key="userID">
          <component :is="Component"/>
        </keep-alive>
      </router-view>
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
import Header from "./navigation/Header.vue";
import {computed} from "vue";
import {useAuthStore} from "./auth/auth-store.ts";

const authStore = useAuthStore();

const userID = computed(() => authStore.user?.id ?? 0)
</script>
