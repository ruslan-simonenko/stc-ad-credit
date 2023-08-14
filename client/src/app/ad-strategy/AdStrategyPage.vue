<template>
  <q-page padding>
    A business can display [Ad Allowance] number of ads in the last [{{ windowSizeInDays }}] days
    <q-markup-table flat bordered>
      <thead>
      <tr>
        <th class="text-left">Rating</th>
        <th class="text-right">Carbon Audit Score Required</th>
        <th class="text-right">Ad Allowance</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="(_, row) in 4" :key="row">
        <td class="text-left">
          <q-icon :name="items[row].icon" :color="items[row].color" size="4em"/>
        </td>
        <td class="text-right">
          {{ items[row].minScore }}
        </td>
        <td class="text-right">
          {{ items[row].adAllowance }}
        </td>
      </tr>
      </tbody>
    </q-markup-table>
  </q-page>
</template>

<script setup lang="ts">
import {reactive, ref} from "vue";

type RatingData = { icon: string, color: string, minScore: number | null, adAllowance: number }

const items = reactive<Array<RatingData>>([
  {rating: 'high', icon: 'sentiment_satisfied', color: 'green', minScore: 0, adAllowance: 0},
  {rating: 'medium', icon: 'sentiment_neutral', color: 'amber', minScore: 0, adAllowance: 0},
  {rating: 'low', icon: 'sentiment_dissatisfied', color: 'red', minScore: 0, adAllowance: 0},
  {rating: 'unknown', icon: 'question_mark', color: 'grey', minScore: null, adAllowance: 0},
])
const windowSizeInDays = ref<number>(0)

</script>

<style scoped>

</style>