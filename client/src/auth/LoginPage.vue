<template>
  <q-page padding>
    <div v-if="authStore.user != null">Welcome, {{ userName }}!</div>
    <GoogleLogin v-else :callback="callback"/>
  </q-page>
</template>

<script setup lang="ts">
import {CallbackTypes, GoogleLogin} from "vue3-google-login"
import {useAuthStore} from "./auth-store.ts";
import {computed} from "vue";

const authStore = useAuthStore()
const userName = computed(() => authStore.user!.name)

const callback: CallbackTypes.CredentialCallback = async (response: CallbackTypes.CredentialPopupResponse) => {
  await authStore.loginWithGoogle(response.credential)
}
</script>
