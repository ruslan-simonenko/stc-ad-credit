<template>
  <q-form @submit="onSubmit" class="q-gutter-md">
    <q-input
        type="email"
        v-model="email"
        label="Email"
    />
    <q-btn label="Add Carbon Auditor" type="submit" color="primary"/>
  </q-form>
</template>

<script setup lang="ts">
import {ref} from "vue";
import {useCarbonAuditorStore} from "./carbon-auditor-store.ts";

const auditorStore = useCarbonAuditorStore();

const email = ref<string>('')

const onSubmit = () => {
  auditorStore.add({email: email.value})
}
</script>

<style scoped>

</style>