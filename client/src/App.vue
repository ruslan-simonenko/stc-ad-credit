<template>
  <q-layout>
    <Header></Header>
    <q-page-container>
      <q-page padding>
        <LoginPage></LoginPage>
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
import LoginPage from "./auth/LoginPage.vue";
import Header from "./navigation/Header.vue";
</script>
