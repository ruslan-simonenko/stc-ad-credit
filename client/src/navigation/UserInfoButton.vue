<template>
  <q-btn-dropdown v-if="authStore.isAuthenticated"
                  flat>
    <template v-slot:label>
      <q-avatar>
        <img :src="userPictureUrl"/>
      </q-avatar>
    </template>
    <q-list>
      <q-item>
        <q-item-section avatar>
          <q-avatar>
            <img :src="userPictureUrl"/>
          </q-avatar>
        </q-item-section>
        <q-item-section>
          <q-item-label>{{ userName }}<br>{{ userEmail }}</q-item-label>
        </q-item-section>
      </q-item>
      <q-separator/>
      <q-item>
        <q-item-section>
          <q-item-label>Role: {{userRole}}</q-item-label>
        </q-item-section>
      </q-item>
      <q-separator/>
      <q-item clickable v-close-popup @click="onLogoutClick">
        <q-item-section side>
          <q-icon name="logout"></q-icon>
        </q-item-section>
        <q-item-section>
          <q-item-label>Logout</q-item-label>
        </q-item-section>
      </q-item>
    </q-list>
  </q-btn-dropdown>
</template>

<script setup lang="ts">
import {useAuthStore} from "../auth/auth-store.ts";
import {computed} from "vue";
import {useRouter} from "vue-router";

const authStore = useAuthStore()
const router = useRouter()

const userName = computed(() => authStore.user!.name)
const userEmail = computed(() => authStore.user!.email)
const userPictureUrl = computed(() => authStore.user!.picture_url)
const userRole = computed(() => authStore.user!.roles[0])

const onLogoutClick = () => {
  authStore.logout().then(() => router.push({name: 'Home'}))
}
</script>

<style scoped>

</style>