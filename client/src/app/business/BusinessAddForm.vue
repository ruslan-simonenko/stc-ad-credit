<template>
  <q-form @submit="onSubmit" class="q-gutter-md">
    <q-input
        type="text"
        v-model="name"
        label="Name"
    />
    <q-input
        type="url"
        v-model="facebookLink"
        label="Facebook Link"
    />
    <q-btn label="Add Business" type="submit" color="primary"/>
  </q-form>
</template>

<script setup lang="ts">
import {ref} from "vue";
import {useBusinessStore} from "./business-store.ts";

const name = ref<string>('')
const facebookLink = ref<string>('')
const businessStore = useBusinessStore();

const onSubmit = async () => {
  await businessStore.add({name: name.value, facebook_url: facebookLink.value})
}
</script>

<style scoped>

</style>