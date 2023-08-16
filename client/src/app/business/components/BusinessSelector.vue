<template>
  <q-select label="Business"
            v-model="business"
            :loading="businessStore.all.fetching"
            :options="businessStore.all.items"
            :rules="businessValidators">
    <template v-slot:option="{ itemProps, opt }: {itemProps: any, opt: Business}">
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
</template>

<script setup lang="ts">
import {Business} from "../business-types.ts";
import {computed, onMounted} from "vue";
import {useBusinessStore} from "../business-store.ts";
import {fieldRequiredValidator} from "../../../utils/form-validators.ts";

const props = defineProps(['modelValue'])
const emit = defineEmits(['update:modelValue'])

const business = computed({
  get() {
    return props.modelValue
  },
  set(value: Business) {
    emit('update:modelValue', value)
  }
})

const businessValidators = [fieldRequiredValidator]

const businessStore = useBusinessStore()

onMounted(() => {
  businessStore.fetch()
});
</script>