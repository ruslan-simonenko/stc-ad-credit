<template>
  <q-form @submit="onSubmit" class="q-gutter-md form">
    <BusinessSelector v-model="business"/>
    <q-input label="Score [0-100]" v-model.number="score" type="number" :rules="scoreValidators"/>
    <q-input label="Date" v-model="reportDate" type="date" :rules="reportDateValidators"/>
    <q-input label="Report URL" v-model="reportUrl" type="url" :rules="reportUrlValidators"/>
    <q-btn label="Submit" type="submit" color="primary"/>
  </q-form>
</template>

<script setup lang="ts">
import {ref} from "vue";
import {Business} from "../business/business-types.ts";
import {useCarbonAuditStore} from "./carbon-audit-store.ts";
import BusinessSelector from "../business/components/BusinessSelector.vue";
import {fieldRequiredValidator} from "../../utils/form-validators.ts";

const carbonAuditStore = useCarbonAuditStore();

const business = ref<Business | null>(null)
const score = ref<number | null>(null)

const scoreValidators = [
  fieldRequiredValidator,
  (value: number) => value >= 0 || 'Must be greater or equal to 0',
  (value: number) => value <= 100 || 'Must be lower or equal to 100',
]
const reportDate = ref<string | null>(null)
const reportDateValidators = [
  fieldRequiredValidator,
  (value: string) => Date.now() >= Date.parse(value) || 'Can not be in future'
]
const reportUrl = ref<string | null>(null)
const reportUrlValidators = [fieldRequiredValidator]

const onSubmit = async () => {
  await carbonAuditStore.add({
    business_id: business.value!.id,
    score: score.value!,
    report_date: new Date(reportDate.value!),
    report_url: reportUrl.value!,
  })
}
</script>

<style scoped>
.form {
  width: 350px
}
</style>