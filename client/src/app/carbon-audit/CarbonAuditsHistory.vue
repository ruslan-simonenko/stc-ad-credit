<template>
  <q-table
      flat bordered
      :grid="$q.screen.lt.md"
      :rows="rows"
      :columns="columns"
      row-key="id"
      :loading="loading"
  >
    <template v-slot:top>
      <div class="text-h6">Carbon Audits</div>
      <q-btn label="Add" v-if="authStore.hasRole(UserRole.CARBON_AUDITOR)"
             color="primary" class="q-ml-sm"
             @click="goToCarbonAuditAddPage"/>
    </template>
    <template v-slot:item="props">
      <div class="q-pa-xs col-xs-12 col-sm-6">
        <q-card bordered flat>
          <q-card-section horizontal>
            <q-list class="col" dense>
              <q-item v-for="column in props.cols" :key="column.name">
                <q-item-section>
                  <q-item-label caption>{{ column.label }}</q-item-label>
                  <q-item-label>{{ column.value }}</q-item-label>
                </q-item-section>
              </q-item>
            </q-list>
          </q-card-section>
        </q-card>
      </div>
    </template>
  </q-table>
</template>

<script setup lang="ts">

import {CarbonAudit} from "./carbon-audit-types.ts";
import {useBusinessStore} from "../business/business-store.ts";
import {Business} from "../business/business-types.ts";
import {computed, onMounted} from "vue";
import {useCarbonAuditStore} from "./carbon-audit-store.ts";
import {QTableProps} from "quasar";
import {UserRole} from "../../user/user.ts";
import {useAuthStore} from "../../auth/auth-store.ts";
import {useRouter} from "vue-router";

const authStore = useAuthStore();
const businessStore = useBusinessStore();
const auditStore = useCarbonAuditStore();

const router = useRouter();

const goToCarbonAuditAddPage = () => router.push({name: 'CarbonAuditAdd'});

const loading = computed(() => businessStore.all.fetching || auditStore.all.fetching)

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

const rows = computed(() => loading.value ? [] : auditStore.all.items)

onMounted(() => {
  auditStore.fetch()
  businessStore.fetch()
});

</script>
