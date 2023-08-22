<template>
  <q-page padding>
    <CarbonAuditAddForm @added="returnToPreviousPage"/>
  </q-page>
</template>

<script setup lang="ts">
import CarbonAuditAddForm from "./CarbonAuditAddForm.vue";

import {useRouter} from "vue-router";

const router = useRouter();

const returnToPreviousPage = () => router.go(-1)
</script>

<style scoped>

</style>