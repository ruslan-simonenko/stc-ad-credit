<template>
  <q-form @submit="onSubmit" class="q-gutter-md form">
    <q-select label="Business"
              v-model="business"
              :loading="businessStore.all.fetching"
              :options="businessStore.all.items"
              :rules="businessValidators">
      <template v-slot:option="{ itemProps, opt }: {opt: Business}">
        <q-item v-bind="itemProps">
          <q-item-section>
            <q-item-label>{{ opt.name }}</q-item-label>
            <q-item-label>{{ opt.facebook_url }}</q-item-label>
          </q-item-section>
        </q-item>
      </template>
      <template v-slot:selected-item="{ opt }: {opt: Business}">
        {{ opt.name }}
      </template>
      <template v-slot:no-option>
        <q-item>
          <q-item-section class="text-grey">
            No results
          </q-item-section>
        </q-item>
      </template>
    </q-select>
    <q-input label="Score [0-100]" v-model="score" type="number" :rules="scoreValidators"/>
    <q-input label="Date" v-model="reportDate" type="date" :rules="reportDateValidators"/>
    <q-input label="Report URL" v-model="reportUrl" type="url" :rules="reportUrlValidators"/>
    <q-btn label="Submit" type="submit" color="primary"/>
  </q-form>
</template>

<script setup lang="ts">
import {useBusinessStore} from "../business/business-store.ts";
import {onMounted, ref} from "vue";
import {Business} from "../business/business-types.ts";
import {useCarbonAuditStore} from "./carbon-audit-store.ts";
import {fieldRequiredValidator} from "../../utils/form-validators.ts";

const businessStore = useBusinessStore();
const carbonAuditStore = useCarbonAuditStore();

const business = ref<Business | null>(null)
const businessValidators = [fieldRequiredValidator]
const score = ref<number | null>(null)
const scoreValidators = [
  fieldRequiredValidator,
  (value: number) => value >= 0 || 'Must be greater or equal to 0',
  (value: number) => value <= 100 || 'Must be lower or equal to 100',
]
const reportDate = ref<Date | null>(null)
const reportDateValidators = [
  fieldRequiredValidator,
  (value: Date) => Date.now() >= Date.parse(value) || 'Can not be in future'
]
const reportUrl = ref<string | null>(null)
const reportUrlValidators = [fieldRequiredValidator]

onMounted(() => {
  businessStore.fetch()
});

const onSubmit = async () => {
  await carbonAuditStore.add({
    business_id: business.value.id,
    score: score.value,
    report_date: reportDate.value,
    report_url: reportUrl.value,
  })
}
</script>

<style scoped>
.form {
  width: 350px
}
</style>