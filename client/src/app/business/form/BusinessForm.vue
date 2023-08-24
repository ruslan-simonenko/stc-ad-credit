<template>
  <q-form @submit="onSubmit" class="q-gutter-md">
    <q-input type="text" v-model="data.name" label="Name"/>
    <div class="row">
      <q-select v-model="data.registrationType" :options="registrationTypes"/>
      <q-input type="text" v-model="data.registrationNumber" label="Registration #" class="q-ml-md col-grow"/>
    </div>
    <q-input type="email" v-model="data.email" label="Contact Email"/>
    <q-input type="url" v-model="data.facebookLink" label="Facebook Link"/>
    <q-btn label="Add Business" type="submit" color="primary"/>
  </q-form>
</template>

<script setup lang="ts">
import {shallowReactive} from "vue";
import {useBusinessStore} from "../business-store.ts";
import {BusinessRegistrationType} from "../business-types.ts";
import {z} from "zod";

const DataSchema = z.object({
  name: z.string(),
  registrationType: z.nativeEnum(BusinessRegistrationType),
  registrationNumber: z.string(),
  email: z.string().nullable(),
  facebookLink: z.string().nullable(),
});
type Data = z.TypeOf<typeof DataSchema>;
const EMPTY_DATA: Data = {
  name: '',
  registrationType: BusinessRegistrationType.NI,
  registrationNumber: '',
  email: null,
  facebookLink: null
};

const businessStore = useBusinessStore();

const emit = defineEmits(['submit']);

const data = shallowReactive<Data>(DataSchema.parse(EMPTY_DATA));
const updateData = (newData: Data) => {
  const newDataCopy = DataSchema.parse(newData);
  data.name = newDataCopy.name;
  data.registrationType = newDataCopy.registrationType;
  data.registrationNumber = newDataCopy.registrationNumber;
  data.email = newDataCopy.email;
  data.facebookLink = newDataCopy.facebookLink;
}

const registrationTypes = Object.values(BusinessRegistrationType)

const onSubmit = async () => {
  await businessStore.add({
    name: data.name,
    registration_type: data.registrationType,
    registration_number: data.registrationNumber,
    email: data.email,
    facebook_url: data.facebookLink,
  })
  resetForm();
  emit('submit');
}

const resetForm = () => updateData(EMPTY_DATA);
</script>

<style scoped>

</style>