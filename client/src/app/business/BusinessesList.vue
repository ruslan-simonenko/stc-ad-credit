<template class="relative-position">
  <q-table
      flat bordered
      title="Businesses"
      :rows="businessStore.all.items"
      :columns="columns"
      :loading="loading"
      row-key="id">
    <template v-slot:body-cell-score="props">
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

const businessStore = useBusinessStore();
const auditStore = useCarbonAuditStore();
const adAllowanceStore = useAdAllowanceStore();
const adStrategyStore = useAdStrategyStore();

const loading = computed<boolean>(() => businessStore.all.fetching || auditStore.all.fetching || adAllowanceStore.data.fetching || adStrategyStore.data.fetching)

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
    format: (score: number | null): { score: number | null, icon: string, color: string } => {
      const strategy = adStrategyStore.data.strategy;
      let icon: string
      let color: string
      if (score == null) {
        icon = 'question_mark'
        color = 'grey'
      } else if (score >= strategy.rating_high_min_score) {
        icon = 'sentiment_satisfied'
        color = 'green'
      } else if (score >= strategy.rating_medium_min_score) {
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
  adAllowanceStore.fetch()
  adStrategyStore.fetch()
});
</script>

<style scoped>
</style>