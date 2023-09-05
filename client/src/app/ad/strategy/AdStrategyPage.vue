<template>
  <q-page padding>
    <div class="column">
      <div v-if="adStrategyStore.data.fetching">Loading...</div>
      <template v-else>
        <div>A business can display [Ad Allowance] number of ads in the last [{{ windowSizeInDays }}] days</div>
        <q-markup-table flat bordered>
          <thead>
          <tr>
            <th class="text-left">Rating</th>
            <th class="text-right"><div class="row inline text-center">Carbon Audit<br/>Score Required</div></th>
            <th class="text-right">Ad Allowance</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="row in rows">
            <td class="text-left">
              <CarbonAuditSentimentIcon :business-registered="false" :score="row.minScore" size="4em"/>
            </td>
            <td class="text-right">
              {{ row.minScore }}
            </td>
            <td class="text-right">
              {{ row.adAllowance }}
            </td>
          </tr>
          </tbody>
        </q-markup-table>
      </template>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import {computed, onMounted} from "vue";
import {useAdStrategyStore} from "./ad-strategy-store.ts";
import CarbonAuditSentimentIcon from "../../carbon-audit/components/CarbonAuditSentimentIcon.vue";

const adStrategyStore = useAdStrategyStore();

type RatingData = { minScore: number | null, adAllowance: number }

const rows = computed<Array<RatingData>>(() => {
  const strategy = adStrategyStore.data.strategy;
  return strategy ? [
    {
      rating: 'high',
      minScore: strategy.rating_high_min_score,
      adAllowance: strategy.ads_allowance_high_rating
    },
    {
      rating: 'medium',
      minScore: strategy.rating_medium_min_score,
      adAllowance: strategy.ads_allowance_medium_rating
    },
    {
      rating: 'low',
      minScore: 0,
      adAllowance: strategy.ads_allowance_low_rating
    },
    {
      rating: 'unknown',
      minScore: null,
      adAllowance: strategy.ads_allowance_unknown_rating
    },
  ] : []
})
const windowSizeInDays = computed<number>(() => adStrategyStore.data.strategy?.ads_allowance_window_days ?? 0)

onMounted(() => adStrategyStore.fetch());
</script>

<style scoped>

</style>