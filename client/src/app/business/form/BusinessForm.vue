<template>
  <q-form @submit="onSubmit" class="q-gutter-md">
    <q-input type="text" v-model="data.name" label="Name"/>
    <div class="row">
      <q-select v-model="data.registration_type" :options="registrationTypes"/>
      <q-input type="text" v-model="data.registration_number" label="Registration #" class="q-ml-md col-grow"/>
    </div>
    <q-input type="email" v-model="data.email" label="Contact Email"/>
    <q-input type="url" v-model="data.facebook_url" label="Facebook Link"/>
    <q-btn :label="props.id == null ? 'Add Business' : 'Update Business'" type="submit" color="primary"/>
  </q-form>
</template>

<script setup lang="ts">
import {computed, onMounted, shallowReactive, watch} from "vue";
import {useBusinessStore} from "../business-store.ts";
import {Business, BusinessFormDTO, BusinessFormDTOSchema, BusinessRegistrationType} from "../business-types.ts";

const EMPTY_DATA: BusinessFormDTO = {
  name: '',
  registration_type: BusinessRegistrationType.NI,
  registration_number: '',
  email: null,
  facebook_url: null
};

const props = defineProps({
  id: Number,
});
const emit = defineEmits(['submit']);

const businessStore = useBusinessStore();

const business = computed<Business | null>(
    () => props.id == null ? null : businessStore.all.items.find((business) => business.id == props.id) ?? null)

const data = shallowReactive<BusinessFormDTO>(BusinessFormDTOSchema.parse(EMPTY_DATA));
const updateData = (newData: BusinessFormDTO) => {
  const newDataCopy = BusinessFormDTOSchema.parse(newData);
  data.name = newDataCopy.name;
  data.registration_type = newDataCopy.registration_type;
  data.registration_number = newDataCopy.registration_number;
  data.email = newDataCopy.email;
  data.facebook_url = newDataCopy.facebook_url;
}
watch(() => business.value, (business: Business | null) => {
  updateData(business == null ? EMPTY_DATA : {
    name: business.name,
    registration_type: business.sensitive!.registration_type,
    registration_number: business.sensitive!.registration_number,
    email: business.sensitive!.email,
    facebook_url: business.facebook_url,
  })
})

const registrationTypes = Object.values(BusinessRegistrationType)

const onSubmit = async () => {
  const business = {
    name: data.name,
    registration_type: data.registration_type,
    registration_number: data.registration_number,
    email: data.email,
    facebook_url: data.facebook_url,
  };
  if (props.id == null) {
    await businessStore.add(business);
  } else {
    await businessStore.update(props.id, business);
  }
  resetForm();
  emit('submit');
}

const resetForm = () => updateData(EMPTY_DATA);

onMounted(() => {
  businessStore.fetch();
});
</script>

<style scoped>

</style>