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

const email = ref<string>('')
const onSubmit = () => {
  console.log('submit')
}
</script>

<style scoped>

</style>