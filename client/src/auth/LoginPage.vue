<template>
  <q-page padding>
    <GoogleLogin :callback="callback"/>
  </q-page>
</template>

<script setup lang="ts">
import {CallbackTypes, GoogleLogin} from "vue3-google-login"
import {useAuthStore} from "./auth-store.ts";
import {useRoute, useRouter} from "vue-router";

const authStore = useAuthStore()
const router = useRouter()
const route = useRoute()

const callback: CallbackTypes.CredentialCallback = async (response: CallbackTypes.CredentialPopupResponse) => {
  await authStore.loginWithGoogle(response.credential)
      .then(() => {
        if ('next' in route.query) {
          router.push(route.query['next'] as string)
        } else {
          router.push({name: "Home"})
        }
      })
}
</script>
