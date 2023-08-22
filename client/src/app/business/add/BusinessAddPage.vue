<template>
  <q-page padding>
    <BusinessAddForm @added="returnToPreviousPage"/>
  </q-page>
</template>

<script setup lang="ts">
import BusinessAddForm from "./BusinessAddForm.vue";
import {useRouter} from "vue-router";

const router = useRouter();

const returnToPreviousPage = () => router.go(-1)
</script>

<style scoped>

</style>