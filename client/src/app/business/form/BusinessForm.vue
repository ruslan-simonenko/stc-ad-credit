<template>
  <q-form @submit="onSubmit" class="q-gutter-md">
    <q-input type="text" v-model="data.name" label="Name"/>
    <q-option-group
        v-if="canAddRegistered"
        v-model="data.registration_tier"
        :options="registrationTiers"
        color="primary"
    />
    <template v-if="data.registration_tier === RegistrationTier.REGISTERED">
      <div class="row">
        <q-select v-model="data.registration_type" :options="registrationTypes"/>
        <q-input type="text" v-model="data.registration_number" label="Registration #" class="q-ml-md col-grow"/>
      </div>
      <q-input type="email" v-model="data.email" label="Contact Email"/>
    </template>
    <q-input type="url" v-model="data.facebook_url" label="Facebook Link"/>
    <q-btn :label="props.id == null ? 'Add Business' : 'Update Business'" type="submit" color="primary"/>
  </q-form>
</template>

<script setup lang="ts">
import {computed, onMounted, shallowReactive, watch} from "vue";
import {useBusinessStore} from "../business-store.ts";
import {Business, BusinessRegistrationType} from "../business-types.ts";
import {v4 as uuidv4} from 'uuid';
import {z} from "zod";
import {useAuthStore} from "../../../auth/auth-store.ts";
import {UserRole} from "../../../user/user.ts";

enum RegistrationTier {
  KNOWN = 'Known',
  REGISTERED = 'Registered',
}

const DataSchema = z.object({
  name: z.string(),
  registration_tier: z.nativeEnum(RegistrationTier),
  registration_type: z.nativeEnum(BusinessRegistrationType),
  registration_number: z.string(),
  email: z.string().nullable(),
  facebook_url: z.string().nullable(),
});
type Data = z.TypeOf<typeof DataSchema>;

const props = defineProps({
  id: Number,
});
const emit = defineEmits(['submit']);

const businessStore = useBusinessStore();
const authStore = useAuthStore();

const canAddRegistered = computed<boolean>(() => authStore.hasRole(UserRole.BUSINESS_MANAGER));
const canSeeSensitiveInfo = computed<boolean>(() => authStore.hasRole(UserRole.BUSINESS_MANAGER));

const business = computed<Business | null>(
    () => props.id == null ? null : businessStore.all.items.find((business) => business.id == props.id) ?? null)

const emptyData = computed<Data>(() => ({
  name: '',
  registration_tier: canAddRegistered.value ? RegistrationTier.REGISTERED : RegistrationTier.KNOWN,
  registration_type: BusinessRegistrationType.NI,
  registration_number: '',
  email: null,
  facebook_url: null
}));
const data = shallowReactive<Data>(DataSchema.parse(emptyData.value));

const updateData = (newData: Data) => {
  const newDataCopy = DataSchema.parse(newData);
  data.name = newDataCopy.name;
  data.registration_tier = newDataCopy.registration_tier;
  data.registration_type = newDataCopy.registration_type;
  data.registration_number = newDataCopy.registration_number;
  data.email = newDataCopy.email;
  data.facebook_url = newDataCopy.facebook_url;
}
watch(() => business.value, (business: Business | null) => {
  let newData: Data;
  if (business == null) {
    newData = emptyData.value;
  } else if (canSeeSensitiveInfo.value) {
    newData = {
      name: business.name,
      registration_tier: business.sensitive!.registration_type === BusinessRegistrationType.KNOWN ? RegistrationTier.KNOWN : RegistrationTier.REGISTERED,
      registration_type: business.sensitive!.registration_type,
      registration_number: business.sensitive!.registration_number,
      email: business.sensitive!.email,
      facebook_url: business.facebook_url,
    };
  } else {
    newData = {
      name: business.name,
      registration_tier: RegistrationTier.KNOWN,
      registration_type: BusinessRegistrationType.KNOWN,
      registration_number: '',
      email: null,
      facebook_url: business.facebook_url,
    };
  }
  updateData(newData);
});
watch(() => data.registration_tier, (newRegistrationTier) => {
  if (newRegistrationTier === RegistrationTier.REGISTERED && data.registration_type === BusinessRegistrationType.KNOWN) {
    data.registration_type = BusinessRegistrationType.VAT;
    data.registration_number = '';
  }
});

const registrationTypes = Object.values(BusinessRegistrationType).filter(registrationType => registrationType != BusinessRegistrationType.KNOWN);
const registrationTiers = [
  {
    value: RegistrationTier.REGISTERED,
    label: 'Registered - participates in STC pilot'
  },
  {
    value: RegistrationTier.KNOWN,
    label: 'Known - utilizes ads on STC notice boards'
  }];


const onSubmit = async () => {
  const isRegistered = data.registration_tier == RegistrationTier.REGISTERED;
  const business = {
    name: data.name,
    registration_type: isRegistered ? data.registration_type : BusinessRegistrationType.KNOWN,
    registration_number: isRegistered ? data.registration_number : uuidv4(),
    email: isRegistered ? data.email : null,
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

const resetForm = () => updateData(emptyData.value);

onMounted(() => {
  businessStore.fetch();
});
</script>

<style scoped>

</style>