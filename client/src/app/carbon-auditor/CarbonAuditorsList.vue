<template>
  <q-list bordered padding>
    <q-item-label header>Carbon Auditors</q-item-label>
    <q-item v-for="auditor in auditors">
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
const auditors = [
  {picture_url: 'https://cdn.quasar.dev/img/avatar4.jpg', name: 'John Doe', email: 'john.doe@gmail.com'},
  {picture_url: 'https://cdn.quasar.dev/img/avatar2.jpg', name: 'Jane Doe', email: 'jane.doe@gmail.com'}
]
</script>
