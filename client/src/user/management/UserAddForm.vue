<template>
  <q-form @submit="onSubmit" class="q-gutter-md">
    <q-input
        type="email"
        v-model="email"
        label="Email"
        :rules="emailValidators"
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
import {fieldRequiredValidator} from "../../utils/form-validators.ts";

const userStore = useUserStore();

const emit = defineEmits(['added']);

const email = ref<string>('')
const roles = ref<Array<UserRole>>([])
const roleOptions = Object.values(UserRole).map(role => ({label: role, value: role}))

const emailValidators = [fieldRequiredValidator];

const onSubmit = async () => {
  await userStore.add({email: email.value, roles: roles.value})
  resetForm()
  emit('added');
}

const resetForm = () => {
  email.value = ''
  roles.value = []
};
</script>

<style scoped>

</style>