<template>
  <q-page padding>
    <UserForm :id="userID" @submit="returnToPreviousPage"/>
  </q-page>
</template>

<script setup lang="ts">
import {useRoute, useRouter} from "vue-router";
import UserForm from "./UserForm.vue";
import {computed} from "vue";

const router = useRouter();
const route = useRoute();

const userID = computed(() => {
  const id = route.params.id as string | undefined
  return id !== undefined ? parseInt(id) : id
});
const returnToPreviousPage = () => router.go(-1)
</script>

<style scoped>

</style>