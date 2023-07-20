<template>
  <q-layout>
    <Header></Header>
    <q-page-container>
      <router-view></router-view>
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
import Header from "./navigation/Header.vue";
</script>
