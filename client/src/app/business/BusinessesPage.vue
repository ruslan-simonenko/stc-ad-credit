<template>
  <q-page padding>
    <BusinessAddForm/>
    <BusinessesList/>
  </q-page>
</template>

<script setup lang="ts">
import BusinessesList from "./BusinessesList.vue";
import BusinessAddForm from "./add/BusinessAddForm.vue";
</script>

<style scoped>

</style>