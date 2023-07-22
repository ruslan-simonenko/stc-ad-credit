<template>
  <q-list bordered padding>
    <q-item-label header>Carbon Auditors</q-item-label>
    <q-item v-for="auditor in auditorStore.all">
      <q-item-section avatar>
        <q-avatar><img :src="auditor.picture_url"></q-avatar>
      </q-item-section>
      <q-item-section>
        <q-item-label>{{ auditor.name }}</q-item-label>
        <q-item-label>{{ auditor.email }}</q-item-label>
      </q-item-section>
    </q-item>
  </q-list>
</template>

<script setup lang="ts">
import {useCarbonAuditorStore} from "./carbon-auditor-store.ts";

const auditorStore = useCarbonAuditorStore();
</script>
