<template>
  <q-page padding>
    <div v-if="currentUser != null">Welcome, {{ currentUser }}!</div>
    <GoogleLogin v-else :callback="callback"/>
  </q-page>
</template>

<script setup lang="ts">
import {CallbackTypes, GoogleLogin} from "vue3-google-login"
import {useApiClientAxios} from "../api/api-client-axios.ts";
import {AxiosResponse} from "axios";
import {ref} from "vue";

const apiClient = useApiClientAxios()

const currentUser = ref<string | null>(null)

const callback: CallbackTypes.CredentialCallback = (response: CallbackTypes.CredentialPopupResponse) => {
  currentUser.value = null
  apiClient.post("/auth/login", {
    credential: response.credential
  }).then((axiosResponse: AxiosResponse) => {
    const name = axiosResponse.data.name;
    if (name != null) {
      currentUser.value = name
      console.log('Authenticated', name)
    } else {
      console.error("Invalid response", axiosResponse)
    }
  })
}
</script>
