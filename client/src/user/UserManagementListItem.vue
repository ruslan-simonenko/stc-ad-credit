<template>
  <q-item>
    <q-item-section avatar>
      <q-skeleton v-if="loading" type="QAvatar" size="3rem"/>
      <q-avatar v-else size="3rem"><img :src="user!.picture_url"></q-avatar>
    </q-item-section>
    <q-item-section>
      <q-item-label>
        <q-skeleton v-if="loading" type="text" width="7rem"/>
        <span v-else>{{ user.name }}</span>
      </q-item-label>
      <q-item-label>
        <q-skeleton v-if="loading" type="text" width="12rem"/>
        <span v-else>{{ user.email }}</span>
      </q-item-label>
    </q-item-section>
    <q-item-section side>
      <div>
        <q-skeleton v-if="loading" type="QToggle"/>
        <q-toggle v-else v-model="enabled"></q-toggle>
      </div>
      <q-btn v-if="showDevTools" @click="loginAs(user!)">[DEV] Login as</q-btn>
    </q-item-section>
  </q-item>
</template>

<script setup lang="ts">
import {User} from "./user.ts";
import {computed, PropType} from "vue";
import {useAuthStore} from "../auth/auth-store.ts";
import {useRouter} from "vue-router";
import {useUserStore} from "./user-store.ts";

const props = defineProps({
  user: Object as PropType<User | null>,
  loading: Boolean
})

const authStore = useAuthStore();
const userStore = useUserStore();
const router = useRouter()

const showDevTools = computed(() => import.meta.env.DEV)

const loginAs = async (user: User) => {
  await authStore.loginAs(user)
  await router.push({name: "Home"})
}

const enabled = computed<boolean>({
  get() {
    return props.user!.roles.length > 0
  },
  set(newValue: boolean) {
    userStore.setEnabled(props.user!.id, newValue)
  }
})
</script>
