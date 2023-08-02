<template>
  <q-list>
    <q-item>
      <BusinessAddForm/>
    </q-item>
    <template v-for="(business, index) in businessStore.all.items">
      <q-separator v-if="index !== 0" spaced inset/>
      <q-item>
        <q-item-section>
          <q-item-label>{{ business.name }}</q-item-label>
          <q-item-label>{{ business.facebookLink }}</q-item-label>
        </q-item-section>
      </q-item>
    </template>
  </q-list>
</template>

<script setup lang="ts">
import {useBusinessStore} from "./business-store.ts";
import BusinessAddForm from "./BusinessAddForm.vue";

const businessStore = useBusinessStore();
</script>

<style scoped>

</style>