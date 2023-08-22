<template>
  <q-form @submit="onSubmit" class="q-gutter-md">
    <q-input type="text" v-model="name" label="Name"/>
    <div class="row">
      <q-select v-model="registrationType" :options="registrationTypes"/>
      <q-input type="text" v-model="registrationNumber" label="Registration #" class="q-ml-md col-grow"/>
    </div>
    <q-input type="email" v-model="email" label="Contact Email"/>
    <q-input type="url" v-model="facebookLink" label="Facebook Link"/>
    <q-btn label="Add Business" type="submit" color="primary"/>
  </q-form>
</template>

<script setup lang="ts">
import {ref} from "vue";
import {useBusinessStore} from "../business-store.ts";
import {BusinessRegistrationType} from "../business-types.ts";

const businessStore = useBusinessStore();

const emit = defineEmits(['added']);

const name = ref<string>('')
const registrationType = ref<BusinessRegistrationType>(BusinessRegistrationType.NI)
const registrationNumber = ref<string>('')
const email = ref<string>('')
const facebookLink = ref<string>('')

const registrationTypes = Object.values(BusinessRegistrationType)

const onSubmit = async () => {
  await businessStore.add({
    name: name.value,
    registration_number: registrationNumber.value,
    registration_type: registrationType.value,
    email: email.value,
    facebook_url: facebookLink.value
  })
  resetForm();
  emit('added');
}

const resetForm = () => {
  name.value = ''
  facebookLink.value = ''
  registrationType.value = BusinessRegistrationType.NI
  registrationNumber.value = ''
  email.value = ''
}
</script>

<style scoped>

</style>