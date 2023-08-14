<template>
  <q-form ref='form' @submit="onSubmit" @reset="onReset">
    <BusinessSelector v-model="business" :rules="businessValidators"/>
    <q-input label="Ad Post URL" v-model="adPostURL" type="url" :rules="adPostURLValidators"/>
    <div>Ads remaining: {{ remainingAds ?? '-' }}</div>
    <q-btn label="Submit" type="submit" color="primary"/>
  </q-form>
</template>
<script setup lang="ts">
import {Business} from "../../business/business-types.ts";
import {computed, onMounted, ref} from "vue";
import {fieldRequiredValidator} from "../../../utils/form-validators.ts";
import {QForm} from "quasar";
import {useAdRecordsStore} from "./ad-records-store.ts";
import BusinessSelector from "../../business/components/BusinessSelector.vue";
import {useAdAllowanceStore} from "../allowance/ad-allowance-store.ts";
import {number} from "zod";

const form = ref<QForm>()
const adRecordsStore = useAdRecordsStore();
const adAllowanceStore = useAdAllowanceStore();

const business = ref<Business | null>(null)
const remainingAds = computed<number | null>(() => {
  if (business.value == null) {
    return null
  }
  const allowance = adAllowanceStore.data.indexed[business.value.id];
  return allowance.allowance - allowance.used_allowance;
})
const businessValidators = [() => remainingAds.value > 0 || 'Ad allowance exhausted!']

const adPostURL = ref<string | null>(null)
const adPostURLValidators = [fieldRequiredValidator]

const onSubmit = async () => {
  await adRecordsStore.add({
    business_id: business.value!.id,
    ad_post_url: adPostURL.value!
  })
  form.value!.reset()
};

const onReset = () => {
  business.value = null
  adPostURL.value = null
}

onMounted(() => {
  adRecordsStore.fetch()
  adAllowanceStore.fetch()
});
</script>