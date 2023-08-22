<template>
  <q-page padding>
    <q-btn @click="goToBusinessAddPage">Add</q-btn>
    <BusinessesList/>
  </q-page>
</template>

<script setup lang="ts">
import BusinessesList from "./BusinessesList.vue";
import BusinessAddForm from "./add/BusinessAddForm.vue";
import {useRouter} from "vue-router";

const router = useRouter();

const goToBusinessAddPage = () => router.push({name: 'BusinessAdd'});
</script>

<style scoped>

</style>