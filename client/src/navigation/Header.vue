<template>
  <q-header elevated>
    <q-toolbar>
      <q-toolbar-title>STC Ad Credit</q-toolbar-title>
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
        </q-list>
      </q-btn-dropdown>
    </q-toolbar>
  </q-header>
</template>

<script setup lang="ts">
import {useAuthStore} from "../auth/auth-store.ts";
import {computed} from "vue";

const authStore = useAuthStore();
const userName = computed(() => authStore.user!.name)
const userEmail = computed(() => authStore.user!.email)
const userPictureUrl = computed(() => authStore.user!.picture_url)

</script>