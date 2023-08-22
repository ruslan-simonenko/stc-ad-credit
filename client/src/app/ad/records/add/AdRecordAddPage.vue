<template>
  <q-page padding>
    <AdRecordAddForm @added="returnToPreviousPage"/>
  </q-page>
</template>

<script setup lang="ts">
import {useRouter} from "vue-router";
import AdRecordAddForm from "./AdRecordAddForm.vue";

const router = useRouter();

const returnToPreviousPage = () => router.go(-1)
</script>

<style scoped>

</style>