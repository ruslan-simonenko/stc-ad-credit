<template>
  <q-table
      class="carbon-audits-table"
      flat bordered
      title="Carbon Audits"
      :rows="rows"
      :columns="columns"
      row-key="name"
  />
</template>

<script setup lang="ts">

import {CarbonAudit} from "./carbon-audit-types.ts";
import {useBusinessStore} from "../business/business-store.ts";
import {Business} from "../business/business-types.ts";
import {computed, onMounted} from "vue";
import {useCarbonAuditStore} from "./carbon-audit-store.ts";
import {QTableProps} from "quasar";


const businessStore = useBusinessStore();
const auditStore = useCarbonAuditStore();

const columns: QTableProps['columns'] = [
  {
    name: 'business',
    label: 'Business',
    align: 'left',
    field: (row: CarbonAudit) => businessStore.all.items.find(item => item.id === row.business_id),
    format: (business: Business) => business.name,
  },
  {
    name: 'score',
    label: 'Score',
    field: (row: CarbonAudit) => row.score,
  },
  {
    name: 'report_date',
    label: 'Date',
    field: (row: CarbonAudit) => row.report_date,
  },
  {
    name: 'report_url',
    label: 'Report',
    align: 'left',
    field: (row: CarbonAudit) => row.report_url,
  }
]

const rows = computed(() => auditStore.all.items)

onMounted(() => {
  auditStore.fetch()
  businessStore.fetch()
});

</script>
