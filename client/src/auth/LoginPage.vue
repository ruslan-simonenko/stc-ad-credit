<template>
  <q-page padding>
    <GoogleLogin :callback="callback"/>
  </q-page>
</template>

<script setup lang="ts">
import {CallbackTypes, GoogleLogin} from "vue3-google-login"

const callback: CallbackTypes.CredentialCallback = (response: CallbackTypes.CredentialPopupResponse) => {
  console.log('Authenticated', response)
}
</script>
