<template>
  <q-page padding>
    <BusinessAddForm/>
    {{businessStore.all}}
  </q-page>
</template>

<script setup lang="ts">
import BusinessAddForm from "./BusinessAddForm.vue";
import {useBusinessStore} from "./business-store.ts";
const businessStore = useBusinessStore();
</script>

<style scoped>

</style>