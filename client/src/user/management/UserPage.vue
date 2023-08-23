<template>
  <q-page padding>
    <UserForm :id="$route.params.id != null ? parseInt($route.params.id) : undefined" @submit="returnToPreviousPage"/>
  </q-page>
</template>

<script setup lang="ts">
import {useRouter} from "vue-router";
import UserForm from "./UserForm.vue";

const router = useRouter();

const returnToPreviousPage = () => router.go(-1)
</script>

<style scoped>

</style>