<template>
  <q-item>
    <q-item-section avatar>
      <q-avatar size="3rem"><img :src="user.picture_url"></q-avatar>
    </q-item-section>
    <q-item-section>
      <q-item-label>{{ user.name }}</q-item-label>
      <q-item-label>{{ user.email }}</q-item-label>
    </q-item-section>
    <q-item-section side>
      <q-toggle v-model="user.enabled"></q-toggle>
      <q-btn v-if="showDevTools" @click="loginAs(user)">[DEV] Login as</q-btn>
    </q-item-section>
  </q-item>
</template>

<script setup lang="ts">
import {User} from "./user.ts";
import {computed, PropType} from "vue";
import {useAuthStore} from "../auth/auth-store.ts";
import {useRouter} from "vue-router";


const props = defineProps({
  user: {
    type: Object as PropType<User>,
    required: true,
  }
})

const authStore = useAuthStore();
const router = useRouter()

const showDevTools = computed(() => import.meta.env.DEV)

const loginAs = async (user: User) => {
  await authStore.loginAs(user)
  await router.push({name: "Home"})
}
</script>
