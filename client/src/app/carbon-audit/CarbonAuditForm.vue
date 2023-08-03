<template>
  <q-form @submit="onSubmit" class="q-gutter-md form">
    <q-select label="Business"
              v-model="business"
              :loading="businessStore.all.fetching"
              :options="businessStore.all.items">
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
    <q-input label="Score [0-100]" v-model="score" type="number"/>
    <q-input label="Date" v-model="reportDate" type="date"/>
    <q-input label="Report URL" v-model="reportUrl" type="url"/>
    <q-btn label="Submit" type="submit" color="primary"/>
  </q-form>
</template>

<script setup lang="ts">
import {useBusinessStore} from "../business/business-store.ts";
import {onMounted, ref} from "vue";
import {Business} from "../business/business-types.ts";

const businessStore = useBusinessStore();

const business = ref<Business | null>(null)
const score = ref<number | null>(null)
const reportDate = ref<Date | null>(null)
const reportUrl = ref<string | null>(null)

onMounted(() => {
  businessStore.fetch()
});

const onSubmit = () => {
  console.log('submit', business, score, reportDate, reportUrl)
}
</script>

<style scoped>
.form {
  width: 350px
}
</style>