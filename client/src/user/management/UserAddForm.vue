<template>
  <q-form @submit="onSubmit" class="q-gutter-md">
    <q-input
        type="email"
        v-model="email"
        label="Email"
    />
    <q-option-group
        v-model="roles"
        :options="roleOptions"
        type="toggle"
    />
    <q-btn label="Add User" type="submit" color="primary"/>
  </q-form>
</template>

<script setup lang="ts">
import {ref} from "vue";
import {useUserStore} from "../user-store.ts";
import {UserRole} from "../user.ts";
import {QForm} from "quasar";

const userStore = useUserStore();

const email = ref<string>('')
const roles = ref<Array<UserRole>>([])
const roleOptions = [{label: 'Admin', value: UserRole.ADMIN}, {label: 'Carbon Auditor', value: UserRole.CARBON_AUDITOR}]

const onSubmit = async () => {
  await userStore.add({email: email.value, roles: roles.value})
  resetForm()
}

const resetForm = () => {
  email.value = ''
  roles.value = []
};
</script>

<style scoped>

</style>