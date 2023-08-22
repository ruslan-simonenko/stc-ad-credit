<template>
  <q-page padding>
    <UserAddForm @added="returnToPreviousPage"/>
  </q-page>
</template>

<script setup lang="ts">
import {useRouter} from "vue-router";
import UserAddForm from "./UserAddForm.vue";

const router = useRouter();

const returnToPreviousPage = () => router.go(-1)
</script>

<style scoped>

</style>