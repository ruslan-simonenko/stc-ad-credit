<template>
  <CarbonAuditAddForm/>
  {{ store.all.items }}
</template>

<script setup lang="ts">
import CarbonAuditAddForm from "./CarbonAuditAddForm.vue";
import {useCarbonAuditStore} from "./carbon-audit-store.ts";
import {onMounted} from "vue";

const store = useCarbonAuditStore();

onMounted(() => store.fetch());
</script>

<style scoped>

</style>