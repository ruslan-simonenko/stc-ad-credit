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
import {useUserStore} from "./user-store.ts";
import {UserRole} from "./user.ts";

const userStore = useUserStore();

const email = ref<string>('')

const onSubmit = () => {
  userStore.add({email: email.value, roles: [UserRole.CARBON_AUDITOR]})
}
</script>

<style scoped>

</style>