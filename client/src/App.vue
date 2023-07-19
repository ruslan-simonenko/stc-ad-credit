<template>
  <q-layout>
    <q-header elevated>
      <q-toolbar>
        <q-toolbar-title>STC Ad Credit</q-toolbar-title>
      </q-toolbar>
    </q-header>
    <q-page-container>
      <q-page padding>
        <LoginPage></LoginPage>
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
import LoginPage from "./auth/LoginPage.vue";
</script>
