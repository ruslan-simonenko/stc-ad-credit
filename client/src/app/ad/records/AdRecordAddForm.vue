<template>
  <q-form ref='form' @submit="onSubmit" @reset="onReset">
    <BusinessSelector v-model="business"/>
    <q-input label="Ad Post URL" v-model="adPostURL" type="url" :rules="adPostURLValidators"/>
    <q-btn label="Submit" type="submit" color="primary"/>
  </q-form>
</template>
<script setup lang="ts">
import {Business} from "../../business/business-types.ts";
import {onMounted, ref} from "vue";
import {fieldRequiredValidator} from "../../../utils/form-validators.ts";
import {QForm} from "quasar";
import {useAdRecordsStore} from "./ad-records-store.ts";
import BusinessSelector from "../../business/components/BusinessSelector.vue";

const form = ref<QForm>()
const adRecordsStore = useAdRecordsStore();

const business = ref<Business | null>(null)

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
});
</script>