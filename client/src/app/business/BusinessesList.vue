<template class="relative-position">
  <q-table
      flat bordered
      title="Businesses"
      :rows="businessStore.all.items"
      :columns="columns"
      :loading="loading"
      row-key="id">
    <template v-slot:top>
      <div class="text-h6">Businesses</div>
      <q-btn label="Add" v-if="authStore.hasRole(UserRole.BUSINESS_MANAGER)" :disable="loading"
             color="primary" class="q-ml-sm"
             @click="goToBusinessAddPage"/>
    </template>
    <template v-if="authStore.hasRole(UserRole.ADMIN)" v-slot:body-cell-score="props">
      <q-td :props="props">
        <div class="row inline items-end">
          <div v-if="props.value.score != null" style="margin-right: .5em">{{ props.value.score }}</div>
          <q-icon :name="props.value.icon" :color="props.value.color" size="2em"/>
        </div>
      </q-td>
    </template>
  </q-table>
</template>

<script setup lang="ts">
import {useBusinessStore} from "./business-store.ts";
import {computed, onMounted} from "vue";
import {useCarbonAuditStore} from "../carbon-audit/carbon-audit-store.ts";
import {Business} from "./business-types.ts";
import {useAdAllowanceStore} from "../ad/allowance/ad-allowance-store.ts";
import {AdAllowance} from "../ad/allowance/ad-allowance-types.ts";
import {useAdStrategyStore} from "../ad/strategy/ad-strategy-store.ts";
import {QTableProps} from "quasar";
import {useAuthStore} from "../../auth/auth-store.ts";
import {UserRole} from "../../user/user.ts";
import {useRouter} from "vue-router";

const authStore = useAuthStore();
const businessStore = useBusinessStore();
const auditStore = useCarbonAuditStore();
const adAllowanceStore = useAdAllowanceStore();
const adStrategyStore = useAdStrategyStore();

const router = useRouter();

const goToBusinessAddPage = () => router.push({name: 'BusinessAdd'});

const loading = computed<boolean>(() => businessStore.all.fetching || auditStore.all.fetching || adAllowanceStore.data.fetching || adStrategyStore.data.fetching)

const prepareColumns = (): QTableProps['columns'] => {

  const businessManagerColumns: QTableProps['columns'] = authStore.hasRole(UserRole.BUSINESS_MANAGER) ? [
    {
      name: 'registration',
      label: 'Registration',
      align: 'left',
      field: (row: Business) => row.sensitive,
      format: (sensitiveData: Business['sensitive']) => `${sensitiveData!.registration_type} ${sensitiveData!.registration_number}`
    },
    {
      name: 'email',
      label: 'Contact Email',
      align: 'left',
      field: (row: Business) => row.sensitive,
      format: (sensitiveData: Business['sensitive']) => `${sensitiveData!.email}`
    },
  ] : [];

  const adminColumns: QTableProps['columns'] = authStore.hasRole(UserRole.ADMIN) ? [
    {
      name: 'score',
      label: 'Carbon Audit Score',
      field: (row: Business) => auditStore.all.items.find(audit => audit.business_id === row.id)?.score,
      format: (score: number | null): { score: number | null, icon: string, color: string } => {
        const strategy = adStrategyStore.data.strategy;
        let icon: string
        let color: string
        if (score == null) {
          icon = 'question_mark'
          color = 'grey'
        } else if (score >= strategy!.rating_high_min_score) {
          icon = 'sentiment_satisfied'
          color = 'green'
        } else if (score >= strategy!.rating_medium_min_score) {
          icon = 'sentiment_neutral'
          color = 'amber'
        } else {
          icon = 'sentiment_dissatisfied'
          color = 'red'
        }
        return {score, icon, color}
      }
    },
    {
      name: 'allowance',
      label: 'Ads Used',
      field: (row: Business) => adAllowanceStore.data.indexed[row.id],
      format: (value: AdAllowance | null): string => value != null ? `${value.used_allowance} / ${value.allowance}` : ''
    }] : [];
  return [
    {
      name: 'name',
      label: 'Name',
      align: 'left',
      field: (row: Business) => row.name,
    },
    ...adminColumns,
    {
      name: 'facebook_url',
      label: 'Facebook URL',
      align: 'left',
      field: (row: Business) => row.facebook_url,
    },
    ...businessManagerColumns
  ];
}

const columns: QTableProps['columns'] = prepareColumns();

onMounted(() => {
  businessStore.fetch()
  if (authStore.hasRole(UserRole.ADMIN)) {
    auditStore.fetch()
    adAllowanceStore.fetch()
    adStrategyStore.fetch()
  }
});
</script>

<style scoped>
</style>