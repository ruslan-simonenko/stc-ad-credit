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
import {computed, shallowReactive, watch} from "vue";
import {useBusinessStore} from "../business-store.ts";
import {Business, BusinessRegistrationType} from "../business-types.ts";
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

const props = defineProps({
  id: Number,
});
const emit = defineEmits(['submit']);

const businessStore = useBusinessStore();

const business = computed<Business | null>(
    () => props.id == null ? null : businessStore.all.items.find((business) => business.id == props.id) ?? null)

const data = shallowReactive<Data>(DataSchema.parse(EMPTY_DATA));
const updateData = (newData: Data) => {
  const newDataCopy = DataSchema.parse(newData);
  data.name = newDataCopy.name;
  data.registrationType = newDataCopy.registrationType;
  data.registrationNumber = newDataCopy.registrationNumber;
  data.email = newDataCopy.email;
  data.facebookLink = newDataCopy.facebookLink;
}
watch(() => business.value, (business: Business|null) => {
  updateData(business == null ? EMPTY_DATA : {
    name: business.name,
    registrationType: business.sensitive!.registration_type,
    registrationNumber: business.sensitive!.registration_number,
    email: business.sensitive!.email,
    facebookLink: business.facebook_url,
  })
})

const registrationTypes = Object.values(BusinessRegistrationType)

const onSubmit = async () => {
  const business = {
    name: data.name,
    registration_type: data.registrationType,
    registration_number: data.registrationNumber,
    email: data.email,
    facebook_url: data.facebookLink,
  };
  if (props.id == null) {
    await businessStore.add(business);
  } else {
    console.log('update', props.id, business);
  }
  resetForm();
  emit('submit');
}

const resetForm = () => updateData(EMPTY_DATA);
</script>

<style scoped>

</style>