<template>
  <q-page padding>
    <q-form ref='form' @submit="onSubmit" @reset="onReset">
      <BusinessSelector v-model="business"/>
      <q-input label="Ad Post URL" v-model="adPostURL" type="url" :rules="adPostURLValidators"/>
      <q-btn label="Submit" type="submit" color="primary"/>
    </q-form>
  </q-page>
</template>

<script setup lang="ts">
import BusinessSelector from "../business/components/BusinessSelector.vue";
import {Business} from "../business/business-types.ts";
import {ref} from "vue";
import {fieldRequiredValidator} from "../../utils/form-validators.ts";
import {QForm} from "quasar";

const form = ref<QForm>()
const business = ref<Business | null>(null)

const adPostURL = ref<string | null>(null)
const adPostURLValidators = [fieldRequiredValidator]

const onSubmit = async () => {
  console.log('submit', business.value, adPostURL.value)
  form.value.reset()
};

const onReset = () => {
  business.value = null
  adPostURL.value = null
}
</script>

<style scoped>

</style>