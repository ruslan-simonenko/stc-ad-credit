<template>
  <q-page padding>
    <BusinessForm :id="$route.params.id != null ? parseInt($route.params.id) : undefined"
                  @submit="returnToPreviousPage"/>
  </q-page>
</template>

<script setup lang="ts">
import {useRouter} from "vue-router";
import BusinessForm from "./BusinessForm.vue";

const router = useRouter();

const returnToPreviousPage = () => router.go(-1)
</script>

<style scoped>

</style>