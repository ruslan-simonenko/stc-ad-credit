<template class="relative-position">
  <q-table
      flat bordered
      title="Businesses"
      :rows="businessStore.all.items"
      :columns="columns"
      row-key="id"
  />
</template>

<script setup lang="ts">
import {useBusinessStore} from "./business-store.ts";
import {onMounted} from "vue";
import {useCarbonAuditStore} from "../carbon-audit/carbon-audit-store.ts";
import {Business} from "./business-types.ts";

const businessStore = useBusinessStore()
const auditStore = useCarbonAuditStore();

const columns = [
  {
    name: 'business',
    label: 'Business',
    align: 'left',
    field: (row: Business) => row.name,
  },
  {
    name: 'score',
    label: 'Carbon Audit Score',
    field: (row: Business) => auditStore.all.items.find(audit => audit.business_id === row.id)?.score,
  },
  {
    name: 'facebook_url',
    label: 'Facebook URL',
    align: 'left',
    field: (row: Business) => row.facebook_url,
  }
]

onMounted(() => {
  businessStore.fetch()
  auditStore.fetch()
});
</script>

<style scoped>
</style>